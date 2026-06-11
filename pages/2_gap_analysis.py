import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.llm_helper import analyze_skill_gap

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🔍", layout="wide")

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
        background: linear-gradient(90deg, #f87171, #fb923c, #fbbf24);
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
        height: 100%;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 16px;
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
    .next-step-box {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-top: 24px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">🔍 Skill Gap Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">See exactly what skills you have and what you need to learn</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHECK SESSION DATA ─────────────────────────────────────
if 'resume_skills' not in st.session_state:
    st.markdown("""
    <div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem; font-weight:700; margin:8px 0'>Resume Not Found!</div>
        <div style='font-size:0.9rem; opacity:0.8'>Please go to Resume page first and upload your resume</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if 'job_description' not in st.session_state:
    st.markdown("""
    <div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem; font-weight:700; margin:8px 0'>Job Description Not Found!</div>
        <div style='font-size:0.9rem; opacity:0.8'>Please go to Resume page and paste a job description first</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

resume_skills = st.session_state['resume_skills']
job_desc = st.session_state['job_description']

# ── READY STATE ───────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"""
    <div style='background:rgba(52,211,153,0.1); border:1px solid
    rgba(52,211,153,0.3); border-radius:12px; padding:16px 20px;
    color:#34d399; font-weight:600;'>
        ✅ Resume loaded — {len(resume_skills)} skills found &nbsp;|&nbsp;
        📋 Job description ready
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ANALYZE BUTTON ────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze = st.button(
        "🚀 Analyze My Skill Gap",
        type="primary",
        use_container_width=True
    )

# ── ANALYSIS RESULTS ──────────────────────────────────────
if analyze:
    with st.spinner("🤖 AI is analyzing your profile... Please wait"):
        result = analyze_skill_gap(resume_skills, job_desc)

    # Parse result
    lines = result.strip().split('\n')
    matching, missing, percentage, summary = [], [], 0, ""

    for line in lines:
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

    st.markdown("---")

    # ── SCORE SECTION ─────────────────────────────────────
    st.markdown("### 📊 Your Match Score")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # Score color
    if percentage >= 70:
        score_color = "#34d399"
        score_emoji = "🟢"
        score_label = "Strong Match!"
    elif percentage >= 40:
        score_color = "#fbbf24"
        score_emoji = "🟡"
        score_label = "Moderate Match"
    else:
        score_color = "#f87171"
        score_emoji = "🔴"
        score_label = "Needs Work"

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num" style="color:{score_color}">{percentage}%</div>
            <div class="stat-lbl">{score_emoji} {score_label}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num" style="color:#34d399">{len(matching)}</div>
            <div class="stat-lbl">✅ Skills You Have</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num" style="color:#f87171">{len(missing)}</div>
            <div class="stat-lbl">❌ Skills Missing</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        total = len(matching) + len(missing)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num" style="color:#60a5fa">{total}</div>
            <div class="stat-lbl">📋 Total Required</div>
        </div>""", unsafe_allow_html=True)

    # Progress bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color:#9ca3af; font-size:0.9rem; margin-bottom:6px;'>
        Match Progress — {percentage}%
    </div>
    <div class="progress-bar-bg">
        <div style='height:100%; width:{percentage}%;
        background: linear-gradient(90deg, {score_color}, #60a5fa);
        border-radius:10px; transition: width 1s ease;'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ROW ────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        # Donut chart
        fig = go.Figure(data=[go.Pie(
            labels=['Skills You Have ✅', 'Skills Missing ❌'],
            values=[len(matching) or 1, len(missing) or 1],
            hole=0.55,
            marker_colors=['#34d399', '#f87171'],
            textinfo='label+percent',
            textfont_size=12,
        )])
        fig.update_layout(
            title=dict(text="Skills Breakdown", font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart
        categories = ['Skills You Have', 'Skills Missing', 'Match Score']
        values = [len(matching), len(missing), percentage]
        colors = ['#34d399', '#f87171', '#a78bfa']

        fig2 = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='outside',
            textfont=dict(color='white', size=13),
        )])
        fig2.update_layout(
            title=dict(text="Skills Overview", font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(t=50, b=20, l=20, r=20),
            height=300,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SKILLS COLUMNS ────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="skills-section">
            <div class="section-title" style="color:#34d399">
                ✅ Skills You Already Have
            </div>
        """, unsafe_allow_html=True)
        if matching:
            html = "".join([f'<span class="have-skill">✅ {s}</span>' for s in matching])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9ca3af">No matching skills found</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="skills-section">
            <div class="section-title" style="color:#f87171">
                ❌ Skills You Need to Learn
            </div>
        """, unsafe_allow_html=True)
        if missing:
            html = "".join([f'<span class="miss-skill">❌ {s}</span>' for s in missing])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9ca3af">No missing skills! Perfect match 🎉</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── AI SUMMARY ────────────────────────────────────────
    if summary:
        st.markdown(f"""
        <div class="summary-box">
            <div style='color:#a78bfa; font-weight:700;
            font-size:0.9rem; margin-bottom:8px;'>
                🤖 AI Career Advisor Says:
            </div>
            {summary}
        </div>
        """, unsafe_allow_html=True)

    # Save to session
    st.session_state['missing_skills'] = missing
    st.session_state['matching_skills'] = matching
    st.session_state['match_percentage'] = percentage

    # ── NEXT STEP BANNER ──────────────────────────────────
    st.markdown("""
    <div class="next-step-box">
        <div style='font-size:1.5rem; font-weight:800; margin-bottom:8px;'>
            🎯 Analysis Complete!
        </div>
        <div style='opacity:0.85; font-size:0.95rem;'>
            Now go to <b>Learning Roadmap</b> from the sidebar
            to get your personalized study plan →
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    🤖 AI Career Copilot — Skill Gap Analysis
</div>
""", unsafe_allow_html=True)