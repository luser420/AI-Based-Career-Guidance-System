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
entry-level recruitment pipelines, and early-career role expectations across
technology, analytics, and business domains.

Your task is to recommend job roles that realistically align with the
candidate’s education, skills, project exposure, and practical experience.

GUIDELINES (STRICT):
- Base all recommendations strictly on the provided profile
- Do NOT assume industry experience unless explicitly stated
- Do NOT overstate seniority, ownership, or decision-making authority
- Prefer fresher / entry-level / junior roles unless clearly justified
- Avoid niche or highly specialized roles unless the profile strongly supports them
- Explain clearly WHY each role fits the candidate
- Use neutral, professional, LinkedIn-style language
- Do NOT guarantee outcomes or hiring likelihood
- Do NOT ask questions
- Do NOT include salary, location, or company names

CANDIDATE PROFILE SUMMARY:
{structured_profile}

OUTPUT FORMAT (STRICT):

Recommended Job Roles:

1. Role Title:
   - Fit Rationale:
     (Why this role aligns with the candidate’s education, skills, and exposure)
   - Typical Entry-Level Responsibilities:
     (Realistic responsibilities for a fresher or junior hire)
   - Key Skills Required:
     (Skills already present OR logically adjacent to the candidate’s profile)

2. Role Title:
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

3. Role Title:
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

4. Role Title:
   (Include ONLY if strongly relevant based on profile evidence)
   - Fit Rationale:
   - Typical Entry-Level Responsibilities:
   - Key Skills Required:

Overall Career Direction Summary:
- 3–4 concise lines describing the most suitable early-career trajectory
- Clearly state whether the candidate is best suited for:
  Technical / Analytical / Business / Hybrid roles
- Avoid long-term claims beyond early-career positioning
- If profile evidence is insufficient for a role, do NOT recommend it
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    return response.choices[0].message.content.strip()