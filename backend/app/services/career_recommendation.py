def recommend_roles(department=None, skills=None, interview_score=0, jd_match=0, experience=None):
    department = department or "General Engineering"
    skills = skills or []
    experience = experience or []
    skill_text = " ".join(str(skill) for skill in skills).lower()

    roles = []

    if "ai" in department.lower() or "machine learning" in skill_text or "python" in skill_text:
        roles.append({
            "role": "AI/ML Engineer",
            "match_score": min(95, max(60, int((interview_score + jd_match) / 2))),
            "reasons": [
                "Strong fit for AI, ML, and Python-based problem solving.",
                "Suitable for data-driven product and model-building roles."
            ]
        })

    if "sql" in skill_text or "data" in skill_text or "python" in skill_text:
        roles.append({
            "role": "Data Scientist",
            "match_score": min(90, max(55, int((interview_score + jd_match + 5) / 2))),
            "reasons": [
                "Strong analytical and data handling skills.",
                "Good alignment with reporting, modeling, and experimentation."
            ]
        })

    if "python" in skill_text or "sql" in skill_text or "javascript" in skill_text:
        roles.append({
            "role": "Software Developer",
            "match_score": min(88, max(50, int((interview_score + jd_match) / 2 - 5))),
            "reasons": [
                "Good application development and problem-solving foundation.",
                "Matches modern software engineering workflows."
            ]
        })

    if not roles:
        roles.append({
            "role": "General Engineer",
            "match_score": max(50, min(85, interview_score)),
            "reasons": [
                "Your profile shows a solid engineering background.",
                "You may benefit from targeted domain specialization."
            ]
        })

    for role in roles:
        if not role.get("experience_required"):
            role["experience_required"] = "Entry to Mid-Level"

    return roles
