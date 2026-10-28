# Resume AI Agent

Resume AI Agent is a project I'm building to help job seekers improve their resumes for specific job descriptions. It checks the resume, calculates an ATS score, finds missing keywords, and suggests areas for improvement.

I'm developing this project using Python and FastAPI, with a focus on making resume optimization simple and useful.

## Features

- Calculate an ATS score based on keywords, skills, and resume sections.
- Analyze job descriptions and extract important keywords.
- Find missing skills and keywords in a resume.
- Check whether a skill is already mentioned in the resume.
- Validate selected keywords before making changes.
- Add verified keywords to the Skills section of a DOCX resume.
- Keep the original resume unchanged when creating an updated copy.

## Technologies Used

- Python
- FastAPI
- Pandas and NumPy (for planned or applicable data-processing features)
- Pydantic
- Python-docx
- pypdf
- Uvicorn
- Git and GitHub

## Project Structure

```text
resume_ai_agent/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       └── main.py
├── requirements.txt
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/santoshkhadul/resume-ai-agent.git
cd resume-ai-agent
```

### 2. Create and activate a virtual environment

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install the required packages

```powershell
pip install -r ..\requirements.txt
```

### 4. Start the server

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to explore and test the APIs.

## Current Progress

The backend includes ATS scoring, job description analysis, keyword matching, keyword validation, and initial DOCX editing functionality.

I'm still working on API testing, document formatting checks, PDF optimization, and the frontend.

## Future Plans

- Build a React frontend.
- Add resume upload and download functionality.
- Improve PDF and DOCX support.
- Check that formatting and page count are preserved.
- Test the complete workflow and deploy the application.

## Developer

**Santosh Khadul**

GitHub: https://github.com/santoshkhadul

This project is a work in progress, and I'm improving it step by step.
