import re


REFUSAL_PHRASES = (
    "i don't know",
    "i do not know",
    "no idea",
    "not sure",
    "i am not sure",
    "i'm not sure",
    "i don't remember",
    "i do not remember",
    "cannot remember",
)

STOP_WORDS = {
    "about", "after", "also", "been", "from", "have", "how", "into",
    "that", "than", "the", "their", "them", "then", "there", "these",
    "they", "this", "what", "when", "which", "with", "would", "your",
}

# Comprehensive technical terms database for domain-specific scoring
TECHNICAL_TERMS_DB = {
    "Machine Learning": [
        "supervised", "unsupervised", "classification", "regression", "clustering",
        "algorithm", "model", "training", "validation", "overfitting", "underfitting",
        "accuracy", "precision", "recall", "f1-score", "roc curve", "auc",
        "cross-validation", "hyperparameter", "optimization", "ensemble"
    ],
    "Deep Learning": [
        "neural network", "layer", "activation", "relu", "sigmoid", "tanh",
        "gradient descent", "backpropagation", "epoch", "batch size", "learning rate",
        "dropout", "batch normalization", "convolution", "pooling", "cnn",
        "rnn", "lstm", "gru", "transformer", "attention"
    ],
    "Data Structures": [
        "array", "linked list", "stack", "queue", "tree", "graph",
        "hash table", "heap", "trie", "binary search", "traversal",
        "time complexity", "space complexity", "big o"
    ],
    "Algorithms": [
        "sorting", "searching", "dynamic programming", "greedy", "divide and conquer",
        "merge sort", "quick sort", "binary search", "dijkstra", "bfs", "dfs"
    ],
    "Web Development": [
        "html", "css", "javascript", "react", "angular", "vue",
        "backend", "frontend", "api", "rest", "database", "sql",
        "nosql", "mongodb", "mysql", "postgresql", "orm"
    ],
    "DevOps": [
        "docker", "kubernetes", "ci/cd", "jenkins", "deployment",
        "aws", "azure", "gcp", "cloud", "microservices", "scalability"
    ]
}


def _extract_keywords(text):
    words = re.findall(r"[A-Za-z][A-Za-z+\-#]*", (text or "").lower())
    return [w for w in words if len(w) > 3 and w not in STOP_WORDS]


def _is_refusal(text):
    normalized = re.sub(r"[^a-z\s']", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return any(phrase in normalized for phrase in REFUSAL_PHRASES)


def _calculate_answer_correctness(answer, question, skills=None, jd_skills=None):
    """
    Calculate how correct/relevant the answer is to the question.
    Returns a score from 0-10 based on content alignment.
    """
    if not answer or not question:
        return 0

    answer_lower = answer.lower()
    question_lower = question.lower()

    # Extract key concepts from question
    question_keywords = _extract_keywords(question)
    answer_keywords = _extract_keywords(answer)

    # A relevant answer should score generously, even if it is short or not perfect.
    matched_keywords = [kw for kw in question_keywords if kw in answer_lower]
    if not matched_keywords and len(answer_keywords) == 0:
        return 0

    if not question_keywords:
        return 6 if len(answer_keywords) > 0 else 0

    relevance = (len(matched_keywords) / len(question_keywords)) * 10

    # Be more forgiving for short but relevant responses.
    if relevance >= 6:
        return min(10, max(7, relevance + 1.5))
    if relevance >= 4:
        return min(10, max(6, relevance + 1.0))
    if relevance >= 2:
        return min(10, max(4.5, relevance + 0.5))
    return min(10, max(0, relevance))


def _detect_technical_depth(answer, skills=None, jd_skills=None):
    """
    Detect the technical depth and complexity of the answer.
    Returns a depth score from 0-10.
    """
    if not answer:
        return 0
    
    answer_lower = answer.lower()
    skills = skills or []
    jd_skills = jd_skills or []
    
    # Count technical terms used
    technical_count = 0
    
    # Check for domain-specific technical terms
    for category, terms in TECHNICAL_TERMS_DB.items():
        for term in terms:
            if term.lower() in answer_lower:
                technical_count += 1
    
    # Check for skills/JD skills mentioned
    for skill in list(skills) + list(jd_skills):
        if str(skill).lower() in answer_lower:
            technical_count += 1
    
    # Calculate depth score
    depth_score = min(10, technical_count * 1.5)
    
    return depth_score


def _detect_completeness(answer, question):
    """
    Assess how complete the answer is (addresses all parts of the question).
    Returns a score from 0-10.
    """
    if not answer:
        return 0

    answer_text = str(answer).strip()
    word_count = len(answer_text.split())

    # Interview scoring should not punish short but correct answers.
    if word_count < 5:
        return 7 if len(answer_text) > 0 else 0
    elif word_count < 15:
        return 8
    elif word_count < 50:
        return 9
    else:
        return 9.5

    return 0


def _detect_reasoning_quality(answer):
    """
    Assess the quality of reasoning/explanation in the answer.
    Returns a score from 0-10.
    """
    if not answer:
        return 0

    answer_lower = answer.lower()
    reasoning_markers = [
        "because", "therefore", "for example", "this is",
        "trade-off", "tradeoff", "metric", "tested",
        "measured", "result", "outcome", "advantage",
        "disadvantage", "approach", "strategy", "step"
    ]

    marker_count = sum(1 for marker in reasoning_markers if marker in answer_lower)
    reasoning_score = min(10, marker_count * 2)

    # Reasoning is valuable but should not collapse otherwise strong answers.
    if reasoning_score == 0 and len(answer_lower.split()) >= 4:
        return 4
    return reasoning_score


def evaluate_answer_details(answer, question=None, skills=None, jd_skills=None):
    """
    Improved answer evaluation that scores 0-10 based on:
    - Correctness (relevance to question)
    - Completeness (addresses all parts)
    - Technical understanding (depth and technical terms)
    - Reasoning quality (explanation and logic)
    - Question-answer alignment
    
    Does NOT primarily use answer length.
    """
    if answer is None:
        answer = ""

    text = str(answer).strip()
    skills = skills or []
    jd_skills = jd_skills or []
    question_text = question or ""

    # Special case: Empty answer
    if not text:
        return {
            "score": 0,
            "feedback": "No answer was provided. Please answer the question directly.",
            "strengths": [],
            "weaknesses": ["No response to evaluate."],
            "missing_concepts": _extract_keywords(question_text)[:4],
            "suggested_improvement": ["Provide a direct answer with one concrete example."],
            "next_question": "Can you explain the basic concept behind your answer?",
            "relevance_score": 0,
            "keywords_found": [],
            "correctness": 0,
            "completeness": 0,
            "technical_depth": 0,
            "reasoning_quality": 0
        }

    # Special case: Refusal (I don't know, No idea, etc.)
    if _is_refusal(text):
        return {
            "score": 1,
            "feedback": "This response does not answer the question. Be transparent, then explain what you do know or how you would investigate it.",
            "strengths": [],
            "weaknesses": ["The response does not demonstrate understanding of the question."],
            "missing_concepts": _extract_keywords(question_text)[:4],
            "suggested_improvement": ["Address the question directly and include a relevant technical detail."],
            "next_question": "What is one related concept or step you can explain?",
            "relevance_score": 0,
            "keywords_found": [],
            "correctness": 1,
            "completeness": 0,
            "technical_depth": 0,
            "reasoning_quality": 0
        }

    # Calculate individual scoring components
    correctness_score = _calculate_answer_correctness(text, question_text, skills, jd_skills)
    completeness_score = _detect_completeness(text, question_text)
    technical_depth_score = _detect_technical_depth(text, skills, jd_skills)
    reasoning_score = _detect_reasoning_quality(text)

    # Interview-style weighting: be generous with relevant answers and avoid harsh penalties
    # for short, correct responses that show understanding.
    weighted_score = (
        correctness_score * 0.45 +
        completeness_score * 0.20 +
        technical_depth_score * 0.20 +
        reasoning_score * 0.15
    )

    if correctness_score >= 7 and text and not _is_refusal(text):
        weighted_score += 0.8

    total_score = max(0, min(10, round(weighted_score, 1)))

    # Extract keywords for feedback
    keywords = []
    keyword_pool = list(skills) + list(jd_skills)
    for item in keyword_pool:
        item_text = str(item).strip()
        if item_text and item_text.lower() in text.lower():
            keywords.append(item_text)

    question_keywords = _extract_keywords(question_text)
    answer_keywords = _extract_keywords(text)
    matched_keywords = [kw for kw in question_keywords if kw in answer_keywords]

    # Generate feedback and suggestions based on score
    if total_score >= 8.5:
        feedback = "Excellent answer! It is relevant, accurate, and demonstrates strong understanding."
        strengths = [
            "Strong technical relevance and accuracy.",
            "Clear and confident explanation.",
            "Demonstrates solid understanding of the topic."
        ]
        weaknesses = []
        performance_level = "Excellent"
    elif total_score >= 7:
        feedback = "Good answer. It is relevant and shows solid understanding, with room for extra detail only if needed."
        strengths = [
            "Relevant and understandable response.",
            "Shows good understanding of the topic.",
            "Includes useful context or examples."
        ]
        weaknesses = [
            "Could include a bit more depth or examples.",
            "Consider adding a clearer trade-off or practical example."
        ]
        performance_level = "Good"
    elif total_score >= 5:
        feedback = "Fair answer. It shows the right idea but could be clearer or slightly more detailed."
        strengths = [
            "Shows some understanding of the topic.",
            "Answer addresses the question at a basic level.",
            "Some relevant content is present."
        ]
        weaknesses = [
            "Answer could benefit from a bit more explanation.",
            "Add a concrete example or more technical context.",
            "Consider explaining the reasoning behind the answer."
        ]
        performance_level = "Satisfactory"
    elif total_score >= 2.5:
        feedback = "Weak answer. It is not fully aligned with the question and needs more relevant detail."
        strengths = [
            "Attempted to answer the question."
        ]
        weaknesses = [
            "Answer lacks sufficient technical detail or clarity.",
            "Connection to the question is weak.",
            "Need to demonstrate deeper understanding."
        ]
        performance_level = "Weak"
    else:
        feedback = "This does not answer the question well enough. It is largely irrelevant, incorrect, or too incomplete."
        strengths = []
        weaknesses = [
            "Answer is not relevant to the question.",
            "No clear technical understanding demonstrated.",
            "The response is too incomplete or incorrect."
        ]
        performance_level = "Poor"

    missing_concepts = []
    for skill in list(skills) + list(jd_skills):
        skill_text = str(skill).strip().lower()
        if skill_text and skill_text not in text.lower():
            missing_concepts.append(skill_text)

    if not missing_concepts:
        missing_concepts = [
            "Practical examples from real projects",
            "Design reasoning or trade-offs",
            "Performance or efficiency considerations"
        ]

    suggestions = [
        "Add concrete examples from your projects.",
        "Explain the reasoning behind your approach.",
        "Mention tools, technologies, or metrics you used."
    ]

    suggested_next_question = None
    if total_score >= 8:
        suggested_next_question = "Why did you choose this approach over other alternatives?"
    elif total_score >= 5:
        suggested_next_question = "Can you walk through a practical example from your experience?"
    else:
        suggested_next_question = "What is the basic concept or fundamental idea behind your answer?"

    relevance = min(100, (len(matched_keywords) / max(1, len(question_keywords))) * 100 if question_keywords else 55)

    return {
        "score": int(total_score),
        "feedback": feedback,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_concepts": missing_concepts[:4],
        "suggested_improvement": suggestions,
        "next_question": suggested_next_question,
        "relevance_score": round(relevance, 1),
        "keywords_found": keywords[:6],
        "performance_level": performance_level,
        "correctness": round(correctness_score, 1),
        "completeness": round(completeness_score, 1),
        "technical_depth": round(technical_depth_score, 1),
        "reasoning_quality": round(reasoning_score, 1)
    }


def evaluate_answer(answer, question=None, skills=None, jd_skills=None):
    details = evaluate_answer_details(answer, question, skills, jd_skills)
    return details["score"], details["feedback"]