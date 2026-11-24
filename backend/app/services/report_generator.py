def generate_interview_report(session_data):

    scores = session_data.get("scores", []) if session_data else []
    answers = session_data.get("answers", []) if session_data else []
    difficulties = session_data.get("difficulties", []) if session_data else []
    follow_ups = session_data.get("follow_ups", []) if session_data else []
    questions = session_data.get("questions", []) if session_data else []
    communication_metrics = session_data.get("communication_metrics", []) if session_data else []

    if not scores:
        average_score = 0
    else:
        average_score = round(sum(scores) / len(scores), 2)

    if average_score >= 8:
        performance = "Excellent"
        recommendation = "Strong Candidate"
    elif average_score >= 6:
        performance = "Good"
        recommendation = "Recommended"
    elif average_score >= 4:
        performance = "Average"
        recommendation = "Needs Improvement"
    else:
        performance = "Needs Improvement"
        recommendation = "Not Recommended"

    strengths = []
    weaknesses = []

    if average_score >= 7:
        strengths.append("Good technical understanding.")
    else:
        weaknesses.append("Technical knowledge needs improvement.")

    if len(answers) >= 3:
        strengths.append("Attempted multiple interview questions.")
    else:
        weaknesses.append("Provide more detailed answers.")

    if average_score >= 8:
        strengths.append("Strong analytical reasoning and depth in responses.")
    elif average_score >= 5:
        strengths.append("Shows basic understanding with room for deeper technical depth.")
    else:
        weaknesses.append("Needs stronger fundamentals and clearer technical explanations.")

    if difficulties:
        progression = " -> ".join(difficulties)
    else:
        progression = "Not tracked"

    topics = []
    if session_data and session_data.get("resume_data"):
        topics.extend(session_data.get("resume_data", {}).get("skills", []))
        topics.extend(session_data.get("resume_data", {}).get("projects", []))

    strongest_topics = topics[:3] if topics else ["Core technical fundamentals"]
    weakest_topics = ["Conceptual depth", "Problem-solving clarity"]

    communication_scores = [item.get("score") for item in communication_metrics if item.get("score") is not None]
    communication_score = round(sum(communication_scores) / len(communication_scores), 1) if communication_scores else 0
    if communication_score >= 8:
        communication_level = "Strong"
    elif communication_score >= 5.5:
        communication_level = "Moderate"
    else:
        communication_level = "Needs Improvement"

    communication_strengths = []
    communication_improvements = []
    for metric in communication_metrics:
        communication_strengths.extend(metric.get("strengths", []))
        communication_improvements.extend(metric.get("improvement_points", []))

    return {
        "total_questions": len(questions),
        "answered_questions": len(answers),
        "average_score": average_score,
        "performance": performance,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendation": recommendation,
        "questions_attempted": answers,
        "strongest_topics": strongest_topics,
        "weakest_topics": weakest_topics,
        "difficulty_progression": progression,
        "technical_strengths": strengths,
        "technical_weaknesses": weaknesses,
        "overall_recommendation": recommendation,
        "follow_up_questions_used": follow_ups,
        "difficulty": session_data.get("difficulty", "medium") if session_data else "medium"
        ,"communication_score": communication_score
        ,"communication_level": communication_level
        ,"communication_strengths": list(dict.fromkeys(communication_strengths))
        ,"communication_improvements": list(dict.fromkeys(communication_improvements))
        ,"visual_engagement_indicators": {
            "face_presence": "Tracked locally in the browser when camera is enabled.",
            "identity_recognition": False
        }
    }