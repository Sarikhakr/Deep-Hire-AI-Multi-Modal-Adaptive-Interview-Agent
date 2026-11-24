import uuid
from datetime import datetime, timezone

sessions = {}


def _normalize_difficulty(score):
    if score is None:
        return "medium"
    if score <= 4:
        return "easy"
    if score <= 7:
        return "medium"
    return "hard"


def create_session(questions, interview_context=None):
    session_id = str(uuid.uuid4())

    interview_context = interview_context or {}
    resume_data = interview_context.get("resume_data", {}) or {}
    jd_skills = interview_context.get("jd_skills", []) or []

    session = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "questions": questions or [],
        "asked_questions": [],
        "current": 0,
        "answers": [],
        "scores": [],
        "feedback": [],
        "difficulties": [],
        "follow_ups": [],
        "question_history": [],
        "topics": [],
        "resume_data": resume_data,
        "jd_skills": jd_skills,
        "difficulty": "medium",
        "question_number": 0,
        "target_questions": 8,
        "max_questions": 10,
        "communication_metrics": [],
        "last_question": None,
        "current_question": None
    }

    if questions:
        session["current_question"] = questions[0]
        session["question_history"].append(questions[0])
        session["last_question"] = questions[0]
        session["question_number"] = 1
        session["asked_questions"].append(questions[0])

    sessions[session_id] = session
    return session_id


def get_question(session_id):
    session = sessions.get(session_id)

    if not session:
        return None

    if session["current"] >= len(session["questions"]):
        return None

    current_question = session["questions"][session["current"]]
    session["current_question"] = current_question
    session["last_question"] = current_question
    session["question_number"] = session["current"] + 1
    return current_question


def save_answer(session_id, answer, score, feedback=None, follow_up_question=None, communication=None):
    session = sessions.get(session_id)

    if not session:
        return None

    session["answers"].append(answer)
    session["scores"].append(score)
    if communication:
        session["communication_metrics"].append(communication)
    if feedback:
        session["feedback"].append(feedback)
    else:
        session["feedback"].append("")

    difficulty = _normalize_difficulty(score)
    session["difficulties"].append(difficulty)
    session["difficulty"] = difficulty

    current_question = session.get("current_question")
    if current_question is not None:
        session["question_history"].append(current_question)

    if follow_up_question:
        session["follow_ups"].append(follow_up_question)

    session["current"] += 1
    session["question_number"] = session["current"] + 1

    answered_count = len(session["answers"])
    average_score = sum(session["scores"]) / answered_count
    weak_answers = sum(1 for answer_score in session["scores"] if answer_score <= 4)
    should_conclude = (
        answered_count >= session.get("max_questions", 10)
        or (answered_count >= session.get("target_questions", 8) and average_score < 7.5)
        or (answered_count >= 5 and weak_answers >= 3 and average_score < 5)
    )

    if should_conclude:
        session["current_question"] = None
        return None

    next_question = _next_adaptive_question(session)
    session["current_question"] = next_question
    return next_question


def _next_adaptive_question(session):
    from backend.app.services.question_generator import generate_question_for_context

    questions = session.get("questions", [])
    if not questions and not session.get("resume_data"):
        return None

    previous_questions = session.get("question_history", [])
    previous_answers = session.get("answers", [])
    previous_scores = session.get("scores", [])
    difficulty = session.get("difficulty", "medium")

    next_question = generate_question_for_context(
        resume_data=session.get("resume_data", {}),
        previous_questions=previous_questions,
        previous_answers=previous_answers,
        previous_scores=previous_scores,
        difficulty=difficulty,
        jd_skills=session.get("jd_skills", [])
    )

    if next_question and next_question not in previous_questions:
        session["asked_questions"].append(next_question)
        return next_question

    for question in questions:
        if question not in previous_questions:
            session["asked_questions"].append(question)
            return question

    return None


def get_report(session_id):
    session = sessions.get(session_id)

    if not session:
        return None

    total = sum(session["scores"])
    average = total / len(session["scores"]) if session["scores"] else 0

    return {
        "questions": session.get("asked_questions", session["questions"]),
        "answers": session["answers"],
        "scores": session["scores"],
        "feedback": session["feedback"],
        "difficulties": session["difficulties"],
        "follow_ups": session["follow_ups"],
        "question_history": session["question_history"],
        "resume_data": session.get("resume_data", {}),
        "jd_skills": session.get("jd_skills", []),
        "total_score": total,
        "average_score": average,
        "difficulty": session.get("difficulty", "medium"),
        "topics": session.get("topics", []),
        "communication_metrics": session.get("communication_metrics", []),
        "created_at": session.get("created_at"),
        "current_question": session.get("current_question")
    }