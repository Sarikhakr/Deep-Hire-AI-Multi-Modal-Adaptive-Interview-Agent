import re


def analyze_communication_confidence(answer_text):
    text = (answer_text or "").strip()
    if not text:
        return {
            "level": "Needs Improvement",
            "score": 0,
            "strengths": [],
            "improvement_points": ["Add a clearer explanation of your experience and results."],
            "summary": "The answer is too brief to assess effective communication."
        }

    sentence_count = len(re.findall(r"[^.!?]+[.!?]", text))
    word_count = len(re.findall(r"\b\w+\b", text))
    technical_terms = [
        "python", "sql", "machine learning", "model", "algorithm", "random forest",
        "deep learning", "aws", "docker", "api", "database", "validation", "optimization"
    ]
    technical_hits = sum(1 for term in technical_terms if term.lower() in text.lower())

    score = 40 + min(40, sentence_count * 7) + min(20, technical_hits * 5) + min(20, max(0, word_count - 20) / 4)
    score = min(100, round(score))

    if score >= 80:
        level = "Strong Communication"
        strengths = [
            "Clear and confident explanation.",
            "Good use of technical language and practical details.",
            "Answer structure is easy to follow."
        ]
        improvement_points = [
            "Try to include more measurable impact and outcomes."
        ]
    elif score >= 55:
        level = "Moderate Communication"
        strengths = [
            "The answer is understandable and mostly structured.",
            "It shows domain knowledge with some context."
        ]
        improvement_points = [
            "Add more examples and explain the reasoning behind key decisions."
        ]
    else:
        level = "Needs Improvement"
        strengths = [
            "The answer includes basic ideas but is still brief."
        ]
        improvement_points = [
            "Use more concrete examples and simplify the structure for clarity.",
            "Explain the result, trade-off, or impact with more detail."
        ]

    return {
        "level": level,
        "score": score,
        "strengths": strengths,
        "improvement_points": improvement_points,
        "summary": f"Communication confidence is {level.lower()} with a score of {score}/100."
    }
