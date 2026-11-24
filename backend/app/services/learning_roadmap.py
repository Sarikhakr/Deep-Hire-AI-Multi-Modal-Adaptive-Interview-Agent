"""
Learning Roadmap Generator
Creates personalized learning recommendations based on interview performance and weak areas.
"""

# Resource database for different topics
RESOURCES_DATABASE = {
    "python": {
        "youtube": ["Python for Beginners (Traversy Media)", "Python Full Tutorial (Corey Schafer)"],
        "official": ["Python Official Documentation", "Python.org Tutorial"],
        "practice": ["LeetCode Python Track", "HackerRank Python", "Codewars"],
        "books": ["Python Crash Course", "Automate the Boring Stuff with Python"]
    },
    "machine learning": {
        "youtube": ["Machine Learning by Andrew Ng (Coursera on YouTube)", "StatQuest with Josh Starmer"],
        "official": ["Scikit-learn Documentation", "TensorFlow Tutorials"],
        "practice": ["Kaggle Competitions", "Google Colab Notebooks"],
        "courses": ["Fast.ai", "Coursera Machine Learning Specialization"]
    },
    "deep learning": {
        "youtube": ["Deep Learning Specialization (Coursera)", "3Blue1Brown Neural Networks"],
        "official": ["PyTorch Documentation", "TensorFlow Documentation"],
        "practice": ["Kaggle Computer Vision Challenges", "Deep Learning Projects"],
        "courses": ["DeepLearning.AI", "Fast.ai Part 2"]
    },
    "data structures": {
        "youtube": ["Data Structures and Algorithms (Striver)", "Abdul Bari DSA Course"],
        "official": ["GeeksforGeeks Data Structures", "Algorithm Visualizer"],
        "practice": ["LeetCode DSA Tag", "HackerRank Data Structures", "Codeforces"],
        "books": ["Introduction to Algorithms (CLRS)", "Cracking the Coding Interview"]
    },
    "sql": {
        "youtube": ["SQL Tutorial for Beginners (Telusko)", "SQL Crash Course (Traversy)"],
        "official": ["MySQL Official Docs", "PostgreSQL Documentation"],
        "practice": ["LeetCode Database", "HackerRank SQL", "SQLZoo"],
        "courses": ["Mode Analytics SQL Tutorial"]
    },
    "javascript": {
        "youtube": ["JavaScript Mastery (Traversy Media)", "The Net Ninja JavaScript"],
        "official": ["MDN Web Docs JavaScript", "JavaScript.info"],
        "practice": ["FreeCodeCamp", "Codewars JavaScript", "Frontend Mentor"],
        "books": ["Eloquent JavaScript", "You Don't Know JS"]
    },
    "react": {
        "youtube": ["React Tutorial for Beginners (Scrimba)", "React Course (Traversy Media)"],
        "official": ["React Official Documentation", "React Hooks Documentation"],
        "practice": ["Build React Projects", "Frontend Mentor React", "Codepen"],
        "courses": ["Udemy React Masterclass", "React Course by Wes Bos"]
    },
    "algorithms": {
        "youtube": ["Algorithms Explained (Striver)", "Abdul Bari Algorithms"],
        "official": ["Algorithm Visualizer", "VisuAlgo"],
        "practice": ["LeetCode Algorithms", "Codeforces", "AtCoder"],
        "books": ["Introduction to Algorithms (CLRS)"]
    },
    "system design": {
        "youtube": ["System Design Interview (Grokking)", "Tech Dummies System Design"],
        "courses": ["Grokking System Design", "ByteByteGo"],
        "practice": ["Design real systems", "Discuss trade-offs"],
        "resources": ["Designing Data-Intensive Applications"]
    },
    "communication": {
        "courses": ["Technical Communication Course"],
        "practice": ["Write technical blogs", "Present projects", "Explain concepts clearly"],
        "resources": ["How to speak by Patrick Winston (MIT)"]
    },
    "problem solving": {
        "youtube": ["How to Solve It (polya)", "Problem Solving techniques"],
        "practice": ["Practice diverse problem types", "Analyze multiple solutions", "Discuss trade-offs"],
        "resources": ["Think Like a Programmer", "The Art and Science of Problem Solving"]
    }
}


def _identify_weak_topics_from_scores(scores, questions, answers):
    """
    Identify weak topics based on low scores and question/answer analysis.
    Returns a list of weak topics with priority levels.
    """
    weak_topics = []
    
    if not scores or len(scores) == 0:
        return weak_topics
    
    # Identify patterns from low scores
    for score, question, answer in zip(scores, questions, answers):
        if score <= 4:  # Low score
            # Extract topic from question
            answer_lower = (answer or "").lower()
            question_lower = (question or "").lower()
            
            topics = _extract_topics_from_text(question_lower + " " + answer_lower)
            for topic in topics:
                weak_topics.append({
                    "skill": topic,
                    "priority": "High" if score <= 2 else "Medium",
                    "reason": f"Scored {score}/10 on related question"
                })
    
    # Identify fundamental concept gaps
    avg_score = sum(scores) / len(scores) if scores else 0
    if avg_score < 5:
        weak_topics.append({
            "skill": "fundamental_concepts",
            "priority": "High",
            "reason": "Overall performance suggests need for fundamental concept review"
        })
    
    return weak_topics


def _extract_topics_from_text(text):
    """Extract technical topics from text."""
    text_lower = text.lower()
    topics = []
    
    topic_keywords = {
        "python": ["python"],
        "java": ["java"],
        "machine learning": ["machine learning", "ml", "classification", "regression"],
        "deep learning": ["deep learning", "neural", "cnn", "rnn", "lstm"],
        "data structures": ["data structure", "array", "linked list", "tree", "graph", "hash"],
        "algorithms": ["algorithm", "sorting", "searching", "complexity"],
        "sql": ["sql", "database", "query", "join"],
        "javascript": ["javascript", "js"],
        "react": ["react"],
        "system design": ["system", "architecture", "scalability", "design"],
        "problem solving": ["problem", "solution", "approach"],
        "communication": ["explain", "describe", "present", "communicate"]
    }
    
    for topic, keywords in topic_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            topics.append(topic)
    
    return list(set(topics))  # Remove duplicates


def build_learning_roadmap(weak_topics=None, interview_data=None):
    """
    Build a comprehensive, personalized learning roadmap based on weak areas.
    
    Args:
        weak_topics: List of weak topic objects with skill, priority, reason
        interview_data: Interview session data containing scores, questions, answers
    
    Returns:
        List of learning recommendations with resources
    """
    weak_topics = weak_topics or []
    interview_data = interview_data or {}
    
    # If weak_topics not provided, extract from interview data
    if not weak_topics and interview_data:
        scores = interview_data.get("scores", [])
        questions = interview_data.get("questions", [])
        answers = interview_data.get("answers", [])
        weak_topics = _identify_weak_topics_from_scores(scores, questions, answers)
    
    roadmap = []
    
    for item in weak_topics:
        if isinstance(item, dict):
            skill = item.get("skill", "Skill")
            priority = item.get("priority", "Medium")
            reason = item.get("reason", f"Learn {skill} through guided practice and projects.")
        else:
            skill = str(item)
            priority = "Medium"
            reason = f"Identified as an area for improvement during the interview."
        
        # Get resources for this skill
        skill_lower = skill.lower().replace(" ", "")
        resources = RESOURCES_DATABASE.get(skill_lower, {})
        
        # If not found, try variations
        if not resources:
            for key in RESOURCES_DATABASE.keys():
                if skill.lower() in key or key in skill.lower():
                    resources = RESOURCES_DATABASE[key]
                    break
        
        # Build learning recommendation
        recommendation = {
            "skill": skill,
            "priority": priority,
            "reason": reason,
            "objective": f"Build strong fundamentals and practical expertise in {skill}.",
            "difficulty_assessment": _assess_difficulty(priority),
            "learning_plan": _build_learning_plan(skill, priority),
            "resources": {
                "youtube": resources.get("youtube", [f"YouTube tutorials on {skill}"]),
                "official_docs": resources.get("official", [f"Official {skill} documentation"]),
                "practice_platforms": resources.get("practice", ["LeetCode", "HackerRank", "Codewars"]),
                "courses": resources.get("courses", [f"Online courses on {skill}"]),
                "books": resources.get("books", [f"Books on {skill}"])
            },
            "estimated_time": _estimate_learning_time(skill, priority),
            "success_criteria": _define_success_criteria(skill),
            "next_steps": _define_next_steps(skill)
        }
        
        roadmap.append(recommendation)
    
    # If no weak topics, provide general guidance
    if not roadmap:
        return [{
            "skill": "Advanced skill development",
            "priority": "Medium",
            "objective": "Continue strengthening your technical foundation and expertise.",
            "reason": "Maintain and expand upon your solid performance.",
            "difficulty_assessment": "Continue with medium to advanced topics",
            "learning_plan": [
                "Explore advanced topics in your areas of strength",
                "Contribute to open-source projects",
                "Build complex, real-world projects",
                "Mentoring junior developers",
                "Reading technical papers and blogs"
            ],
            "resources": {
                "youtube": ["Tech talks and advanced tutorials"],
                "courses": ["Advanced Specialization courses"],
                "practice_platforms": ["Kaggle competitions", "Coding contests"]
            },
            "estimated_time": "Ongoing",
            "success_criteria": ["Complete advanced projects", "Contribute to open source", "Share knowledge"],
            "next_steps": ["Choose an advanced specialization", "Build portfolio projects", "Network with industry"]
        }]
    
    return roadmap


def _assess_difficulty(priority):
    """Assess the difficulty of the learning path based on priority."""
    if priority == "High":
        return "Review fundamentals first, then move to practice"
    elif priority == "Medium":
        return "Balance theory with hands-on practice"
    else:
        return "Continue learning with projects and real-world application"


def _build_learning_plan(skill, priority):
    """Build a structured learning plan."""
    if priority == "High":
        return [
            f"1. Understand core concepts of {skill}",
            f"2. Complete fundamental tutorials and courses",
            f"3. Solve 10-20 basic practice problems",
            f"4. Build a small project using {skill}",
            f"5. Review and practice regularly"
        ]
    elif priority == "Medium":
        return [
            f"1. Review key concepts in {skill}",
            f"2. Complete intermediate tutorials or courses",
            f"3. Solve 20-40 practice problems of varying difficulty",
            f"4. Build a medium-complexity project",
            f"5. Contribute to open source or real projects"
        ]
    else:
        return [
            f"1. Deepen expertise in {skill}",
            f"2. Explore advanced applications and optimizations",
            f"3. Solve complex problems and contribute to innovation",
            f"4. Build production-grade systems",
            f"5. Mentor others and share knowledge"
        ]


def _estimate_learning_time(skill, priority):
    """Estimate how long it should take to improve in this skill."""
    if priority == "High":
        return "4-8 weeks (with consistent daily practice)"
    elif priority == "Medium":
        return "2-4 weeks (with regular practice)"
    else:
        return "Ongoing (continuous improvement)"


def _define_success_criteria(skill):
    """Define what success looks like for this skill."""
    return [
        f"Can explain {skill} concepts clearly and confidently",
        f"Successfully solve intermediate problems in {skill}",
        f"Can apply {skill} in a real project",
        f"Understand trade-offs and best practices in {skill}",
        f"Can teach others about {skill}"
    ]


def _define_next_steps(skill):
    """Define concrete next steps for learning."""
    return [
        f"Today: Watch a 10-15 minute introductory video on {skill}",
        f"This week: Complete one full tutorial on {skill}",
        f"Next week: Start solving beginner-level problems",
        f"In 2 weeks: Begin building a small project",
        f"In 1 month: Share your learning progress and projects"
    ]
