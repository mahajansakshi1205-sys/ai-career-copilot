import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.llm_helper import generate_interview_questions, evaluate_answer

st.set_page_config(
    page_title="Interview Prep",
    page_icon="🎤",
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
        background: linear-gradient(90deg, #fb923c, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .question-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 12px;
        border-left: 4px solid #a78bfa;
    }
    .question-num {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }
    .question-text {
        color: #e2e8f0;
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.5;
    }
    .tech-badge {
        display: inline-block;
        background: rgba(96,165,250,0.15);
        border: 1px solid rgba(96,165,250,0.3);
        color: #60a5fa;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .behav-badge {
        display: inline-block;
        background: rgba(251,146,60,0.15);
        border: 1px solid rgba(251,146,60,0.3);
        color: #fb923c;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .score-box {
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .feedback-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 12px;
        color: #e2e8f0;
        font-size: 0.9rem;
        line-height: 1.7;
    }
    .warning-box {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #fbbf24;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">🎤 Interview Prep</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Practice with AI-generated role-specific interview questions</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHECK SESSION ─────────────────────────────────────────
if 'job_description' not in st.session_state:
    st.markdown("""
    <div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem; font-weight:700; margin:8px 0'>
            Job Description Not Found!
        </div>
        <div style='font-size:0.9rem; opacity:0.8'>
            Please go to Resume page and paste a job description first
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── SETTINGS ──────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div style='background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:12px; padding:16px 20px;
    color:#34d399; font-weight:600;'>
        ✅ Job description loaded — Ready to generate questions!
    </div>
    """, unsafe_allow_html=True)

with col2:
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
        index=1
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── GENERATE BUTTON ───────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button(
        "🎯 Generate Interview Questions",
        type="primary",
        use_container_width=True
    )

# ── QUESTIONS ─────────────────────────────────────────────
if generate:
    with st.spinner("🤖 AI is preparing your interview questions..."):
        result = generate_interview_questions(
            st.session_state['job_description'],
            difficulty
        )

    # Parse questions
    lines = result.strip().split('\n')
    technical_qs = []
    behavioral_qs = []
    current = None

    for line in lines:
        line = line.strip()
        if 'TECHNICAL:' in line:
            current = 'tech'
        elif 'BEHAVIORAL:' in line:
            current = 'behav'
        elif line and line[0].isdigit() and '.' in line:
            question = line.split('.', 1)[-1].strip()
            if question:
                if current == 'tech':
                    technical_qs.append(question)
                elif current == 'behav':
                    behavioral_qs.append(question)

    st.session_state['technical_qs'] = technical_qs
    st.session_state['behavioral_qs'] = behavioral_qs
    st.session_state['job_desc_for_eval'] = st.session_state['job_description']

# Show questions if they exist
if 'technical_qs' in st.session_state:
    technical_qs = st.session_state['technical_qs']
    behavioral_qs = st.session_state['behavioral_qs']

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style='background:rgba(96,165,250,0.1);
        border:1px solid rgba(96,165,250,0.2);
        border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:800;
            color:#60a5fa;'>{len(technical_qs)}</div>
            <div style='color:#9ca3af; font-size:0.8rem;'>
                Technical Questions
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:rgba(251,146,60,0.1);
        border:1px solid rgba(251,146,60,0.2);
        border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:800;
            color:#fb923c;'>{len(behavioral_qs)}</div>
            <div style='color:#9ca3af; font-size:0.8rem;'>
                Behavioral Questions
            </div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background:rgba(167,139,250,0.1);
        border:1px solid rgba(167,139,250,0.2);
        border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:800;
            color:#a78bfa;'>{len(technical_qs)+len(behavioral_qs)}</div>
            <div style='color:#9ca3af; font-size:0.8rem;'>
                Total Questions
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Technical Questions
    if technical_qs:
        st.markdown("### 💻 Technical Questions")
        for i, q in enumerate(technical_qs):
            st.markdown(f"""
            <div class="question-card">
                <div class="tech-badge">Technical</div>
                <div class="question-num">Question {i+1}</div>
                <div class="question-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Behavioral Questions
    if behavioral_qs:
        st.markdown("### 🤝 Behavioral Questions")
        for i, q in enumerate(behavioral_qs):
            st.markdown(f"""
            <div class="question-card"
            style="border-left-color:#fb923c;">
                <div class="behav-badge">Behavioral</div>
                <div class="question-num">Question {i+1}</div>
                <div class="question-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── PRACTICE MODE ─────────────────────────────────────
    st.markdown("### 🎯 Practice Mode — Get AI Feedback")
    st.markdown('<p style="color:#9ca3af;">Pick a question, write your answer, get instant AI feedback!</p>', unsafe_allow_html=True)

    all_questions = technical_qs + behavioral_qs

    if all_questions:
        selected_q = st.selectbox(
            "Choose a question to practice:",
            all_questions
        )

        user_answer = st.text_area(
            "✍️ Your Answer:",
            height=150,
            placeholder="Type your answer here..."
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            evaluate = st.button(
                "🤖 Get AI Feedback",
                type="primary",
                use_container_width=True
            )

        if evaluate and user_answer:
            with st.spinner("🤖 AI is evaluating your answer..."):
                feedback = evaluate_answer(
                    selected_q,
                    user_answer,
                    st.session_state.get('job_desc_for_eval', '')
                )

            # Parse feedback
            score = 0
            strengths = ""
            improvements = ""
            ideal = ""

            for line in feedback.strip().split('\n'):
                if "SCORE:" in line:
                    try:
                        score = int(line.replace("SCORE:", "").strip())
                    except:
                        score = 5
                elif "STRENGTHS:" in line:
                    strengths = line.replace("STRENGTHS:", "").strip()
                elif "IMPROVEMENTS:" in line:
                    improvements = line.replace("IMPROVEMENTS:", "").strip()
                elif "IDEAL_ANSWER:" in line:
                    ideal = line.replace("IDEAL_ANSWER:", "").strip()

            # Score color
            if score >= 8:
                sc = "#34d399"
                slabel = "Excellent! 🌟"
            elif score >= 5:
                sc = "#fbbf24"
                slabel = "Good! Keep Improving 💪"
            else:
                sc = "#f87171"
                slabel = "Needs Practice 📚"

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Your Feedback")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="score-box"
                style="background:rgba(0,0,0,0.3);
                border:2px solid {sc};">
                    <div style='font-size:2.5rem;
                    font-weight:800; color:{sc};'>
                        {score}/10
                    </div>
                    <div style='color:#9ca3af;
                    font-size:0.85rem;'>{slabel}</div>
                </div>""", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if strengths:
                    st.markdown(f"""
                    <div class="feedback-box"
                    style="border-left:4px solid #34d399;">
                        <div style='color:#34d399; font-weight:700;
                        margin-bottom:8px;'>✅ Strengths</div>
                        {strengths}
                    </div>""", unsafe_allow_html=True)
            with col2:
                if improvements:
                    st.markdown(f"""
                    <div class="feedback-box"
                    style="border-left:4px solid #f87171;">
                        <div style='color:#f87171; font-weight:700;
                        margin-bottom:8px;'>📈 Improvements</div>
                        {improvements}
                    </div>""", unsafe_allow_html=True)

            if ideal:
                st.markdown(f"""
                <div class="feedback-box"
                style="border-left:4px solid #a78bfa; margin-top:12px;">
                    <div style='color:#a78bfa; font-weight:700;
                    margin-bottom:8px;'>💡 Ideal Answer</div>
                    {ideal}
                </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    🤖 AI Career Copilot — Interview Prep
</div>
""", unsafe_allow_html=True)