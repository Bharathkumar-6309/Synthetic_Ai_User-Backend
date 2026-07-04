# Synthetic User Generation Platform

An AI-powered web application that lets product teams, startups, and researchers
simulate user research without needing real participants. The platform generates
realistic virtual personas who provide product feedback through surveys and
conversational interviews, then extracts actionable insights and exports a
professional research report.

---

## Project Overview

| | |
|---|---|
| **Frontend** | Streamlit (Python), Plotly visualizations |
| **Backend** | Planned — REST API (FastAPI/Flask/Spring Boot, your choice) |
| **AI Provider** | Groq API (LLM-powered persona generation & responses) |
| **Status** | Frontend complete and running on mock data · Backend not yet built |

### Target Users

| User Type | Use Case |
|---|---|
| Product Managers | Validate product ideas before development |
| Startup Founders | Test MVPs without user recruitment costs |
| UX Researchers | Conduct rapid user research |
| Student Teams | Academic projects with limited resources |
| Design Teams | Get early feedback on prototypes |

---

## Repository Structure

```
synthetic-user-generation-platform/
├── frontend/                  # Streamlit app — see frontend/README.md for details
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── services/
│   │   ├── api_client.py      # Single switchboard: mock data vs real backend
│   │   └── mock_data.py       # Fake persona/survey/insight generator
│   ├── utils/
│   ├── styles/
│   ├── config.py              # USE_MOCK_DATA toggle, backend URL, Groq settings
│   └── requirements.txt
│
└── backend/                   # Not yet built — see "Backend" section below
    ├── (planned) API layer implementing the contract in this README
    └── (planned) Groq integration for persona generation & responses
```

---

## Frontend

Multi-page Streamlit app covering the full workflow:

1. **Home** — overview, quick stats, recent experiments
2. **Experiment Workspace** — define product, audience, objectives, persona count
3. **Persona Gallery** — browse generated personas, filter, launch surveys/interviews
4. **Survey Mode** — ask all personas the same question(s), compare responses
5. **Interview Mode** — one-on-one chat with a persona, memory-aware
6. **Insights Dashboard** — adoption %, sentiment, theme clusters (Plotly charts)
7. **Report Generator** — preview and export a PDF research report

### Run it

```bash
cd frontend
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

It runs fully on **mock data** out of the box — no backend required to try the
whole flow end to end, including PDF export.

Full details, file-by-file breakdown, and the mock→real switch mechanism are in
[`frontend/README.md`](frontend/README.md).

---

## Backend (planned)

The backend isn't built yet. It needs to expose the following REST contract —
the frontend already calls these exact paths via `frontend/services/api_client.py`,
so once these exist you just flip `USE_MOCK_DATA=false`.

### Experiments
```
POST   /api/experiments              # Create experiment
GET    /api/experiments/{id}         # Get experiment details
PUT    /api/experiments/{id}         # Update experiment
DELETE /api/experiments/{id}         # Delete experiment
GET    /api/experiments              # List all experiments
```

### Personas
```
POST   /api/personas/generate        # Generate personas (calls Groq)
GET    /api/personas/{id}            # Get persona details
GET    /api/personas/experiment/{id} # Get personas for experiment
```

### Survey
```
POST   /api/survey/run               # Run survey question across personas (calls Groq)
GET    /api/survey/results/{id}      # Get survey results
```

### Interview
```
POST   /api/interview/start          # Start interview session
POST   /api/interview/message        # Send message, get persona reply (calls Groq)
GET    /api/interview/history/{id}   # Get chat history
DELETE /api/interview/end/{id}       # End interview
```

### Insights
```
POST   /api/insights/extract         # Extract themes/sentiment (calls Groq)
GET    /api/insights/{id}            # Get insights
```

### Reports
```
POST   /api/reports/generate         # Generate report data
GET    /api/reports/{id}             # Get report data
```

### Why Groq lives on the backend, not the frontend

The backend should hold the `GROQ_API_KEY` and make all Groq calls server-side.
This keeps the key out of the browser/Streamlit client and gives you one place
to control prompts, rate limits, and caching for persona generation, survey
scoring, interview replies, and insight extraction.

### Suggested stack

Any framework works as long as it implements the contract above — FastAPI,
Flask, or Spring Boot are all reasonable choices. FastAPI is a natural fit if
you want to stay in Python end-to-end alongside the Streamlit frontend.

---

## Environment Variables

| Variable | Where | Purpose |
|---|---|---|
| `USE_MOCK_DATA` | frontend | `true` while backend is unbuilt, `false` once live |
| `BACKEND_BASE_URL` | frontend | Base URL of your backend API |
| `GROQ_API_KEY` | backend | Groq API key (server-side only) |
| `GROQ_MODEL` | backend | Groq model name, e.g. `llama-3.3-70b-versatile` |

---

## Roadmap

- [x] Streamlit frontend — all 7 pages, mock data mode
- [x] PDF report export
- [ ] Backend API implementing the contract above
- [ ] Groq integration for persona generation, survey, interview, insights
- [ ] Swap frontend to live mode (`USE_MOCK_DATA=false`)
- [ ] Persistence (database for experiments/personas/results)
- [ ] Auth (if multi-user)
- [ ] Deployment (frontend + backend hosting)

---

## Success Metrics

**User Experience**
- Time to complete first experiment: < 5 minutes
- Error rate: < 2%

**Performance**
- Page load time: < 2 seconds
- Persona generation display: < 3 seconds
- Dashboard rendering: < 1 second

**Functionality**
- All 7 frontend pages working
- All backend endpoints integrated
- Export features functional
