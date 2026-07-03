# AI Lead Qualification & Follow-up Agent

A professional AI-powered web application that helps sales teams analyze incoming leads using the Google Gemini API. This application provides automated lead qualification, scoring, and personalized follow-up generation.

## 🎯 Overview

The AI Lead Qualification & Follow-up Agent streamlines the sales process by:
- **Automatically qualifying leads** based on predefined criteria
- **Generating AI-powered insights** about lead potential
- **Creating personalized follow-up messages** using natural language processing
- **Tracking lead status** through an intuitive dashboard
- **Providing actionable recommendations** for sales teams

## 🏗️ Project Structure

```
AI_LEAD/
├── backend/                    # FastAPI backend application
│   ├── agents/                # AI agents for lead analysis
│   │   └── lead_analyzer.py   # Lead qualification and analysis logic
│   ├── api/                   # API endpoints
│   │   ├── routes/            # Route handlers
│   │   │   ├── health.py      # Health check endpoints
│   │   │   └── leads.py       # Lead management endpoints
│   │   └── __init__.py
│   ├── services/              # Business logic services
│   │   ├── gemini_service.py  # Gemini API integration
│   │   └── lead_service.py    # Lead database operations
│   ├── database/              # Database configuration
│   │   └── database.py        # SQLAlchemy setup
│   ├── models/                # Database models
│   │   └── lead.py            # Lead ORM model
│   ├── schemas/               # Pydantic schemas (validation)
│   │   └── lead_schema.py     # Lead API schemas
│   ├── config/                # Configuration management
│   │   └── settings.py        # Environment settings
│   ├── utils/                 # Utility functions
│   │   └── logger.py          # Logging configuration
│   ├── prompts/               # AI prompt templates
│   │   └── lead_prompts.py    # Lead analysis prompts
│   ├── main.py                # FastAPI app entry point
│   └── __init__.py
│
├── frontend/                  # Streamlit frontend application
│   ├── app.py                 # Main Streamlit app
│   ├── pages/                 # Streamlit pages
│   │   ├── home.py            # Home/welcome page
│   │   └── dashboard.py       # Lead management dashboard
│   ├── components/            # Reusable UI components
│   │   └── ui_components.py   # Common Streamlit components
│   ├── assets/                # Static assets
│   └── __init__.py
│
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.104.1
- **Frontend**: Streamlit 1.28.1
- **Database**: SQLite with SQLAlchemy ORM
- **AI/LLM**: Google Gemini API
- **Data Validation**: Pydantic 2.5.2
- **Python**: 3.12+
- **Server**: Uvicorn

## 📋 Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Google Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Git (optional)

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd AI_LEAD
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root by copying `.env.example`:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./ai_lead.db
```

### 5. Initialize Database

The database is automatically initialized when the backend starts, but you can manually initialize it:

```bash
# This is handled automatically in main.py startup
```

### 6. Run the Application

#### Start Backend (FastAPI)

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
python -m backend.main
```

**macOS/Linux:**
```bash
export PYTHONPATH=.
python -m backend.main
```

The backend will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`
- Alternative Docs: `http://localhost:8000/api/redoc`

#### Start Frontend (Streamlit) - In a New Terminal

```bash
streamlit run frontend/app.py
```

The frontend will open at: `http://localhost:8501`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### Health Check
```
GET /health
```

#### Leads Management

**Create Lead:**
```
POST /leads
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Tech Corp",
  "phone": "+1234567890",
  "source": "Website",
  "notes": "Interested in premium plan"
}
```

**Get Lead:**
```
GET /leads/{lead_id}
```

**List Leads:**
```
GET /leads?skip=0&limit=10&status=new
```

**Update Lead:**
```
PUT /leads/{lead_id}
Content-Type: application/json
```

**Delete Lead:**
```
DELETE /leads/{lead_id}
```

**Get Qualified Leads:**
```
GET /leads/qualified/list?skip=0&limit=10
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API Key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./ai_lead.db` |
| `DEBUG` | Enable debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Database

The application uses SQLite by default. To use PostgreSQL:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/db_name
   ```

## 🤖 AI Features (Ready for Implementation)

The application structure is ready for AI implementation with:

- **Lead Analyzer Agent**: In `backend/agents/lead_analyzer.py`
- **Gemini Service**: In `backend/services/gemini_service.py`
- **Prompt Templates**: In `backend/prompts/lead_prompts.py`

To enable AI features:

1. Install Gemini SDK:
   ```bash
   pip install google-generativeai
   ```

2. Implement the `analyze_lead()` method in `backend/services/gemini_service.py`

3. Add your Gemini API key to `.env`

## 📊 Database Schema

### Leads Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(255) | Lead contact name |
| `email` | String(255) | Email address (unique) |
| `phone` | String(20) | Phone number |
| `company` | String(255) | Company name |
| `source` | String(100) | Lead source |
| `notes` | Text | Additional notes |
| `analysis` | Text | AI-generated analysis |
| `qualification_score` | Float | 0-100 score |
| `is_qualified` | Boolean | Qualification status |
| `status` | String(50) | Lead status |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

## 🧪 Testing

Run tests with:

```bash
pytest tests/
pytest tests/ -v  # Verbose mode
pytest tests/ --cov  # With coverage report
```

## 📝 Code Structure & Best Practices

### Architecture Principles

1. **Separation of Concerns**: Distinct layers for API, services, database, and UI
2. **DRY (Don't Repeat Yourself)**: Reusable components and services
3. **SOLID Principles**: Single responsibility, open/closed, Liskov substitution, etc.
4. **Type Hints**: Full type annotations for better IDE support and error detection
5. **Logging**: Comprehensive logging for debugging and monitoring
6. **Configuration Management**: Centralized settings using Pydantic

### Folder Organization

- **`agents/`**: AI agents containing decision logic
- **`api/routes/`**: API endpoint handlers
- **`services/`**: Business logic and external integrations
- **`database/`**: ORM and database configuration
- **`models/`**: SQLAlchemy models
- **`schemas/`**: Pydantic validation schemas
- **`config/`**: Application settings
- **`utils/`**: Helper functions and logging
- **`prompts/`**: AI prompt templates

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file with real keys
2. **CORS**: Configure allowed origins in production
3. **Input Validation**: All inputs validated with Pydantic
4. **SQL Injection**: Protected by SQLAlchemy ORM
5. **Error Handling**: Detailed errors logged, generic responses returned

## 🚢 Deployment

### Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "-m", "backend.main"]
```

Build and run:
```bash
docker build -t ai-lead-agent .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key ai-lead-agent
```

### Heroku/Cloud Platforms

1. Update `requirements.txt`
2. Create `Procfile`:
   ```
   web: python -m backend.main
   web: streamlit run frontend/app.py
   ```

## 📖 Development Workflow

1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Push to repository: `git push origin feature/your-feature`
4. Create a pull request

## 🐛 Troubleshooting

### Database Issues
- Delete `ai_lead.db` and restart to reinitialize
- Check `DATABASE_URL` in `.env`

### API Connection Issues
- Ensure backend is running: `python -m backend.main`
- Check port 8000 is not in use

### Gemini API Errors
- Verify API key is correct in `.env`
- Check API quotas in Google Cloud Console

### Streamlit Issues
- Clear cache: `streamlit cache clear`
- Reinstall: `pip install --upgrade streamlit`

## 📞 Support & Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Google Gemini API](https://ai.google.dev)

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎓 Next Steps

1. **Configure Gemini API**: Add your API key and implement AI logic
2. **Customize Prompts**: Modify lead analysis prompts in `backend/prompts/`
3. **Add Authentication**: Implement user authentication and authorization
4. **Extend Schema**: Add custom fields to leads based on your needs
5. **Deploy**: Move to production using Docker or cloud platforms
6. **Monitor**: Set up logging and monitoring for production

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Ready for AI Implementation
