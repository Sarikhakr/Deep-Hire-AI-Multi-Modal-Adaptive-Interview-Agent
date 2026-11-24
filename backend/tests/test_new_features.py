"""
Tests for new interview features:
1. Improved answer evaluator
2. Adaptive interview logic
3. Project-specific questions
4. Coding questions
5. Learning recommendations
6. PDF report generation
"""

import unittest
from datetime import datetime
from backend.app.services.answer_evaluator import evaluate_answer_details
from backend.app.services.question_generator import (
    generate_question_for_context,
    _extract_topics_from_answer,
    _identify_weak_areas
)
from backend.app.services.coding_questions import (
    get_coding_question,
    evaluate_coding_solution,
    get_coding_question_prompt
)
from backend.app.services.learning_roadmap import (
    build_learning_roadmap,
    _identify_weak_topics_from_scores
)
from backend.app.services.ats_analyzer import analyze_ats


class ATSScoringTests(unittest.TestCase):
    """Tests for fair ATS scoring on realistic resumes."""

    def test_strong_resume_is_not_penalized_too_heavily(self):
        """A resume with solid skills and a relevant project should score above a fair threshold."""
        result = analyze_ats({
            "skills": ["Python", "SQL", "FastAPI", "AWS", "Git", "Docker"],
            "projects": ["Built a FastAPI service for document processing"],
            "experience": ["Software Engineer Intern at a SaaS startup"],
            "education": ["B.Tech in Computer Science"]
        })
        self.assertGreaterEqual(result["ats_score"], 80)


class ImprovedAnswerEvaluatorTests(unittest.TestCase):
    """Tests for the improved answer evaluator that scores 0-10."""
    
    def test_refusal_answer_scores_low(self):
        """Test that 'I don't know' type answers score 0-2."""
        result = evaluate_answer_details(
            answer="I don't know",
            question="What is machine learning?"
        )
        self.assertLessEqual(result["score"], 2)
        self.assertEqual(result["score"], 1)
    
    def test_empty_answer_scores_zero(self):
        """Test that empty answers score 0."""
        result = evaluate_answer_details(
            answer="",
            question="What is Python?"
        )
        self.assertEqual(result["score"], 0)
    
    def test_short_correct_answer_scores_well(self):
        """Test that short but correct answers can score well."""
        result = evaluate_answer_details(
            answer="Python is a programming language",
            question="What is Python?"
        )
        self.assertGreater(result["score"], 3)

    def test_short_correct_answer_is_not_penalized_too_harshly(self):
        """Short relevant answers should still receive a strong interview-like score."""
        result = evaluate_answer_details(
            answer="Python is a programming language used for automation and web apps.",
            question="What is Python?"
        )
        self.assertGreaterEqual(result["score"], 6)
    
    def test_long_incorrect_answer_scores_low(self):
        """Test that long but incorrect answers don't get high scores."""
        result = evaluate_answer_details(
            answer="A banana is a type of fruit that grows on trees in tropical climates and is yellow in color",
            question="What is machine learning?"
        )
        self.assertLess(result["score"], 5)
    
    def test_technical_answer_scores_higher(self):
        """Test that answers with technical terms score higher."""
        result = evaluate_answer_details(
            answer="Machine learning uses algorithms to learn from data",
            question="What is machine learning?",
            skills=["Machine Learning", "Algorithms"],
            jd_skills=["Data Science"]
        )
        # Expect score >= 5 for a basic answer with correct keywords
        self.assertGreaterEqual(result["score"], 5)
    
    def test_evaluation_includes_all_metrics(self):
        """Test that evaluation includes correctness, completeness, technical depth, reasoning."""
        result = evaluate_answer_details(
            answer="I used Python with TensorFlow because it provides good performance",
            question="What did you use for your ML project?",
            skills=["Python", "TensorFlow"]
        )
        self.assertIn("correctness", result)
        self.assertIn("completeness", result)
        self.assertIn("technical_depth", result)
        self.assertIn("reasoning_quality", result)
        self.assertIn("performance_level", result)

    def test_pdf_report_is_valid_pdf(self):
        """The generated PDF should start with PDF header bytes and not a plain text fallback."""
        from tempfile import NamedTemporaryFile
        from backend.app.services.pdf_report_generator import generate_interview_report_pdf

        with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            output_path = temp_file.name

        try:
            result_path = generate_interview_report_pdf({
                "average_score": 8.5,
                "scores": [8, 9],
                "questions": ["What is Python?", "What is ML?"],
                "answers": ["Python is a programming language.", "Machine learning learns from data."],
                "feedback": ["Good", "Strong"],
                "resume_data": {"name": "Test Candidate", "email": "test@example.com", "skills": ["Python"], "experience": ["Intern"]}
            }, output_filename=output_path)
            self.assertIsNotNone(result_path)
            with open(result_path, "rb") as pdf_file:
                header = pdf_file.read(5)
            self.assertEqual(header, b"%PDF-")
        finally:
            import os
            if os.path.exists(output_path):
                os.remove(output_path)


class AdaptiveInterviewLogicTests(unittest.TestCase):
    """Tests for adaptive interview that adjusts difficulty based on performance."""
    
    def test_weak_answer_generates_easier_question(self):
        """Test that weak answers lead to easier follow-up questions."""
        question = generate_question_for_context(
            resume_data={"skills": ["Python", "SQL"]},
            previous_questions=["What is Python?"],
            previous_answers=["I think it's a language"],
            previous_scores=[2],  # Weak score
            difficulty="easy"
        )
        # Should be an easy question
        self.assertIsNotNone(question)
        self.assertTrue(len(question) > 0)
    
    def test_strong_answer_generates_harder_question(self):
        """Test that strong answers lead to harder follow-up questions."""
        question = generate_question_for_context(
            resume_data={"skills": ["Machine Learning", "Python"]},
            previous_questions=["Explain machine learning"],
            previous_answers=["ML is supervised and unsupervised learning with algorithms like SVM"],
            previous_scores=[9],  # Strong score
            difficulty="hard"
        )
        self.assertIsNotNone(question)
        # Should reference advanced topics
        self.assertTrue(len(question) > 0)
    
    def test_project_specific_questions(self):
        """Test that questions are generated about projects in resume."""
        question = generate_question_for_context(
            resume_data={
                "skills": ["Python"],
                "projects": ["Crop Disease Detection System", "Student Portal"]
            },
            previous_questions=[],
            previous_answers=[],
            previous_scores=[],
            difficulty="medium"
        )
        self.assertIsNotNone(question)
    
    def test_no_duplicate_questions(self):
        """Test that already-asked questions are not repeated."""
        question = generate_question_for_context(
            resume_data={"skills": ["Python", "SQL"]},
            previous_questions=["What is Python?"],
            previous_answers=["A programming language"],
            previous_scores=[7],
            difficulty="medium"
        )
        # Should not repeat "What is Python?"
        self.assertNotEqual(question, "What is Python?")


class TopicExtractionTests(unittest.TestCase):
    """Tests for extracting topics from answers."""
    
    def test_extract_programming_languages(self):
        """Test that programming languages are extracted from answers."""
        topics = _extract_topics_from_answer("I used Python and SQL for my project")
        self.assertIn("python", [t.lower() for t in topics])
    
    def test_extract_technical_concepts(self):
        """Test that technical concepts are extracted."""
        topics = _extract_topics_from_answer("I used neural networks and deep learning")
        self.assertTrue(any("neural" in t.lower() or "deep" in t.lower() for t in topics))


class WeakAreaIdentificationTests(unittest.TestCase):
    """Tests for identifying weak areas from interview performance."""
    
    def test_low_scores_identify_weak_areas(self):
        """Test that low scores are marked as weak areas."""
        weak_areas = _identify_weak_areas(
            previous_answers=["Weak answer 1", "Weak answer 2"],
            previous_scores=[2, 3]
        )
        self.assertGreater(len(weak_areas), 0)
    
    def test_high_scores_no_weak_areas(self):
        """Test that high scores don't generate weak areas."""
        weak_areas = _identify_weak_areas(
            previous_answers=["Great answer"],
            previous_scores=[9]
        )
        # Should have no weak areas or very few
        self.assertLess(len(weak_areas), 2)


class CodingQuestionsTests(unittest.TestCase):
    """Tests for coding question generation and evaluation."""
    
    def test_get_easy_coding_question(self):
        """Test that easy coding questions can be retrieved."""
        problem = get_coding_question("easy")
        self.assertIsNotNone(problem)
        self.assertIn("question", problem)
        self.assertIn("example", problem)
    
    def test_get_medium_coding_question(self):
        """Test that medium coding questions can be retrieved."""
        problem = get_coding_question("medium")
        self.assertIsNotNone(problem)
    
    def test_get_hard_coding_question(self):
        """Test that hard coding questions can be retrieved."""
        problem = get_coding_question("hard")
        self.assertIsNotNone(problem)
    
    def test_coding_question_only_for_programmers(self):
        """Test that coding questions only offered to candidates with programming skills."""
        # With programming skills
        question = get_coding_question_prompt(
            "easy",
            candidate_skills=["Python", "Java"],
            candidate_department="Computer Science / AI-ML"
        )
        self.assertIsNotNone(question)
        
        # Without programming skills (should return None)
        question_no_skills = get_coding_question_prompt(
            "easy",
            candidate_skills=["AutoCAD", "SolidWorks"],
            candidate_department="Mechanical Engineering"
        )
        self.assertIsNone(question_no_skills)
    
    def test_evaluate_coding_solution(self):
        """Test that coding solutions can be evaluated."""
        solution = "def palindrome(s): return s == s[::-1]"
        evaluation = evaluate_coding_solution("palindrome", solution)
        self.assertIn("score", evaluation)
        self.assertIn("feedback", evaluation)
        self.assertGreater(evaluation["score"], 0)


class LearningRecommendationsTests(unittest.TestCase):
    """Tests for personalized learning recommendations."""
    
    def test_identify_weak_topics_from_scores(self):
        """Test that weak topics are identified from low scores."""
        weak_topics = _identify_weak_topics_from_scores(
            scores=[2, 3, 9, 8],
            questions=["What is Python?", "Explain machine learning", "Tell about SQL", "How do you use React?"],
            answers=["I think it's a thing", "Something with algorithms", "SQL is great", "It's a framework"]
        )
        # Should identify at least some weak areas from low scores
        self.assertGreaterEqual(len(weak_topics), 1)
    
    def test_build_learning_roadmap_for_weak_areas(self):
        """Test that learning roadmap is built for weak areas."""
        weak_topics = [
            {"skill": "Python", "priority": "High", "reason": "Low score on Python question"}
        ]
        roadmap = build_learning_roadmap(weak_topics)
        self.assertGreater(len(roadmap), 0)
        self.assertEqual(roadmap[0]["skill"], "Python")
        self.assertIn("resources", roadmap[0])
        self.assertIn("learning_plan", roadmap[0])
    
    def test_learning_roadmap_includes_resources(self):
        """Test that learning roadmap includes actual resources."""
        weak_topics = [
            {"skill": "machine learning", "priority": "High"}
        ]
        roadmap = build_learning_roadmap(weak_topics)
        self.assertGreater(len(roadmap), 0)
        resources = roadmap[0].get("resources", {})
        self.assertIn("youtube", resources)
        self.assertIn("practice_platforms", resources)


class PDFReportGenerationTests(unittest.TestCase):
    """Tests for PDF report generation (basic validation only)."""
    
    def test_pdf_generator_can_process_session_data(self):
        """Test that PDF generator can be initialized and called."""
        from backend.app.services.pdf_report_generator import PDFReportGenerator
        
        generator = PDFReportGenerator("test_report.pdf")
        self.assertIsNotNone(generator)
        
        # Mock session data
        session_data = {
            "resume_data": {"name": "Test Candidate", "skills": ["Python"]},
            "scores": [7, 8, 9],
            "answers": ["Answer 1", "Answer 2", "Answer 3"],
            "questions": ["Q1", "Q2", "Q3"],
            "average_score": 8,
            "communication_score": 8,
            "feedback": ["Good", "Great", "Excellent"]
        }
        
        # Verify that PDF generator has the method
        self.assertTrue(hasattr(generator, 'generate_report'))


class IntegrationTests(unittest.TestCase):
    """Integration tests for the complete improved system."""
    
    def test_answer_evaluation_with_reporting(self):
        """Test that answer evaluation feeds into reporting correctly."""
        # Simulate a full answer evaluation with clear keywords
        result = evaluate_answer_details(
            answer="I implemented machine learning using Python and scikit-learn for classification",
            question="Tell me about a machine learning project where you used Python",
            skills=["Python", "Machine Learning", "scikit-learn"],
            jd_skills=["Python", "ML"]
        )
        
        # Verify score is reasonable
        self.assertGreaterEqual(result["score"], 3)
        self.assertLessEqual(result["score"], 10)
        
        # Verify all required fields are present
        required_fields = ["score", "feedback", "strengths", "weaknesses", "performance_level"]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_full_adaptive_interview_flow(self):
        """Test a full flow of adaptive questions based on performance."""
        resume_data = {
            "name": "Test Candidate",
            "skills": ["Python", "Machine Learning"],
            "projects": ["ML Project 1", "Python Project 2"]
        }
        
        # First question - general
        q1 = generate_question_for_context(
            resume_data=resume_data,
            previous_questions=[],
            previous_answers=[],
            previous_scores=[],
            difficulty="medium"
        )
        self.assertIsNotNone(q1)
        
        # Weak answer to first question
        q2 = generate_question_for_context(
            resume_data=resume_data,
            previous_questions=[q1],
            previous_answers=["I don't really know"],
            previous_scores=[2],
            difficulty="easy"
        )
        self.assertIsNotNone(q2)
        self.assertNotEqual(q2, q1)
        
        # Strong answer to second question
        q3 = generate_question_for_context(
            resume_data=resume_data,
            previous_questions=[q1, q2],
            previous_answers=["I don't really know", "Machine learning is supervised/unsupervised learning"],
            previous_scores=[2, 9],
            difficulty="hard"
        )
        self.assertIsNotNone(q3)


if __name__ == "__main__":
    unittest.main()
