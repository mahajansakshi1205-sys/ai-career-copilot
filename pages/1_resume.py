import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.pdf_reader import extract_text_from_pdf, extract_skills_from_text

st.set_page_config(page_title="Resume Upload", page_icon="📄", layout="wide")

# Custom CSS
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
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .upload-box {
        background: rgba(255,255,255,0.04);
        border: 2px dashed rgba(167,139,250,0.5);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-icon {
        font-size: 3.5rem;
        margin-bottom: 12px;
    }
    .upload-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 8px;
    }
    .upload-hint {
        color: #6b7280;
        font-size: 0.85rem;
    }
    .skill-tag {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #34d399;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
        font-weight: 500;
    }
    .skills-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 16px;
    }
    .stat-card {
        background: rgba(167,139,250,0.1);
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 800;
        color: #a78bfa;
    }
    .stat-lbl {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
    }
    .job-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(96,165,250,0.3);
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
    }
    .success-banner {
        background: linear-gradient(90deg, rgba(52,211,153,0.15), rgba(96,165,250,0.15));
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 12px;
        padding: 16px 20px;
        color: #34d399;
        font-weight: 600;
        margin: 16px 0;
    }
    .next-btn {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 16px;
    }
    .stTextArea textarea {
    background: #1a1a2e !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 0.9rem !important;
    caret-color: #ffffff !important;
}

.stTextArea textarea::placeholder {
    color: #6b7280 !important;
}

/* Fix text area label */
.stTextArea label {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">📄 Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Upload your resume and AI will extract all your skills instantly</div>', unsafe_allow_html=True)

st.markdown("---")

# ── UPLOAD SECTION ────────────────────────────────────────
st.markdown("""
<div class="upload-box">
    <div class="upload-icon">📂</div>
    <div class="upload-title">Drop your Resume PDF here</div>
    <div class="upload-hint">Supports PDF format • Max 200MB</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your Resume PDF",
    type="pdf",
    label_visibility="collapsed"
)

# ── AFTER UPLOAD ──────────────────────────────────────────
if uploaded_file is not None:

    st.markdown("""
    <div class="success-banner">
        ✅ Resume uploaded successfully! Extracting your skills...
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("🤖 AI is reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills_from_text(resume_text)

    # Stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">{len(skills)}</div>
            <div class="stat-lbl">Skills Found</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">{len(resume_text.split())}</div>
            <div class="stat-lbl">Words in Resume</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">✅</div>
            <div class="stat-lbl">Ready to Analyze</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Skills found
    st.markdown('<div class="skills-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Skills Found in Your Resume</div>', unsafe_allow_html=True)

    if skills:
        skills_html = "".join([f'<span class="skill-tag">✅ {skill}</span>' for skill in skills])
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.warning("No common skills detected. Try a different resume format.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Save to session
    st.session_state['resume_text'] = resume_text
    st.session_state['resume_skills'] = skills

    # Resume text expander
    with st.expander("📃 View Full Extracted Resume Text"):
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.3); padding:20px;
        border-radius:12px; color:#9ca3af; font-size:0.85rem;
        line-height:1.7; white-space:pre-wrap;'>{resume_text}</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Job Description Section
    st.markdown('<div class="job-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Paste Job Description</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:0.9rem; margin-bottom:12px;">Copy any job posting and paste it below — AI will compare it with your resume</p>', unsafe_allow_html=True)

    job_desc = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the full job description here...\n\nExample:\nWe are looking for a Python Developer with experience in...",
        label_visibility="collapsed"
    )

    if job_desc:
        st.session_state['job_description'] = job_desc
        st.markdown("""
        <div class="success-banner">
            ✅ Job Description saved! Now go to Skill Gap Analysis from the sidebar →
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tips section when no file uploaded
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.04); border:1px solid
        rgba(255,255,255,0.1); border-radius:12px; padding:20px; text-align:center;'>
            <div style='font-size:2rem'>📝</div>
            <div style='color:#e2e8f0; font-weight:600; margin:8px 0'>Step 1</div>
            <div style='color:#9ca3af; font-size:0.85rem'>Upload your PDF resume using the button above</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.04); border:1px solid
        rgba(255,255,255,0.1); border-radius:12px; padding:20px; text-align:center;'>
            <div style='font-size:2rem'>🤖</div>
            <div style='color:#e2e8f0; font-weight:600; margin:8px 0'>Step 2</div>
            <div style='color:#9ca3af; font-size:0.85rem'>AI reads and extracts all your skills automatically</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.04); border:1px solid
        rgba(255,255,255,0.1); border-radius:12px; padding:20px; text-align:center;'>
            <div style='font-size:2rem'>🎯</div>
            <div style='color:#e2e8f0; font-weight:600; margin:8px 0'>Step 3</div>
            <div style='color:#9ca3af; font-size:0.85rem'>Paste job description and go to Skill Gap Analysis</div>
        </div>""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    🤖 AI Career Copilot — Resume Analyzer
</div>
""", unsafe_allow_html=True)