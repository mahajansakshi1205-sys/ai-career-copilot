import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(chat_id, text):
    """
    Send a plain text message via Telegram Bot API.
    Returns (success: bool, message: str) — never silently fails.
    """

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN missing in .env file"
    if not chat_id:
        return False, "No chat_id provided"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        data = response.json()

        if data.get("ok"):
            return True, "Message sent successfully to Telegram"
        else:
            error_desc = data.get("description", "Unknown error")
            return False, f"Telegram API error: {error_desc}"

    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Failed to send message: {str(e)}"


def send_job_alert_telegram(chat_id, jobs, search_query):
    """Format jobs as a Telegram message and send it"""

    if not jobs:
        return False, "No jobs to send"

    lines = [
        f"<b>AI Career Copilot — Job Alert</b>",
        f"Found {len(jobs)} jobs for <b>{search_query}</b>\n"
    ]

    for job in jobs[:8]:
        title    = job.get('title', 'N/A')
        company  = job.get('company', 'N/A')
        location = job.get('location', 'N/A')
        score    = job.get('match_score', 0)
        link     = job.get('apply_link', '')

        lines.append(
            f"<b>{title}</b>\n"
            f"{company} — {location}\n"
            f"Match: {score}%\n"
            f"<a href=\"{link}\">Apply Here</a>\n"
        )

    lines.append(
        f"\nSent {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )

    text = "\n".join(lines)

    # Telegram has a 4096 character limit per message
    if len(text) > 4000:
        text = text[:3950] + "\n\n...truncated"

    return send_telegram_message(chat_id, text)


def test_bot_connection():
    """Verify the bot token is valid by calling getMe"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        return False, "No bot token in .env"

    url = f"https://api.telegram.org/bot{bot_token}/getMe"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("ok"):
            bot_name = data["result"].get("username", "")
            return True, f"Connected to bot: @{bot_name}"
        else:
            return False, "Invalid bot token"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def save_telegram_preference(chat_id, query, location, frequency):
    """Save alert preference to SQLite"""
    import sqlite3
    DB_PATH = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'careers.db'
    )
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telegram_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            query TEXT NOT NULL,
            location TEXT,
            frequency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        INSERT INTO telegram_preferences (chat_id, query, location, frequency)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, query, location, frequency))
    conn.commit()
    conn.close()


def get_saved_telegram_alerts():
    """Get all saved Telegram alert preferences"""
    import sqlite3
    import pandas as pd
    DB_PATH = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'careers.db'
    )
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM telegram_preferences ORDER BY created_at DESC",
            conn
        )
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df