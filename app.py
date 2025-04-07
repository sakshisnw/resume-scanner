import streamlit as st
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import PyPDF2


# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Resume Scanner")

st.title("AI Resume Scanner & Job Matcher")
st.subheader("Paste your resume and a job description. We'll compare them for you.")

# -------------------------------
# Text Inputs
# -------------------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        if file_type == 'txt':
            return str(uploaded_file.read(), "utf-8")
        elif file_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            return "".join(page.extract_text() for page in pdf_reader.pages)
        elif file_type == 'docx':
            return docx2txt.process(uploaded_file)
        else:
            st.warning("Unsupported file type. Please upload a TXT, PDF, or DOCX file.")
    return ""

st.subheader("Upload Resume and Job Description")

resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "txt", "docx"])
job_file = st.file_uploader("Upload Job Description", type=["pdf", "txt", "docx"])

resume_text = extract_text_from_file(resume_file)
job_text = extract_text_from_file(job_file)


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
