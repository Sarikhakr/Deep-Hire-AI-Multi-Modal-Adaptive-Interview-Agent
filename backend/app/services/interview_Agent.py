def generate_greeting(resume_data):
    """
    Generates a personalized greeting for the candidate.
    """

    name = resume_data.get("name", "Candidate")
    skills = resume_data.get("skills", [])
    internships = resume_data.get("internships", [])

    greeting = f"Hello {name}!\n\n"
    greeting += "Welcome to DeepHire AI.\n\n"
    greeting += "I have analyzed your resume.\n"

    if skills:
        greeting += (
            f"I noticed you have skills in {', '.join(skills[:5])}.\n"
        )

    if internships:
        greeting += (
            f"You have completed {len(internships)} internship(s), which is a great addition to your profile.\n"
        )

    greeting += "\nLet's begin your interview!"

    return greeting