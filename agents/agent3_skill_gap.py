from groq import Groq


def skill_gap_analysis_agent(
    structured_profile: str,
    job_recommendations: str,
    groq_client: Groq
) -> str:
    """
    Evaluates the candidate’s readiness for the recommended roles by identifying
    genuine skill gaps and suggesting targeted upskilling actions.
    """

    prompt = f"""
You are a Senior Career Development Consultant specializing in workforce
readiness and early-career skill alignment.

Your task is to analyze the candidate’s profile against the recommended job
roles and identify ONLY meaningful skill gaps that could impact employability.

Guidelines:
- Focus strictly on skills relevant to the recommended roles
- Do NOT invent gaps if the candidate already meets expectations
- Clearly distinguish between strengths and gaps
- Keep the tone supportive, practical, and realistic
- Avoid generic advice
- Do NOT ask questions

CANDIDATE PROFILE SUMMARY:
{structured_profile}

RECOMMENDED JOB ROLES:
{job_recommendations}

OUTPUT FORMAT (STRICT):

Role-Wise Skill Readiness:

1. Role Title:
   - Skills Already Aligned:
   - Skills Requiring Improvement:
   - Critical Missing Skills (if any):

2. Role Title (if applicable):
   - Skills Already Aligned:
   - Skills Requiring Improvement:
   - Critical Missing Skills (if any):

Targeted Upskilling Plan:
- Skill / Area:
  Recommended Action:
  Suggested Tools / Platforms:

Career Readiness Assessment:
- Overall Readiness Level (Low / Moderate / Strong):
- 2–3 lines explaining job-readiness distance
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    return response.choices[0].message.content.strip()