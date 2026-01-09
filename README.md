# AI Career Guidance & Resume Builder

This is a **multi-agent AI Career Guidance System** that evaluates a candidate’s profile, recommends suitable job roles, identifies skill gaps, and generates a professional resume.  
It uses **Groq’s Llama-4 Scout 17B** model for natural language understanding and Streamlit for an interactive web interface.

## Features

1. **Candidate Profile Understanding (Agent 1)**
   - Analyzes your profile information or uploaded resume
   - Structures details clearly for downstream agents

2. **Job Recommendation (Agent 2)**
   - Suggests realistic and suitable job roles based on skills, experience, and interests

3. **Skill Gap Analysis (Agent 3)**
   - Identifies relevant missing or underdeveloped skills
   - Provides practical upskilling suggestions (dynamic, personalized)

4. **Resume Generation (Agent 4)**
   - Generates an **ATS-friendly professional resume**
   - Highlights strengths aligned with recommended job roles
   - Includes projects, education, achievements, and skills

## Tech Stack

- **Frontend / Web Interface:** Streamlit  
- **Backend / LLM Integration:** Groq Llama-4 Scout 17B  
- **Resume Parsing:** `pdfplumber` (PDF), `docx2txt` (DOCX)  
- **Programming Language:** Python 3.10+
