import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import os

# Download stopwords if not already downloaded
# We can wrap it in a try-except to handle network issues gracefully if already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def calculate_match(resume_text, job_text):
    clean_resume = clean_text(resume_text)
    clean_job = clean_text(job_text)
    
    if not clean_resume or not clean_job:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "verdict": "Invalid input: Make sure both resume and job description contain text."
        }

    vectorizer = TfidfVectorizer()
    
    # Check if there is enough vocabulary
    try:
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_job])
    except ValueError:
        # Happens if text is empty after cleaning
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "verdict": "Could not extract meaningful keywords. Resume or job description may be too short."
        }

    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    match_percentage = round(score * 100, 2)
    
    all_words = vectorizer.get_feature_names_out()
    resume_vector = tfidf_matrix[0].toarray()[0]
    job_vector = tfidf_matrix[1].toarray()[0]
    
    missing = [w for w, j, r in zip(all_words, job_vector, resume_vector) if j > 0 and r == 0]
    matched = [w for w, j, r in zip(all_words, job_vector, resume_vector) if j > 0 and r > 0]
    
    # Sort missing by their TF-IDF importance in the job description (descending)
    missing_with_scores = [(w, j) for w, j, r in zip(all_words, job_vector, resume_vector) if j > 0 and r == 0]
    missing_with_scores.sort(key=lambda x: x[1], reverse=True)
    missing_sorted = [w for w, _ in missing_with_scores]
    
    if match_percentage >= 70:
        verdict = "Strong Match ✓"
    elif match_percentage >= 45:
        verdict = "Moderate Match — review missing keywords"
    else:
        verdict = "Weak Match — resume needs significant updates"

    return {
        "score": match_percentage,
        "matched": matched,
        "missing": missing_sorted,
        "verdict": verdict
    }
