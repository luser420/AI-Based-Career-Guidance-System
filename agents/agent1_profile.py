from groq import Groq


def get_groq_client(api_key: str):
    return Groq(api_key=api_key)


def validate_candidate_profile(profile: dict) -> dict:
    if not profile:
        raise ValueError("Candidate profile is empty.")

    required_fields = ["name", "education", "technical_skills"]
    for field in required_fields:
        if field not in profile or not profile[field]:
            raise ValueError(f"Missing required profile field: {field}")

    return profile


def candidate_understanding_agent(candidate_profile: dict, groq_client: Groq) -> str:
    """
    candidate_profile: dict with keys
        - name
        - education {degree, specialization, institution}
        - technical_skills (list)
        - soft_skills (list)
        - projects (str)
        - achievements (str)
    groq_client: Groq API client
    """
    # Build prompt from dictionary
    profile_text = f"""
Name: {candidate_profile['name']}

Education:
- Degree: {candidate_profile['education']['degree']}
- Specialization: {candidate_profile['education']['specialization']}
- Institution: {candidate_profile['education']['institution']}

Technical Skills:
{', '.join(candidate_profile['technical_skills'])}

Non-Technical Skills:
{', '.join(candidate_profile['soft_skills'])}

Projects / Experience:
{candidate_profile['projects']}

Achievements:
{candidate_profile['achievements']}
"""

    prompt = f"""
You are a Senior Career Consultant with extensive experience in early-career
and mid-career professional guidance, talent assessment, and recruiter-facing
profile evaluation.

Your task is to analyze the candidate information collected via a structured
professional profile form and produce a **clear, well-organized, recruiter-style
career overview** that can be used by downstream AI agents.

--------------------------------------------------
STRICT GUIDELINES (NON-NEGOTIABLE)
--------------------------------------------------
- Use ONLY the information explicitly provided in the input
- Do NOT ask follow-up questions
- Do NOT fabricate qualifications, experience, or metrics
- Clearly distinguish between:
  - Explicitly stated information
  - Reasoned professional inference
- Maintain a professional, LinkedIn-style tone
- Avoid emojis, buzzwords, and marketing language
- Keep wording neutral, factual, and structured
- Ensure consistent formatting across sections

--------------------------------------------------
CANDIDATE PROFILE DATA (PRIMARY SOURCE)
--------------------------------------------------
{candidate_profile}

--------------------------------------------------
OUTPUT FORMAT (STRICT – FOLLOW EXACTLY)
--------------------------------------------------

## Candidate Overview
- Name:
- Education (Degree, Specialization, Institution):
- Current Career Stage:
  (Choose one: Student / Fresher / Early Professional / Experienced)

---

## Core Skill Summary

### Technical Skills
- (List only explicitly mentioned or clearly implied technical skills)

### Professional / Soft Skills
- (Communication, leadership, teamwork, etc., if provided)

### Tools & Technologies
- (Programming languages, software, platforms, frameworks, tools)

---

## Professional Exposure

### Projects Summary
- (Brief, factual overview of academic or personal projects)

### Practical Experience Level
- (None / Academic Projects / Internships / Work Experience)

### Key Strength Indicators
- (Observed strengths based on education, projects, or exposure)

---

## Career Inclinations

### Explicitly Stated Interests
- (Only interests clearly mentioned by the candidate)

### Consultant Inference (With Reasoning)
- (Carefully inferred career direction based on skills, education, and projects)

---

## Achievements & Differentiators

### Academic / Professional Achievements
- (Awards, certifications, recognitions – ONLY if explicitly stated)

### Extracurricular Activities
- (Clubs, societies, competitions, hackathons, volunteering, sports,
  community initiatives, leadership roles, or event participation)

- Note:
  - Include extracurriculars only if provided
  - Do NOT exaggerate impact
  - Do NOT convert participation into achievements unless explicitly stated

---

## Primary Career Domain Fit
- Suggested Domain:
- Justification:
  (1–2 concise lines linking profile strengths to the domain)

---

## Profile Completeness Notes

### Strongly Defined Areas
- (Sections where information is clear and detailed)

### Missing or Weakly Defined Areas
- (Areas with limited or unclear information – no judgmental tone)
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()