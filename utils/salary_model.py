import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import os

# ── TRAINING DATA — Very conservative Indian market ───────
SALARY_DATA = [
    # role, experience, location, skills_count, remote, salary_lpa
    ("Python Developer",     0, "Bangalore", 5,  False, 2.5),
    ("Python Developer",     1, "Bangalore", 7,  False, 3.8),
    ("Python Developer",     2, "Bangalore", 8,  True,  5.2),
    ("Python Developer",     3, "Bangalore", 10, True,  7.0),
    ("Python Developer",     5, "Bangalore", 12, True,  10.0),
    ("Python Developer",     0, "Mumbai",    5,  False, 2.3),
    ("Python Developer",     2, "Mumbai",    8,  False, 4.8),
    ("Python Developer",     0, "Indore",    4,  False, 1.8),
    ("Python Developer",     1, "Indore",    6,  False, 2.8),
    ("Python Developer",     2, "Indore",    8,  True,  4.0),
    ("Data Analyst",         0, "Bangalore", 5,  False, 2.2),
    ("Data Analyst",         1, "Bangalore", 7,  False, 3.5),
    ("Data Analyst",         2, "Bangalore", 8,  False, 5.0),
    ("Data Analyst",         3, "Bangalore", 10, True,  7.0),
    ("Data Analyst",         0, "Mumbai",    5,  False, 2.0),
    ("Data Analyst",         2, "Mumbai",    7,  False, 4.5),
    ("Data Analyst",         0, "Indore",    4,  False, 1.6),
    ("Data Analyst",         1, "Indore",    6,  False, 2.5),
    ("ML Engineer",          0, "Bangalore", 7,  False, 4.0),
    ("ML Engineer",          1, "Bangalore", 9,  False, 6.0),
    ("ML Engineer",          2, "Bangalore", 11, True,  8.5),
    ("ML Engineer",          3, "Bangalore", 13, True,  11.0),
    ("ML Engineer",          5, "Bangalore", 15, True,  15.0),
    ("ML Engineer",          0, "Mumbai",    7,  False, 3.5),
    ("ML Engineer",          2, "Mumbai",    10, True,  7.5),
    ("ML Engineer",          0, "Indore",    6,  False, 2.8),
    ("Data Scientist",       0, "Bangalore", 8,  False, 4.5),
    ("Data Scientist",       1, "Bangalore", 10, False, 6.5),
    ("Data Scientist",       2, "Bangalore", 12, True,  9.0),
    ("Data Scientist",       3, "Bangalore", 14, True,  12.0),
    ("Data Scientist",       5, "Bangalore", 16, True,  17.0),
    ("Data Scientist",       0, "Mumbai",    8,  False, 4.0),
    ("Data Scientist",       0, "Indore",    7,  False, 3.0),
    ("Web Developer",        0, "Bangalore", 5,  False, 2.0),
    ("Web Developer",        1, "Bangalore", 7,  False, 3.2),
    ("Web Developer",        2, "Bangalore", 9,  True,  5.0),
    ("Web Developer",        3, "Bangalore", 11, True,  7.0),
    ("Web Developer",        0, "Mumbai",    5,  False, 1.8),
    ("Web Developer",        0, "Indore",    4,  False, 1.5),
    ("Full Stack Developer", 0, "Bangalore", 8,  False, 3.0),
    ("Full Stack Developer", 1, "Bangalore", 10, False, 4.5),
    ("Full Stack Developer", 2, "Bangalore", 12, True,  6.5),
    ("Full Stack Developer", 3, "Bangalore", 14, True,  9.0),
    ("Full Stack Developer", 0, "Mumbai",    8,  False, 2.8),
    ("Full Stack Developer", 0, "Indore",    7,  False, 2.2),
    ("DevOps Engineer",      0, "Bangalore", 7,  False, 3.5),
    ("DevOps Engineer",      1, "Bangalore", 9,  False, 5.5),
    ("DevOps Engineer",      2, "Bangalore", 11, True,  8.0),
    ("DevOps Engineer",      3, "Bangalore", 13, True,  11.0),
    ("DevOps Engineer",      0, "Mumbai",    7,  False, 3.2),
    ("DevOps Engineer",      0, "Indore",    6,  False, 2.5),
    ("AI Engineer",          0, "Bangalore", 9,  False, 5.0),
    ("AI Engineer",          1, "Bangalore", 11, True,  7.5),
    ("AI Engineer",          2, "Bangalore", 13, True,  11.0),
    ("AI Engineer",          3, "Bangalore", 15, True,  15.0),
    ("AI Engineer",          5, "Bangalore", 17, True,  20.0),
    ("AI Engineer",          0, "Mumbai",    9,  False, 4.5),
    ("AI Engineer",          0, "Indore",    8,  False, 3.5),
]

# Skill impact — very small bonuses
SKILL_SALARY_IMPACT = {
    "python":           0.5,
    "machine learning": 0.8,
    "deep learning":    1.0,
    "tensorflow":       0.9,
    "pytorch":          0.9,
    "docker":           0.6,
    "kubernetes":       0.8,
    "aws":              0.7,
    "azure":            0.6,
    "sql":              0.3,
    "pandas":           0.4,
    "numpy":            0.3,
    "react":            0.5,
    "nodejs":           0.4,
    "fastapi":          0.5,
    "langchain":        1.0,
    "nlp":              0.8,
    "data science":     0.8,
    "git":              0.1,
    "streamlit":        0.2,
    "flutter":          0.4,
    "java":             0.4,
    "javascript":       0.4,
    "spark":            0.7,
    "kafka":            0.7,
}

# Location multipliers
LOCATION_MULTIPLIER = {
    "Bangalore": 1.00,
    "Mumbai":    0.90,
    "Hyderabad": 0.88,
    "Pune":      0.82,
    "Chennai":   0.82,
    "Delhi":     0.85,
    "Indore":    0.65,
    "Jaipur":    0.62,
    "Ahmedabad": 0.68,
}


def train_salary_model():
    df = pd.DataFrame(
        SALARY_DATA,
        columns=[
            'role', 'experience', 'location',
            'skills_count', 'remote', 'salary'
        ]
    )

    role_encoder     = LabelEncoder()
    location_encoder = LabelEncoder()

    df['role_enc']     = role_encoder.fit_transform(df['role'])
    df['location_enc'] = location_encoder.fit_transform(df['location'])
    df['remote_enc']   = df['remote'].astype(int)

    X = df[['role_enc', 'experience', 'location_enc',
             'skills_count', 'remote_enc']]
    y = df['salary']

    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
    model.fit(X, y)

    return model, role_encoder, location_encoder


def predict_salary(role, experience, location,
                   skills, remote=False):

    model, role_enc, loc_enc = train_salary_model()

    known_roles = [
        "Python Developer", "Data Analyst",
        "ML Engineer", "Data Scientist",
        "Web Developer", "Full Stack Developer",
        "DevOps Engineer", "AI Engineer"
    ]
    known_locs = [
        "Bangalore", "Mumbai", "Indore",
        "Chennai", "Hyderabad", "Delhi", "Pune"
    ]

    role_match = role if role in known_roles else "Python Developer"
    loc_match  = location if location in known_locs else "Bangalore"

    try:
        role_encoded = role_enc.transform([role_match])[0]
        loc_encoded  = loc_enc.transform([loc_match])[0]
    except:
        role_encoded = 0
        loc_encoded  = 0

    features = np.array([[
        role_encoded, experience,
        loc_encoded, len(skills), int(remote)
    ]])

    base_salary = model.predict(features)[0]

    # ── Skill bonus: tiny & capped at 1.0 LPA ─────────────
    skill_bonus     = 0
    skill_breakdown = {}

    for skill in skills:
        impact = SKILL_SALARY_IMPACT.get(skill.lower(), 0.1)
        skill_bonus += impact * 0.03   # very small per skill
        skill_breakdown[skill] = impact

    skill_bonus = min(skill_bonus, 1.0)  # max 1 LPA from skills

    # ── Location multiplier ────────────────────────────────
    loc_multiplier  = LOCATION_MULTIPLIER.get(loc_match, 0.75)
    adjusted_salary = (base_salary * loc_multiplier) + skill_bonus

    # ── Hard caps by experience (strict) ──────────────────
    exp_caps = {
        0: 5.0,   # fresher max 5 LPA
        1: 7.5,   # 1 yr max 7.5 LPA
        2: 11.0,  # 2 yr max 11 LPA
        3: 14.0,  # 3 yr max 14 LPA
    }
    cap = exp_caps.get(experience, 20.0)
    adjusted_salary = min(adjusted_salary, cap)

    final_salary = round(adjusted_salary, 1)

    # Tight range ±8%
    salary_min = round(final_salary * 0.92, 1)
    salary_max = round(final_salary * 1.08, 1)

    return {
        "predicted":       final_salary,
        "salary_min":      salary_min,
        "salary_max":      salary_max,
        "base_salary":     round(base_salary, 1),
        "skill_bonus":     round(skill_bonus, 1),
        "skill_breakdown": dict(
            sorted(
                skill_breakdown.items(),
                key=lambda x: x[1],
                reverse=True
            )[:8]
        ),
        "market_position": get_market_position(
            final_salary, role_match
        )
    }


def get_market_position(salary, role):
    benchmarks = {
        "Python Developer":     {"low": 2.5, "mid": 5,  "high": 10},
        "Data Analyst":         {"low": 2.0, "mid": 4.5,"high": 9},
        "ML Engineer":          {"low": 4.0, "mid": 8,  "high": 14},
        "Data Scientist":       {"low": 4.5, "mid": 9,  "high": 16},
        "Web Developer":        {"low": 2.0, "mid": 4,  "high": 8},
        "Full Stack Developer": {"low": 3.0, "mid": 6.5,"high": 12},
        "DevOps Engineer":      {"low": 3.5, "mid": 8,  "high": 14},
        "AI Engineer":          {"low": 5.0, "mid": 10, "high": 18},
    }

    bench = benchmarks.get(
        role, {"low": 2.5, "mid": 6, "high": 12}
    )

    if salary >= bench["high"]:
        return "Top 10% — Expert Level"
    elif salary >= bench["mid"]:
        return "Top 30% — Above Average"
    elif salary >= bench["low"]:
        return "Average Market Rate"
    else:
        return "Below Average — Focus on Skills"


def get_skill_recommendations(current_skills, role):
    role_skills = {
        "Python Developer":     ["fastapi", "docker", "aws", "machine learning"],
        "Data Analyst":         ["machine learning", "python", "sql", "spark"],
        "ML Engineer":          ["deep learning", "tensorflow", "aws", "kubernetes"],
        "Data Scientist":       ["deep learning", "spark", "aws", "langchain"],
        "Web Developer":        ["react", "nodejs", "docker", "aws"],
        "Full Stack Developer": ["docker", "kubernetes", "aws", "react"],
        "DevOps Engineer":      ["kubernetes", "aws", "kafka", "docker"],
        "AI Engineer":          ["langchain", "pytorch", "kubernetes", "aws"],
    }

    recommended   = role_skills.get(role, ["docker", "aws", "machine learning"])
    current_lower = [s.lower() for s in current_skills]
    missing       = [s for s in recommended if s not in current_lower]

    result = []
    for skill in missing[:5]:
        impact = SKILL_SALARY_IMPACT.get(skill, 0.3)
        result.append({
            "skill":  skill,
            "impact": impact,
            "bonus":  f"+{round(impact * 0.03, 2)} LPA"
        })

    return result
