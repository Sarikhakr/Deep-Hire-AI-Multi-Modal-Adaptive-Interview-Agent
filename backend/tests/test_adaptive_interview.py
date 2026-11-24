import unittest

from backend.app.services.interview_session import create_session, save_answer, get_question
from backend.app.services.question_generator import generate_question_for_context, generate_questions


class AdaptiveInterviewTests(unittest.TestCase):
    def test_session_tracks_progression_and_adapts_difficulty(self):
        session_id = create_session(
            ["Initial question"],
            interview_context={
                "resume_data": {
                    "department": "Computer Science / AI-ML",
                    "skills": ["Python", "Machine Learning"],
                    "projects": ["Crop disease detection"],
                    "experience": ["AI Intern"]
                }
            }
        )

        next_question = save_answer(session_id, "I used Random Forest for crop disease prediction.", 9, "Strong answer")
        self.assertIsNotNone(next_question)
        self.assertNotEqual(next_question, "Initial question")
        self.assertIn("Random Forest", next_question)

        session = create_session(["Initial question"], interview_context={"resume_data": {"department": "General Engineering", "skills": ["Python"], "projects": [], "experience": []}})
        weak_question = save_answer(session, "Not much", 2, "Weak answer")
        self.assertIsNotNone(weak_question)
        self.assertTrue(
            any(keyword in weak_question.lower() for keyword in ["python", "basic", "fundamental", "explain", "what"])
        )

    def test_question_generator_uses_resume_and_department_context(self):
        question = generate_question_for_context(
            resume_data={
                "department": "Civil Engineering",
                "skills": ["AutoCAD", "Surveying"],
                "projects": ["Bridge design"],
                "experience": ["Site Engineer"],
            },
            previous_questions=[],
            previous_answers=[],
            previous_scores=[],
            difficulty="medium",
            jd_skills=["AutoCAD", "Construction"]
        )

        self.assertIsInstance(question, str)
        self.assertTrue(len(question) > 10)

    def test_programming_resumes_include_coding_questions(self):
        questions = generate_questions(
            {
                "department": "Computer Science / AI-ML",
                "skills": ["Python", "Machine Learning", "SQL"],
                "projects": ["Crop disease detection"],
                "experience": ["AI Intern"],
            },
            jd_skills=["Python", "SQL"],
            max_questions=12
        )

        self.assertTrue(any("Coding Problem" in q or "Write a function" in q or "SQL" in q for q in questions))


if __name__ == "__main__":
    unittest.main()
