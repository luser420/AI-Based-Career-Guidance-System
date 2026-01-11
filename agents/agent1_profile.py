from groq import Groq


def get_groq_client(api_key: str):
    return Groq(api_key=api_key)


def validate_candidate_profile(profile: dict) -> dict:
    if not profile:
        raise ValueError("Candidate profile is empty.")

    required_fields = ["name", "education", "technical_skills"]
    for field in required_fields:
        if field not in profile or not profile[field]:
            raise ValueError(f"Missing required profile field: {field}")

    return profile


def candidate_understanding_agent(
    candidate_profile: dict,
    groq_client: Groq
) -> str:
    """
    Transforms structured candidate data into a professional,
    LinkedIn-style profile understanding.
    """

    candidate_profile = validate_candidate_profile(candidate_profile)

    prompt = f"""
You are a Senior Career Consultant with extensive experience in early-career
and mid-career professional guidance.

Your task is to analyze the following candidate data collected via a
professional profile form and produce a clear, structured career overview.

Guidelines:
- Use ONLY the provided information
- Clearly separate explicit data from inferred insights
- Maintain a LinkedIn-style, professional tone
- Do NOT ask questions
- Do NOT fabricate details
- Avoid emojis and marketing language

CANDIDATE PROFILE DATA:
{candidate_profile}

OUTPUT FORMAT:

Candidate Overview:
- Name:
- Education (Degree, Specialization, Institution):
- Current Career Stage (Student / Fresher / Early Professional / Experienced):

Core Skill Summary:
- Technical Skills:
- Non-Technical / Professional Skills:
- Tools & Technologies:

Professional Exposure:
- Projects Summary:
- Practical Experience Level:
- Key Strength Indicators:

Career Inclinations:
- Explicitly Stated Interests:
- Consultant Inference (with reasoning):

Achievements & Differentiators:
- Academic / Professional Achievements:
- Extracurricular Highlights:

Primary Career Domain Fit:
- Suggested Domain:
- Justification:

Profile Completeness Notes:
- Strongly Defined Areas:
- Missing or Weakly Defined Areas:
"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()