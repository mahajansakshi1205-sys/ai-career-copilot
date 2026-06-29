import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_live_jobs(job_title, location="India",
                   experience="", job_type=""):
    """Fetch real jobs from JSearch API"""

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    query = f"{job_title} in {location}"
    if experience:
        query += f" {experience}"

    params = {
        "query": query,
        "page": "1",
        "num_pages": "2",
        "date_posted": "week",
        "country": "in"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        data = response.json()

        jobs = []
        for job in data.get("data", []):
            jobs.append({
                "title":       job.get("job_title", "N/A"),
                "company":     job.get("employer_name", "N/A"),
                "location":    job.get("job_city", "N/A") or
                               job.get("job_country", "India"),
                "description": job.get(
                    "job_description", ""
                )[:500],
                "salary_min":  job.get("job_min_salary"),
                "salary_max":  job.get("job_max_salary"),
                "apply_link":  job.get("job_apply_link", ""),
                "posted_on":   job.get(
                    "job_posted_at_datetime_utc", ""
                )[:10],
                "job_type":    job.get(
                    "job_employment_type", "Full Time"
                ),
                "source":      job.get("job_publisher", "Job Board"),
                "remote":      job.get(
                    "job_is_remote", False
                ),
                "logo":        job.get(
                    "employer_logo", ""
                ),
            })

        return jobs

    except Exception as e:
        return []


def calculate_job_match(job_description, resume_skills):
    """Calculate how well a job matches resume"""

    if not resume_skills or not job_description:
        return 0

    job_lower    = job_description.lower()
    matched      = 0

    for skill in resume_skills:
        if skill.lower() in job_lower:
            matched += 1

    match_pct = int((matched / len(resume_skills)) * 100)
    return min(match_pct, 100)


def filter_jobs(jobs, min_match=0,
                remote_only=False, job_type="All"):
    """Filter jobs based on criteria"""

    filtered = []
    for job in jobs:
        if remote_only and not job.get('remote'):
            continue
        if job_type != "All" and job.get('job_type') != job_type:
            continue
        if job.get('match_score', 0) < min_match:
            continue
        filtered.append(job)

    return filtered