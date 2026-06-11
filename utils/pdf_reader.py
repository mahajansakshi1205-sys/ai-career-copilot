import PyPDF2 
import re

def extract_text_from_pdf(uploaded_file): 
    """Read PDF and extract all text""" 
    text = "" 
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
      text += page.extract_text()

    return text
def extract_skills_from_text(text): 
    """Find common skills from resume text"""

# Common skills list to look for
    common_skills = [
    "python", "java", "javascript", "sql", "html", "css",
    "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "tensorflow", "pytorch",
    "react", "nodejs", "django", "flask", "fastapi",
    "git", "docker", "aws", "azure", "mongodb",
    "communication", "leadership", "teamwork",
    "excel", "powerpoint", "tableau", "power bi"
    ]

    text_lower = text.lower()
    found_skills = []

    for skill in common_skills:
       if skill in text_lower:
         found_skills.append(skill)

    return found_skills