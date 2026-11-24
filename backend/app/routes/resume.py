from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.app.utils.pdf_parser import extract_text_from_pdf
from backend.app.services.resume_analyzer import analyze_resume
from backend.app.services.resume_score import calculate_resume_score
from backend.app.services.resume_feedback import generate_feedback
from backend.app.services.ats_analyzer import analyze_ats
from backend.app.models.jd_models import JDRequest
from backend.app.services.jd_matcher import match_job_description

from backend.app.services.interview_Agent import generate_greeting
from backend.app.services.question_generator import generate_questions
from backend.app.services.interview_session import create_session

#from backend.app.services.department_detector import detect
from backend.app.services.department_detector import detect_department
router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Save uploaded resume
    file_path = os.path.join(UPLOAD_FOLDER, "resume.pdf")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Analyze Resume
    resume_data = analyze_resume(text)

    # Resume Score
    score = calculate_resume_score(resume_data)
    resume_data["resume_score"] = score

    # Resume Feedback
    feedback = generate_feedback(resume_data)
    resume_data["strengths"] = feedback["strengths"]
    resume_data["weaknesses"] = feedback["weaknesses"]

    # ATS Analysis
    ats_result = analyze_ats(resume_data)
    resume_data["ats_score"] = ats_result["ats_score"]
    resume_data["missing_sections"] = ats_result["missing_sections"]
    resume_data["ats_suggestions"] = ats_result["ats_suggestions"]

    # AI Greeting
    greeting = generate_greeting(resume_data)

    # Generate Interview Questions
    questions = generate_questions(resume_data, max_questions=10)

    # Create Interview Session
    session_id = create_session(
        questions,
        interview_context={
            "resume_data": resume_data,
            "jd_skills": []
        }
    )

    return {
        "message": "Resume analyzed successfully",
        "greeting": greeting,
        "session_id": session_id,
        "first_question": questions[0] if questions else None,
        "questions": questions,
        "data": resume_data
    }


@router.post("/jd-match")
async def jd_match(request: JDRequest):

    file_path = os.path.join(UPLOAD_FOLDER, "resume.pdf")

    if not os.path.exists(file_path):
        return {
            "message": "Please upload a resume first."
        }

    # Extract Resume
    text = extract_text_from_pdf(file_path)

    resume_data = analyze_resume(text)

    department = detect_department(resume_data)
    resume_data["department"] = department

    # Match with Job Description
    result = match_job_description(
        resume_data,
        request.job_description
    )

    return {
        "message": "JD Matching Completed",
        "data": result
    }