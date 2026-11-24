import random
import re

from backend.app.services.coding_questions import get_coding_question_prompt


def _normalize_skill(value):
    if not value:
        return ""
    return str(value).strip().lower()


def _score_to_difficulty(score):
    if score is None:
        return "medium"
    if score <= 4:
        return "easy"
    if score <= 7:
        return "medium"
    return "hard"


def _build_skill_questions(skill_name):
    skill = skill_name.strip()
    questions = {
        "Python": "How have you used Python in your projects?",
        "Machine Learning": "Which machine learning algorithm have you used and why?",
        "Deep Learning": "Explain one deep learning model you have worked with.",
        "TensorFlow": "How have you used TensorFlow in your projects?",
        "AWS": "How would you deploy an application using AWS?",
        "MongoDB": "Why would you choose MongoDB for an application?",
        "SQL": "Explain the difference between INNER JOIN and LEFT JOIN in SQL.",
        "Git": "How do you use Git when working on a project?",
        "AutoCAD": "Describe how you used AutoCAD in a design or drafting project.",
        "Surveying": "How has surveying influenced your engineering decisions on-site?",
        "Structural Design": "Explain a structural design problem you solved and how you approached it.",
        "Thermodynamics": "Explain a thermodynamics concept you applied in an engineering project.",
        "CAD": "How has CAD improved your design workflow in engineering work?",
        "Embedded Systems": "Explain one embedded systems project you worked on and the design trade-offs involved.",
        "Power Systems": "Describe a power systems challenge you solved and how you analyzed it.",
        "Signal Processing": "How do you evaluate signal quality or filtering in a communication system?",
        "Data Structures": "How have data structures improved the performance of your solution?",
        "Algorithms": "Explain how you choose an algorithm for a problem under time and resource constraints."
    }
    return questions.get(skill, f"Can you explain how you applied {skill} in a real project?")


def _build_follow_up_question(answer, previous_question, resume_data=None, jd_skills=None):
    resume_data = resume_data or {}
    jd_skills = jd_skills or []
    answer_text = (answer or "").lower()

    keywords = []
    for skill in resume_data.get("skills", []):
        skill_name = str(skill).lower()
        if skill_name in answer_text:
            keywords.append(skill_name)

    project_names = resume_data.get("projects", [])
    for project in project_names:
        p = str(project).lower()
        if len(p) > 3 and p in answer_text:
            keywords.append(p)

    for skill in jd_skills:
        s = str(skill).lower()
        if s in answer_text:
            keywords.append(s)

    common_terms = [
        "random forest", "neural network", "cnn", "rnn", "sql", "python",
        "machine learning", "deep learning", "aws", "mongodb", "autocad",
        "solidworks", "transformer", "microcontroller", "thermodynamics",
        "surveying", "foundation", "cad", "power system", "signal processing"
    ]
    for term in common_terms:
        if term in answer_text:
            keywords.append(term)

    if not keywords:
        direct_terms = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", answer or "")
        for term in direct_terms:
            keywords.append(term.lower())

    if not keywords:
        if len((answer or "").split()) >= 25:
            if jd_skills:
                skill = str(jd_skills[0])
                return f"Why did you choose {skill} over other alternatives in your solution?"
            return "What trade-offs did you consider when making the design or technical decision in your answer?"
        return "Can you explain the basic idea behind the technology you mentioned in simpler terms?"

    topic = keywords[0].replace("-", " ")
    if topic == "random forest":
        return "Why did you choose Random Forest instead of a neural network or another algorithm for this problem?"
    if len(topic) > 2:
        return f"Why did you choose {topic.title()} as the key approach in this situation?"

    return "Can you explain the reasoning behind the decision you just described?"


def generate_questions(resume_data, jd_skills=None, max_questions=10):
    questions = []

    department = resume_data.get("department", "General Engineering")
    skills = resume_data.get("skills", [])
    projects = resume_data.get("projects", [])
    experience = resume_data.get("experience", [])
    jd_skills = jd_skills or []

    department_questions = {
        "Computer Science / AI-ML": [
            "Explain a machine learning project you have implemented.",
            "What is the difference between supervised and unsupervised learning?",
            "What is the difference between CNN and RNN?",
            "How do you evaluate the performance of a machine learning model?",
            "Explain overfitting and how you can prevent it.",
            "How would you deploy a machine learning model in production?"
        ],
        "Electronics and Communication": [
            "What is the difference between analog and digital signals?",
            "Explain the working of a microcontroller.",
            "What is an embedded system?",
            "Explain the difference between a microprocessor and microcontroller.",
            "What are the applications of IoT in electronics?",
            "How do you test and validate a communication system design?"
        ],
        "Electrical Engineering": [
            "Explain the working principle of a transformer.",
            "What is the difference between AC and DC?",
            "What are electrical machines?",
            "Explain the concept of power factor.",
            "What are the major components of a power system?",
            "How do you analyze efficiency in an electrical system?"
        ],
        "Mechanical Engineering": [
            "Explain the first law of thermodynamics.",
            "What is the difference between CNC and conventional machining?",
            "What is CAD and how is it used in mechanical engineering?",
            "Explain the difference between stress and strain.",
            "What are the applications of SolidWorks in mechanical design?",
            "How would you improve the efficiency of a mechanical system?"
        ],
        "Civil Engineering": [
            "What is the difference between cement and concrete?",
            "Explain the different types of foundations.",
            "What is surveying and why is it important?",
            "Explain the difference between dead load and live load.",
            "What are the applications of AutoCAD in civil engineering?",
            "How do you ensure structural safety in a design review?"
        ],
        "General Engineering": [
            "Tell me about your engineering background.",
            "Explain one technical project you have worked on.",
            "What technical skills are you most confident in?",
            "Describe a challenging problem you solved.",
            "Why did you choose your engineering specialization?",
            "How do you validate an engineering solution in practice?"
        ]
    }

    questions.extend(department_questions.get(department, department_questions["General Engineering"]))

    for skill in skills:
        if skill:
            questions.append(_build_skill_questions(str(skill)))

    for skill in jd_skills:
        if skill:
            skill_name = str(skill)
            if skill_name not in skills:
                questions.append(_build_skill_questions(skill_name))

    for project in projects[:2]:
        project_name = str(project).strip()
        if project_name:
            questions.append(f"Explain your project '{project_name}'. What was your role and which technologies did you use?")

    for exp in experience[:1]:
        exp_name = str(exp).strip()
        if exp_name:
            questions.append(f"Tell me about your experience at '{exp_name}'. What did you learn from it?")

    coding_question = get_coding_question_prompt(
        difficulty="easy",
        candidate_skills=list(skills) + list(jd_skills),
        candidate_department=department,
    )
    if coding_question:
        questions.append(coding_question)

    unique_questions = []
    for question in questions:
        if question and question not in unique_questions:
            unique_questions.append(question)

    if len(unique_questions) < max_questions:
        general_questions = [
            "Explain a technical problem you solved and how you approached it.",
            "What is one concept you are most confident in and why?",
            "How do you decide which tools or technologies to use for a project?",
            "Describe a project where you improved quality, speed, or performance."
        ]
        for q in general_questions:
            if q not in unique_questions:
                unique_questions.append(q)

    random.SystemRandom().shuffle(unique_questions)
    selected_questions = unique_questions[:max_questions]
    if coding_question and max_questions > 0 and coding_question not in selected_questions:
        selected_questions[-1] = coding_question
    return selected_questions


def generate_question_for_context(resume_data=None, previous_questions=None, previous_answers=None, previous_scores=None, difficulty="medium", jd_skills=None):
    resume_data = resume_data or {}
    previous_questions = previous_questions or []
    previous_answers = previous_answers or []
    previous_scores = previous_scores or []
    jd_skills = jd_skills or []

    pool = generate_questions(resume_data, jd_skills=jd_skills, max_questions=50)

    if difficulty == "easy":
        easy_prompts = [
            "Explain the basic concept behind one tool or technology from your resume.",
            "What is the main purpose of the project or work you described in your resume?",
            "What is a technical concept you understand well and can explain clearly?"
        ]
        pool = easy_prompts + pool
    elif difficulty == "hard":
        advanced_prompts = [
            "How would you optimize a system or model for scale, performance, or reliability?",
            "What trade-offs would you consider when choosing architecture or algorithms for a real-world problem?",
            "Explain how you would validate and improve the quality of a technical solution in production."
        ]
        pool = pool + advanced_prompts

    filtered = []
    for q in pool:
        if q not in previous_questions and q not in filtered:
            filtered.append(q)

    if previous_answers and previous_scores:
        last_score = previous_scores[-1]
        last_answer = previous_answers[-1]
        if last_score >= 8 and last_answer:
            follow_up = _build_follow_up_question(last_answer, previous_questions[-1] if previous_questions else None, resume_data, jd_skills)
            if follow_up and follow_up not in previous_questions:
                return follow_up

    if not any("Coding Problem" in q for q in previous_questions):
        coding_question = next((q for q in filtered if "Coding Problem" in q), None)
        if coding_question:
            return coding_question

    if filtered:
        return filtered[0]

    if resume_data.get("department"):
        return f"Can you explain one project or concept from your {resume_data.get('department')} background in more detail?"

    return "Explain a technical project or problem you are proud of and the reasoning behind your approach."
