import streamlit as st
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Resume Scanner")

st.title("AI Resume Scanner & Job Matcher")
st.subheader("Paste your resume and a job description. We'll compare them for you.")

# -------------------------------
# Text Inputs
# -------------------------------
resume_text = st.text_area("Paste Your Resume Text", height=300)
job_text = st.text_area("Paste Job Description", height=300)

# -------------------------------
# Text Cleaning Function
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Preview Cleaned Text
# -------------------------------
if st.button("Clean & Preview Text"):
    if resume_text and job_text:
        st.write("Cleaned Resume:")
        st.text(clean_text(resume_text))

        st.write("Cleaned Job Description:")
        st.text(clean_text(job_text))
    else:
        st.warning("Please enter both resume and job description.")

# -------------------------------
# Similarity Calculation Function
# -------------------------------
def calculate_similarity(resume, job):
    texts = [resume, job]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0] * 100

# -------------------------------
# Match Button + Score Result
# -------------------------------
st.markdown("---")
st.subheader("Match Result")

if st.button("Match Resume to Job Description"):
    if resume_text and job_text:
        cleaned_resume = clean_text(resume_text)
        cleaned_job = clean_text(job_text)

        score = calculate_similarity(cleaned_resume, cleaned_job)

        st.success(f"Match Score: {score:.2f}%")

        if score > 80:
            st.info("Great match! You're highly aligned with the job.")
        elif score > 50:
            st.warning("Partial match. Consider tailoring your resume.")
        else:
            st.error("Low match. Try aligning your resume better.")
    else:
        st.warning("Please fill in both the resume and job description.")
