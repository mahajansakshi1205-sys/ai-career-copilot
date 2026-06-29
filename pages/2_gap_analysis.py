import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.llm_helper import analyze_skill_gap

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg,
            #0f0c29, #302b63, #24243e);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg,
            #f87171, #fb923c, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .stat-num {
        font-size: 2.2rem;
        font-weight: 800;
    }
    .stat-lbl {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-top: 6px;
    }
    .have-skill {
        display: inline-block;
        background: rgba(52,211,153,0.15);
        border: 1px solid rgba(52,211,153,0.4);
        color: #34d399;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        font-weight: 500;
    }
    .miss-skill {
        display: inline-block;
        background: rgba(248,113,113,0.15);
        border: 1px solid rgba(248,113,113,0.4);
        color: #f87171;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        font-weight: 500;
    }
    .skills-section {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 16px;
    }
    .salary-card {
        background: rgba(52,211,153,0.08);
        border: 1px solid rgba(52,211,153,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .demand-high {
        background: rgba(52,211,153,0.15);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .demand-medium {
        background: rgba(251,191,36,0.15);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .demand-low {
        background: rgba(248,113,113,0.15);
        color: #f87171;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .priority-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(167,139,250,0.2);
        border-left: 4px solid #a78bfa;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .summary-box {
        background: linear-gradient(135deg,
            rgba(167,139,250,0.1),
            rgba(96,165,250,0.1));
        border: 1px solid rgba(167,139,250,0.3);
        border-left: 4px solid #a78bfa;
        border-radius: 12px;
        padding: 20px 24px;
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.7;
        margin-top: 20px;
    }
    .warning-box {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #fbbf24;
    }
    .progress-bar-bg {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 14px;
        margin: 10px 0 20px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🔍 Skill Gap Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">AI analyzes your skills vs job requirements with salary impact & market demand</div>', unsafe_allow_html=True)
st.markdown("---")

if 'resume_skills' not in st.session_state:
    st.markdown("""<div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem;font-weight:700;margin:8px 0'>Resume Not Found!</div>
        <div style='font-size:0.9rem;opacity:0.8'>Please upload your resume first</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

if 'job_description' not in st.session_state:
    st.markdown("""<div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem;font-weight:700;margin:8px 0'>Job Description Not Found!</div>
        <div style='font-size:0.9rem;opacity:0.8'>Please paste a job description on Resume page</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

resume_skills = st.session_state['resume_skills']
job_desc      = st.session_state['job_description']

st.markdown(f"""
<div style='background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);
border-radius:12px;padding:16px 20px;color:#34d399;font-weight:600;margin-bottom:20px;'>
    ✅ Resume loaded — {len(resume_skills)} skills found &nbsp;|&nbsp; 📋 Job description ready
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze = st.button("🚀 Analyze My Skill Gap", type="primary", use_container_width=True)

if analyze:
    with st.spinner("🤖 AI is analyzing your profile..."):
        result = analyze_skill_gap(resume_skills, job_desc)

    lines      = result.strip().split('\n')
    matching   = []
    missing    = []
    percentage = 0
    summary    = ""
    salary_impact   = {}
    market_demand   = {}
    priority_skills = []

    section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "MATCHING SKILLS:" in line:
            text = line.replace("MATCHING SKILLS:", "").strip()
            matching = [s.strip() for s in text.split(',') if s.strip()]
        elif "MISSING SKILLS:" in line:
            text = line.replace("MISSING SKILLS:", "").strip()
            missing = [s.strip() for s in text.split(',') if s.strip()]
        elif "MATCH PERCENTAGE:" in line:
            try:
                percentage = int(line.replace("MATCH PERCENTAGE:", "").strip())
            except:
                percentage = 0
        elif "SUMMARY:" in line:
            summary = line.replace("SUMMARY:", "").strip()
        elif "SALARY_IMPACT:" in line:
            section = "salary"
        elif "MARKET_DEMAND:" in line:
            section = "demand"
        elif "PRIORITY_TO_LEARN:" in line:
            section = "priority"
        elif section == "salary" and ":" in line and "MARKET" not in line:
            parts = line.split(":")
            if len(parts) == 2:
                salary_impact[parts[0].strip()] = parts[1].strip()
        elif section == "demand" and ":" in line and "PRIORITY" not in line:
            parts = line.split(":")
            if len(parts) == 2:
                market_demand[parts[0].strip()] = parts[1].strip()
        elif section == "priority" and line and line[0].isdigit():
            priority_skills.append(line)

    st.markdown("---")

    # ── SCORE SECTION ─────────────────────────────────────
    st.markdown("<h3 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>📊 Your Match Score</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if percentage >= 70:
        score_color = "#34d399"; score_emoji = "🟢"; score_label = "Strong Match!"
    elif percentage >= 40:
        score_color = "#fbbf24"; score_emoji = "🟡"; score_label = "Moderate Match"
    else:
        score_color = "#f87171"; score_emoji = "🔴"; score_label = "Needs Work"

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        (f"{percentage}%", f"{score_emoji} {score_label}", score_color),
        (len(matching),    "✅ Skills You Have",           "#34d399"),
        (len(missing),     "❌ Skills Missing",            "#f87171"),
        (len(matching)+len(missing), "📋 Total Required", "#60a5fa"),
    ]
    for col, (num, lbl, color) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-num" style="color:{color};">{num}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='color:#9ca3af;font-size:0.9rem;margin:20px 0 6px;'>Match Progress — {percentage}%</div>
    <div class="progress-bar-bg">
        <div style='height:100%;width:{percentage}%;
        background:linear-gradient(90deg,{score_color},#60a5fa);border-radius:10px;'></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=['Skills You Have ✅', 'Skills Missing ❌'],
            values=[len(matching) or 1, len(missing) or 1],
            hole=0.55, marker_colors=['#34d399', '#f87171'],
            textinfo='label+percent', textfont_size=12)])
        fig.update_layout(title=dict(text="Skills Breakdown", font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False,
            height=300, margin=dict(t=50, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if salary_impact:
            skills_list  = list(salary_impact.keys())[:6]
            impacts_list = []
            for v in list(salary_impact.values())[:6]:
                try:
                    num = float(v.replace("+","").replace("LPA","").strip())
                    impacts_list.append(num)
                except:
                    impacts_list.append(1.0)
            fig2 = go.Figure(data=[go.Bar(
                x=impacts_list, y=skills_list, orientation='h',
                marker_color='#34d399',
                text=[f"+{v}" for v in impacts_list],
                textposition='outside', textfont=dict(color='white'))])
            fig2.update_layout(
                title=dict(text="💰 Salary Impact by Skill (LPA)", font=dict(color='white', size=15)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='white', height=300,
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SKILLS COLUMNS ────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="skills-section">
            <div class="section-title" style="color:#34d399;">✅ Skills You Already Have</div>""",
            unsafe_allow_html=True)
        if matching:
            st.markdown("".join([f'<span class="have-skill">✅ {s}</span>' for s in matching]),
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="skills-section">
            <div class="section-title" style="color:#f87171;">❌ Skills You Need to Learn</div>""",
            unsafe_allow_html=True)
        if missing:
            st.markdown("".join([f'<span class="miss-skill">❌ {s}</span>' for s in missing]),
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SALARY IMPACT ─────────────────────────────────────
    if salary_impact:
        st.markdown("<h3 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>💰 Salary Impact of Missing Skills</h3>", unsafe_allow_html=True)
        st.markdown('<p style="color:#9ca3af;font-size:0.9rem;margin-bottom:16px;">Learn these skills to increase your salary</p>', unsafe_allow_html=True)
        for skill, impact in list(salary_impact.items())[:6]:
            demand = market_demand.get(skill, "Medium")
            if "High" in demand:
                demand_html = f'<span class="demand-high">🔥 {demand}</span>'
            elif "Medium" in demand:
                demand_html = f'<span class="demand-medium">⚡ {demand}</span>'
            else:
                demand_html = f'<span class="demand-low">📉 {demand}</span>'
            st.markdown(f"""<div class="salary-card">
                <div>
                    <div style='color:#e2e8f0;font-weight:600;font-size:0.95rem;'>{skill}</div>
                    <div style='margin-top:6px;'>{demand_html}</div>
                </div>
                <div style='color:#34d399;font-size:1.3rem;font-weight:800;'>{impact}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PRIORITY TO LEARN ─────────────────────────────────
    if priority_skills:
        st.markdown("<h3 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>🎯 Priority Skills to Learn First</h3>", unsafe_allow_html=True)
        st.markdown('<p style="color:#9ca3af;font-size:0.9rem;margin-bottom:16px;">AI recommends learning in this order</p>', unsafe_allow_html=True)
        for item in priority_skills:
            st.markdown(f"""<div class="priority-card">
                <div style='color:#e2e8f0;font-size:0.9rem;line-height:1.6;'>{item}</div>
            </div>""", unsafe_allow_html=True)

    # ── AI SUMMARY ────────────────────────────────────────
    if summary:
        st.markdown(f"""<div class="summary-box">
            <div style='color:#a78bfa;font-weight:700;font-size:0.9rem;margin-bottom:8px;'>🤖 AI Career Advisor Says:</div>
            {summary}
        </div>""", unsafe_allow_html=True)

    st.session_state['missing_skills']   = missing
    st.session_state['matching_skills']  = matching
    st.session_state['match_percentage'] = percentage
    st.session_state['salary_impact']    = salary_impact

    st.markdown("""<div style='background:linear-gradient(90deg,#7c3aed,#2563eb);
    border-radius:16px;padding:24px;text-align:center;margin-top:24px;color:white;'>
        <div style='font-size:1.3rem;font-weight:800;margin-bottom:8px;'>🎯 Analysis Complete!</div>
        <div style='opacity:0.85;font-size:0.9rem;'>
            Now go to <b>🗺️ Learning Roadmap</b> from sidebar to get your study plan →
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div style='text-align:center;color:#4b5563;font-size:0.8rem;'>
    🤖 AI Career Copilot — Skill Gap Analysis with Salary Intelligence
</div>""", unsafe_allow_html=True)