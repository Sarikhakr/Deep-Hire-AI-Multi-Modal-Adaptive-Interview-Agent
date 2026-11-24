def detect_department(resume_data):

    text = " ".join(
        resume_data.get("education", [])
        + resume_data.get("skills", [])
        + resume_data.get("projects", [])
    ).lower()

    if any(word in text for word in [
        "artificial intelligence",
        "machine learning",
        "computer science",
        "python",
        "tensorflow",
        "deep learning"
    ]):
        return "Computer Science / AI-ML"

    if any(word in text for word in [
        "mechanical",
        "thermodynamics",
        "manufacturing",
        "solid mechanics",
        "cad"
    ]):
        return "Mechanical Engineering"

    if any(word in text for word in [
        "civil",
        "structural engineering",
        "surveying",
        "construction",
        "autocad"
    ]):
        return "Civil Engineering"

    if any(word in text for word in [
        "electronics",
        "embedded systems",
        "microcontroller",
        "digital electronics",
        "ece"
    ]):
        return "Electronics and Communication"

    if any(word in text for word in [
        "electrical",
        "power systems",
        "electrical machines",
        "eee"
    ]):
        return "Electrical Engineering"

    return "General Engineering"