"""
Coding and DSA (Data Structures & Algorithms) questions module.
Includes easy, medium, and hard coding problems appropriate for different skill levels.
"""

CODING_PROBLEMS = {
    "easy": [
        {
            "id": "palindrome",
            "question": "Write a function to check if a string is a palindrome (ignoring spaces and case).",
            "example": 'Input: "A man a plan a canal Panama" Output: True',
            "concepts": ["String manipulation", "Two pointers"],
            "time_complexity": "O(n)"
        },
        {
            "id": "reverse_string",
            "question": "Write a function to reverse a string or number without using built-in reverse methods.",
            "example": 'Input: "hello" Output: "olleh" | Input: 12345 Output: 54321',
            "concepts": ["String/Number manipulation", "Loops"],
            "time_complexity": "O(n)"
        },
        {
            "id": "fibonacci",
            "question": "Write a function to find the nth Fibonacci number.",
            "example": 'Input: 6 Output: 8 (sequence: 0, 1, 1, 2, 3, 5, 8)',
            "concepts": ["Recursion/Iteration", "Dynamic Programming basics"],
            "time_complexity": "O(n)"
        },
        {
            "id": "prime_number",
            "question": "Write a function to check if a number is prime.",
            "example": 'Input: 17 Output: True | Input: 18 Output: False',
            "concepts": ["Math", "Loops", "Conditional logic"],
            "time_complexity": "O(sqrt(n))"
        },
        {
            "id": "unit_digit",
            "question": "Write a function to find the unit digit (last digit) of a factorial n!. Example: 5! = 120, unit digit = 0.",
            "example": 'Input: 5 Output: 0 | Input: 4 Output: 4 (4! = 24)',
            "concepts": ["Math", "Pattern recognition"],
            "time_complexity": "O(1) with pattern"
        },
        {
            "id": "count_digits",
            "question": "Write a function to count the number of digits in a positive integer.",
            "example": 'Input: 12345 Output: 5 | Input: 99 Output: 2',
            "concepts": ["Math", "String conversion"],
            "time_complexity": "O(n) or O(log n)"
        }
    ],
    "medium": [
        {
            "id": "array_rotation",
            "question": "Write a function to rotate an array left by k positions.",
            "example": 'Input: [1,2,3,4,5], k=2 Output: [3,4,5,1,2]',
            "concepts": ["Arrays", "Rotation techniques"],
            "time_complexity": "O(n)"
        },
        {
            "id": "lcm_gcd",
            "question": "Write a function to find the LCM (Least Common Multiple) and GCD (Greatest Common Divisor) of two numbers.",
            "example": 'Input: 12, 18 Output: GCD=6, LCM=36',
            "concepts": ["Math", "Euclidean algorithm"],
            "time_complexity": "O(log(min(a,b)))"
        },
        {
            "id": "remove_duplicates",
            "question": "Write a function to remove duplicates from a sorted array in-place.",
            "example": 'Input: [1,1,2,2,2,3] Output: [1,2,3] (return 3, first 3 elements modified)',
            "concepts": ["Arrays", "Two pointers"],
            "time_complexity": "O(n)"
        },
        {
            "id": "binary_search",
            "question": "Write a binary search function to find a target in a sorted array.",
            "example": 'Input: [1,3,5,7,9], target=7 Output: index 3 or True',
            "concepts": ["Searching", "Divide and conquer"],
            "time_complexity": "O(log n)"
        },
        {
            "id": "merge_sorted_arrays",
            "question": "Write a function to merge two sorted arrays into one sorted array.",
            "example": 'Input: [1,3,5], [2,4,6] Output: [1,2,3,4,5,6]',
            "concepts": ["Arrays", "Merging", "Two pointers"],
            "time_complexity": "O(n + m)"
        },
        {
            "id": "anagram_check",
            "question": "Write a function to check if two strings are anagrams of each other.",
            "example": 'Input: "listen", "silent" Output: True',
            "concepts": ["Strings", "Hash maps", "Sorting"],
            "time_complexity": "O(n log n) or O(n)"
        },
        {
            "id": "max_subarray",
            "question": "Write a function to find the maximum sum of a contiguous subarray (Kadane's algorithm).",
            "example": 'Input: [-2,1,-3,4,-1,2,1,-5,4] Output: 6 (subarray [4,-1,2,1])',
            "concepts": ["Dynamic programming", "Arrays"],
            "time_complexity": "O(n)"
        }
    ],
    "hard": [
        {
            "id": "longest_substring",
            "question": "Write a function to find the length of the longest substring without repeating characters.",
            "example": 'Input: "abcabcbb" Output: 3 (substring "abc")',
            "concepts": ["Strings", "Sliding window", "Hash maps"],
            "time_complexity": "O(n)"
        },
        {
            "id": "three_sum",
            "question": "Write a function to find all unique triplets in an array that sum to a target value.",
            "example": 'Input: [-1,0,1,2,-1,-4], target=0 Output: [[-1,-1,2], [-1,0,1]]',
            "concepts": ["Arrays", "Sorting", "Two pointers"],
            "time_complexity": "O(n^2)"
        },
        {
            "id": "lru_cache",
            "question": "Implement an LRU (Least Recently Used) Cache with get and put operations in O(1) time.",
            "example": 'LRU Cache with capacity 2: put(1,1), put(2,2), get(1)→1, put(3,3), get(2)→-1',
            "concepts": ["Hash map", "Linked list", "Cache design"],
            "time_complexity": "O(1) for both operations"
        },
        {
            "id": "word_ladder",
            "question": "Given two words and a word list, find the shortest transformation sequence from one word to another (changing one letter at a time).",
            "example": 'Start: "hit", End: "cog", List: ["hot","dot","dog","lot","log","cog"] → ["hit","hot","dot","dog","cog"]',
            "concepts": ["Graph", "BFS", "Word problems"],
            "time_complexity": "O(n * l^2) where n is word count, l is word length"
        },
        {
            "id": "combination_sum",
            "question": "Find all unique combinations in a list that sum to a target. Numbers can be reused.",
            "example": 'Candidates: [2,3,6,7], target=7 → [[2,2,3], [7]]',
            "concepts": ["Recursion", "Backtracking", "Dynamic programming"],
            "time_complexity": "O(N^(T/M)) where T is target, M is minimal value"
        }
    ]
}

SQL_PROBLEMS = {
    "easy": [
        {
            "id": "basic_select",
            "question": "Write a SQL query to select all columns from a 'users' table where age > 25, ordered by name.",
            "example": 'SELECT * FROM users WHERE age > 25 ORDER BY name;',
            "concepts": ["SELECT", "WHERE", "ORDER BY"],
        },
        {
            "id": "join_basic",
            "question": "Explain the difference between INNER JOIN and LEFT JOIN. Give an example.",
            "example": 'INNER JOIN: Returns only matching rows | LEFT JOIN: Returns all from left table + matching from right',
            "concepts": ["INNER JOIN", "LEFT JOIN", "Table relationships"],
        },
        {
            "id": "aggregate_functions",
            "question": "Write a query to find the average salary by department from an 'employees' table.",
            "example": 'SELECT department, AVG(salary) FROM employees GROUP BY department;',
            "concepts": ["GROUP BY", "Aggregate functions"],
        }
    ],
    "medium": [
        {
            "id": "multiple_joins",
            "question": "Join three tables: users, orders, and products. Get customer name, order date, and product name.",
            "example": 'SELECT u.name, o.order_date, p.product_name FROM users u JOIN orders o ON u.id=o.user_id JOIN products p ON o.product_id=p.id',
            "concepts": ["Multiple JOINs", "Table relationships"],
        },
        {
            "id": "subquery",
            "question": "Write a query to find all employees whose salary is above the average salary.",
            "example": 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);',
            "concepts": ["Subqueries", "Aggregate functions"],
        }
    ]
}


def get_coding_question(difficulty="easy"):
    """Get a coding problem of a specific difficulty level."""
    problems = CODING_PROBLEMS.get(difficulty, CODING_PROBLEMS["easy"])
    if not problems:
        return None
    
    import random
    return random.choice(problems)


def format_coding_question_for_interview(problem):
    """Format a coding problem for presentation in the interview."""
    if not problem:
        return None
    
    formatted = f"""Coding Problem ({problem.get('concepts', ['General'])[0]}):

{problem['question']}

Example: {problem['example']}

Please write the solution, explain your approach, and discuss:
1. Time complexity
2. Space complexity
3. Edge cases"""
    
    return formatted


def get_coding_question_prompt(difficulty="easy", candidate_skills=None, candidate_department=None):
    """
    Get an appropriate coding question based on:
    - Difficulty level (easy/medium/hard)
    - Candidate's skills (if CS/Programming focused)
    - Candidate's department
    """
    candidate_skills = candidate_skills or []
    
    # If candidate has programming languages in skills, offer coding question
    programming_skills = ["Python", "Java", "C++", "JavaScript", "SQL"]
    has_programming_skill = any(skill in programming_skills for skill in candidate_skills)
    
    if not has_programming_skill and candidate_department not in ["Computer Science / AI-ML", "Electronics and Communication"]:
        return None
    
    # For SQL-heavy roles, offer SQL problems
    if "SQL" in candidate_skills or "MongoDB" in candidate_skills:
        sql_problems = SQL_PROBLEMS.get(difficulty, SQL_PROBLEMS.get("easy"))
        if sql_problems:
            import random
            problem = random.choice(sql_problems)
            return format_coding_question_for_interview(problem)
    
    # Otherwise, offer general coding problems
    problem = get_coding_question(difficulty)
    if problem:
        return format_coding_question_for_interview(problem)
    
    return None


def evaluate_coding_solution(problem_id, solution_code, expected_output=None):
    """
    Evaluate a coding solution based on:
    - Correctness (logic)
    - Code quality
    - Explanation of approach
    - Time/space complexity
    
    Note: This is a simplified evaluation framework.
    In production, you might use code execution or static analysis.
    """
    if not solution_code or len(solution_code.strip()) < 10:
        return {
            "score": 0,
            "feedback": "No solution or incomplete code provided.",
            "issues": ["Code is empty or too short"]
        }
    
    evaluation = {
        "score": 5,  # Default middle score
        "feedback": "Solution provided. Need to review for correctness and efficiency.",
        "issues": [],
        "strengths": []
    }
    
    # Check for basic structure
    if any(keyword in solution_code.lower() for keyword in ["def ", "function", "class"]):
        evaluation["strengths"].append("Code has proper function/class structure")
    else:
        evaluation["issues"].append("Missing function or class definition")
    
    # Check for comments/explanation
    if "#" in solution_code or "/*" in solution_code:
        evaluation["strengths"].append("Code includes comments")
    else:
        evaluation["issues"].append("Code lacks comments or explanation")
    
    # Basic assessment
    if len(evaluation["issues"]) > 2:
        evaluation["score"] = 3
        evaluation["feedback"] = "Solution has structural issues. Review logic and approach."
    elif len(evaluation["strengths"]) > 1:
        evaluation["score"] = 7
        evaluation["feedback"] = "Solution appears well-structured. Good approach demonstrated."
    
    return evaluation
