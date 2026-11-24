def generate_feedback(data):

    strengths = []
    weaknesses = []

    # Skills
    if len(data["skills"]) >= 8:
        strengths.append("Strong technical skill set.")
    else:
        weaknesses.append("Add more technical skills relevant to your target role.")

    # Projects
    if len(data["projects"]) >= 3:
        strengths.append("Good number of academic/personal projects.")
    else:
        weaknesses.append("Include more practical projects.")

    # Experience
    if len(data["experience"]) > 0:
        strengths.append("Relevant internship/work experience found.")
    else:
        weaknesses.append("Try to gain internship or practical experience.")

    # Education
    if len(data["education"]) > 0:
        strengths.append("Educational details are clearly mentioned.")
    else:
        weaknesses.append("Include your educational qualifications.")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses
    }