from groq import Groq


def resume_generation_agent(
    structured_profile: str,
    job_recommendations: str,
    skill_gap_analysis: str,
    groq_client: Groq
) -> str:
    """
    Generates a clean, ATS-friendly resume with proper markdown formatting.
    """

    prompt = f"""
You are a Senior Resume Writer and Hiring Consultant with extensive experience
in ATS optimization, LinkedIn recruiter screening, and early-to-mid career hiring
across technology, analytics, and business domains.

Your task is to generate a **high-quality, professional, ATS-friendly resume**
that accurately represents the candidate’s background and aligns strongly with
the recommended job roles.

The resume must look suitable for:
- LinkedIn Easy Apply
- ATS systems (Greenhouse, Workday, Lever)
- Entry-level to early-career hiring managers

--------------------------------------------------
STRICT RULES (NON-NEGOTIABLE)
--------------------------------------------------
- Use Markdown headings ONLY (##, ###)
- Use bullet points ONLY (no paragraphs)
- Maintain clean spacing and consistent formatting
- No emojis, tables, icons, or decorative symbols
- No first-person pronouns (I, me, my, we)
- Do NOT fabricate experience, metrics, companies, or responsibilities
- Do NOT exaggerate seniority or leadership scope
- Do NOT mention skill gaps, weaknesses, or missing skills
- Resume must be honest, realistic, and recruiter-friendly
- Avoid marketing buzzwords and fluff
- Use clear, action-oriented language
- Keep content concise and ATS-readable

--------------------------------------------------
INPUT CONTEXT
--------------------------------------------------

### Candidate Profile (Primary Source of Truth)
{structured_profile}

### Target Job Roles (For Alignment & Positioning)
{job_recommendations}

### Skill Gap Insights (INTERNAL CONTEXT ONLY)
{skill_gap_analysis}
(Note: These insights are for internal alignment ONLY.
Do NOT reference or mention gaps in the resume.)

--------------------------------------------------
RESUME OUTPUT FORMAT (STRICT)
--------------------------------------------------

# Full Name
**Target Professional Title**
(Derive the title realistically from the recommended job roles)

---

## Professional Summary
- 3–4 concise bullet points summarizing:
  - Educational background
  - Core technical/domain strengths
  - Practical exposure (projects, internships, tools)
  - Alignment with target job roles
- Keep tone professional and factual

---

## Core Skills

### Technical Skills
- List only skills explicitly mentioned or clearly implied

### Tools & Technologies
- Software, platforms, frameworks, libraries

### Domain / Functional Skills
- Business, analytical, or role-specific capabilities

---

## Projects / Professional Experience
(Include ONLY what is available in the profile)

### Project / Experience Title
- Action-oriented bullet points describing:
  - What was done
  - Tools or technologies used
  - Nature of contribution and learning outcomes
- Focus on responsibilities and exposure, not impact exaggeration

(Repeat sections only if multiple projects/experiences exist)

---

## Education
- Degree, Specialization
- Institution / University

---

## Achievements & Certifications
- Include ONLY if explicitly provided in the profile
- Certifications, awards, competitions, leadership roles
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()