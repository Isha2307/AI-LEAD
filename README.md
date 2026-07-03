# 🤖 AI Lead Qualifier

An AI-powered lead qualification platform for sales teams. Automatically analyzes, scores, and generates personalized outreach emails for incoming leads using Google Gemini AI.

---

## 🎯 What It Does

| Feature | Description |
|---|---|
| 🔍 **Lead Analysis** | Extracts structured insights — industry, pain points, budget, timeline |
| ⭐ **Lead Scoring** | 0–100 priority score with Hot / Warm / Cold classification |
| ✉️ **Email Generator** | Personalized B2B outreach emails adapted to lead priority |
| 🔄 **Full Pipeline** | Run all three agents in sequence from a single form |
| 📂 **Lead Database** | Browse and manage all stored leads |

---

## 🏗️ Project Structure

```
AI-LEAD/
├── backend/
│   ├── agents/
│   │   ├── lead_analyzer.py      # Lead analysis agent
│   │   ├── lead_scorer.py        # Lead scoring agent
│   │   └── email_generator.py    # Email generation agent
│   ├── api/routes/
│   │   ├── health.py             # Health check endpoint
│   │   └── leads.py              # Lead API endpoints
│   ├── services/
│   │   ├── gemini_service.py     # Google Gemini integration
│   │   └── lead_service.py       # Database operations
│   ├── database/database.py      # SQLAlchemy setup
│   ├── models/lead.py            # ORM models
│   ├── schemas/lead_schema.py    # Pydantic schemas
│   ├── config/settings.py        # Environment settings
│   ├── prompts/lead_prompts.py   # AI prompt templates
│   └── main.py                   # FastAPI entry point
├── app.py                        # Streamlit frontend
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Tech Stack

- **Backend** — FastAPI + Uvicorn
- **Frontend** — Streamlit (dark-theme UI)
- **Database** — SQLite via SQLAlchemy ORM
- **AI** — Google Gemini API (`gemini-pro`)
- **Validation** — Pydantic v2
- **Python** — 3.12+

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repo-url>
cd AI-LEAD
```

### 2. Create & activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```powershell
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` and set your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./ai_lead.db
```

Get a free key at [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## ▶️ Running the Application

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — Backend (FastAPI)

**Windows:**
```powershell
$env:PYTHONPATH = "c:\path\to\AI-LEAD"
& ".venv\Scripts\python.exe" backend\main.py
```

**macOS / Linux:**
```bash
PYTHONPATH=. python backend/main.py
```

Backend runs at → **http://localhost:8000**
- Swagger docs: http://localhost:8000/api/docs

### Terminal 2 — Frontend (Streamlit)

**Windows:**
```powershell
& ".venv\Scripts\streamlit.exe" run app.py
```

**macOS / Linux:**
```bash
streamlit run app.py
```

Frontend runs at → **http://localhost:8501**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/v1/health` | Backend health check |
| `POST` | `/api/v1/leads/analyze` | Analyze a lead |
| `POST` | `/api/v1/leads/score` | Score a lead (0–100) |
| `POST` | `/api/v1/leads/generate-email` | Generate outreach email |
| `GET`  | `/api/v1/leads/` | List all leads |
| `GET`  | `/api/docs` | Interactive Swagger UI |

### Example: Analyze a Lead

```bash
curl -X POST http://localhost:8000/api/v1/leads/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Mitchell",
    "email": "s.mitchell@nexasoft.io",
    "company": "NexaSoft Technologies",
    "industry": "SaaS",
    "employee_count": 420,
    "lead_message": "We need AI-powered lead qualification. Budget $150K, timeline Q3 2025."
  }'
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | **Required** |
| `DATABASE_URL` | Database connection string | `sqlite:///./ai_lead.db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `False` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## 🔒 Security Notes

- Never commit your `.env` file — it's in `.gitignore`
- All API inputs are validated with Pydantic schemas
- SQLAlchemy ORM protects against SQL injection

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'fastapi'`**
→ You're using the global Python instead of the venv. Use `.venv\Scripts\python.exe` explicitly.

**Backend not connecting**
→ Ensure the backend is running on port 8000 before starting Streamlit.

**Gemini API errors**
→ Check your `GEMINI_API_KEY` in `.env` and verify quota at [Google Cloud Console](https://console.cloud.google.com).

**Database issues**
→ Delete `ai_lead.db` and restart the backend — it auto-initializes.

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

**Version:** 1.1.0 | **Updated:** July 2025 | **Status:** ✅ Production Ready
