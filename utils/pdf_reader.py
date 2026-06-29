import pdfplumber
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ── COMPREHENSIVE SKILLS DATABASE ─────────────────────────
SKILLS_DATABASE = {
    "programming_languages": [
        "python", "java", "javascript", "typescript",
        "c++", "c#", "c", "r", "scala", "kotlin",
        "swift", "dart", "golang", "rust", "php",
        "ruby", "matlab", "bash", "shell"
    ],
    "ai_ml": [
        "machine learning", "deep learning",
        "artificial intelligence", "neural network",
        "natural language processing", "nlp",
        "computer vision", "reinforcement learning",
        "transfer learning", "data science",
        "scikit-learn", "tensorflow", "pytorch",
        "keras", "xgboost", "lightgbm", "catboost",
        "huggingface", "transformers", "bert",
        "langchain", "openai", "llm"
    ],
    "data": [
        "pandas", "numpy", "matplotlib", "seaborn",
        "plotly", "tableau", "power bi", "excel",
        "data analysis", "data visualization",
        "data engineering", "etl", "spark",
        "hadoop", "kafka", "airflow"
    ],
    "web": [
        "html", "css", "react", "angular", "vue",
        "nodejs", "django", "flask", "fastapi",
        "streamlit", "rest api", "graphql",
        "javascript", "typescript", "bootstrap",
        "tailwind", "nextjs"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb",
        "sqlite", "redis", "firebase", "oracle",
        "cassandra", "dynamodb", "neo4j"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud",
        "docker", "kubernetes", "git", "github",
        "gitlab", "ci/cd", "jenkins", "linux",
        "terraform", "ansible"
    ],
    "mobile": [
        "flutter", "android", "ios", "react native",
        "kotlin", "swift", "dart", "android studio"
    ],
    "soft_skills": [
        "leadership", "communication", "teamwork",
        "problem solving", "project management",
        "agile", "scrum", "time management",
        "critical thinking", "collaboration"
    ]
}


def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text


def extract_skills_from_text(text):
    """Extract skills using spaCy + skills database"""
    text_lower = text.lower()
    found_skills = []

    # Match from skills database
    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            if skill in text_lower:
                if skill not in found_skills:
                    found_skills.append(skill)

    return found_skills


def extract_skills_by_category(text):
    """Extract skills organized by category"""
    text_lower = text.lower()
    categorized = {}

    for category, skills in SKILLS_DATABASE.items():
        found = []
        for skill in skills:
            if skill in text_lower:
                found.append(skill)
        if found:
            categorized[category] = found

    return categorized


def calculate_ats_score(resume_text, job_description):
    """Calculate ATS compatibility score"""
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    # Extract words from job description
    job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_lower))

    # Common words to ignore
    ignore_words = {
        "the", "and", "for", "with", "this",
        "that", "will", "have", "from", "they",
        "are", "our", "your", "you", "we",
        "can", "all", "any", "not", "but"
    }
    job_words = job_words - ignore_words

    # Count matches
    matched = 0
    matched_keywords = []
    missing_keywords = []

    for word in job_words:
        if word in resume_lower:
            matched += 1
            matched_keywords.append(word)
        else:
            missing_keywords.append(word)

    total = len(job_words)
    ats_score = int((matched / total) * 100) if total > 0 else 0

    return {
        "ats_score": ats_score,
        "matched_keywords": matched_keywords[:15],
        "missing_keywords": missing_keywords[:15],
        "total_keywords": total,
        "matched_count": matched
    }


def extract_resume_info(text):
    """Extract basic info from resume using spaCy"""
    doc = nlp(text)

    # Extract emails
    emails = re.findall(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        text
    )

    # Extract phone numbers
    phones = re.findall(
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        text
    )

    # Extract organizations using spaCy
    organizations = [
        ent.text for ent in doc.ents
        if ent.label_ == "ORG"
    ][:5]

    # Word count
    word_count = len(text.split())

    return {
        "email": emails[0] if emails else "Not found",
        "phone": phones[0] if phones else "Not found",
        "organizations": organizations,
        "word_count": word_count,
    }