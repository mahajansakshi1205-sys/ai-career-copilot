import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import (
    init_database,
    add_job_application,
    get_all_applications,
    update_application_status,
    delete_application,
    get_stats
)

st.set_page_config(
    page_title="Job Tracker",
    page_icon="📊",
    layout="wide"
)

# Initialize database
init_database()

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
        background: linear-gradient(90deg, #34d399, #a78bfa, #60a5fa);
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
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-num {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .stat-lbl {
        font-size: 0.85rem;
        color: #9ca3af;
    }
    .form-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
    }
    .section-label {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .status-applied {
        background: rgba(96,165,250,0.2);
        color: #60a5fa;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-interview {
        background: rgba(251,191,36,0.2);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-offer {
        background: rgba(52,211,153,0.2);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-rejected {
        background: rgba(248,113,113,0.2);
        color: #f87171;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .job-row {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 10px;
    }
    .company-name {
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    .job-title {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-top: 2px;
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #4b5563;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="page-title">📊 Job Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Track all your job applications in one place</div>', unsafe_allow_html=True)
st.markdown("---")

# ── STATS DASHBOARD ───────────────────────────────────────
stats = get_stats()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="stat-card"
    style="background:rgba(167,139,250,0.1);
    border-color:rgba(167,139,250,0.3);">
        <div class="stat-num" style="color:#a78bfa;">
            {stats['total']}
        </div>
        <div class="stat-lbl">Total Applied</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card"
    style="background:rgba(96,165,250,0.1);
    border-color:rgba(96,165,250,0.3);">
        <div class="stat-num" style="color:#60a5fa;">
            {stats['applied']}
        </div>
        <div class="stat-lbl">📨 Pending</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card"
    style="background:rgba(251,191,36,0.1);
    border-color:rgba(251,191,36,0.3);">
        <div class="stat-num" style="color:#fbbf24;">
            {stats['interview']}
        </div>
        <div class="stat-lbl">🎤 Interviews</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card"
    style="background:rgba(52,211,153,0.1);
    border-color:rgba(52,211,153,0.3);">
        <div class="stat-num" style="color:#34d399;">
            {stats['offer']}
        </div>
        <div class="stat-lbl">🎉 Offers</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-card"
    style="background:rgba(248,113,113,0.1);
    border-color:rgba(248,113,113,0.3);">
        <div class="stat-num" style="color:#f87171;">
            {stats['rejected']}
        </div>
        <div class="stat-lbl">❌ Rejected</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CHARTS ROW ────────────────────────────────────────────
df = get_all_applications()

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        # Status donut chart
        status_counts = df['status'].value_counts()
        colors_map = {
            'Applied': '#60a5fa',
            'Interview': '#fbbf24',
            'Offer': '#34d399',
            'Rejected': '#f87171'
        }
        colors = [colors_map.get(s, '#a78bfa')
                 for s in status_counts.index]

        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.55,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12,
        )])
        fig.update_layout(
            title=dict(
                text="Applications by Status",
                font=dict(color='white', size=15)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False,
            height=280,
            margin=dict(t=50, b=10, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Applications over time
        if 'date_applied' in df.columns and df['date_applied'].notna().any():
            df['date_applied'] = pd.to_datetime(
                df['date_applied'], errors='coerce'
            )
            daily = df.groupby('date_applied').size().reset_index()
            daily.columns = ['date', 'count']

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=daily['date'],
                y=daily['count'],
                mode='lines+markers',
                line=dict(color='#a78bfa', width=3),
                marker=dict(size=8, color='#a78bfa'),
                fill='tozeroy',
                fillcolor='rgba(167,139,250,0.1)'
            ))
            fig2.update_layout(
                title=dict(
                    text="Applications Over Time",
                    font=dict(color='white', size=15)
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=280,
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                margin=dict(t=50, b=10, l=10, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

# ── ADD NEW APPLICATION FORM ──────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">➕ Add New Job Application</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company = st.text_input(
        "🏢 Company Name *",
        placeholder="e.g. Google, Microsoft..."
    )
    job_title = st.text_input(
        "💼 Job Title *",
        placeholder="e.g. Python Developer..."
    )
    job_link = st.text_input(
        "🔗 Job Link",
        placeholder="Paste job URL here..."
    )
    location = st.text_input(
        "📍 Location",
        placeholder="e.g. Bangalore, Remote..."
    )

with col2:
    salary = st.text_input(
        "💰 Salary Range",
        placeholder="e.g. 5-8 LPA..."
    )
    status = st.selectbox(
        "📌 Status",
        ["Applied", "Interview", "Offer", "Rejected"]
    )
    date_applied = st.date_input(
        "📅 Date Applied",
        value=date.today()
    )
    notes = st.text_area(
        "📝 Notes",
        placeholder="Any notes about this application...",
        height=100
    )

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    add_btn = st.button(
        "✅ Add Application",
        type="primary",
        use_container_width=True
    )

if add_btn:
    if not company or not job_title:
        st.error("❌ Please fill Company Name and Job Title!")
    else:
        add_job_application(
            company, job_title, job_link,
            str(date_applied), status, notes,
            salary, location
        )
        st.success(f"✅ Application for **{job_title}** at **{company}** added!")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── ALL APPLICATIONS LIST ─────────────────────────────────
st.markdown("### 📋 All Applications")
st.markdown("<br>", unsafe_allow_html=True)

df = get_all_applications()

if df.empty:
    st.markdown("""
    <div class="empty-state">
        <div style='font-size:3rem'>📭</div>
        <div style='font-size:1.1rem; margin-top:12px;
        color:#6b7280;'>No applications yet!</div>
        <div style='font-size:0.9rem; margin-top:8px;
        color:#4b5563;'>Add your first job application above</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Filter by status
    filter_status = st.selectbox(
        "Filter by Status:",
        ["All", "Applied", "Interview", "Offer", "Rejected"]
    )

    if filter_status != "All":
        df = df[df['status'] == filter_status]

    st.markdown(f"""
    <div style='color:#9ca3af; font-size:0.85rem;
    margin-bottom:16px;'>
        Showing {len(df)} application(s)
    </div>
    """, unsafe_allow_html=True)

    # Status colors
    status_colors = {
        'Applied': '#60a5fa',
        'Interview': '#fbbf24',
        'Offer': '#34d399',
        'Rejected': '#f87171'
    }

    # Show each application
    for _, row in df.iterrows():
        color = status_colors.get(row['status'], '#a78bfa')

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.markdown(f"""
            <div style='padding:8px 0;'>
                <div class="company-name">
                    🏢 {row['company_name']}
                </div>
                <div class="job-title">
                    💼 {row['job_title']}
                </div>
                <div style='color:#4b5563;
                font-size:0.78rem; margin-top:4px;'>
                    📍 {row.get('location','N/A')} &nbsp;|&nbsp;
                    💰 {row.get('salary_range','N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='padding-top:12px;'>
                <span style='background:rgba(255,255,255,0.06);
                border:1px solid {color}44;
                color:{color};
                padding:5px 12px;
                border-radius:20px;
                font-size:0.8rem;
                font-weight:600;'>
                    {row['status']}
                </span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='color:#6b7280;
            font-size:0.82rem; padding-top:14px;'>
                📅 {row.get('date_applied','N/A')}
            </div>
            """, unsafe_allow_html=True)

        with col4:
            # Update status
            new_status = st.selectbox(
                "Update",
                ["Applied", "Interview", "Offer", "Rejected"],
                index=["Applied", "Interview",
                       "Offer", "Rejected"].index(
                    row['status']
                ) if row['status'] in [
                    "Applied", "Interview",
                    "Offer", "Rejected"
                ] else 0,
                key=f"status_{row['id']}",
                label_visibility="collapsed"
            )
            if new_status != row['status']:
                update_application_status(row['id'], new_status)
                st.rerun()

        # Notes
        if row.get('notes'):
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.2);
            border-radius:8px; padding:10px 14px;
            color:#6b7280; font-size:0.82rem;
            margin-bottom:4px;'>
                📝 {row['notes']}
            </div>
            """, unsafe_allow_html=True)

        # Delete button
        if st.button(f"🗑️ Delete", key=f"del_{row['id']}"):
            delete_application(row['id'])
            st.success("Deleted!")
            st.rerun()

        st.markdown("""
        <hr style='border:none;
        border-top:1px solid rgba(255,255,255,0.05);
        margin:8px 0;'>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.8rem;'>
    🤖 AI Career Copilot — Job Application Tracker
</div>
""", unsafe_allow_html=True)