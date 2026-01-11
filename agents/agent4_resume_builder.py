from groq import Groq


def resume_generation_agent(
    candidate_profile_summary: str,
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
screening resumes for LinkedIn, ATS systems, and early-career hiring pipelines.

Your task is to generate a professional resume that accurately represents the
candidate’s background and aligns with the recommended job roles.

Rules:
- Use ONLY the provided information
- Do NOT fabricate experience, metrics, or skills
- Do NOT mention skill gaps or weaknesses
- Align strengths and wording with target job roles
- Keep the resume honest, realistic, and recruiter-friendly
- Adjust content depth based on career stage
- Avoid marketing language and excessive buzzwords
- No emojis, tables, or first-person pronouns

CANDIDATE PROFILE SUMMARY:
{candidate_profile_summary}

TARGET JOB ROLES:
{job_recommendations}

SKILL GAP INSIGHTS (INTERNAL CONTEXT ONLY — DO NOT MENTION):
{skill_gap_analysis}

RESUME FORMAT (STRICT — SINGLE COLUMN):

Header:
- Full Name
- Target Professional Title (derived from recommended roles)

Professional Summary:
- 3–4 concise lines highlighting background and role alignment

Core Skills:
- Technical Skills:
- Tools & Technologies:
- Domain / Functional Skills:

Projects / Professional Experience:
- Project or Experience Title
  • Action-oriented bullet points reflecting actual work done
  • Focus on responsibilities, exposure, and learning outcomes

Education:
- Degree, Specialization
- Institution

Achievements & Activities:
- Include ONLY if explicitly available in the profile
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()