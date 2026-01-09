from groq import Groq


def resume_generation_agent(
    structured_profile: str,
    job_recommendations: str,
    skill_gap_analysis: str,
    groq_client: Groq
) -> str:
    """
    Generates a professional, ATS-friendly resume aligned with the
    candidate's profile and target job roles.
    """

    prompt = f"""
You are a Senior Resume Writer and Hiring Consultant.

Your task is to generate a **professional, ATS-friendly resume** based on the
candidate profile and target job roles.

Rules:
- Do NOT mention skill gaps
- Do NOT fabricate experience
- Keep resume realistic and honest
- Align strengths with recommended roles
- Adjust depth based on experience level
- Use clean, simple formatting
- Avoid excessive buzzwords

CANDIDATE PROFILE:
{structured_profile}

TARGET JOB ROLES:
{job_recommendations}

SKILL GAP INSIGHTS (INTERNAL CONTEXT ONLY):
{skill_gap_analysis}

RESUME STRUCTURE (STRICT):

Header:
- Name
- Professional Title

Professional Summary:
- 3–4 lines

Key Skills:
- Grouped logically (Technical / Tools / Domain)

Projects / Experience:
- Based on available data
- Use bullet points

Education:
- Degree, institution, specialization

Achievements:
- Only if available

Formatting Rules:
- No tables
- No emojis
- No first-person pronouns
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    return response.choices[0].message.content.strip()