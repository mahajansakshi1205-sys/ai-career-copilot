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
    """Analyze skill gap with salary impact"""

    prompt = PromptTemplate(
        input_variables=["resume_skills", "job_description"],
        template="""
        You are an expert career advisor and salary analyst.

        Candidate's skills: {resume_skills}
        Job Description: {job_description}

        Analyze and return EXACTLY in this format:

        MATCHING SKILLS: skill1, skill2, skill3
        MISSING SKILLS: skill1, skill2, skill3
        MATCH PERCENTAGE: 75
        SUMMARY: Write 2 lines about candidate fit.

        SALARY_IMPACT:
        skill1: +X LPA
        skill2: +X LPA
        skill3: +X LPA

        MARKET_DEMAND:
        skill1: High/Medium/Low
        skill2: High/Medium/Low
        skill3: High/Medium/Low

        PRIORITY_TO_LEARN:
        1. skill1 - reason why
        2. skill2 - reason why
        3. skill3 - reason why
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "resume_skills": ", ".join(resume_skills),
        "job_description": job_description
    })

    return response.content


def generate_cover_letter(resume_text, job_description,
                          candidate_name=""):
    """Generate professional cover letter"""

    prompt = PromptTemplate(
        input_variables=[
            "resume_text",
            "job_description",
            "candidate_name"
        ],
        template="""
        You are a professional cover letter writer.

        Candidate Name: {candidate_name}
        Resume: {resume_text}
        Job Description: {job_description}

        Write a professional cover letter.
        Keep it under 300 words.
        Make it sound human and natural.

        Format:
        - Opening: Strong introduction
        - Middle: Key matching skills
        - Third: Why this company
        - Closing: Call to action
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "candidate_name": candidate_name
    })

    return response.content


def generate_interview_questions(job_description,
                                 difficulty="Medium"):
    """Generate interview questions"""

    prompt = PromptTemplate(
        input_variables=["job_description", "difficulty"],
        template="""
        You are an expert interviewer.

        Job Description: {job_description}
        Difficulty: {difficulty}

        Generate exactly 10 interview questions.

        Return EXACTLY in this format:

        TECHNICAL:
        1. question here
        2. question here
        3. question here
        4. question here
        5. question here

        BEHAVIORAL:
        6. question here
        7. question here
        8. question here
        9. question here
        10. question here
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "job_description": job_description,
        "difficulty": difficulty
    })

    return response.content


def evaluate_answer(question, answer, job_description):
    """Evaluate interview answer"""

    prompt = PromptTemplate(
        input_variables=["question", "answer",
                         "job_description"],
        template="""
        You are an expert interviewer.

        Job Context: {job_description}
        Question: {question}
        Answer: {answer}

        Evaluate and return EXACTLY:

        SCORE: (1 to 10)
        STRENGTHS: (what was good)
        IMPROVEMENTS: (what to improve)
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


def generate_learning_roadmap(missing_skills,
                              job_description,
                              current_level="Beginner"):
    """Generate personalized learning roadmap"""

    prompt = PromptTemplate(
        input_variables=[
            "missing_skills",
            "job_description",
            "current_level"
        ],
        template="""
        You are an expert career coach.

        Current Level: {current_level}
        Missing Skills: {missing_skills}
        Target Job: {job_description}

        Create a week by week learning roadmap.

        Return EXACTLY in this format:

        TOTAL_WEEKS: (number)
        GOAL: (one line goal)

        WEEK_1:
        TITLE: (week title)
        SKILLS: (skill1, skill2)
        TASKS: (task1 | task2 | task3)
        RESOURCES: (resource1 | resource2)
        OUTCOME: (what student achieves)

        WEEK_2:
        TITLE: (week title)
        SKILLS: (skill1, skill2)
        TASKS: (task1 | task2 | task3)
        RESOURCES: (resource1 | resource2)
        OUTCOME: (what student achieves)

        Continue for all weeks. Maximum 6 weeks.
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "missing_skills": ", ".join(missing_skills)
        if isinstance(missing_skills, list)
        else missing_skills,
        "job_description": job_description,
        "current_level": current_level
    })

    return response.content


def get_market_insights(skills, job_title):
    """Get market insights for skills"""

    prompt = PromptTemplate(
        input_variables=["skills", "job_title"],
        template="""
        You are a job market expert.

        Skills: {skills}
        Job Title: {job_title}

        Return EXACTLY in this format:

        TRENDING_SKILLS: skill1, skill2, skill3
        DECLINING_SKILLS: skill1, skill2
        AVG_SALARY: X to Y LPA
        JOB_OUTLOOK: (2-3 lines about market)
        TOP_COMPANIES: company1, company2, company3
        CERTIFICATIONS: cert1, cert2, cert3
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "skills": ", ".join(skills),
        "job_title": job_title
    })

    return response.content