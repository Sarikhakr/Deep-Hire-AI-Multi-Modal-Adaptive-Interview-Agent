# DeepHire AI – AI-Powered Recruitment and Interview Platform

## Overview

DeepHire AI is an AI-powered recruitment platform designed to improve the recruitment process through intelligent resume analysis, Applicant Tracking System (ATS) compatibility scoring, job description matching, skill gap identification, and AI-assisted interview evaluation.

The platform aims to help candidates understand their strengths, identify areas for improvement, and evaluate how well their profiles match specific job requirements.

## Key Features

### 1. Resume Analysis
- Upload and process resumes in PDF format.
- Extract relevant information from resumes.
- Analyze candidate qualifications and skills.
- Identify resume strengths and areas for improvement.

### 2. ATS Compatibility Analysis
- Evaluate resume compatibility with Applicant Tracking Systems.
- Analyze resume content against job requirements.
- Provide insights to help improve resume relevance.

### 3. Resume–Job Description Matching
- Compare candidate resumes with job descriptions.
- Use TF-IDF and cosine similarity for text similarity analysis.
- Estimate how closely a resume aligns with a given job role.

### 4. Skill Gap Analysis
- Identify relevant skills present in a candidate's resume.
- Highlight skills that may be missing from the job requirements.
- Provide personalized suggestions for improving job readiness.

### 5. AI-Assisted Interview System
- Support interview sessions through the interview modules.
- Evaluate candidate answers using the answer evaluation components.
- Explore voice-based interview interaction and speech recognition capabilities.

### 6. Candidate Feedback and Reporting
- Provide feedback based on resume and job matching analysis.
- Support candidate evaluation and scoring.
- Include reporting functionality for presenting evaluation results.

## Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python, JavaScript |
| Backend Framework | FastAPI |
| Frontend | React, JSX |
| Database | MongoDB |
| API Server | Uvicorn |
| Authentication | JWT |
| NLP and Text Similarity | TF-IDF, Cosine Similarity |
| Resume Processing | PDF text extraction |
| Development Tools | Visual Studio Code, Git, GitHub |

Note: The exact libraries and implementations depend on the modules and dependencies included in the project.

## Project Structure

```text
deep hire AI/
|
|-- ai_models/
|
|-- backend/
|   |-- app/
|   |-- tests/
|   |-- __init__.py
|   |-- .env
|   |-- main.py
|   |-- requirements.txt
|
|-- datasets/
|
|-- docs/
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|
|-- reports/
|
|-- rough/
|
|-- uploads/
|
|-- venv/
|
|-- .gitignore
|-- advanced_demo.py
|-- demo_fixes.py
|-- FIXES_SUMMARY.md
|-- IMPLEMENTATION_REPORT.md
|-- QUICK_START.md
|-- test_db.py
|-- README.md
```

This structure summarizes the folders and files visible in the development environment. Additional files may exist inside individual directories.

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python
- Node.js and npm
- MongoDB or a valid MongoDB connection
- Git

### Step 1: Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/DeepHire-AI.git
cd DeepHire-AI
```

### Step 2: Set Up the Backend

Create and activate a Python virtual environment from the project root.

```bash
python -m venv venv
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r backend/requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file inside the `backend` directory and configure the environment variables required by the application.

These may include:

- MongoDB connection string
- JWT secret key
- Authentication configuration
- Other required API credentials

Use the variable names expected by the application code. Do not upload passwords, API keys, JWT secrets, or other sensitive information to GitHub.

### Step 4: Start the Backend Server

From the project root, run:

```bash
uvicorn main:app --reload --app-dir backend
```

Alternatively, open the `backend` directory in the terminal and run:

```bash
uvicorn main:app --reload
```

The API server should be available at:

http://127.0.0.1:8000

To access the interactive API documentation, open:

http://127.0.0.1:8000/docs

### Step 5: Start the Frontend

Open a second terminal in VS Code and run:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by the frontend development server in your browser.

Ensure that the frontend API configuration points to the correct backend URL and that the backend allows requests from the frontend origin.

### Step 6: Verify the Database Connection

Ensure that MongoDB is running or that the configured MongoDB connection is accessible.

Check the backend terminal for database connection errors before testing registration, login, resume uploads, and other application features.

## Running the Application

Start both services in separate terminals:

| Service | Command | Purpose |
|---|---|---|
| Backend | `uvicorn main:app --reload --app-dir backend` | Runs the FastAPI application |
| Frontend | `cd frontend` followed by `npm run dev` | Starts the frontend development server |

The frontend and backend must both be running for features that require API communication.

## Future Enhancements

Potential enhancements for the platform include:

- Adaptive interview questions based on candidate responses.
- Improved speech and communication analysis.
- Explainable candidate scoring and ranking.
- Personalized skill-development roadmaps.
- Enhanced recruiter dashboards and analytics.
- Further improvements to interview evaluation and reporting.

These enhancements should be considered planned work unless they are implemented and verified in the current version.

## Project Objective

The objective of DeepHire AI is to develop an intelligent recruitment platform that combines resume analysis, job compatibility evaluation, and interview assistance to support better-informed candidate assessment.

## Contributors

Developed collaboratively as a software project.

Add the names and GitHub profile links of the project contributors here.

## License

A license has not yet been specified. Add an appropriate open-source license if you intend to distribute the project under open-source terms.

