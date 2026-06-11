from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def analyze_skill_gap(resume_skills, job_description):
    prompt = PromptTemplate(
        input_variables=["resume_skills", "job_description"],
        template="""
        You are a career advisor AI.
        Candidate's skills from resume: {resume_skills}
        Job Description: {job_description}
        Analyze and return EXACTLY in this format:
        MATCHING SKILLS: skill1, skill2, skill3
        MISSING SKILLS: skill1, skill2, skill3
        MATCH PERCENTAGE: 75
        SUMMARY: Write 2 lines about the candidate's fit for this role.
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "resume_skills": ", ".join(resume_skills),
        "job_description": job_description
    })
    return response.content

def generate_cover_letter(resume_text, job_description, candidate_name=""):
    prompt = PromptTemplate(
        input_variables=["resume_text", "job_description", "candidate_name"],
        template="""
        You are a professional cover letter writer.
        Candidate Name: {candidate_name}
        Candidate Resume: {resume_text}
        Job Description: {job_description}
        Write a professional cover letter under 300 words.
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "candidate_name": candidate_name
    })
    return response.content

def generate_interview_questions(job_description, difficulty="Medium"):
    prompt = PromptTemplate(
        input_variables=["job_description", "difficulty"],
        template="""
        You are an expert interviewer.
        Job Description: {job_description}
        Difficulty Level: {difficulty}
        Generate exactly 10 interview questions.
        TECHNICAL:
        1. question
        2. question
        3. question
        4. question
        5. question
        BEHAVIORAL:
        6. question
        7. question
        8. question
        9. question
        10. question
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "job_description": job_description,
        "difficulty": difficulty
    })
    return response.content

def evaluate_answer(question, answer, job_description):
    prompt = PromptTemplate(
        input_variables=["question", "answer", "job_description"],
        template="""
        You are an expert interviewer.
        Job Context: {job_description}
        Question: {question}
        Candidate's Answer: {answer}
        Evaluate and return EXACTLY:
        SCORE: (1 to 10)
        STRENGTHS: (what was good)
        IMPROVEMENTS: (what could be better)
        IDEAL_ANSWER: (better version in 2-3 lines)
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "question": question,
        "answer": answer,
        "job_description": job_description
    })
    return response.content

def generate_learning_roadmap(missing_skills, job_description, current_level="Beginner"):
    prompt = PromptTemplate(
        input_variables=["missing_skills", "job_description", "current_level"],
        template="""
        You are a career coach.
        Student's Current Level: {current_level}
        Missing Skills: {missing_skills}
        Target Job: {job_description}
        Create a week by week learning roadmap. Maximum 6 weeks.
        TOTAL_WEEKS: (number)
        GOAL: (one line)
        WEEK_1:
        TITLE: SKILLS: TASKS: RESOURCES: OUTCOME:
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "missing_skills": ", ".join(missing_skills) if isinstance(missing_skills, list) else missing_skills,
        "job_description": job_description,
        "current_level": current_level
    })
    return response.content
