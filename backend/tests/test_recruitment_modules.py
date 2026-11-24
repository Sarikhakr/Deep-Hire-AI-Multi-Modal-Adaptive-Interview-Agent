import unittest

from backend.app.services.skill_gap_service import analyze_skill_gap
from backend.app.services.learning_roadmap import build_learning_roadmap
from backend.app.services.career_recommendation import recommend_roles
from backend.app.services.communication_confidence import analyze_communication_confidence


class RecruitmentModulesTests(unittest.TestCase):
    def test_skill_gap_analysis(self):
        result = analyze_skill_gap(
            candidate_skills=["Python", "SQL", "Machine Learning", "AWS"],
            required_skills=["Python", "SQL", "Machine Learning", "AWS", "Docker"],
        )
        self.assertEqual(result["skill_match_percentage"], 80)
        self.assertIn("Docker", result["missing_skills"])
        self.assertIn("High Priority", [item["priority"] for item in result["missing_skill_details"]])

    def test_learning_roadmap(self):
        roadmap = build_learning_roadmap([{"skill": "Docker", "priority": "High"}])
        self.assertTrue(len(roadmap) >= 1)
        self.assertEqual(roadmap[0]["skill"], "Docker")

    def test_career_recommendation(self):
        roles = recommend_roles(
            department="Computer Science / AI-ML",
            skills=["Python", "Machine Learning", "SQL"],
            interview_score=85,
            jd_match=80,
            experience=["AI Intern"]
        )
        self.assertTrue(len(roles) >= 1)
        self.assertTrue(any(r["role"] in ["AI/ML Engineer", "Data Scientist", "Software Developer"] for r in roles))

    def test_communication_confidence(self):
        result = analyze_communication_confidence("I used Random Forest and tuned the model with cross-validation to improve accuracy.")
        self.assertIn(result["level"], ["Strong Communication", "Moderate Communication", "Needs Improvement"])


if __name__ == "__main__":
    unittest.main()
