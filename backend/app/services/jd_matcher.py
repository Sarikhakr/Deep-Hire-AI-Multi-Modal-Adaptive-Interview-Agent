import re

def match_job_description(resume_data, job_description):

    resume_skills = set(skill.lower() for skill in resume_data["skills"])

    # Extract words from JD
    words = re.findall(r"[A-Za-z\+\#]+", job_description.lower())

    jd_words = set(words)

    matched = []
    missing = []

    for skill in resume_skills:
        if skill in jd_words:
            matched.append(skill.title())

    for word in jd_words:
        if word in [
            "python",
            "java",
            "c++",
            "sql",
            "html",
            "css",
            "javascript",
            "machine",
            "learning",
            "tensorflow",
            "pytorch",
            "mongodb",
            "fastapi",
            "aws",
            "docker",
            "git"
        ]:
            if word.title() not in matched:
                missing.append(word.title())

    total = len(matched) + len(missing)

    score = 0 if total == 0 else round((len(matched) / total) * 100)

    return {
        "jd_match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }