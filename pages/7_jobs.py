import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.job_fetcher import (
    fetch_live_jobs,
    calculate_job_match,
    filter_jobs
)

st.set_page_config(
    page_title="Live Jobs",
    page_icon="💼",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg,
            #0f0c29, #302b63, #24243e);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ── Main content text white (sidebar excluded) ── */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {
        color: #ffffff !important;
    }
    [data-testid="stMain"] .stMarkdown h1,
    [data-testid="stMain"] .stMarkdown h2,
    [data-testid="stMain"] .stMarkdown h3,
    [data-testid="stMain"] .stMarkdown h4,
    [data-testid="stMain"] .stMarkdown p {
        color: #ffffff !important;
    }
    [data-testid="stMain"] label,
    [data-testid="stMain"] div[data-testid="stWidgetLabel"] p,
    [data-testid="stMain"] div[data-testid="stWidgetLabel"] label {
        color: #ffffff !important;
    }
    [data-testid="stMain"] p,
    [data-testid="stMain"] span {
        color: #ffffff;
    }
    hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg,
            #34d399, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .job-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 8px;
    }
    .company-name {
        color: #a78bfa;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .job-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .job-meta {
        color: #ffffff;
        font-size: 0.82rem;
        margin-bottom: 12px;
        line-height: 1.8;
    }
    .match-high {
        background: rgba(52,211,153,0.15);
        border: 1px solid rgba(52,211,153,0.3);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .match-mid {
        background: rgba(251,191,36,0.15);
        border: 1px solid rgba(251,191,36,0.3);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .match-low {
        background: rgba(248,113,113,0.15);
        border: 1px solid rgba(248,113,113,0.3);
        color: #f87171;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .search-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
    }

    /* ── Input fields: dark text so it's visible ── */
    .stTextInput input {
        background: rgba(255,255,255,0.9) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #1a1a2e !important;
    }
    .stTextInput input::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }

    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        color: #ffffff !important;
    }
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown(
    '<div class="page-title">Live Job Search</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="page-sub">Search real jobs from LinkedIn, Indeed and Glassdoor with AI match scoring</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ── RESUME STATUS ─────────────────────────────────────────
resume_skills = st.session_state.get('resume_skills', [])

if resume_skills:
    st.markdown(f"""
    <div style='background:rgba(52,211,153,0.1);
    border:1px solid rgba(52,211,153,0.3);
    border-radius:12px; padding:14px 20px;
    color:#34d399; font-weight:600;
    margin-bottom:20px;'>
        Resume loaded with {len(resume_skills)} skills
        — AI will score each job for you!
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='background:rgba(251,191,36,0.1);
    border:1px solid rgba(251,191,36,0.3);
    border-radius:12px; padding:14px 20px;
    color:#fbbf24; font-weight:600;
    margin-bottom:20px;'>
        Upload resume first for AI match scoring.
        You can still search jobs without it.
    </div>
    """, unsafe_allow_html=True)

# ── SEARCH BOX ────────────────────────────────────────────
st.markdown('<div class="search-box">', unsafe_allow_html=True)
st.markdown("""
<div style='color:#a78bfa; font-size:0.8rem;
font-weight:700; letter-spacing:0.12em;
text-transform:uppercase; margin-bottom:16px;'>
    Search Jobs
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    job_title = st.text_input(
        "Job Title",
        placeholder="e.g. Python Developer, Data Analyst...",
        value="Python Developer",
        label_visibility="collapsed"
    )
with col2:
    location = st.text_input(
        "Location",
        placeholder="e.g. Bangalore, Indore...",
        value="India",
        label_visibility="collapsed"
    )
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button(
        "Search Jobs",
        type="primary",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────
with st.expander("Filters"):
    col1, col2, col3 = st.columns(3)
    with col1:
        min_match = st.slider(
            "Minimum Match Score",
            0, 100, 0, 5
        )
    with col2:
        remote_only = st.checkbox("Remote Only")
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Match Score", "Latest First",
             "Company Name"]
        )

# ── SEARCH ────────────────────────────────────────────────
if search_btn:
    with st.spinner("Searching for jobs..."):
        jobs = fetch_live_jobs(job_title, location)

    if jobs:
        for job in jobs:
            job['match_score'] = calculate_job_match(
                job['description'],
                resume_skills
            )

        filtered = filter_jobs(
            jobs,
            min_match=min_match,
            remote_only=remote_only
        )

        if sort_by == "Match Score":
            filtered.sort(
                key=lambda x: x['match_score'],
                reverse=True
            )
        elif sort_by == "Latest First":
            filtered.sort(
                key=lambda x: x['posted_on'],
                reverse=True
            )
        elif sort_by == "Company Name":
            filtered.sort(key=lambda x: x['company'])

        st.session_state['search_results'] = filtered
        st.session_state['search_query']   = job_title

        avg_match  = int(
            sum(j['match_score'] for j in filtered) /
            len(filtered)
        ) if filtered else 0
        high_match = len([
            j for j in filtered
            if j['match_score'] >= 70
        ])

        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div style='font-size:1.6rem;
                font-weight:800; color:#a78bfa;'>
                    {len(filtered)}
                </div>
                <div style='color:#ffffff;
                font-size:0.82rem; margin-top:4px;'>
                    Jobs Found
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div style='font-size:1.6rem;
                font-weight:800; color:#60a5fa;'>
                    {avg_match}%
                </div>
                <div style='color:#ffffff;
                font-size:0.82rem; margin-top:4px;'>
                    Avg Match
                </div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div style='font-size:1.6rem;
                font-weight:800; color:#34d399;'>
                    {high_match}
                </div>
                <div style='color:#ffffff;
                font-size:0.82rem; margin-top:4px;'>
                    Strong Matches
                </div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div style='font-size:1.3rem;
                font-weight:800; color:#fbbf24;'>
                    {location}
                </div>
                <div style='color:#ffffff;
                font-size:0.82rem; margin-top:4px;'>
                    Location
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.warning("No jobs found! Try different keywords.")

# ── DISPLAY JOBS ──────────────────────────────────────────
if 'search_results' in st.session_state:
    results = st.session_state['search_results']
    query   = st.session_state.get('search_query', '')

    st.markdown(f"""
    <div style='color:#ffffff; font-size:0.85rem;
    margin-bottom:20px;'>
        Showing {len(results)} jobs for {query}
    </div>
    """, unsafe_allow_html=True)

    for i, job in enumerate(results):
        score = job.get('match_score', 0)

        # Clean values
        company  = str(job.get('company',   'Company'))
        title    = str(job.get('title',     'Job Title'))
        loc      = str(job.get('location',  'India'))
        jtype    = str(job.get('job_type',  'Full Time'))
        posted   = str(job.get('posted_on', 'Recently'))
        source   = str(job.get('source',    'Job Board'))
        applyurl = str(job.get('apply_link',''))
        desc     = str(job.get('description',''))

        # Match label
        if score >= 70:
            match_class = "match-high"
            match_label = "Strong Match"
        elif score >= 40:
            match_class = "match-mid"
            match_label = "Good Match"
        else:
            match_class = "match-low"
            match_label = "Low Match"

        # ── JOB CARD ──────────────────────────────────────
        st.markdown(f"""
        <div class="job-card">
            <div class="company-name">{company}</div>
            <div class="job-title">{title}</div>
            <div class="job-meta">
                Location: {loc} &nbsp;|&nbsp;
                Type: {jtype} &nbsp;|&nbsp;
                Posted: {posted} &nbsp;|&nbsp;
                Via: {source}
            </div>
            <span class="{match_class}">
                {score}% {match_label}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── EXTRA TAGS ROW ────────────────────────────────
        tag1, tag2, tag3, spacer = st.columns(
            [1, 1, 1, 3]
        )

        with tag1:
            st.markdown(f"""
            <div style='background:rgba(167,139,250,0.12);
            border:1px solid rgba(167,139,250,0.3);
            color:#a78bfa; padding:6px 14px;
            border-radius:20px; font-size:0.78rem;
            font-weight:600; text-align:center;'>
                via {source}
            </div>
            """, unsafe_allow_html=True)

        with tag2:
            if job.get('salary_min') and job.get('salary_max'):
                st.markdown(f"""
                <div style='background:rgba(52,211,153,0.12);
                border:1px solid rgba(52,211,153,0.3);
                color:#34d399; padding:6px 14px;
                border-radius:20px; font-size:0.78rem;
                font-weight:600; text-align:center;'>
                    {job['salary_min']} - {job['salary_max']}
                </div>
                """, unsafe_allow_html=True)
            elif job.get('remote'):
                st.markdown("""
                <div style='background:rgba(96,165,250,0.12);
                border:1px solid rgba(96,165,250,0.3);
                color:#60a5fa; padding:6px 14px;
                border-radius:20px; font-size:0.78rem;
                font-weight:600; text-align:center;'>
                    Remote
                </div>
                """, unsafe_allow_html=True)

        # ── DESCRIPTION ───────────────────────────────────
        if desc:
            with st.expander("View Job Description"):
                st.markdown(f"""
                <div style='color:#ffffff;
                font-size:0.88rem; line-height:1.7;
                background:rgba(0,0,0,0.2);
                padding:16px; border-radius:10px;'>
                    {desc[:600]}...
                </div>
                """, unsafe_allow_html=True)

        # ── BUTTONS ───────────────────────────────────────
        btn1, btn2, spacer2 = st.columns([1, 1, 3])

        with btn1:
            if applyurl:
                st.markdown(f"""
                <a href="{applyurl}" target="_blank"
                style='display:block; text-align:center;
                background:linear-gradient(
                    90deg,#7c3aed,#2563eb);
                color:white; padding:10px 20px;
                border-radius:10px; font-size:0.85rem;
                font-weight:600; text-decoration:none;'>
                    Apply Now
                </a>
                """, unsafe_allow_html=True)

        with btn2:
            btn_key = f"save_{i}_{company[:10]}"
            if st.button(
                "Save to Tracker",
                key=btn_key
            ):
                st.session_state['prefill_company'] = company
                st.session_state['prefill_title']   = title
                st.session_state['prefill_link']    = applyurl
                st.success("Saved! Go to Job Tracker!")

        # Divider
        st.markdown(
            "<hr class='divider'>",
            unsafe_allow_html=True
        )

# ── EMPTY STATE ───────────────────────────────────────────
if 'search_results' not in st.session_state \
        and not search_btn:

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    tips = [
        ("Search Any Role",
         "Enter any job title like Python Developer"),
        ("AI Match Score",
         "Each job gets a score based on your resume"),
        ("Save to Tracker",
         "One click to save jobs to your tracker"),
    ]

    for col, (tip_title, tip_desc) in zip(
        [col1, col2, col3], tips
    ):
        with col:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.07);
            border-radius:16px; padding:24px;
            text-align:center;'>
                <div style='color:#ffffff;
                font-weight:700; margin-bottom:8px;
                font-size:1rem;'>
                    {tip_title}
                </div>
                <div style='color:#ffffff;
                font-size:0.85rem; line-height:1.6;'>
                    {tip_desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#ffffff;
font-size:0.8rem;'>
    AI Career Copilot - Live Job Search
    powered by JSearch API
</div>
""", unsafe_allow_html=True)