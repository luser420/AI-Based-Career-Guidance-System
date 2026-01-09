from groq import Groq


def skill_gap_analysis_agent(
    structured_profile: str,
    job_recommendations: str,
    groq_client: Groq
) -> str:
    """
    Performs a personalized skill gap analysis based on the candidate profile
    and recommended job roles.
    """

    prompt = f"""
You are a Senior Career Development & Workforce Readiness Expert.

Your task is to identify **relevant skill gaps** between the candidate's
current profile and the recommended job roles.

Guidelines:
- Analyze ONLY skills relevant to the suggested roles
- Do NOT force a fixed number of skills
- Mention gaps only if they genuinely exist
- Keep tone supportive and constructive
- Suggest upskilling only where necessary
- Avoid generic or obvious advice

CANDIDATE PROFILE:
{structured_profile}

RECOMMENDED JOB ROLES:
{job_recommendations}

OUTPUT FORMAT (STRICT):

Skill Gaps:
- (List only missing or underdeveloped skills, if any)

Upskilling Recommendations:
- (Practical learning actions, tools, or focus areas — only if required)

Career Readiness Insight:
(2–3 lines on overall readiness for the suggested roles)
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()