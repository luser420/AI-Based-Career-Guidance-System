from groq import Groq


def job_recommendation_agent(
    structured_profile: str,
    groq_client: Groq
) -> str:
    """
    Recommends realistic, entry-to-early career job roles based on a
    professionally structured candidate profile.
    """

    prompt = f"""
You are a Senior Career Consultant with strong knowledge of hiring trends,
entry-level recruitment, and early-career role expectations.

Your task is to recommend job roles that realistically align with the
candidate’s education, skills, and practical exposure.

Guidelines:
- Base recommendations strictly on the provided profile
- Do NOT overstate seniority or readiness
- Prefer fresher / entry-level / junior roles unless clearly justified
- Explain WHY each role fits the candidate
- Maintain a professional, LinkedIn-style tone
- Do NOT guarantee outcomes
- Do NOT ask questions

CANDIDATE PROFILE SUMMARY:
{structured_profile}

OUTPUT FORMAT (STRICT):

Recommended Job Roles:

1. Role Title:
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

2. Role Title:
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

3. Role Title:
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

4. Role Title (only if strongly relevant):
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

Overall Career Direction Summary:
- 3–4 lines describing the most suitable career trajectory
- Mention whether the candidate is best suited for:
  Technical / Analytical / Business / Hybrid roles
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    return response.choices[0].message.content.strip()