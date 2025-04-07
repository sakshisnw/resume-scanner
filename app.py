import streamlit as st
import re
import string

st.set_page_config(page_title="AI Resume Scanner", page_icon="📄")

st.title(" AI Resume Scanner & Job Matcher")
st.subheader("Paste your resume and a job description. We'll compare them for you!")

# Text Inputs
resume_text = st.text_area(" Paste Your Resume Text", height=300)
job_text = st.text_area(" Paste Job Description", height=300)

# Clean function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Apply cleaning
if st.button(" Clean & Preview Text"):
    if resume_text and job_text:
        st.write("Cleaned Resume:")
        st.text(clean_text(resume_text))

        st.write("Cleaned Job Description:")
        st.text(clean_text(job_text))
    else:
        st.warning("Please enter both texts.")
