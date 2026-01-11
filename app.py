import streamlit as st
from groq import Groq

from agents.agent1_profile import candidate_understanding_agent
from agents.agent2_jobs import job_recommendation_agent
from agents.agent3_skill_gap import skill_gap_analysis_agent
from agents.agent4_resume_builder import resume_generation_agent


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Based Career Guidance System",
    layout="wide"
)

st.title("AI-Based Career Guidance System")
st.caption("Multi-Agent Career Evaluation • LinkedIn-Style • Professional & Explainable")


# ---------------- API KEY ----------------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("GROQ_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()


# ---------------- SESSION STATE ----------------
for key in [
    "structured_profile",
    "job_recommendations",
    "skill_gap_analysis",
    "generated_resume"
]:
    if key not in st.session_state:
        st.session_state[key] = None


# =========================================================
# AGENT 1 — LINKEDIN-STYLE PROFILE FORM
# =========================================================
st.header("Candidate Profile")

with st.form("candidate_profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        degree = st.selectbox(
            "Highest Degree",
            ["B.Tech", "B.Sc", "B.Com", "BA", "M.Tech", "M.Sc", "MBA", "Other"]
        )
        specialization = st.text_input("Specialization")
        institution = st.text_input("Institution / University")

    with col2:
        technical_skills = st.text_area(
            "Technical Skills (comma-separated)",
            placeholder="Python, SQL, Machine Learning, Power BI"
        )
        soft_skills = st.text_area(
            "Non-Technical Skills",
            placeholder="Communication, Leadership, Problem Solving"
        )

    projects = st.text_area(
        "Projects / Internships",
        placeholder="Describe projects, tools used, and outcomes"
    )

    achievements = st.text_area(
        "Achievements / Certifications / Extra-Curricular Activities ",
        placeholder="Certifications, awards, hackathons, etc."
    )

    submitted = st.form_submit_button("Analyze My Profile")


# ---------------- RUN AGENT 1 ----------------
if submitted:
    if not name or not degree or not technical_skills:
        st.warning("Please fill in at least Name, Degree, and Technical Skills.")
    else:
        with st.spinner("Analyzing profile like a career consultant..."):
            try:
                # This is the call to your agent function
                st.session_state.structured_profile = candidate_understanding_agent(
                    candidate_profile={
                        "name": name,
                        "education": {
                            "degree": degree,
                            "specialization": specialization,
                            "institution": institution
                        },
                        "technical_skills": [s.strip() for s in technical_skills.split(",") if s.strip()],
                        "soft_skills": [s.strip() for s in soft_skills.split(",") if s.strip()],
                        "projects": projects,
                        "achievements": achievements
                    },
                    groq_client=groq_client
                )
                st.success("Profile analyzed!")
            except Exception as e:
                st.error(f"Agent 1 failed: {e}")

# This part is now outside the try/except block
if st.session_state.structured_profile:
    st.subheader("📌 Structured Candidate Profile")
    st.markdown(st.session_state.structured_profile)


# =========================================================
# AGENT 2 — JOB RECOMMENDATIONS
# =========================================================
if st.session_state.structured_profile:
    st.divider()
    st.header("Job Role Recommendations")

    if st.button("Recommend Job Roles"):
        with st.spinner("Identifying best-fit roles..."):
            try:
                st.session_state.job_recommendations = job_recommendation_agent(
                    structured_profile=st.session_state.structured_profile,
                    groq_client=groq_client
                )
                st.success("Job recommendations generated.")
            except Exception as e:
                st.error(f"Agent 2 failed: {e}")

    if st.session_state.job_recommendations:
        st.text(st.session_state.job_recommendations)


# =========================================================
# AGENT 3 — SKILL GAP ANALYSIS
# =========================================================
if st.session_state.job_recommendations:
    st.divider()
    st.header("Skill Gap Analysis")

    if st.button("Analyze Skill Gaps"):
        with st.spinner("Evaluating industry readiness..."):
            try:
                st.session_state.skill_gap_analysis = skill_gap_analysis_agent(
                    structured_profile=st.session_state.structured_profile,
                    job_recommendations=st.session_state.job_recommendations,
                    groq_client=groq_client
                )
                st.success("Skill gap analysis completed.")
            except Exception as e:
                st.error(f"Agent 3 failed: {e}")

    if st.session_state.skill_gap_analysis:
        st.text(st.session_state.skill_gap_analysis)


# =========================================================
# AGENT 4 — RESUME GENERATION
# =========================================================
if st.session_state.skill_gap_analysis:
    st.divider()
    st.header("ATS-Friendly Resume")

    if st.button("Generate Resume"):
        with st.spinner("Generating professional resume..."):
            try:
                st.session_state.generated_resume = resume_generation_agent(
                    structured_profile=st.session_state.structured_profile,
                    job_recommendations=st.session_state.job_recommendations,
                    skill_gap_analysis=st.session_state.skill_gap_analysis,
                    groq_client=groq_client
                )
                st.success("Resume generated successfully.")
            except Exception as e:
                st.error(f"Agent 4 failed: {e}")

    if st.session_state.generated_resume:
        st.text(st.session_state.generated_resume)