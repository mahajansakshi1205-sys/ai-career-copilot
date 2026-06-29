import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.salary_model import (
    predict_salary,
    get_skill_recommendations
)

st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💰",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg,
            #0f0c29, #302b63, #24243e);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ── Main content text overrides (sidebar excluded) ── */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {
        color: #ffffff !important;
    }
    [data-testid="stMain"] .stMarkdown h1,
    [data-testid="stMain"] .stMarkdown h2,
    [data-testid="stMain"] .stMarkdown h3,
    [data-testid="stMain"] .stMarkdown h4,
    [data-testid="stMain"] .stMarkdown p {
        color: #ffffff !important;
    }
    /* Widget labels in main content only */
    [data-testid="stMain"] label,
    [data-testid="stMain"] .stSelectbox label,
    [data-testid="stMain"] .stSlider label,
    [data-testid="stMain"] .stTextArea label,
    [data-testid="stMain"] .stTextInput label,
    [data-testid="stMain"] .stCheckbox label,
    [data-testid="stMain"] .stCheckbox span,
    [data-testid="stMain"] div[data-testid="stWidgetLabel"] p,
    [data-testid="stMain"] div[data-testid="stWidgetLabel"] label,
    [data-testid="stMain"] div[data-testid="stWidgetLabel"] span {
        color: #ffffff !important;
    }
    /* Slider tick text */
    [data-testid="stMain"] .stSlider [data-testid="stTickBarMin"],
    [data-testid="stMain"] .stSlider [data-testid="stTickBarMax"],
    [data-testid="stMain"] .stSlider p {
        color: #ffffff !important;
    }
    /* Checkbox label text */
    [data-testid="stMain"] .stCheckbox > label > div > p {
        color: #ffffff !important;
    }
    /* Generic text in main content only */
    [data-testid="stMain"] p,
    [data-testid="stMain"] span {
        color: #ffffff;
    }
    hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg,
            #34d399, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .input-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .section-label {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .salary-display {
        background: linear-gradient(135deg,
            rgba(52,211,153,0.15),
            rgba(96,165,250,0.15));
        border: 2px solid rgba(52,211,153,0.4);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        margin: 20px 0;
    }
    .salary-amount {
        font-size: 3.5rem;
        font-weight: 900;
        color: #34d399;
        line-height: 1;
    }
    .salary-range {
        color: #ffffff;
        font-size: 1rem;
        margin-top: 8px;
    }
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }
    .skill-impact-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(52,211,153,0.2);
        border-left: 4px solid #34d399;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .recommend-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(167,139,250,0.2);
        border-left: 4px solid #a78bfa;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .position-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-top: 12px;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        color: #ffffff !important;
    }
    .stSlider {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown(
    '<div class="page-title">Salary Predictor</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="page-sub">AI predicts your salary based on role, skills, experience and location</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ── INPUT FORM ────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label">Your Profile</div>',
        unsafe_allow_html=True
    )

    role = st.selectbox(
        "Job Role",
        [
            "Python Developer",
            "Data Analyst",
            "ML Engineer",
            "Data Scientist",
            "Web Developer",
            "Full Stack Developer",
            "DevOps Engineer",
            "AI Engineer"
        ]
    )

    experience = st.slider(
        "Years of Experience",
        0, 10, 0
    )

    location = st.selectbox(
        "Location",
        [
            "Bangalore",
            "Mumbai",
            "Indore",
            "Chennai",
            "Hyderabad",
            "Delhi",
            "Pune"
        ]
    )

    remote = st.checkbox("Open to Remote Work")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label">Your Skills</div>',
        unsafe_allow_html=True
    )

    # Use resume skills if available
    resume_skills = st.session_state.get('resume_skills', [])

    if resume_skills:
        st.markdown(f"""
        <div style='background:rgba(52,211,153,0.1);
        border:1px solid rgba(52,211,153,0.3);
        border-radius:10px; padding:12px 16px;
        color:#34d399; font-size:0.85rem;
        margin-bottom:12px;'>
            Resume loaded with {len(resume_skills)} skills
        </div>
        """, unsafe_allow_html=True)
        use_resume = st.checkbox(
            "Use skills from my resume",
            value=True
        )
    else:
        use_resume = False

    if not use_resume:
        skills_input = st.text_area(
            "Enter your skills (one per line)",
            placeholder="python\nmachine learning\ndocker\naws\nsql",
            height=150
        )
        skills = [
            s.strip().lower()
            for s in skills_input.split('\n')
            if s.strip()
        ]
    else:
        skills = resume_skills

    st.markdown(f"""
    <div style='color:#ffffff; font-size:0.82rem;
    margin-top:8px;'>
        {len(skills)} skills selected
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── PREDICT BUTTON ────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_btn = st.button(
        "Predict My Salary",
        type="primary",
        use_container_width=True
    )

# ── PREDICTION RESULTS ────────────────────────────────────
if predict_btn:
    if not skills:
        st.error("Please add at least one skill!")
    else:
        with st.spinner("AI is calculating your salary..."):
            result = predict_salary(
                role, experience,
                location, skills, remote
            )

        st.markdown("---")
        st.markdown("### Your Salary Prediction")
        st.markdown("<br>", unsafe_allow_html=True)

        # Main salary display
        predicted  = result['predicted']
        sal_min    = result['salary_min']
        sal_max    = result['salary_max']
        position   = result['market_position']
        base       = result['base_salary']
        bonus      = result['skill_bonus']

        # Position color
        if "Top 10" in position:
            pos_color = "#34d399"
            pos_bg    = "rgba(52,211,153,0.15)"
        elif "Top 30" in position:
            pos_color = "#60a5fa"
            pos_bg    = "rgba(96,165,250,0.15)"
        elif "Average" in position:
            pos_color = "#fbbf24"
            pos_bg    = "rgba(251,191,36,0.15)"
        else:
            pos_color = "#f87171"
            pos_bg    = "rgba(248,113,113,0.15)"

        st.markdown(f"""
        <div class="salary-display">
            <div style='color:#ffffff; font-size:0.9rem;
            margin-bottom:8px;'>
                Predicted Annual Salary
            </div>
            <div class="salary-amount">
                {predicted} LPA
            </div>
            <div class="salary-range">
                Range: {sal_min} LPA - {sal_max} LPA
            </div>
            <div class="position-badge"
            style="background:{pos_bg};
            color:{pos_color};
            border:1px solid {pos_color}44;
            margin-top:16px;">
                {position}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        stats = [
            (f"{base} LPA",       "Base Salary",    "#a78bfa"),
            (f"+{bonus} LPA",     "Skills Bonus",   "#34d399"),
            (f"{experience} yrs", "Experience",     "#60a5fa"),
            (f"{len(skills)}",    "Skills Count",   "#fbbf24"),
        ]
        for col, (val, lbl, color) in zip(
            [col1, col2, col3, col4], stats
        ):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div style='font-size:1.5rem;
                    font-weight:800; color:{color};'>
                        {val}
                    </div>
                    <div style='color:#ffffff;
                    font-size:0.82rem; margin-top:4px;'>
                        {lbl}
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts row
        col1, col2 = st.columns(2)

        with col1:
            # Skill impact chart
            breakdown = result.get('skill_breakdown', {})
            if breakdown:
                skill_names  = list(breakdown.keys())
                skill_values = list(breakdown.values())

                fig = go.Figure(data=[go.Bar(
                    x=skill_values,
                    y=skill_names,
                    orientation='h',
                    marker_color='#34d399',
                    text=[
                        f"+{v} LPA" for v in skill_values
                    ],
                    textposition='outside',
                    textfont=dict(color='white'),
                )])
                fig.update_layout(
                    title=dict(
                        text="Skill Salary Impact",
                        font=dict(color='white', size=15)
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=320,
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        title="LPA Impact"
                    ),
                    margin=dict(t=50, b=20, l=10, r=80)
                )
                st.plotly_chart(
                    fig, use_container_width=True
                )

        with col2:
            # Salary breakdown donut
            fig2 = go.Figure(data=[go.Pie(
                labels=['Base Salary', 'Skills Bonus'],
                values=[base, max(bonus, 0.1)],
                hole=0.55,
                marker_colors=['#a78bfa', '#34d399'],
                textinfo='label+percent',
                textfont_size=12,
            )])
            fig2.update_layout(
                title=dict(
                    text="Salary Breakdown",
                    font=dict(color='white', size=15)
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False,
                height=320,
                margin=dict(t=50, b=20, l=10, r=10)
            )
            st.plotly_chart(
                fig2, use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Skill impact list
        st.markdown("### Skills Salary Contribution")
        st.markdown(
            '<p style="color:#ffffff; font-size:0.9rem; margin-bottom:16px;">How each of your skills contributes to salary</p>',
            unsafe_allow_html=True
        )

        for skill, impact in breakdown.items():
            bar_width = min(int((impact / 4) * 100), 100)
            st.markdown(f"""
            <div class="skill-impact-card">
                <div>
                    <div style='color:#ffffff;
                    font-weight:600; font-size:0.9rem;'>
                        {skill}
                    </div>
                    <div style='background:rgba(255,255,255,0.1);
                    border-radius:4px; height:6px;
                    margin-top:8px; width:200px;'>
                        <div style='height:100%;
                        width:{bar_width}%;
                        background:#34d399;
                        border-radius:4px;'></div>
                    </div>
                </div>
                <div style='color:#34d399;
                font-size:1.1rem; font-weight:800;'>
                    +{impact} LPA
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Recommendations
        recommendations = get_skill_recommendations(
            skills, role
        )

        if recommendations:
            st.markdown("### Learn These to Earn More")
            st.markdown(
                '<p style="color:#ffffff; font-size:0.9rem; margin-bottom:16px;">Add these skills to boost your salary significantly</p>',
                unsafe_allow_html=True
            )

            for rec in recommendations:
                skill_name = str(rec['skill'])
                bonus_text = str(rec['bonus'])
                impact_val = float(rec['impact'])
                bar_w = min(
                    int((impact_val / 4) * 100), 100
                )

                st.markdown(f"""
                <div class="recommend-card">
                    <div style='display:flex;
                    justify-content:space-between;
                    align-items:center;'>
                        <div>
                            <div style='color:#ffffff;
                            font-weight:700;
                            font-size:0.95rem;'>
                                {skill_name}
                            </div>
                            <div style='color:#ffffff;
                            font-size:0.82rem;
                            margin-top:4px;'>
                                High demand skill
                                for {role}
                            </div>
                        </div>
                        <div style='color:#a78bfa;
                        font-size:1.2rem;
                        font-weight:800;'>
                            {bonus_text}
                        </div>
                    </div>
                    <div style='background:rgba(255,255,255,0.08);
                    border-radius:4px; height:6px;
                    margin-top:12px;'>
                        <div style='height:100%;
                        width:{bar_w}%;
                        background:linear-gradient(
                            90deg, #a78bfa, #60a5fa);
                        border-radius:4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Next step banner
        st.markdown("""
        <div style='background:linear-gradient(
        90deg,#7c3aed,#2563eb);
        border-radius:16px; padding:24px;
        text-align:center; margin-top:24px;
        color:white;'>
            <div style='font-size:1.3rem;
            font-weight:800; margin-bottom:8px;'>
                Now you know your worth!
            </div>
            <div style='color:#ffffff; font-size:0.9rem;'>
                Go to Market Intelligence page
                to see live salary trends
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#ffffff;
font-size:0.8rem;'>
    AI Career Copilot - Salary Predictor
    powered by ML Model
</div>
""", unsafe_allow_html=True)
