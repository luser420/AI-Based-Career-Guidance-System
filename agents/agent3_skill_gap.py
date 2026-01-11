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
You are a Senior Career Development Consultant.

Your task is to analyze the candidate profile against the recommended job roles
and present a **clear, readable skill gap analysis**.

STRICT FORMATTING RULES:
- Use Markdown headings (##, ###)
- Use bullet points only (no long paragraphs)
- Keep spacing clean and readable
- Be concise and practical
- No emojis
- No generic advice

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
- ✅ Skills Already Aligned:
- ⚠️ Skills Requiring Improvement:
- ❌ Critical Missing Skills (if any):

(Repeat only for relevant roles)

---

### Targeted Upskilling Plan
- **Skill / Area** → Recommended Action → Tools / Platforms

---

### Career Readiness Assessment
- **Overall Readiness Level:** Low / Moderate / Strong
- **Insight:** 2–3 lines on job readiness and gap severity
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()