# 🤖 AI Career Copilot

> Your personal AI-powered career advisor — from resume to offer letter!

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 🎯 What is this?

AI Career Copilot is a smart full-stack web application that helps students and job seekers land their dream job using the power of AI. Upload your resume, paste any job description — the AI does the rest!

Built with **26 technologies** spanning NLP, machine learning, LLM reasoning, API integration, database management, and real-time notifications.

---

## ✨ Features

| Page | Feature | Description |
|---|---|---|
| 📄 | **Resume Analyzer** | Upload PDF — spaCy NLP extracts 70+ skills across 8 categories + ATS score |
| 🔍 | **Skill Gap Analysis** | AI compares your skills vs job requirements with salary impact per skill |
| 🎤 | **Interview Prep** | Role-specific questions generated + AI scores your answers with feedback |
| 💰 | **Salary Predictor** | ML model (Gradient Boosting) predicts salary range based on role, skills, location |
| 💼 | **Live Job Search** | Real jobs from LinkedIn, Indeed & Glassdoor via JSearch API with match scoring |
| 📊 | **Job Tracker** | SQLite-backed application tracker with status pipeline and visual dashboard |
| 📱 | **Telegram Alerts** | Instant job alerts sent to your Telegram via Bot API |
| 📥 | **Reports** | Download skill gap as PDF and job data as Excel |

---

## 🛠️ Tech Stack

### Core
| Technology | Purpose |
|---|---|
| Python 3.12 | Primary programming language |
| Streamlit | Multi-page web application framework |
| Custom CSS | Dark gradient UI theme |

### AI & NLP
| Technology | Purpose |
|---|---|
| LangChain | Prompt orchestration and LLM chain management |
| Groq (Llama 3 8B) | LLM backend for reasoning and text generation |
| spaCy | Named entity recognition for resume parsing |
| pdfplumber | PDF text extraction |

### Machine Learning & Data
| Technology | Purpose |
|---|---|
| scikit-learn | Gradient Boosting salary prediction model |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Plotly | Interactive charts and dashboards |

### APIs & Integrations
| Technology | Purpose |
|---|---|
| JSearch (RapidAPI) | Live job listings from LinkedIn, Indeed, Glassdoor |
| Telegram Bot API | Real-time job alert notifications |
| Requests | HTTP calls to external APIs |

### Storage & Reports
| Technology | Purpose |
|---|---|
| SQLite | Job tracker and alert preferences |
| ReportLab | PDF report generation |
| OpenPyXL | Excel report generation |
| python-dotenv | Secure API key management |

---

## 📁 Project Structure
ai-career-copilot/

│

├── app.py                    ← Homepage + sidebar navigation

├── .env                      ← API keys (not uploaded to GitHub)

├── requirements.txt          ← All dependencies

│

├── pages/

│   ├── 1_resume.py           ← Resume upload + spaCy NLP analysis

│   ├── 2_gap_analysis.py     ← Skill gap + salary impact

│   ├── 5_interview.py        ← Interview prep + AI scoring

│   ├── 6_tracker.py          ← Job application tracker

│   ├── 7_jobs.py             ← Live job search

│   ├── 8_salary.py           ← Salary predictor ML model

│   ├── 11_alerts.py          ← Telegram job alerts

│   └── 12_reports.py         ← PDF & Excel downloads

│

├── utils/

│   ├── pdf_reader.py         ← PDF extraction + skill detection + ATS

│   ├── llm_helper.py         ← All LangChain/Groq prompt chains

│   ├── salary_model.py       ← Gradient Boosting model

│   ├── job_fetcher.py        ← JSearch API integration

│   ├── database.py           ← SQLite CRUD operations

│   ├── telegram_alerts.py    ← Telegram Bot API

│   └── report_generator.py   ← PDF + Excel generation

│

└── data/

└── careers.db            ← SQLite database (auto-created)

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/mahajansakshi1205-sys/ai-career-copilot.git
cd ai-career-copilot
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Create `.env` file
```env
GROQ_API_KEY=your_groq_api_key
RAPIDAPI_KEY=your_rapidapi_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

**Get your free API keys:**
- Groq → [console.groq.com](https://console.groq.com)
- RapidAPI JSearch → [rapidapi.com](https://rapidapi.com) → search "JSearch"
- Telegram Bot → message @BotFather on Telegram → /newbot

### 5. Run the app
```bash
streamlit run app.py
```

### 6. Open browser
http://localhost:8501

---

## 📸 How It Works
Upload Resume PDF

↓

spaCy NLP extracts 70+ skills across 8 categories

↓

Paste any Job Description

↓

Groq LLM finds skill gaps + salary impact per skill

↓

ML model predicts your salary range

↓

Search live jobs — each scored against your resume

↓

Practice interview questions with AI feedback

↓

Track all applications in one dashboard

↓

Get Telegram alerts for new matching jobs

↓

Download PDF/Excel reports
---

## 📦 Requirements

```txt
streamlit
langchain
langchain-groq
langchain-core
groq
pandas
numpy
plotly
pdfplumber
spacy
scikit-learn
requests
python-dotenv
fastapi
uvicorn
reportlab
openpyxl
python-telegram-bot
```

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GROQ_API_KEY` | Groq LLM API key (free) | console.groq.com |
| `RAPIDAPI_KEY` | JSearch job listings API | rapidapi.com |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | api.telegram.org/botTOKEN/getUpdates |

---

## 👩‍💻 Built By

**Sakshi Mahajan**
B.Tech Computer Science & Engineering
Medicaps University, Indore (2023–2027)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/sakshi-mahajan)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/mahajansakshi1205-sys)

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE)

---

⭐ If you found this useful, please give it a star!
