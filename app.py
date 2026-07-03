"""
AI Lead Qualification & Follow-up Agent
Streamlit Web UI — seamless integration with the FastAPI backend.
"""

import streamlit as st
import requests
import time

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Lead Qualifier",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ─────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000/api/v1"
PRIORITY_COLORS = {"Hot": "#ff4b4b", "Warm": "#ffa500", "Cold": "#4b8bf4"}
PRIORITY_ICONS  = {"Hot": "🔥", "Warm": "🔶", "Cold": "❄️"}

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e0e0e0;
  }

  /* ── App background ── */
  [data-testid="stAppViewContainer"] { background: #0d0d16; }
  [data-testid="stHeader"]           { background: transparent; }
  [data-testid="stDecoration"]       { display: none; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #0a0a12;
    border-right: 1px solid #1e1e32;
  }
  [data-testid="stSidebar"] * { color: #c8c8d8 !important; }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] .stMarkdown strong { color: #ffffff !important; }

  /* ── Cards ── */
  .card {
    background: #13131f;
    border: 1px solid #1e1e35;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    transition: border-color .25s ease, box-shadow .25s ease;
  }
  .card:hover {
    border-color: #5865f2;
    box-shadow: 0 4px 24px rgba(88,101,242,.12);
  }

  /* ── Metric tiles ── */
  .metric-tile {
    background: #13131f;
    border: 1px solid #1e1e35;
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
  }
  .metric-tile .value { font-size: 2.2rem; font-weight: 700; color: #7c83fd; line-height: 1; }
  .metric-tile .label { font-size: 0.72rem; color: #666; text-transform: uppercase; letter-spacing: .1em; margin-top: 6px; }

  /* ── Priority badges ── */
  .badge-hot  { background: rgba(255,75,75,.14); color:#ff4b4b; border:1px solid rgba(255,75,75,.3);  padding:3px 11px; border-radius:20px; font-size:.82rem; font-weight:600; white-space:nowrap; }
  .badge-warm { background: rgba(255,165,0,.14); color:#ffa500; border:1px solid rgba(255,165,0,.3); padding:3px 11px; border-radius:20px; font-size:.82rem; font-weight:600; white-space:nowrap; }
  .badge-cold { background: rgba(75,139,244,.14); color:#4b8bf4; border:1px solid rgba(75,139,244,.3); padding:3px 11px; border-radius:20px; font-size:.82rem; font-weight:600; white-space:nowrap; }
  .badge-unknown { background:rgba(150,150,150,.14); color:#aaa; border:1px solid rgba(150,150,150,.3); padding:3px 11px; border-radius:20px; font-size:.82rem; font-weight:600; }

  /* ── Score bar ── */
  .score-track { background:#1a1a2e; border-radius:4px; height:8px; overflow:hidden; margin:10px 0; }
  .score-fill  { height:100%; border-radius:4px; transition:width .6s ease; }

  /* ── Email preview ── */
  .email-box {
    background: #0f0f1e;
    border: 1px solid #1e1e35;
    border-radius: 12px;
    padding: 22px;
    font-size: .9rem;
    line-height: 1.75;
    color: #c8c8d8;
    white-space: pre-wrap;
  }
  .email-subject { color: #7c83fd; font-weight: 600; font-size: 1rem; margin-bottom: 14px; }
  .email-divider { border:none; border-top:1px solid #1e1e35; margin:10px 0; }

  /* ── Step pill ── */
  .step-pill {
    display:inline-block;
    background:#7c83fd18;
    border:1px solid #7c83fd44;
    color:#7c83fd;
    padding:2px 10px;
    border-radius:20px;
    font-size:.72rem;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:.08em;
    margin-bottom:6px;
  }

  /* ── Section header ── */
  .section-header {
    font-size:1.2rem; font-weight:700; color:#fff;
    border-bottom:2px solid #7c83fd33;
    padding-bottom:8px; margin-bottom:18px;
  }

  /* ── Inputs ── */
  [data-testid="stTextInput"] input,
  [data-testid="stTextArea"] textarea,
  [data-testid="stNumberInput"] input {
    background:#0f0f1e !important;
    border:1px solid #1e1e35 !important;
    color:#e0e0e0 !important;
    border-radius:8px !important;
  }
  [data-testid="stTextInput"] input:focus,
  [data-testid="stTextArea"] textarea:focus {
    border-color:#5865f2 !important;
    box-shadow:0 0 0 2px rgba(88,101,242,.2) !important;
  }
  [data-baseweb="select"] { background:#0f0f1e !important; }
  [data-baseweb="select"] > div { background:#0f0f1e !important; border-color:#1e1e35 !important; }

  /* ── Buttons ── */
  [data-testid="stButton"] > button,
  [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #5865f2, #7c83fd);
    color:#fff; border:none; border-radius:10px;
    font-weight:600; padding:10px 26px;
    transition:opacity .2s ease, transform .15s ease;
    width:100%;
  }
  [data-testid="stButton"] > button:hover,
  [data-testid="stFormSubmitButton"] > button:hover { opacity:.88; transform:translateY(-1px); }

  /* ── Tabs ── */
  [data-baseweb="tab-list"] { background:#13131f; border-radius:10px; padding:4px; gap:4px; }
  [data-baseweb="tab"]      { border-radius:8px !important; color:#888 !important; }
  [aria-selected="true"]    { background:#5865f222 !important; color:#7c83fd !important; }

  /* ── Expander ── */
  [data-testid="stExpander"] { background:#13131f; border:1px solid #1e1e35; border-radius:10px; }
  [data-testid="stExpander"] summary { color:#c8c8d8 !important; }

  /* ── Alerts ── */
  .stSuccess { background:#0d1f14 !important; border:1px solid #1a4d2a !important; }
  .stError   { background:#1f0d0d !important; border:1px solid #4d1a1a !important; }
  .stInfo    { background:#0d0f1f !important; border:1px solid #1a1e4d !important; }
  .stWarning { background:#1f1a0d !important; border:1px solid #4d3a1a !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width:6px; }
  ::-webkit-scrollbar-track { background:#0d0d16; }
  ::-webkit-scrollbar-thumb { background:#1e1e35; border-radius:3px; }
  ::-webkit-scrollbar-thumb:hover { background:#2a2a4e; }

  /* ── Page header ── */
  .page-header { margin-bottom:24px; }
  .page-header h1 { color:#fff; font-size:1.75rem; font-weight:700; margin:0; }
  .page-header p  { color:#777; font-size:.9rem; margin-top:4px; }
  .page-divider   { border:none; border-top:1px solid #1e1e35; margin:18px 0; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────
def api_post(endpoint: str, payload: dict) -> tuple[dict | None, int, str | None]:
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=payload, timeout=30)
        if r.status_code == 200:
            return r.json(), 200, None
        return None, r.status_code, r.json().get("detail", r.text)
    except requests.exceptions.ConnectionError:
        return None, 0, "Cannot connect to backend at http://localhost:8000. Make sure the server is running."
    except Exception as e:
        return None, 0, str(e)


def api_get(endpoint: str) -> tuple[dict | None, str | None]:
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to backend."
    except Exception as e:
        return None, str(e)


def score_color(score: int) -> str:
    if score >= 80: return "#ff4b4b"
    if score >= 50: return "#ffa500"
    return "#4b8bf4"


def badge(priority: str | None) -> str:
    """Render a colored priority badge. Safely handles None."""
    if not priority or not isinstance(priority, str):
        return '<span class="badge-unknown">— Unknown</span>'
    key = priority.strip().lower()
    icon = PRIORITY_ICONS.get(priority.strip(), "")
    return f'<span class="badge-{key}">{icon} {priority.strip()}</span>'


@st.cache_data(ttl=5)
def check_server() -> bool:
    """Cache the health check for 5 s to avoid hammering the backend on reruns."""
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f'<div class="page-header"><h1>{icon} {title}</h1>'
        + (f'<p>{subtitle}</p>' if subtitle else "")
        + '</div><hr class="page-divider">',
        unsafe_allow_html=True,
    )


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 AI Lead Qualifier")
    st.markdown("---")

    server_ok = check_server()
    if server_ok:
        st.success("✅ Backend Online")
    else:
        st.error("❌ Backend Offline")
        st.caption("Start: `python backend/main.py`")

    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "📋 Analyze Lead", "⭐ Score Lead", "✉️ Generate Email", "🔄 Full Pipeline", "📂 All Leads"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Powered by Gemini AI · Python 3.12 · FastAPI")


# ─── Test email fixture ────────────────────────────────────────────────────────
TEST_EMAIL = {
    "company":     "NexaSoft Technologies",
    "priority":    "Hot",
    "budget":      "$150K–$300K",
    "timeline":    "Q3 2025",
    "requirement": (
        "We need an AI-powered lead qualification and CRM automation system. "
        "Our sales team of 45 reps is manually reviewing 500+ leads per week, "
        "causing slow response times and lost deals. We want automated scoring, "
        "priority routing, and personalized outreach at scale within 60 days."
    ),
}

TEST_LEAD = {
    "name":     "Sarah Mitchell",
    "email":    "s.mitchell@nexasoft.io",
    "company":  "NexaSoft Technologies",
    "industry": "SaaS / Enterprise Software",
    "emp":      420,
    "message": (
        "Hi, I'm the VP of Revenue Operations at NexaSoft Technologies (420 employees, Series B). "
        "We're looking to implement an AI-driven lead qualification platform to replace our current "
        "manual process. Our reps spend 3+ hours/day triaging leads and we're losing hot prospects. "
        "Budget is $150K–$300K and we need something live by Q3 2025. Happy to schedule a call this week."
    ),
}


# ─── Page: Dashboard ───────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    page_header("🤖", "AI Lead Qualification Dashboard",
                "Intelligent lead analysis, scoring & outreach — all in one place.")

    col1, col2, col3, col4 = st.columns(4)
    tiles = [
        ("3", "AI Agents"), ("∞", "Leads / Day"),
        ("0–100", "Score Range"), ("~2 s", "Avg Response"),
    ]
    for col, (val, lbl) in zip([col1, col2, col3, col4], tiles):
        col.markdown(
            f'<div class="metric-tile"><div class="value">{val}</div><div class="label">{lbl}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    agents = [
        ("Agent 1", "🔍 Lead Analysis",
         "Extracts structured insights from raw CRM data — industry, pain points, budget, timeline, and engagement level."),
        ("Agent 2", "⭐ Lead Scoring",
         "Multi-criteria scoring assigns 0–100 priority score (Hot / Warm / Cold) with confidence & reasoning."),
        ("Agent 3", "✉️ Email Generator",
         "Writes professional, tone-adapted B2B outreach emails tailored to lead priority level."),
    ]
    for col, (pill, title, desc) in zip([c1, c2, c3], agents):
        col.markdown(
            f'<div class="card"><div class="step-pill">{pill}</div>'
            f'<h3 style="color:#fff;margin:8px 0 4px">{title}</h3>'
            f'<p style="color:#888;font-size:.88rem;line-height:1.55;margin:0">{desc}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔗 Quick API Reference"):
        st.code("""POST /api/v1/leads/analyze        → Extract lead insights
POST /api/v1/leads/score          → Priority score (0–100)
POST /api/v1/leads/generate-email → Personalized outreach
GET  /api/v1/leads/               → List all leads
GET  /api/docs                    → Swagger UI""")


# ─── Page: Analyze Lead ────────────────────────────────────────────────────────
elif page == "📋 Analyze Lead":
    page_header("📋", "Lead Analysis", "Extract structured intelligence from raw lead information.")

    with st.form("analyze_form"):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full Name *",      value=TEST_LEAD["name"],    placeholder="Sarah Mitchell")
            email    = st.text_input("Email *",           value=TEST_LEAD["email"],   placeholder="sarah@company.com")
            company  = st.text_input("Company *",         value=TEST_LEAD["company"], placeholder="Acme Corp")
        with c2:
            industry = st.text_input("Industry *",        value=TEST_LEAD["industry"], placeholder="Financial Services")
            emp      = st.number_input("Employee Count *", min_value=1, value=TEST_LEAD["emp"])

        message = st.text_area("Lead Message / Context *", value=TEST_LEAD["message"], height=130)
        submitted = st.form_submit_button("🔍 Analyze Lead", use_container_width=True)

    if submitted:
        payload = {"name": name, "email": email, "company": company,
                   "industry": industry, "employee_count": int(emp), "lead_message": message}
        with st.spinner("Analyzing lead with AI…"):
            data, status, error = api_post("/leads/analyze", payload)

        if error:
            st.error(f"**{status} Error:** {error}")
        else:
            st.success("✅ Analysis complete!")
            a = data["analysis"]

            col1, col2, col3 = st.columns(3)
            col1.metric("Industry",  a.get("industry", "—"))
            col2.metric("Budget",    a.get("budget") or a.get("estimated_budget") or "—")
            col3.metric("Timeline",  a.get("timeline") or a.get("decision_timeline") or "—")

            st.markdown("<hr class='page-divider'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**📌 Summary**");    st.info(a.get("summary", "—"))
                st.markdown("**🎯 Requirement**"); st.info(a.get("requirement", "—"))
                st.markdown("**⚡ Urgency**");     st.info(a.get("urgency", "—"))
            with c2:
                st.markdown("**😣 Pain Points**")
                pains = a.get("pain_points", [])
                if isinstance(pains, list):
                    for p in pains:
                        st.markdown(f"• {p}")
                else:
                    st.write(pains)
                st.markdown("**🏢 Company Size**"); st.info(a.get("company_size", "—"))

            with st.expander("📄 Raw JSON"):
                st.json(data)

            st.session_state["last_analysis"] = data


# ─── Page: Score Lead ──────────────────────────────────────────────────────────
elif page == "⭐ Score Lead":
    page_header("⭐", "Lead Scoring", "Run the multi-criteria scoring algorithm to assign a priority level.")

    with st.form("score_form"):
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *",      value=TEST_LEAD["name"],    placeholder="John Smith")
            email   = st.text_input("Email *",           value=TEST_LEAD["email"],   placeholder="john@company.com")
            company = st.text_input("Company *",         value=TEST_LEAD["company"], placeholder="Tech Corp")
        with c2:
            industry = st.text_input("Industry *",       value=TEST_LEAD["industry"], placeholder="Software")
            emp      = st.number_input("Employee Count *", min_value=1, value=TEST_LEAD["emp"])

        message = st.text_area("Lead Message *", value=TEST_LEAD["message"], height=100)

        st.markdown("**📊 Analysis Context** (optional override)")
        cc1, cc2 = st.columns(2)
        with cc1:
            summary  = st.text_input("Summary",  value="AI qualification solution needed")
            budget   = st.text_input("Budget",   value="$150K–$300K")
        with cc2:
            timeline = st.text_input("Timeline", value="Q3 2025")
            urgency  = st.text_input("Urgency",  value="High")

        submitted = st.form_submit_button("⭐ Score Lead", use_container_width=True)

    if submitted:
        analysis = {
            "summary": summary, "requirement": summary, "budget": budget,
            "timeline": timeline, "urgency": urgency, "company_size": str(emp),
            "industry": industry, "pain_points": ["Evaluated from lead message"],
            "company_name": company, "estimated_budget": budget,
            "decision_timeline": timeline, "engagement_level": urgency,
            "technology_stack": [], "key_decision_makers": [],
        }
        payload = {"name": name, "email": email, "company": company,
                   "industry": industry, "employee_count": int(emp),
                   "lead_message": message, "analysis": analysis}
        with st.spinner("Scoring lead…"):
            data, status, error = api_post("/leads/score", payload)

        if error:
            st.error(f"**{status} Error:** {error}")
        else:
            s = data["scoring"]
            score    = s.get("lead_score") or s.get("score", 0)
            priority = s.get("priority", "Cold")
            conf     = s.get("confidence", 0)
            color    = score_color(score)

            st.success("✅ Scoring complete!")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                st.markdown(
                    f'<div class="metric-tile"><div class="value" style="color:{color}">{score}</div>'
                    f'<div class="label">Lead Score</div></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="metric-tile"><div class="value" style="font-size:1.7rem">'
                    f'{PRIORITY_ICONS.get(priority, "")} {priority}</div>'
                    f'<div class="label">Priority Level</div></div>',
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown("**Score Bar**")
                st.markdown(
                    f'<div class="score-track"><div class="score-fill" style="width:{score}%;background:{color}"></div></div>'
                    f'<div style="color:#888;font-size:.85rem">Confidence: {conf}%</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr class='page-divider'>", unsafe_allow_html=True)
            st.markdown("**🧠 Reasoning**")
            for r in s.get("reasoning", []):
                st.markdown(f"• {r}")

            with st.expander("📄 Raw JSON"):
                st.json(data)

            st.session_state["last_scoring"] = data


# ─── Page: Generate Email ──────────────────────────────────────────────────────
elif page == "✉️ Generate Email":
    page_header("✉️", "Email Generator", "Generate a personalized outreach email adapted to lead priority.")

    st.info("📧 **Test data pre-filled** — just click *Generate Email* to see a live result!", icon="💡")

    with st.form("email_form"):
        c1, c2 = st.columns(2)
        with c1:
            company  = st.text_input("Company *",  value=TEST_EMAIL["company"],  placeholder="Enterprise Corp")
            priority = st.selectbox("Priority *", ["Hot", "Warm", "Cold"],
                                    index=["Hot", "Warm", "Cold"].index(TEST_EMAIL["priority"]))
        with c2:
            budget   = st.text_input("Budget",   value=TEST_EMAIL["budget"],   placeholder="$50K–$100K")
            timeline = st.text_input("Timeline", value=TEST_EMAIL["timeline"], placeholder="Q4 2025")

        requirement = st.text_area("Requirement / Use-case *",
                                   value=TEST_EMAIL["requirement"], height=110)
        submitted = st.form_submit_button("✉️ Generate Email", use_container_width=True)

    if submitted:
        payload = {"company": company, "requirement": requirement,
                   "budget": budget, "timeline": timeline, "priority": priority}
        with st.spinner("Writing email with AI…"):
            data, status, error = api_post("/leads/generate-email", payload)

        if error:
            st.error(f"**{status} Error:** {error}")
        else:
            ec      = data["email_content"]
            subject = ec.get("subject", "")
            body    = ec.get("email", "")

            st.success("✅ Email generated!")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("**📧 Email Preview**")
                st.markdown(
                    f'<div class="email-box">'
                    f'<div class="email-subject">Subject: {subject}</div>'
                    f'<hr class="email-divider">'
                    f'<div>{body}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown("**📋 Metadata**")
                st.markdown(f"**Company:** {data.get('company', company)}")
                st.markdown(f"**Priority:** {badge(priority)}", unsafe_allow_html=True)
                st.markdown(f"**Characters:** {len(body):,}")
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    "⬇️ Download .txt",
                    data=f"Subject: {subject}\n\n{body}",
                    file_name=f"email_{company.lower().replace(' ', '_')}.txt",
                )

            with st.expander("📄 Raw JSON"):
                st.json(data)


# ─── Page: Full Pipeline ───────────────────────────────────────────────────────
elif page == "🔄 Full Pipeline":
    page_header("🔄", "Full Pipeline",
                "Run a lead through all three agents in sequence — Analysis → Scoring → Email.")

    with st.form("pipeline_form"):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full Name *",      value=TEST_LEAD["name"],    placeholder="Mike Chen")
            email    = st.text_input("Email *",           value=TEST_LEAD["email"],   placeholder="mike@startup.io")
            company  = st.text_input("Company *",         value=TEST_LEAD["company"], placeholder="StartupXYZ")
        with c2:
            industry = st.text_input("Industry *",        value=TEST_LEAD["industry"], placeholder="Technology")
            emp      = st.number_input("Employee Count *", min_value=1, value=TEST_LEAD["emp"])

        message = st.text_area("Lead Message / Context *", value=TEST_LEAD["message"], height=120)
        submitted = st.form_submit_button("🚀 Run Full Pipeline", use_container_width=True)

    if submitted:
        base = {"name": name, "email": email, "company": company,
                "industry": industry, "employee_count": int(emp), "lead_message": message}

        st.markdown("<hr class='page-divider'>", unsafe_allow_html=True)

        # Step 1 — Analyze
        st.markdown('<div class="step-pill">Step 1 / 3</div> 🔍 Analyzing lead…', unsafe_allow_html=True)
        with st.spinner(""):
            data1, s1, e1 = api_post("/leads/analyze", base)
        if e1:
            st.error(f"Analysis failed: {e1}"); st.stop()
        a = data1["analysis"]
        st.success(f"✅ Analysis — Budget: **{a.get('budget') or a.get('estimated_budget', '—')}** · Industry: **{a.get('industry', '—')}**")

        # Step 2 — Score
        analysis_payload = {
            **a,
            "company_name": a.get("company_name", company),
            "estimated_budget": a.get("estimated_budget") or a.get("budget", ""),
            "decision_timeline": a.get("decision_timeline") or a.get("timeline", ""),
            "engagement_level": a.get("engagement_level") or a.get("urgency", ""),
            "technology_stack": a.get("technology_stack", []),
            "key_decision_makers": a.get("key_decision_makers", []),
        }
        payload2 = {**base, "analysis": analysis_payload}

        st.markdown('<div class="step-pill">Step 2 / 3</div> ⭐ Scoring lead…', unsafe_allow_html=True)
        with st.spinner(""):
            data2, s2, e2 = api_post("/leads/score", payload2)
        if e2:
            st.error(f"Scoring failed: {e2}"); st.stop()
        sc       = data2["scoring"]
        score    = sc.get("lead_score") or sc.get("score", 0)
        priority = sc.get("priority", "Cold")
        color    = score_color(score)
        st.success(f"✅ Score — **{score}/100** · {badge(priority)}", unsafe_allow_html=True)

        # Step 3 — Email
        req_text = a.get("requirement", message[:150])
        payload3 = {
            "company": company, "requirement": req_text,
            "budget": a.get("budget") or a.get("estimated_budget", "TBD"),
            "timeline": a.get("timeline") or a.get("decision_timeline", "TBD"),
            "priority": priority,
        }

        st.markdown('<div class="step-pill">Step 3 / 3</div> ✉️ Writing email…', unsafe_allow_html=True)
        with st.spinner(""):
            data3, s3, e3 = api_post("/leads/generate-email", payload3)
        if e3:
            st.error(f"Email generation failed: {e3}"); st.stop()
        ec      = data3["email_content"]
        subject = ec.get("subject", "")
        body    = ec.get("email", "")
        st.success(f"✅ Email — Subject: **{subject}**")

        # ── Results ──
        st.markdown("<hr class='page-divider'>", unsafe_allow_html=True)
        st.markdown("## 🎯 Pipeline Results")

        c1, c2, c3 = st.columns(3)
        c1.metric("Lead Score",   f"{score}/100")
        c2.metric("Priority",     f"{PRIORITY_ICONS.get(priority, '')} {priority}")
        c3.metric("Confidence",   f"{sc.get('confidence', 0)}%")

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🔍 Analysis", "⭐ Scoring", "✉️ Email"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Summary**"); st.info(a.get("summary", "—"))
                st.markdown("**Urgency**"); st.info(a.get("urgency", "—"))
            with col2:
                st.markdown("**Pain Points**")
                for p in (a.get("pain_points") or []):
                    st.markdown(f"• {p}")

        with tab2:
            st.markdown(
                f'<div class="score-track"><div class="score-fill" style="width:{score}%;background:{color}"></div></div>',
                unsafe_allow_html=True,
            )
            st.markdown("**Reasoning**")
            for r in sc.get("reasoning", []):
                st.markdown(f"• {r}")

        with tab3:
            st.markdown(
                f'<div class="email-box">'
                f'<div class="email-subject">Subject: {subject}</div>'
                f'<hr class="email-divider">'
                f'<div>{body}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Download Email",
                data=f"Subject: {subject}\n\n{body}",
                file_name=f"email_{company.lower().replace(' ', '_')}.txt",
            )


# ─── Page: All Leads ───────────────────────────────────────────────────────────
elif page == "📂 All Leads":
    page_header("📂", "All Leads", "Browse all leads stored in the database.")

    col_r, _ = st.columns([1, 5])
    with col_r:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()

    data, error = api_get("/leads/")
    if error:
        st.error(error)
    elif not data:
        st.info("No leads in the database yet. Run the Full Pipeline to add some!")
    else:
        leads = data if isinstance(data, list) else data.get("leads", [])
        total = len(leads)
        hot   = sum(1 for l in leads if l.get("priority") == "Hot")
        warm  = sum(1 for l in leads if l.get("priority") == "Warm")
        cold  = sum(1 for l in leads if l.get("priority") == "Cold")

        c1, c2, c3, c4 = st.columns(4)
        for col, (val, lbl) in zip(
            [c1, c2, c3, c4],
            [(total, "Total Leads"), (f"🔥 {hot}", "Hot"), (f"🔶 {warm}", "Warm"), (f"❄️ {cold}", "Cold")],
        ):
            col.markdown(
                f'<div class="metric-tile"><div class="value">{val}</div><div class="label">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr class='page-divider'>", unsafe_allow_html=True)
        for lead in leads:
            priority_val = lead.get("priority") or "Unknown"
            label = (
                f"**{lead.get('name', '—')}** @ {lead.get('company', '—')} — "
                f"{PRIORITY_ICONS.get(priority_val, '')} {priority_val}"
            )
            with st.expander(label, expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Email:** {lead.get('email', '—')}")
                c2.write(f"**Score:** {lead.get('lead_score', '—')}")
                c3.write(f"**Status:** {lead.get('status', '—')}")
                if lead.get("email_subject"):
                    st.markdown(f"**Email Subject:** {lead['email_subject']}")
                # Show badge in expander body (safe to render HTML here)
                st.markdown(
                    f"**Priority:** {badge(priority_val)}",
                    unsafe_allow_html=True,
                )
