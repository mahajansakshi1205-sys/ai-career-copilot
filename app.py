import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(167,139,250,0.2);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] a span {
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stSidebarNav"] a:hover span {
        color: #a78bfa !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #a78bfa !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 10px;
    }

    /* Hero */
    .hero-badge {
        display: inline-block;
        background: rgba(167,139,250,0.15);
        border: 1px solid rgba(167,139,250,0.3);
        color: #a78bfa;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 900;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin-bottom: 16px;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #9ca3af;
        line-height: 1.7;
        max-width: 600px;
        margin-bottom: 32px;
    }

    /* Stats */
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .stat-num {
        font-size: 2.2rem;
        font-weight: 800;
    }
    .stat-lbl {
        color: #9ca3af;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 28px 22px;
        text-align: center;
        height: 100%;
        transition: all 0.3s;
    }
    .feature-card:hover {
        background: rgba(167,139,250,0.08);
        border-color: rgba(167,139,250,0.3);
        transform: translateY(-4px);
    }
    .feature-emoji {
        font-size: 2.8rem;
        margin-bottom: 14px;
    }
    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #6b7280;
        line-height: 1.6;
    }

    /* Steps */
    .step-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }

    /* Tech badges */
    .tech-badge {
        display: inline-block;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: #9ca3af;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
        font-weight: 500;
    }

    /* CTA */
    .cta-box {
        background: linear-gradient(135deg, #7c3aed, #2563eb, #0891b2);
        border-radius: 24px;
        padding: 48px 40px;
        text-align: center;
        margin: 32px 0;
    }

    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #e2e8f0;
        margin-bottom: 8px;
    }
    .section-sub {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 28px;
    }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <div style='font-size:2.5rem;'>🤖</div>
        <div style='font-size:1.1rem; font-weight:800;
        color:#ffffff; margin-top:8px;'>
            AI Career Copilot
        </div>
        <div style='font-size:0.75rem; color:#9ca3af;
        margin-top:4px;'>Your AI Career Advisor</div>
    </div>
    <hr style='border:none; border-top:1px solid
    rgba(255,255,255,0.08); margin:0 0 20px;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='color:#a78bfa; font-size:0.75rem;
    font-weight:700; letter-spacing:0.12em;
    text-transform:uppercase; margin-bottom:12px;
    padding:0 8px;'>
        Navigation
    </div>
    """, unsafe_allow_html=True)

    # Progress indicators
    resume_done  = '✅' if 'resume_skills'  in st.session_state else '⭕'
    gap_done     = '✅' if 'missing_skills' in st.session_state else '⭕'
    cover_done   = '✅' if 'cover_letter'   in st.session_state else '⭕'
    roadmap_done = '✅' if 'roadmap_weeks'  in st.session_state else '⭕'

    st.markdown(f"""
    <div style='padding:0 8px;'>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            {resume_done} 📄 Resume Analyzer
        </div>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            {gap_done} 🔍 Skill Gap Analysis
        </div>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            {roadmap_done} 🗺️ Learning Roadmap
        </div>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            {cover_done} ✉️ Cover Letter
        </div>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            ⭕ 🎤 Interview Prep
        </div>
        <div style='padding:10px 12px; border-radius:10px;
        color:#ffffff; font-size:0.875rem; margin-bottom:4px;
        background:rgba(255,255,255,0.03);'>
            ⭕ 📊 Job Tracker
        </div>
    </div>
    <hr style='border:none; border-top:1px solid
    rgba(255,255,255,0.08); margin:20px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='color:#a78bfa; font-size:0.75rem;
    font-weight:700; letter-spacing:0.12em;
    text-transform:uppercase; margin-bottom:12px;
    padding:0 8px;'>
        How to Use
    </div>
    <div style='padding:0 8px; color:#ffffff;
    font-size:0.82rem; line-height:2;'>
        1️⃣ Upload Resume<br>
        2️⃣ Paste Job Description<br>
        3️⃣ Run Skill Gap Analysis<br>
        4️⃣ Get Learning Roadmap<br>
        5️⃣ Generate Cover Letter<br>
        6️⃣ Practice Interviews<br>
        7️⃣ Track Applications
    </div>
    """, unsafe_allow_html=True)

# ── HERO SECTION ──────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="hero-badge">🚀 AI Powered Career Tool</div>
    <div class="hero-title">
        Land Your<br>Dream Job<br>with AI
    </div>
    <div class="hero-sub">
        Upload your resume, paste any job description —
        AI analyzes your skills, fills the gaps,
        writes your cover letter, and preps you
        for interviews. All in one place.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:rgba(255,255,255,0.03);
    border:1px solid rgba(167,139,250,0.2);
    border-radius:24px; padding:32px; margin-top:20px;'>
        <div style='font-size:0.8rem; color:#a78bfa;
        font-weight:700; letter-spacing:0.1em;
        text-transform:uppercase; margin-bottom:20px;'>
            ✨ What AI Does For You
        </div>
        <div style='color:#ffffff; font-size:0.9rem;
        line-height:2.2;'>
            📄 Reads & analyzes your resume<br>
            🔍 Finds your skill gaps instantly<br>
            🗺️ Builds personalized study plan<br>
            ✉️ Writes tailored cover letters<br>
            🎤 Generates interview questions<br>
            📊 Tracks all job applications
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── STATS ROW ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

stats_data = [
    ("7",     "AI Features",    "#a78bfa"),
    ("100%",  "Personalized",   "#60a5fa"),
    ("24/7",  "Available",      "#34d399"),
    ("⚡",    "Instant Results","#fbbf24"),
]
for col, (num, label, color) in zip(
    [col1, col2, col3, col4], stats_data
):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num" style="color:{color};">
                {num}
            </div>
            <div class="stat-lbl">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FEATURES GRID ─────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-bottom:32px;'>
    <div class="section-header">✨ Everything You Need</div>
    <div class="section-sub">
        7 powerful AI features to help you get hired faster
    </div>
</div>
""", unsafe_allow_html=True)

features = [
    ("📄", "Resume Analyzer",
     "Upload PDF resume — AI extracts all your skills automatically",
     "#a78bfa"),
    ("🔍", "Skill Gap Analysis",
     "Compare your skills vs job requirements with match score",
     "#60a5fa"),
    ("🗺️", "Learning Roadmap",
     "Week by week personalized study plan for missing skills",
     "#34d399"),
    ("✉️", "Cover Letter",
     "AI writes a tailored professional cover letter in seconds",
     "#fbbf24"),
    ("🎤", "Interview Prep",
     "Practice with role-specific questions and get AI feedback",
     "#f472b6"),
    ("📊", "Job Tracker",
     "Track all applications with status and visual dashboard",
     "#fb923c"),
]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
for i, (emoji, title, desc, color) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card"
        style="border-top: 3px solid {color};">
            <div class="feature-emoji">{emoji}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        <br>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── HOW IT WORKS ──────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-bottom:32px;'>
    <div class="section-header">🚀 How It Works</div>
    <div class="section-sub">4 simple steps to your dream job</div>
</div>
""", unsafe_allow_html=True)

steps = [
    ("1", "📤", "Upload Resume",
     "Upload your PDF resume and AI reads all your skills"),
    ("2", "📋", "Paste Job Description",
     "Copy any job posting and paste it into the app"),
    ("3", "🤖", "AI Analyzes Everything",
     "AI finds gaps, writes cover letter and builds study plan"),
    ("4", "🎯", "Land the Job",
     "Practice interviews, track applications and get hired!"),
]

cols = st.columns(4)
for col, (num, emoji, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div class="step-card">
            <div style='width:40px; height:40px;
            border-radius:50%;
            background:linear-gradient(135deg,#7c3aed,#2563eb);
            display:flex; align-items:center;
            justify-content:center;
            margin:0 auto 12px;
            font-weight:800; font-size:1.1rem;
            color:white;'>{num}</div>
            <div style='font-size:1.8rem;
            margin-bottom:10px;'>{emoji}</div>
            <div style='font-weight:700; color:#ffffff;
            margin-bottom:8px; font-size:0.95rem;'>
                {title}
            </div>
            <div style='color:#6b7280; font-size:0.82rem;
            line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── TECH STACK ────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <div class="section-header">🛠️ Built With</div>
    <div class="section-sub">
        Modern AI and Python technologies
    </div>
</div>
""", unsafe_allow_html=True)

techs = [
    "🐍 Python",   "⚡ Streamlit", "🧠 LangChain",
    "🤖 OpenAI",   "🐼 Pandas",    "🔢 NumPy",
    "📊 Plotly",   "🗄️ SQLite",    "📄 PyPDF2",
    "🔐 FastAPI"
]
tech_html = "".join([
    f'<span class="tech-badge">{t}</span>' for t in techs
])
st.markdown(
    f'<div style="text-align:center;">{tech_html}</div>',
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CTA BANNER ────────────────────────────────────────────
st.markdown("""
<div class="cta-box">
    <div style='font-size:2rem; font-weight:900;
    color:white; margin-bottom:12px;'>
        🎯 Ready to Get Started?
    </div>
    <div style='color:rgba(255,255,255,0.85);
    font-size:1rem; margin-bottom:24px; line-height:1.7;'>
        Click on <b>📄 1 resume</b> in the sidebar
        to upload your resume and begin your journey!
    </div>
    <div style='background:rgba(255,255,255,0.15);
    border:1px solid rgba(255,255,255,0.3);
    border-radius:12px; padding:12px 24px;
    display:inline-block; color:white;
    font-weight:700; font-size:0.9rem;'>
        ← Click Resume in Sidebar to Start 🚀
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px 0;'>
    <div style='font-size:1.5rem; margin-bottom:8px;'>🤖</div>
    <div style='color:#6b7280; font-size:0.85rem;'>
        AI Career Copilot — Built with ❤️ using
        Python · Streamlit · LangChain · OpenAI
    </div>
    <div style='color:#374151; font-size:0.75rem;
    margin-top:6px;'>
        Your personal AI career advisor — available 24/7
    </div>
</div>
""", unsafe_allow_html=True)