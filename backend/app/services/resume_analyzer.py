SKILLS_DATABASE = [
    "Python",
    "C++",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Machine Learning",
    "Deep Learning",
    "CNN",
    "RNN",
    "TensorFlow",
    "PyTorch",
    "MongoDB",
    "FastAPI",
    "AWS",
    "Git",
    "Docker"
]

EDUCATION_KEYWORDS = [
    "Bachelor",
    "Master",
    "B.E",
    "B.Tech",
    "M.Tech",
    "Computer Science",
    "Artificial Intelligence",
    "Machine Learning",
    "CGPA",
    "Higher Secondary",
    "SSLC",
    "HSE"
]


def analyze_resume(text: str):

    data = {
        "name": "",
        "skills": [],
        "education": [],
        "projects": [],
        "experience": []
    }

    lines = text.split("\n")
    text_lower = text.lower()

    # -----------------------
    # Name
    # -----------------------
    for line in lines:
        if line.strip():
            data["name"] = line.strip()
            break

    # -----------------------
    # Skills
    # -----------------------
    for skill in SKILLS_DATABASE:
        if skill.lower() in text_lower:
            data["skills"].append(skill)

    # -----------------------
    # Education
    # -----------------------
    for keyword in EDUCATION_KEYWORDS:
        if keyword.lower() in text_lower:
            data["education"].append(keyword)

    # -----------------------
    # Projects & Experience
    # -----------------------

    current_section = None

    SECTION_HEADERS = [
        "PROJECTS",
        "RELEVANT EXPERIENCE",
        "SKILLS",
        "EDUCATION",
        "CERTIFICATIONS",
        "ACHIEVEMENTS"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        upper = line.upper()

        # Detect Sections
        if "PROJECTS" in upper:
            current_section = "projects"
            continue

        elif "RELEVANT EXPERIENCE" in upper or upper == "EXPERIENCE":
            current_section = "experience"
            continue

        elif any(
            header in upper
            for header in SECTION_HEADERS
            if header not in ["PROJECTS", "RELEVANT EXPERIENCE"]
        ):
            current_section = None
            continue

        # -----------------------
        # Projects
        # -----------------------
        if current_section == "projects":

            if line.startswith("•"):
                continue

            if len(line.split()) > 8:
                continue

            data["projects"].append(line)

        # Experience
        # -----------------------
        elif current_section == "experience":

            if line.startswith("•"):
                continue

            if any(month in line for month in [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec",
                "2024","2025","2026","2027","2028"
            ]):
                continue

            data["experience"].append(line)

    return data