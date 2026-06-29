import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.report_generator import (
    generate_skill_gap_pdf,
    generate_roadmap_pdf,
    generate_jobs_excel,
    generate_applications_excel
)
from utils.database import get_all_applications

st.set_page_config(page_title="Reports", page_icon="📥", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .page-title {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #fbbf24, #34d399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .page-sub { color: #9ca3af; font-size: 1rem; margin-bottom: 2rem; }
    .report-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 24px; margin-bottom: 16px;
    }
    .report-title { color: #ffffff; font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
    .report-desc { color: #6b7280; font-size: 0.85rem; margin-bottom: 16px; }
    .status-ready { color: #34d399; font-size: 0.82rem; font-weight: 600; }
    .status-missing { color: #fbbf24; font-size: 0.82rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Reports</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Download your data as PDF or Excel files</div>', unsafe_allow_html=True)
st.markdown("---")

candidate_name = st.text_input("Your Name (for reports)", value="Sakshi Mahajan")

st.markdown("<br>", unsafe_allow_html=True)

# ── REPORT 1: SKILL GAP PDF ───────────────────────────────
st.markdown('<div class="report-card">', unsafe_allow_html=True)
st.markdown('<div class="report-title">Skill Gap Analysis — PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="report-desc">Your match score, matched skills, missing skills and AI summary as a PDF.</div>', unsafe_allow_html=True)

if 'matching_skills' in st.session_state:
    st.markdown('<div class="status-ready">Data available — ready to download</div>', unsafe_allow_html=True)

    pdf_buffer = generate_skill_gap_pdf(
        matching_skills=st.session_state.get('matching_skills', []),
        missing_skills=st.session_state.get('missing_skills', []),
        match_percentage=st.session_state.get('match_percentage', 0),
        summary="",
        candidate_name=candidate_name
    )

    st.download_button(
        label="Download Skill Gap PDF",
        data=pdf_buffer,
        file_name="skill_gap_report.pdf",
        mime="application/pdf"
    )
else:
    st.markdown('<div class="status-missing">Run Skill Gap Analysis first to unlock this report</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── REPORT 2: ROADMAP PDF ─────────────────────────────────
st.markdown('<div class="report-card">', unsafe_allow_html=True)
st.markdown('<div class="report-title">Learning Roadmap — PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="report-desc">Your full week by week learning plan as a PDF you can print or save.</div>', unsafe_allow_html=True)

if 'roadmap_weeks' in st.session_state:
    st.markdown('<div class="status-ready">Data available — ready to download</div>', unsafe_allow_html=True)

    pdf_buffer = generate_roadmap_pdf(
        weeks=st.session_state.get('roadmap_weeks', []),
        goal=st.session_state.get('roadmap_goal', ''),
        candidate_name=candidate_name
    )

    st.download_button(
        label="Download Roadmap PDF",
        data=pdf_buffer,
        file_name="learning_roadmap.pdf",
        mime="application/pdf"
    )
else:
    st.markdown('<div class="status-missing">Generate a Learning Roadmap first to unlock this report</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── REPORT 3: JOB SEARCH EXCEL ────────────────────────────
st.markdown('<div class="report-card">', unsafe_allow_html=True)
st.markdown('<div class="report-title">Job Search Results — Excel</div>', unsafe_allow_html=True)
st.markdown('<div class="report-desc">All jobs from your last search with match scores, as a spreadsheet.</div>', unsafe_allow_html=True)

if 'search_results' in st.session_state and st.session_state['search_results']:
    st.markdown('<div class="status-ready">Data available — ready to download</div>', unsafe_allow_html=True)

    excel_buffer = generate_jobs_excel(
        jobs=st.session_state['search_results'],
        search_query=st.session_state.get('search_query', 'Jobs')
    )

    st.download_button(
        label="Download Jobs Excel",
        data=excel_buffer,
        file_name="job_search_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.markdown('<div class="status-missing">Search for jobs first to unlock this report</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── REPORT 4: APPLICATIONS EXCEL ──────────────────────────
st.markdown('<div class="report-card">', unsafe_allow_html=True)
st.markdown('<div class="report-title">Job Applications — Excel</div>', unsafe_allow_html=True)
st.markdown('<div class="report-desc">All applications you have logged in your Job Tracker, as a spreadsheet.</div>', unsafe_allow_html=True)

applications_df = get_all_applications()

if not applications_df.empty:
    st.markdown('<div class="status-ready">Data available — ready to download</div>', unsafe_allow_html=True)

    excel_buffer = generate_applications_excel(applications_df)

    st.download_button(
        label="Download Applications Excel",
        data=excel_buffer,
        file_name="job_applications.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.markdown('<div class="status-missing">Add applications in Job Tracker first to unlock this report</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    AI Career Copilot - Reports
</div>
""", unsafe_allow_html=True)