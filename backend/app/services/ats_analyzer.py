import re


def _normalize_keyword(value):
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9+#]+", " ", str(value)).strip().lower()


def _extract_keywords(values):
    keywords = set()

    if not values:
        return keywords

    if isinstance(values, str):
        values = [values]

    for item in values:
        if item is None:
            continue
        if isinstance(item, (list, tuple, set)):
            keywords.update(_extract_keywords(item))
            continue

        normalized = _normalize_keyword(item)
        if not normalized:
            continue

        tokens = re.findall(r"[a-z0-9+#]{2,}", normalized)
        keywords.update(tokens)

    return keywords


def analyze_ats(data):
    data = data or {}
    skills = [str(skill) for skill in (data.get("skills") or []) if skill]
    experience = data.get("experience") or []
    projects = data.get("projects") or []
    education = data.get("education") or []
    jd_skills = data.get("jd_skills") or []
    jd_description = data.get("job_description") or ""

    score = 100
    missing_sections = []
    suggestions = []

    if not skills:
        score -= 20
        missing_sections.append("Skills")
        suggestions.append("Add a skills section with relevant technical tools and frameworks.")
    elif len(skills) < 4:
        score -= 8
        suggestions.append("Add more technical skills tied to the role.")

    if not experience:
        score -= 10
        missing_sections.append("Experience")
        suggestions.append("Add internship or work experience, even if brief.")
    elif len(experience) == 1:
        score -= 4

    if not projects:
        score -= 10
        missing_sections.append("Projects")
        suggestions.append("Include 1-2 strong projects that show practical application.")
    elif len(projects) == 1:
        score -= 4
        suggestions.append("Add one additional project or a deeper case study.")

    if not education:
        score -= 6
        missing_sections.append("Education")
        suggestions.append("Include the degree, field of study, and timeline clearly.")

    optional_sections = {
        "Certifications": "Add a certifications section if relevant to the role.",
        "GitHub": "Include a GitHub profile or project links.",
        "LinkedIn": "Add a LinkedIn profile for recruiter visibility."
    }

    # JD relevance should influence scoring, but only when there is actual JD data.
    jd_keywords = _extract_keywords(jd_skills)
    if jd_description:
        jd_keywords.update(_extract_keywords(jd_description))

    if jd_keywords:
        resume_keywords = _extract_keywords(skills)
        matched_jd_keywords = jd_keywords & resume_keywords
        if matched_jd_keywords:
            relevance_bonus = min(12, round((len(matched_jd_keywords) / max(1, len(jd_keywords))) * 12, 1))
            score += relevance_bonus
            suggestions.append(f"Strong keyword overlap with the job description ({len(matched_jd_keywords)} matches).")
        else:
            score -= 6
            suggestions.append("Add more job-relevant skills and keywords from the job description.")

    for section, suggestion in optional_sections.items():
        if not any(section.lower() in str(value).lower() for value in [data.get("certifications"), data.get("github"), data.get("linkedin"), data.get("links") or []]):
            suggestions.append(suggestion)

    score = max(0, min(100, round(score, 1)))

    return {
        "ats_score": score,
        "missing_sections": list(dict.fromkeys(missing_sections)),
        "ats_suggestions": list(dict.fromkeys(suggestions))
    }