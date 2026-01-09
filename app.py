import streamlit as st
import tempfile
from groq import Groq

from agents.agent1_profile import (
    extract_text_from_pdf,
    extract_text_from_docx,
    clean_text,
    candidate_understanding_agent
)

from agents.agent2_jobs import job_recommendation_agent
from agents.agent3_skill_gap import skill_gap_analysis_agent
from agents.agent4_resume_builder import resume_generation_agent


st.set_page_config(
    page_title="AI-Based Career Guidance System",
    layout="wide"
)

st.title("AI-Based Career Guidance System")
st.caption("Multi-Agent Career Evaluation • Professional & Explainable")

# -------- API KEY SETUP (STREAMLIT SECRETS) --------
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("GROQ_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()


for key in [
    "profile_text",
    "structured_profile",
    "job_recommendations",
    "skill_gap_analysis",
    "generated_resume"
]:
    if key not in st.session_state:
        st.session_state[key] = None


st.header("Agent 1: Resume Understanding & Profile Analysis")

input_mode = st.radio(
    "How would you like to provide your profile?",
    ["Upload Resume (PDF / DOCX)", "Paste Profile Text"]
)

profile_text = ""
source_type = ""

if input_mode == "Upload Resume (PDF / DOCX)":
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        try:
            if uploaded_file.name.endswith(".pdf"):
                profile_text = extract_text_from_pdf(file_path)
            else:
                profile_text = extract_text_from_docx(file_path)

            profile_text = clean_text(profile_text)
            source_type = "resume"

            st.success("Resume uploaded and processed successfully.")

        except Exception as e:
            st.error(f"Resume processing failed: {e}")

else:
    profile_text = st.text_area(
        "Paste your resume or profile text here:",
        height=300
    )
    source_type = "manual"


if st.button("Run Agent 1: Analyze Profile"):
    if not profile_text or len(profile_text) < 100:
        st.warning("Please provide sufficient profile information.")
    else:
        with st.spinner("Agent 1 is analyzing the profile..."):
            try:
                st.session_state.structured_profile = candidate_understanding_agent(
                    profile_text=profile_text,
                    source=source_type,
                    groq_client=groq_client
                )

                st.success("Agent 1 analysis completed.")

            except Exception as e:
                st.error(f"Agent 1 failed: {e}")


if st.session_state.structured_profile:
    st.subheader("Structured Candidate Profile")
    st.text(st.session_state.structured_profile)

if st.session_state.structured_profile:
    st.divider()
    st.header("Agent 2: Job Role Recommendations")

    if st.button("Run Agent 2: Recommend Job Roles"):
        with st.spinner("Agent 2 is evaluating suitable job roles..."):
            try:
                st.session_state.job_recommendations = job_recommendation_agent(
                    structured_profile=st.session_state.structured_profile,
                    groq_client=groq_client
                )

                st.success("Job recommendations generated.")

            except Exception as e:
                st.error(f"Agent 2 failed: {e}")

    if st.session_state.job_recommendations:
        st.subheader("Recommended Job Roles")
        st.text(st.session_state.job_recommendations)


if st.session_state.job_recommendations:
    st.divider()
    st.header("Agent 3: Skill Gap Analysis")

    if st.button("Run Agent 3: Analyze Skill Gaps"):
        with st.spinner("Agent 3 is analyzing skill gaps..."):
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
        st.subheader("Skill Gap & Upskilling Insights")
        st.text(st.session_state.skill_gap_analysis)


if st.session_state.skill_gap_analysis:
    st.divider()
    st.header("Agent 4: Resume Generation")

    if st.button("Run Agent 4: Generate Resume"):
        with st.spinner("Agent 4 is generating a professional resume..."):
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
        st.subheader("Generated ATS-Friendly Resume")
        st.text(st.session_state.generated_resume)