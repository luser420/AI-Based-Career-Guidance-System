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
You are a Senior Resume Writer and Hiring Consultant.

Generate a **professional, ATS-friendly resume** using the information below.

STRICT RULES:
- Use Markdown headings
- Clean spacing
- Bullet points only
- No emojis
- No tables
- No first-person language
- Do NOT mention skill gaps

---

## Candidate Profile
{structured_profile}

---

## Target Job Roles
{job_recommendations}

---

## Resume Output (STRICT FORMAT)

# Full Name
**Target Professional Title**

---

## Professional Summary
- 3–4 concise bullet points aligned to target roles

---

## Core Skills
**Technical Skills**
- ...

**Tools & Technologies**
- ...

**Domain Skills**
- ...

---

## Projects / Experience
**Project / Role Title**
- Action-oriented bullet points
- Focus on responsibilities and learning outcomes

---

## Education
- Degree, Specialization  
- Institution

---

## Achievements
- Include ONLY if explicitly present
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()