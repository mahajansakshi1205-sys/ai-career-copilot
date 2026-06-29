import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.telegram_alerts import (
    send_job_alert_telegram,
    test_bot_connection,
    save_telegram_preference,
    get_saved_telegram_alerts
)
from utils.job_fetcher import fetch_live_jobs, calculate_job_match

st.set_page_config(page_title="Job Alerts", page_icon="📱", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .page-title {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .page-sub { color: #9ca3af; font-size: 1rem; margin-bottom: 2rem; }
    .input-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 16px; padding: 24px; margin-bottom: 16px;
    }

    /* ── Headings ── */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
        -webkit-text-fill-color: #e2e8f0 !important;
    }

    /* ── Widget labels ── */
    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        -webkit-text-fill-color: #c4b5fd !important;
    }

    /* ── ALL inputs ── */
    input,
    .stTextInput input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input,
    div[data-baseweb="base-input"] > input {
        background: rgba(30,27,75,0.85) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
        caret-color: #c4b5fd !important;
    }
    input::placeholder {
        color: #7c6fad !important;
        -webkit-text-fill-color: #7c6fad !important;
        opacity: 1 !important;
    }

    /* ── BaseWeb wrappers ── */
    [data-baseweb="input"],
    [data-baseweb="base-input"] {
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

    /* ── Expander ── */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader {
        color: #c4b5fd !important;
        -webkit-text-fill-color: #c4b5fd !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">📱 Telegram Job Alerts</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Get instant job alerts sent directly to your Telegram</div>', unsafe_allow_html=True)
st.markdown("---")

# ── BOT CONNECTION CHECK ──────────────────────────────────
bot_token_set = bool(os.getenv("TELEGRAM_BOT_TOKEN"))

if not bot_token_set:
    st.markdown("""
    <div style='background:rgba(251,191,36,0.1);
    border:1px solid rgba(251,191,36,0.3);
    border-radius:12px; padding:16px 20px;
    color:#fbbf24; margin-bottom:20px;'>
        ⚠️ TELEGRAM_BOT_TOKEN is missing in your .env file.
    </div>
    """, unsafe_allow_html=True)
else:
    success, msg = test_bot_connection()
    color = "#34d399" if success else "#f87171"
    bg    = "rgba(52,211,153,0.1)" if success else "rgba(248,113,113,0.1)"
    bdr   = "rgba(52,211,153,0.3)" if success else "rgba(248,113,113,0.3)"
    st.markdown(f"""
    <div style='background:{bg};border:1px solid {bdr};
    border-radius:12px;padding:16px 20px;
    color:{color};margin-bottom:20px;'>
        {msg}
    </div>""", unsafe_allow_html=True)

# ── HOW TO GET CHAT ID ────────────────────────────────────
with st.expander("💡 How do I find my Chat ID?"):
    st.markdown("""
    1. Open Telegram and message your bot anything (e.g. "hi")
    2. Open this URL in your browser, replacing TOKEN with your bot token:
       `https://api.telegram.org/botTOKEN/getUpdates`
    3. Look for `"chat":{"id": 123456789}` in the response
    4. That number is your Chat ID — paste it below
    """)

# ── SETUP FORM ────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>⚙️ Set Up a New Alert</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # ── PERMANENT FIX: no default value, user types their own chat_id ──
    chat_id = st.text_input(
        "Your Telegram Chat ID",
        placeholder="Enter your Chat ID here..."
    )
    query = st.text_input(
        "Job Title to Track",
        placeholder="e.g. Python Developer..."
    )
with col2:
    location  = st.text_input("Location", placeholder="e.g. India, Bangalore...")
    frequency = st.selectbox("Frequency", ["Daily", "Weekly"])

save_btn = st.button("💾 Save Alert", type="primary")
if save_btn:
    if not chat_id:
        st.error("❌ Please enter your Telegram Chat ID")
    elif not query:
        st.error("❌ Please enter a job title to track")
    else:
        save_telegram_preference(chat_id, query, location, frequency)
        st.success(f"✅ Alert saved for '{query}' in {location} — {frequency}")

st.markdown('</div>', unsafe_allow_html=True)

# ── SEND TEST NOW ─────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>🚀 Send a Test Alert Now</h4>", unsafe_allow_html=True)
st.markdown('<p style="color:#9ca3af;font-size:0.85rem;">Fetches current jobs and sends them to your Telegram right now.</p>', unsafe_allow_html=True)

# ── PERMANENT FIX: empty by default, user types their own ──
test_chat_id = st.text_input(
    "Send test to Chat ID",
    placeholder="Enter your Chat ID to send test..."
)
test_query = st.text_input(
    "Search Query for Test",
    placeholder="e.g. Python Developer...",
    key="test_query"
)
test_btn = st.button("📨 Send Test Message")

if test_btn:
    if not bot_token_set:
        st.error("❌ Cannot send — TELEGRAM_BOT_TOKEN is not configured in .env")
    elif not test_chat_id:
        st.error("❌ Enter your Chat ID first")
    elif not test_query:
        st.error("❌ Enter a search query")
    else:
        with st.spinner("🔍 Fetching jobs and sending to Telegram..."):
            resume_skills = st.session_state.get('resume_skills', [])
            jobs = fetch_live_jobs(test_query, location if location else "India")
            for job in jobs:
                job['match_score'] = calculate_job_match(
                    job.get('description', ''), resume_skills
                )
            jobs.sort(key=lambda x: x['match_score'], reverse=True)
            success, message = send_job_alert_telegram(test_chat_id, jobs, test_query)

        if success:
            st.success(f"✅ {message}")
            st.balloons()
        else:
            st.error(f"❌ {message}")

st.markdown('</div>', unsafe_allow_html=True)

# ── SAVED ALERTS ──────────────────────────────────────────
st.markdown("---")
st.markdown("<h3 style='color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;'>📋 Your Saved Alerts</h3>", unsafe_allow_html=True)

alerts_df = get_saved_telegram_alerts()
if alerts_df.empty:
    st.markdown("""
    <div style='text-align:center;padding:40px;color:#6b7280;'>
        📭 No alerts saved yet — set one up above!
    </div>
    """, unsafe_allow_html=True)
else:
    st.dataframe(alerts_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#4b5563;font-size:0.8rem;'>
    🤖 AI Career Copilot — Telegram Job Alerts
</div>
""", unsafe_allow_html=True)