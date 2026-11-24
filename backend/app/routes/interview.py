import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.app.services.interview_session import (
    create_session,
    get_question,
    save_answer,
    get_report
)
from backend.app.services.answer_evaluator import evaluate_answer
from backend.app.services.communication_confidence import analyze_communication_confidence
from backend.app.services.question_generator import _build_follow_up_question
from backend.app.services.report_generator import generate_interview_report
from backend.app.services.pdf_report_generator import generate_interview_report_pdf

router = APIRouter(prefix="/interview", tags=["Interview"])
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


class StartInterviewRequest(BaseModel):
    questions: list[str]
    resume_data: dict | None = None
    jd_skills: list[str] | None = None


class AnswerRequest(BaseModel):
    session_id: str
    answer: str
    communication: dict | None = None


class CommunicationRequest(BaseModel):
    transcript: str


@router.post("/start")
def start_interview(request: StartInterviewRequest):
    session_id = create_session(
        request.questions,
        interview_context={
            "resume_data": request.resume_data or {},
            "jd_skills": request.jd_skills or []
        }
    )

    return {
        "session_id": session_id,
        "question": get_question(session_id)
    }


@router.post("/answer")
def submit_answer(request: AnswerRequest):
    session_data = get_report(request.session_id)
    previous_questions = session_data.get("question_history", []) if session_data else []
    resume_data = (session_data or {}).get("resume_data", {}) if session_data else {}
    jd_skills = (session_data or {}).get("jd_skills", []) if session_data else []
    current_question = (session_data or {}).get("current_question") or (
        previous_questions[-1] if previous_questions else None
    )
    score, feedback = evaluate_answer(
        request.answer,
        question=current_question,
        skills=resume_data.get("skills", []),
        jd_skills=jd_skills
    )

    follow_up_question = None
    if score >= 8 and request.answer.strip():
        follow_up_question = _build_follow_up_question(
            request.answer,
            previous_questions[-1] if previous_questions else None,
            resume_data,
            jd_skills
        )

    next_question = save_answer(
        request.session_id,
        request.answer,
        score,
        feedback,
        follow_up_question,
        request.communication
    )

    if next_question is None:
        session_data = get_report(request.session_id)
        final_report = generate_interview_report(session_data)
        return {
            "message": "Interview Completed",
            "report": final_report
        }

    return {
        "score": score,
        "feedback": feedback,
        "next_question": next_question,
        "difficulty": "easy" if score <= 4 else "medium" if score <= 7 else "hard",
        "follow_up_question": follow_up_question
    }


@router.post("/communication-confidence")
def communication_confidence(request: CommunicationRequest):
    result = analyze_communication_confidence(request.transcript)
    return {
        "level": result["level"],
        "score": result["score"],
        "summary": result["summary"],
        "strengths": result["strengths"],
        "improvement_points": result["improvement_points"],
        "communication_feedback": result["summary"]
    }


@router.get("/download-report/{session_id}")
def download_report(session_id: str):
    session_data = get_report(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    filename = f"deep_hire_interview_report_{session_id}.pdf"
    output_path = os.path.join(REPORTS_DIR, filename)
    report_summary = generate_interview_report(session_data)
    pdf_data = {**session_data, **report_summary}
    generated_path = generate_interview_report_pdf(pdf_data, output_filename=output_path)

    if not generated_path or not os.path.exists(generated_path):
        raise HTTPException(status_code=500, detail="Unable to generate PDF report.")

    return FileResponse(
        path=generated_path,
        media_type="application/pdf",
        filename="DeepHire_Interview_Report.pdf"
    )