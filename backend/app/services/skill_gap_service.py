def analyze_skill_gap(candidate_skills=None, required_skills=None):
    candidate_skills = candidate_skills or []
    required_skills = required_skills or []

    normalized_candidate = {str(skill).strip().lower() for skill in candidate_skills if str(skill).strip()}
    normalized_required = [str(skill).strip() for skill in required_skills if str(skill).strip()]

    matched_skills = []
    missing_skills = []
    missing_skill_details = []

    for skill in normalized_required:
        skill_key = skill.lower()
        if skill_key in normalized_candidate:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            priority = "High Priority" if skill.lower() in {"docker", "aws", "kubernetes", "mlops", "python", "sql"} else "Medium Priority"
            missing_skill_details.append({
                "skill": skill,
                "priority": priority,
                "reason": f"Add hands-on practice with {skill} to close the skill gap."
            })

    skill_match_percentage = 0 if not normalized_required else round((len(matched_skills) / len(normalized_required)) * 100)

    return {
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage,
        "missing_skill_details": missing_skill_details,
        "summary": f"You match {skill_match_percentage}% of the required skills and need improvement in {len(missing_skills)} area(s)."
    }
