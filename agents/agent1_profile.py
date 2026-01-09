import re
import pdfplumber
import docx2txt
from groq import Groq


# ---------- LLM CLIENT ----------
def get_groq_client(api_key: str):
    return Groq(api_key=api_key)


# ---------- FILE TEXT EXTRACTION ----------
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    return docx2txt.process(file_path).strip()


# ---------- TEXT CLEANING ----------
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()


def validate_profile_text(text: str) -> str:
    if not text or len(text) < 100:
        raise ValueError("Profile information is too short for meaningful analysis.")
    return text[:6000]  # context safety


# ---------- AGENT 1 CORE LOGIC ----------
def candidate_understanding_agent(
    profile_text: str,
    source: str,
    groq_client: Groq
) -> str:

    profile_text = validate_profile_text(profile_text)

    prompt = f"""
You are a Senior Career Consultant and Resume Evaluation Expert.

Your task is to professionally analyze and structure the candidate profile.

Rules:
- Do NOT fabricate information
- Clearly mark inferred vs explicit details
- Maintain professional tone

INPUT SOURCE: {source.upper()}

CANDIDATE DATA:
{profile_text}

OUTPUT FORMAT:

Candidate Overview:
- Name:
- Education:
- Experience Level:

Core Skill Summary:
- Technical Skills:
- Analytical / Domain Skills:
- Tools & Technologies:

Career Interests:
- Stated Interests:
- Inferred Inclinations (with reasoning):

Professional Experience Insight:
- Experience Classification:
- Practical Exposure Level:
- Key Strength Indicators:

Achievements & Projects:
- Highlighted Achievements:
- Notable Projects:

Primary Professional Domain:
- Domain Name:
- Justification:

Data Confidence Notes:
- Missing or unclear information:
- Assumptions made:
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    return response.choices[0].message.content.strip()