from groq import Groq


def job_recommendation_agent(
    structured_profile: str,
    groq_client: Groq
) -> str:
    """
    Analyzes a structured candidate profile and recommends suitable job roles
    with professional reasoning.
    """

    prompt = f"""
You are a Senior Career Advisor with extensive hiring and industry exposure.

Your task is to recommend **realistic and suitable job roles** for the candidate
based strictly on the provided profile.

Guidelines:
- Recommend roles aligned with skills, education, and experience level
- Do NOT exaggerate seniority
- Prefer entry-level or early-career roles where appropriate
- Recommendations must be advisory, not guaranteed
- Use professional, career-consultant language
- Provide clear reasoning

CANDIDATE PROFILE:
{structured_profile}

OUTPUT FORMAT (STRICT):

Recommended Job Roles:
1. Job Title – 1–2 line justification
2. Job Title – 1–2 line justification
3. Job Title – 1–2 line justification
4. Job Title – 1–2 line justification
5. Job Title – 1–2 line justification
(Include more ONLY if strongly relevant)

Overall Career Direction Summary:
(3–4 lines explaining the general career trajectory)
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()