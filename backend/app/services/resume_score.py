def calculate_resume_score(data):

    score = 0

    # Skills
    score += min(len(data["skills"]) * 5, 40)

    # Projects
    score += min(len(data["projects"]) * 10, 30)

    # Experience
    score += min(len(data["experience"]) * 10, 20)

    # Education
    if len(data["education"]) > 0:
        score += 10

    return min(score, 100)