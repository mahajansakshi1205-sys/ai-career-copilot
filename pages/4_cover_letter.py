import streamlit as st
import sys
import os

sys.path.insert(0, r'C:\Users\Sakshi\ai-career-copilot')
from utils.llm_helper import generate_cover_letter
st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="✉️",
    layout="wide"
)

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
        background: linear-gradient(90deg, #34d399, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .letter-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(52,211,153,0.3);
        border-left: 4px solid #34d399;
        border-radius: 16px;
        padding: 32px;
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.9;
        white-space: pre-wrap;
        font-family: Georgia, serif;
    }
    .input-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .section-label {
        color: #a78bfa;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .tip-box {
        background: rgba(251,191,36,0.08);
        border: 1px solid rgba(251,191,36,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        color: #fbbf24;
        font-size: 0.85rem;
        margin-bottom: 16px;
    }
    .success-banner {
        background: linear-gradient(90deg,
            rgba(52,211,153,0.15),
            rgba(96,165,250,0.15));
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 12px;
        padding: 16px 20px;
        color: #34d399;
        font-weight: 600;
        margin: 16px 0;
        text-align: center;
    }
    .warning-box {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #fbbf24;
    }

    /* ── ALL inputs & textareas ── */
    input,
    textarea,
    .stTextInput input,
    .stTextArea textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    [data-baseweb="base-input"] input,
    [data-baseweb="base-input"] textarea,
    div[data-baseweb="base-input"] > input,
    div[data-baseweb="base-input"] > textarea {
        background: rgba(30,27,75,0.85) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
        caret-color: #c4b5fd !important;
    }

    /* ── Placeholder ── */
    input::placeholder,
    textarea::placeholder {
        color: #7c6fad !important;
        -webkit-text-fill-color: #7c6fad !important;
        opacity: 1 !important;
    }

    /* ── BaseWeb wrappers ── */
    [data-baseweb="input"],
    [data-baseweb="base-input"],
    [data-baseweb="textarea"] {
        background: rgba(30,27,75,0.85) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        border-radius: 10px !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: rgba(30,27,75,0.85) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
    }

    /* ── Widget labels ── */
    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        -webkit-text-fill-color: #c4b5fd !important;
    }

    /* ── Headings ── */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #e2e8f0 !important;
        -webkit-text-fill-color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">✉️ Cover Letter Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">AI writes a professional cover letter tailored to your target job</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHECK SESSION ─────────────────────────────────────────
if 'resume_text' not in st.session_state:
    st.markdown("""
    <div class="warning-box">
        <div style='font-size:2.5rem'>⚠️</div>
        <div style='font-size:1.1rem; font-weight:700; margin:8px 0'>Resume Not Found!</div>
        <div style='font-size:0.9rem; opacity:0.8'>Please upload your resume first from the Resume page</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── INPUT SECTION ─────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">👤 Your Name</div>', unsafe_allow_html=True)
    candidate_name = st.text_input(
        "Name",
        placeholder="Enter your full name...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📋 Job Description</div>', unsafe_allow_html=True)
    saved_jd = st.session_state.get('job_description', '')
    job_desc = st.text_area(
        "Job Description",
        value=saved_jd,
        height=180,
        placeholder="Paste job description here...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tip-box">
        💡 <b>Tips for best results:</b><br><br>
        ✅ Enter your real full name<br>
        ✅ Use the complete job description<br>
        ✅ Make sure resume is uploaded<br>
        ✅ Edit the letter after generating
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:rgba(167,139,250,0.1);
    border:1px solid rgba(167,139,250,0.2);
    border-radius:12px; padding:16px; margin-top:8px;'>
        <div style='color:#a78bfa; font-weight:700; margin-bottom:10px;'>📄 Resume Status</div>
        <div style='color:#34d399; font-size:0.9rem;'>✅ Resume loaded successfully</div>
        <div style='color:#9ca3af; font-size:0.8rem; margin-top:6px;'>
            {len(st.session_state.get('resume_skills', []))} skills detected
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GENERATE BUTTON ───────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button(
        "✨ Generate Cover Letter",
        type="primary",
        use_container_width=True
    )

# ── GENERATED LETTER ──────────────────────────────────────
if generate:
    if not job_desc:
        st.error("❌ Please paste a job description first!")
    elif not candidate_name:
        st.warning("⚠️ Please enter your name for a personalized letter!")
    else:
        with st.spinner("✍️ AI is writing your cover letter..."):
            letter = generate_cover_letter(
                st.session_state['resume_text'],
                job_desc,
                candidate_name
            )

        st.markdown('<div class="success-banner">✅ Cover Letter Generated Successfully!</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>📄 Your Cover Letter</h3>", unsafe_allow_html=True)
        st.markdown(f'<div class="letter-box">{letter}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download Cover Letter",
                data=letter,
                file_name="cover_letter.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.code(letter, language=None)

        st.session_state['cover_letter'] = letter

        st.markdown("""
        <div style='background:linear-gradient(90deg,#7c3aed,#2563eb);
        border-radius:16px; padding:24px; text-align:center;
        margin-top:24px; color:white;'>
            <div style='font-size:1.3rem; font-weight:800; margin-bottom:8px;'>
                🎯 Cover Letter Ready!
            </div>
            <div style='opacity:0.85; font-size:0.9rem;'>
                Now go to <b>Interview Questions</b> page from sidebar to prepare for interviews →
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    🤖 AI Career Copilot — Cover Letter Generator
</div>
""", unsafe_allow_html=True)