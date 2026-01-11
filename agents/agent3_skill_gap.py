from groq import Groq


def skill_gap_analysis_agent(
    structured_profile: str,
    job_recommendations: str,
    groq_client: Groq
) -> str:
    """
    Produces a clean, readable, LinkedIn-style skill gap analysis.
    """

    prompt = f"""
You are a Senior Career Development Consultant with strong exposure to
entry-level hiring expectations, recruiter screening standards, and
role-readiness evaluation.

Your task is to analyze the candidate profile against the recommended
job roles and present a clear, structured, and honest skill gap analysis.

TONE REQUIREMENTS:
- Professional, realistic, and supportive
- Avoid excessive positivity
- Acknowledge gaps clearly where they impact employability
- Provide a mild reality check without discouraging language
- Sound like a career consultant giving practical guidance

ANALYSIS GUIDELINES:
- Base analysis strictly on the provided data
- Do NOT assume professional experience unless stated
- Identify gaps only when they affect real-world hiring decisions
- Avoid generic or motivational advice
- Do NOT ask questions
- Do NOT exaggerate readiness

STRICT FORMATTING RULES:
- Use Markdown headings only (##, ###)
- Use bullet points only (no paragraphs)
- Clean spacing and readable structure
- No emojis
- No tables

---

## Candidate Profile Summary
{structured_profile}

---

## Recommended Job Roles
{job_recommendations}

---

## Skill Gap Analysis (OUTPUT FORMAT)

### Role-wise Skill Readiness

**Role: <Job Title>**
- Skills Already Aligned:
  - (Clearly demonstrated skills)
- Skills Requiring Strengthening:
  - (Present but not yet industry-ready)
- Critical Missing Skills:
  - (Only if they materially impact entry-level hiring readiness)

(Repeat only for roles with genuine relevance)

---

### Targeted Upskilling Plan
- **Skill / Area** → Practical Next Step → Tools / Platforms
  - Focus on skills that improve short-term employability
  - Avoid long-term or unrealistic expectations

---

### Career Readiness Assessment
- **Overall Readiness Level:** Low / Moderate / Strong
- **Reality Check Insight:**
  - 2–3 bullets explaining:
    - What roles the candidate is realistically competitive for now
    - What gaps may limit immediate hiring
    - What improvements would most impact readiness
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()