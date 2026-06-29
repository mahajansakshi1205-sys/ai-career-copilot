import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.pdf_reader import (
    extract_text_from_pdf,
    extract_skills_from_text,
    extract_skills_by_category,
    calculate_ats_score,
    extract_resume_info
)

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
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
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 800;
    }
    .stat-lbl {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
    }
    .category-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
    }
    .category-title {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .skill-tag {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 3px;
    }
    .ats-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
    }
    .info-box {
        background: rgba(167,139,250,0.08);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
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

    /* ── Fix all Streamlit default dark headings ── */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    /* Specifically target st.markdown heading anchors */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #e2e8f0 !important;
    }
    /* Streamlit element containers */
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown(
    '<div class="page-title">📄 Resume Analyzer</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="page-sub">Upload your resume — AI deeply analyzes your skills, ATS score & profile</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ── UPLOAD ────────────────────────────────────────────────
st.markdown("""
<div style='background:rgba(255,255,255,0.03);
border:2px dashed rgba(167,139,250,0.4);
border-radius:20px; padding:40px;
text-align:center; margin-bottom:24px;'>
    <div style='font-size:3rem; margin-bottom:12px;'>📂</div>
    <div style='font-size:1.2rem; font-weight:700;
    color:#e2e8f0; margin-bottom:8px;'>
        Drop your Resume PDF here
    </div>
    <div style='color:#6b7280; font-size:0.85rem;'>
        Supports PDF format • Powered by pdfplumber + spaCy NLP
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose Resume PDF",
    type="pdf",
    label_visibility="collapsed"
)

# ── AFTER UPLOAD ──────────────────────────────────────────
if uploaded_file is not None:

    with st.spinner("🤖 AI is deeply analyzing your resume..."):
        resume_text    = extract_text_from_pdf(uploaded_file)
        skills         = extract_skills_from_text(resume_text)
        skills_by_cat  = extract_skills_by_category(resume_text)
        resume_info    = extract_resume_info(resume_text)

    st.markdown("""
    <div class="success-banner">
        ✅ Resume analyzed successfully using spaCy NLP!
    </div>
    """, unsafe_allow_html=True)

    # ── STATS ROW ─────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        (len(skills),               "Skills Found",     "#a78bfa"),
        (len(skills_by_cat),        "Categories",       "#60a5fa"),
        (resume_info['word_count'], "Resume Words",     "#34d399"),
        ("✅",                      "NLP Analysis Done","#fbbf24"),
    ]

    for col, (num, lbl, color) in zip(
        [col1, col2, col3, col4], stats
    ):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-num" style="color:{color};">
                    {num}
                </div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RESUME INFO ───────────────────────────────────────
    st.markdown(
        "<h3 style='color:#e2e8f0;'>👤 Resume Information</h3>",
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="info-box">
            <div style='color:#a78bfa; font-size:0.8rem;
            font-weight:700; text-transform:uppercase;
            letter-spacing:0.1em; margin-bottom:12px;'>
                Contact Info
            </div>
            <div style='color:#e2e8f0; font-size:0.9rem;
            line-height:2;'>
                📧 {resume_info['email']}<br>
                📱 {resume_info['phone']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        orgs = resume_info['organizations']
        orgs_text = " • ".join(orgs) if orgs else "Not detected"
        st.markdown(f"""
        <div class="info-box">
            <div style='color:#a78bfa; font-size:0.8rem;
            font-weight:700; text-transform:uppercase;
            letter-spacing:0.1em; margin-bottom:12px;'>
                Organizations Detected
            </div>
            <div style='color:#e2e8f0; font-size:0.9rem;
            line-height:2;'>
                🏢 {orgs_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SKILLS BY CATEGORY ────────────────────────────────
    st.markdown(
        "<h3 style='color:#e2e8f0;'>🎯 Skills Found by Category</h3>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    category_config = {
        "programming_languages": ("💻", "Programming Languages", "#a78bfa"),
        "ai_ml":                 ("🤖", "AI & Machine Learning",  "#f472b6"),
        "data":                  ("📊", "Data & Analytics",       "#60a5fa"),
        "web":                   ("🌐", "Web Development",        "#34d399"),
        "databases":             ("🗄️", "Databases",              "#fbbf24"),
        "cloud_devops":          ("☁️", "Cloud & DevOps",         "#fb923c"),
        "mobile":                ("📱", "Mobile Development",     "#06b6d4"),
        "soft_skills":           ("🤝", "Soft Skills",            "#8b5cf6"),
    }

    col1, col2 = st.columns(2)
    cols = [col1, col2]

    for idx, (cat, skills_list) in enumerate(
        skills_by_cat.items()
    ):
        config = category_config.get(
            cat, ("📌", cat.replace("_", " ").title(), "#a78bfa")
        )
        emoji, title, color = config

        with cols[idx % 2]:
            tags_html = "".join([
                f"""<span class="skill-tag"
                style="background:{color}18;
                border:1px solid {color}44;
                color:{color};">
                ✅ {s}</span>"""
                for s in skills_list
            ])
            st.markdown(f"""
            <div class="category-card"
            style="border-left:3px solid {color};">
                <div class="category-title"
                style="color:{color};">
                    {emoji} {title}
                </div>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)

    # ── RESUME TEXT EXPANDER ──────────────────────────────
    with st.expander("📃 View Full Extracted Resume Text"):
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.3);
        padding:20px; border-radius:12px;
        color:#9ca3af; font-size:0.85rem;
        line-height:1.7; white-space:pre-wrap;'>
            {resume_text}
        </div>
        """, unsafe_allow_html=True)

    # Save to session
    st.session_state['resume_text']   = resume_text
    st.session_state['resume_skills'] = skills
    st.session_state['skills_by_cat'] = skills_by_cat

    st.markdown("---")

    # ── JOB DESCRIPTION ───────────────────────────────────
    st.markdown("""
    <div style='font-size:1.3rem; font-weight:700;
    color:#60a5fa; margin-bottom:8px;'>
        📋 Paste Job Description
    </div>
    <p style='color:#9ca3af; font-size:0.9rem;
    margin-bottom:12px;'>
        Paste any job description — AI will compare
        it with your resume and calculate ATS score
    </p>
    """, unsafe_allow_html=True)

    saved_jd = st.session_state.get('job_description', '')
    job_desc = st.text_area(
        "Job Description",
        value=saved_jd,
        height=200,
        placeholder="Paste full job description here...",
        label_visibility="collapsed"
    )

    if job_desc:
        st.session_state['job_description'] = job_desc

        # ── ATS SCORE ─────────────────────────────────────
        ats_result = calculate_ats_score(resume_text, job_desc)
        ats_score  = ats_result['ats_score']

        # ATS color
        if ats_score >= 70:
            ats_color = "#34d399"
            ats_label = "Excellent ATS Match! 🌟"
        elif ats_score >= 40:
            ats_color = "#fbbf24"
            ats_label = "Moderate ATS Match 💪"
        else:
            ats_color = "#f87171"
            ats_label = "Low ATS Match — Improve Resume 📝"

        st.markdown('<div class="ats-box">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='color:#a78bfa; font-size:0.8rem;
        font-weight:700; text-transform:uppercase;
        letter-spacing:0.12em; margin-bottom:16px;'>
            🤖 ATS Compatibility Score
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style='text-align:center;'>
                <div style='font-size:3rem; font-weight:900;
                color:{ats_color};'>{ats_score}%</div>
                <div style='color:#9ca3af; font-size:0.85rem;
                margin-top:4px;'>{ats_label}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='text-align:center;'>
                <div style='font-size:2rem; font-weight:800;
                color:#34d399;'>
                    {ats_result['matched_count']}
                </div>
                <div style='color:#9ca3af; font-size:0.85rem;'>
                    Keywords Matched
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='text-align:center;'>
                <div style='font-size:2rem; font-weight:800;
                color:#f87171;'>
                    {ats_result['total_keywords'] - ats_result['matched_count']}
                </div>
                <div style='color:#9ca3af; font-size:0.85rem;'>
                    Keywords Missing
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div style='margin:16px 0 8px;
        color:#9ca3af; font-size:0.85rem;'>
            ATS Score — {ats_score}%
        </div>
        <div style='background:rgba(255,255,255,0.1);
        border-radius:10px; height:12px; overflow:hidden;'>
            <div style='height:100%; width:{ats_score}%;
            background:linear-gradient(90deg,
            {ats_color}, #60a5fa);
            border-radius:10px;'></div>
        </div>
        """, unsafe_allow_html=True)

        # Matched keywords
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='color:#34d399; font-weight:700;
            margin:16px 0 8px; font-size:0.9rem;'>
                ✅ Matched Keywords
            </div>
            """, unsafe_allow_html=True)
            matched_html = "".join([
                f"""<span style='display:inline-block;
                background:rgba(52,211,153,0.1);
                border:1px solid rgba(52,211,153,0.3);
                color:#34d399; padding:4px 10px;
                border-radius:20px; font-size:0.78rem;
                margin:3px;'>✅ {k}</span>"""
                for k in ats_result['matched_keywords']
            ])
            st.markdown(matched_html, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='color:#f87171; font-weight:700;
            margin:16px 0 8px; font-size:0.9rem;'>
                ❌ Missing Keywords
            </div>
            """, unsafe_allow_html=True)
            missing_html = "".join([
                f"""<span style='display:inline-block;
                background:rgba(248,113,113,0.1);
                border:1px solid rgba(248,113,113,0.3);
                color:#f87171; padding:4px 10px;
                border-radius:20px; font-size:0.78rem;
                margin:3px;'>❌ {k}</span>"""
                for k in ats_result['missing_keywords']
            ])
            st.markdown(missing_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="success-banner">
            ✅ Job Description saved!
            Now go to 🔍 Skill Gap Analysis →
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

else:
    # Tips when no file uploaded
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    tips = [
        ("📝", "Step 1", "Upload your PDF resume above"),
        ("🤖", "Step 2", "AI reads and analyzes with spaCy NLP"),
        ("🎯", "Step 3", "Paste job description to get ATS score"),
    ]
    for col, (emoji, title, desc) in zip(
        [col1, col2, col3], tips
    ):
        with col:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px; padding:24px;
            text-align:center;'>
                <div style='font-size:2.5rem;
                margin-bottom:12px;'>{emoji}</div>
                <div style='color:#e2e8f0; font-weight:700;
                margin-bottom:8px;'>{title}</div>
                <div style='color:#6b7280;
                font-size:0.85rem;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563;
font-size:0.8rem;'>
    🤖 AI Career Copilot — Resume Analyzer
    powered by pdfplumber + spaCy NLP
</div>
""", unsafe_allow_html=True)