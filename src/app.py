# app.py
import streamlit as st
from io import BytesIO
import os
import tailor_resume
from tailor_resume import tailor_resume_in_memory

# Page config
st.set_page_config(page_title="Resume Tailor", layout="centered")

st.title("📄 Resume Tailor")
st.markdown("Upload your resume and paste the job description to get a tailored version.")

# Input fields
job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")

uploaded_file = st.file_uploader("Upload Your Resume (.docx)", type="docx")

# OpenAI Key (required if USE_OPENAI=1, please include quotation marks like "sk-xxxx")
openai_key = st.text_input("OpenAI API Key required, please include quotation marks like 'sk-xxxx'", type="password")
model = st.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)

if st.button("Tailor Resume"):
    if not uploaded_file or not job_description.strip():
        st.error("Please upload a resume and provide a job description.")
    else:
        uploaded_resume_bytes = uploaded_file.read()
        with open("temp_resume.docx", "wb") as f:
            f.write(uploaded_resume_bytes)

        tailored_bytes = tailor_resume.tailor_resume_in_memory("temp_resume.docx", job_description)
        with open("resume_tailored.docx", "wb") as f:
            f.write(tailored_bytes)

        cover_letter_path = "resume_tailored_cover_letter.docx"
        tailor_resume.generate_cover_letter("temp_resume.docx", job_description, cover_letter_path)
        with open(cover_letter_path, "rb") as f:
            cover_letter_bytes = f.read()

        recruiter_msg_path = "resume_tailored_recruiter_msg.txt"
        tailor_resume.generate_recruiter_message("temp_resume.docx", job_description, recruiter_msg_path)
        with open(recruiter_msg_path, "rb") as f:
            recruiter_msg_bytes = f.read()

        # Store in session state
        st.session_state["tailored_bytes"] = tailored_bytes
        st.session_state["cover_letter_bytes"] = cover_letter_bytes
        st.session_state["recruiter_msg_bytes"] = recruiter_msg_bytes
        st.success("Resume tailored! Download your files below.")

# Show download buttons if files exist in session state
if "tailored_bytes" in st.session_state:
    st.download_button(
        "Download Tailored Resume (.docx)",
        st.session_state["tailored_bytes"],
        file_name="resume_tailored.docx"
    )
if "cover_letter_bytes" in st.session_state:
    st.download_button(
        "Download Cover Letter (.docx)",
        st.session_state["cover_letter_bytes"],
        file_name="resume_tailored_cover_letter.docx"
    )
if "recruiter_msg_bytes" in st.session_state:
    st.download_button(
        "Download Recruiter Message (.txt)",
        st.session_state["recruiter_msg_bytes"],
        file_name="resume_tailored_recruiter_msg.txt"
    )