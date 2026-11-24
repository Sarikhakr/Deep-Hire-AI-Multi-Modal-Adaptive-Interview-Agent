#!/usr/bin/env python3
"""
Advanced demo showing specialized ML/DL/Python/Java/SQL questions
appearing during interview progression
"""

from backend.app.services.question_generator import generate_question_for_context

print("=" * 80)
print("ADVANCED QUESTION SPECIALIZATION DEMO")
print("=" * 80)

# Test 1: ML Specialist - Force specialized questions to appear
print("\n[Test 1] ML Specialist - Triggering Specialized ML Questions")
print("-" * 80)

ml_candidate = {
    "department": "Computer Science / AI-ML",
    "skills": ["Machine Learning", "Deep Learning", "Python", "TensorFlow", "Numpy"],
    "projects": ["Image Classification", "NLP Chatbot"]
}

# Multiple questions asked, skills being explored
previous_questions = [
    "Tell me about your ML projects",
    "How do you handle overfitting?",
    "Explain your deep learning experience"
]

previous_answers = [
    "Built CNN with TensorFlow for image classification",
    "Used regularization and dropout",
    "Built LSTM networks for time series"
]

previous_scores = [8, 7, 7]  # Good scores, will trigger advanced questions

question = generate_question_for_context(
    resume_data=ml_candidate,
    previous_questions=previous_questions,
    previous_answers=previous_answers,
    previous_scores=previous_scores,
    difficulty="hard"
)

print(f"Generated Specialized Question:\n{question}\n")

if any(kw in question.lower() for kw in ["supervised", "unsupervised", "feature engineering", "algorithm", "overfitting", "underfitting", "neural network", "activation", "gradient", "loss"]):
    print("✓ SPECIALIZED ML QUESTION DETECTED!")
else:
    print("- Generic question (specialized questions come from pool)")

# Test 2: Python Developer - Specialized Python Questions
print("\n\n[Test 2] Python Developer - Triggering Specialized Python Questions")
print("-" * 80)

python_candidate = {
    "department": "Computer Science / AI-ML",
    "skills": ["Python", "Data Structures", "SQL", "Pandas", "Numpy"],
    "projects": ["Data Pipeline", "Analytics Dashboard"]
}

previous_questions = [
    "Tell me about your Python projects",
    "How do you optimize code performance?",
]

previous_answers = [
    "Built data pipeline with pandas and numpy",
    "Used profiling tools and optimized database queries"
]

previous_scores = [7.5, 6.5]

question = generate_question_for_context(
    resume_data=python_candidate,
    previous_questions=previous_questions,
    previous_answers=previous_answers,
    previous_scores=previous_scores,
    difficulty="medium"
)

print(f"Generated Specialized Question:\n{question}\n")

if any(kw in question.lower() for kw in ["python", "data structure", "list", "dictionary", "tuple", "comprehension", "lambda", "exception", "error", "optimize"]):
    print("✓ SPECIALIZED PYTHON QUESTION DETECTED!")
else:
    print("- Generic question (specialized questions in expanded pool)")

# Test 3: Java Developer
print("\n\n[Test 3] Java Developer - Triggering Specialized Java Questions")
print("-" * 80)

java_candidate = {
    "department": "Computer Science / AI-ML",
    "skills": ["Java", "OOP", "SQL", "Spring"],
    "projects": ["Microservices API", "Database System"]
}

previous_questions = [
    "Tell me about your Java backend development",
    "How do you design for scalability?"
]

previous_answers = [
    "Built microservices using Spring and Docker",
    "Implemented load balancing and caching"
]

previous_scores = [8, 7.5]

# Manually check the pool building to see all questions
from backend.app.services.question_generator import _identify_weak_areas

weak_areas = _identify_weak_areas(
    previous_answers=previous_answers,
    previous_scores=previous_scores
)

print(f"Weak areas identified: {weak_areas}")

question = generate_question_for_context(
    resume_data=java_candidate,
    previous_questions=previous_questions,
    previous_answers=previous_answers,
    previous_scores=previous_scores,
    difficulty="hard"
)

print(f"\nGenerated Specialized Question:\n{question}\n")

if any(kw in question.lower() for kw in ["java", "oop", "inheritance", "polymorphism", "encapsulation", "exception", "thread", "memory", "gc"]):
    print("✓ SPECIALIZED JAVA QUESTION DETECTED!")
else:
    print("- Advanced question (specialized Java questions in pool)")

# Test 4: SQL/Database Specialist
print("\n\n[Test 4] SQL/Database Specialist - Triggering Specialized SQL Questions")
print("-" * 80)

sql_candidate = {
    "department": "Computer Science / AI-ML",
    "skills": ["SQL", "Database Design", "PostgreSQL", "Optimization"],
    "projects": ["Data Warehouse", "Query Optimization"]
}

previous_questions = [
    "Tell me about database work",
    "How do you optimize slow queries?"
]

previous_answers = [
    "Designed star schema for data warehouse",
    "Added indexes and rewrote complex JOINs"
]

previous_scores = [8.5, 8]
question = generate_question_for_context(
    resume_data=sql_candidate,
    previous_questions=previous_questions,
    previous_answers=previous_answers,
    previous_scores=previous_scores,
    difficulty="hard"
)

print(f"Generated Specialized Question:\n{question}\n")

if any(kw in question.lower() for kw in ["sql", "join", "index", "query", "aggregate", "where", "having", "normal", "relationship", "optimize"]):
    print("✓ SPECIALIZED SQL QUESTION DETECTED!")
else:
    print("- Advanced question (specialized SQL questions in expanded pool)")

# Test 5: Simulate full interview with progressive specialization
print("\n\n[Test 5] PROGRESSIVE INTERVIEW - Questions Become More Specialized")
print("-" * 80)

candidate_profile = {
    "department": "Computer Science / AI-ML",
    "skills": ["Machine Learning", "Python", "TensorFlow", "SQL"],
    "projects": ["Recommendation Engine", "Data Analysis"]
}

print("\nSimulating 5-question interview progression:\n")

for q_num in range(1, 6):
    # Simulate previous answers
    prev_q = [
        "Your background",
        "ML projects you built",
        "Data handling approach",
        "Performance optimization",
        "Deployment strategy"
    ][:q_num]
    
    prev_a = [
        "CS grad with ML focus",
        "Built recommendation system with Python",
        "Used pandas for data preprocessing",
        "Optimized model training with batch processing",
        "Deployed on AWS with containerization"
    ][:q_num]
    
    # Varying scores to show adaptation
    prev_scores_list = [6.5, 7.5, 6, 7.5, 8][:q_num]
    
    question = generate_question_for_context(
        resume_data=candidate_profile,
        previous_questions=prev_q,
        previous_answers=prev_a,
        previous_scores=prev_scores_list,
        difficulty="medium"
    )
    
    print(f"Q{q_num}: {question[:120]}...")
    
    # Check if specialized
    specialist_keywords = ["python", "ml", "tensorflow", "data structure", "sql", "algorithm", "neural", "learning", "optimization"]
    is_specialized = any(kw in question.lower() for kw in specialist_keywords)
    print(f"    Type: {'[SPECIALIZED]' if is_specialized else '[GENERAL]'}\n")

# ============================================================================
# EXPLANATION OF HOW SPECIALIZED QUESTIONS WORK
# ============================================================================
print("\n" + "=" * 80)
print("HOW SPECIALIZED QUESTIONS WORK")
print("=" * 80)

explanation = """
The question generation system builds a dynamic pool of questions including:

1. ADAPTIVE DIFFICULTY:
   • Weak answers (≤4) → Easier fundamental questions
   • Average answers (5-7) → Clarification and follow-up questions
   • Good answers (>7) → Advanced technical questions
   • Strong answers (9+) → Deep technical/project questions

2. SKILL-BASED SPECIALIZATION:
   Questions are tailored to specific skills:
   
   • Machine Learning: Feature engineering, algorithms, evaluation metrics
   • Deep Learning: Neural networks, architectures (CNN/RNN), optimization
   • Python: Data structures, libraries (pandas/numpy), exceptions, optimization
   • Java: OOP principles, multithreading, memory management
   • SQL: JOINs, indexes, normalization, query optimization
   • C++: Memory management, STL, performance

3. PROFILE-AWARE QUESTIONS:
   • Department-specific questions (CS/AI-ML, Electronics, Mechanical, Civil, etc.)
   • Project-specific follow-ups from actual resume
   • JD skill requirements matching
   • Experience level progression

4. QUESTION POOL BUILDING:
   The system creates a pool of ~20-30 candidate questions per query:
   - Difficulty-adjusted questions
   - Skill-based specialized questions
   - Project follow-up questions
   - General technical questions
   
   The FIRST relevant question from this pool is returned,
   avoiding duplicates and unrelated questions.

5. CODING QUESTIONS:
   Offered after 2+ answers to programming candidates:
   - DSA (Data Structures & Algorithms): Easy/Medium/Hard
   - SQL: Database design and optimization
   - Automatic difficulty scaling based on performance

RESULT: Questions progressively become more technical and specialized
        as the interview progresses and candidate expertise is demonstrated.
"""

print(explanation)

print("=" * 80)
