import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.llm_helper import generate_learning_roadmap

st.set_page_config(
    page_title="Learning Roadmap",
    page_icon="🗺️",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #fbbf24, #f472b6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .week-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .week-number {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .week-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #e2e8f0;
        margin-bottom: 16px;
    }
    .skill-tag {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px;
    }
    .task-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #d1d5db;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .resource-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #60a5fa;
        font-size: 0.85rem;
        padding: 5px 0;
    }
    .outcome-box {
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 16px;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .warning-box {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #fbbf24;
    }
    .goal-box {
        background: linear-gradient(135deg,
            rgba(167,139,250,0.15),
            rgba(96,165,250,0.15));
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 28px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">🗺️ Learning Roadmap</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Your personalized week by week study plan to land your dream job</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHECK SESSION ─────────────────────────────────────────
if 'missing_skills' not in st.session_state:
    st.markdown("""
    <div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem; font-weight:700; margin:8px 0'>
            Skill Analysis Not Done Yet!
        </div>
        <div style='font-size:0.9rem; opacity:0.8'>
            Please go to Skill Gap Analysis page first
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

missing_skills = st.session_state['missing_skills']
job_desc = st.session_state.get('job_description', '')

# ── SETTINGS ROW ──────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
    <div style='background:rgba(52,211,153,0.1);
    border:1px solid rgba(52,211,153,0.3);
    border-radius:12px; padding:16px 20px;
    color:#34d399; font-weight:600;'>
        ✅ {len(missing_skills)} missing skills detected — Ready to build your roadmap!
    </div>
    """, unsafe_allow_html=True)

with col2:
    level = st.selectbox(
        "Your Current Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=0
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button(
        "🚀 Generate Roadmap",
        type="primary",
        use_container_width=True
    )

# ── MISSING SKILLS PREVIEW ────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### <span style='color:white'>🎯 Skills You Need to Learn:</span>", unsafe_allow_html=True)
skills_html = "".join([
    f"""<span style='display:inline-block;
    background:rgba(248,113,113,0.15);
    border:1px solid rgba(248,113,113,0.3);
    color:#f87171; padding:6px 14px;
    border-radius:20px; font-size:0.85rem;
    margin:4px; font-weight:500;'>❌ {s}</span>"""
    for s in missing_skills
])
st.markdown(skills_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── GENERATE ROADMAP ──────────────────────────────────────
if generate:
    with st.spinner("🤖 AI is building your personalized roadmap..."):
        result = generate_learning_roadmap(
            missing_skills,
            job_desc,
            level
        )

    # ── PARSE RESULT ──────────────────────────────────────
    lines = result.strip().split('\n')
    total_weeks = 0
    goal = ""
    weeks = []
    current_week = None

    week_colors = [
        "#a78bfa", "#60a5fa", "#34d399",
        "#fbbf24", "#f472b6", "#fb923c"
    ]

    for line in lines:
        line = line.strip()
        if line.startswith("TOTAL_WEEKS:"):
            try:
                total_weeks = int(line.replace("TOTAL_WEEKS:", "").strip())
            except:
                total_weeks = 0
        elif line.startswith("GOAL:"):
            goal = line.replace("GOAL:", "").strip()
        elif line.startswith("WEEK_") and line.endswith(":"):
            if current_week:
                weeks.append(current_week)
            week_num = line.replace("WEEK_", "").replace(":", "").strip()
            current_week = {
                "number": week_num,
                "title": "",
                "skills": [],
                "tasks": [],
                "resources": [],
                "outcome": ""
            }
        elif current_week:
            if line.startswith("TITLE:"):
                current_week["title"] = line.replace("TITLE:", "").strip()
            elif line.startswith("SKILLS:"):
                skills_text = line.replace("SKILLS:", "").strip()
                current_week["skills"] = [s.strip() for s in skills_text.split(',')]
            elif line.startswith("TASKS:"):
                tasks_text = line.replace("TASKS:", "").strip()
                current_week["tasks"] = [t.strip() for t in tasks_text.split('|')]
            elif line.startswith("RESOURCES:"):
                res_text = line.replace("RESOURCES:", "").strip()
                current_week["resources"] = [r.strip() for r in res_text.split('|')]
            elif line.startswith("OUTCOME:"):
                current_week["outcome"] = line.replace("OUTCOME:", "").strip()

    if current_week:
        weeks.append(current_week)

    st.session_state['roadmap_weeks'] = weeks
    st.session_state['roadmap_goal'] = goal
    st.session_state['roadmap_total'] = total_weeks

# ── DISPLAY ROADMAP ───────────────────────────────────────
if 'roadmap_weeks' in st.session_state:
    weeks = st.session_state['roadmap_weeks']
    goal = st.session_state.get('roadmap_goal', '')
    total_weeks = st.session_state.get('roadmap_total', len(weeks))

    week_colors = [
        "#a78bfa", "#60a5fa", "#34d399",
        "#fbbf24", "#f472b6", "#fb923c"
    ]

    # Goal banner
    if goal:
      st.markdown(f"""
    <div class="goal-box">
        <div style='color:#a78bfa; font-size:0.8rem;
        font-weight:700; letter-spacing:0.15em;
        text-transform:uppercase; margin-bottom:8px;'>
            🎯 Your Goal
        </div>
        <div style='color:#e2e8f0; font-size:1.1rem;
        font-weight:600; line-height:1.6;'>{goal}</div>
    </div>
    """, unsafe_allow_html=True)