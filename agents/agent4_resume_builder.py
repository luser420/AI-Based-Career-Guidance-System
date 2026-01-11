from groq import Groq


def resume_generation_agent(
    structured_profile: str,
    job_recommendations: str,
    skill_gap_analysis: str,
    groq_client: Groq
) -> str:
    """
    Generates a clean, professional, ATS-friendly resume aligned with
    the candidate’s profile and recommended job roles.
    """

    prompt = f"""
You are a Senior Resume Writer and Hiring Consultant with extensive experience
screening resumes for LinkedIn and ATS systems.

Rules:
- Use ONLY provided information
- Do NOT fabricate experience
- Do NOT mention skill gaps
- Align wording with target roles
- Keep resume honest and recruiter-friendly
- No emojis, tables, or first-person pronouns

CANDIDATE PROFILE SUMMARY:
{structured_profile}

TARGET JOB ROLES:
{job_recommendations}

SKILL GAP INSIGHTS (INTERNAL — DO NOT MENTION):
{skill_gap_analysis}

RESUME FORMAT (STRICT):

Header:
- Full Name
- Target Professional Title

Professional Summary:
- 3–4 lines

Core Skills:
- Technical Skills
- Tools & Technologies
- Domain Skills

Projects / Experience:
- Bullet points based on actual work

Education:
- Degree, Specialization
- Institution

Achievements:
- Only if explicitly mentioned
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()