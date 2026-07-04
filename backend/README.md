# Synthetic User Generation Platform — Backend

**Milestone 1 (Week 1-2): Experiment Workspace + Persona Generation Agent**

## What's implemented in this milestone

| Deliverable | Where |
|---|---|
| System architecture, agent roles, persona data model | this doc + `app/models/`, `app/agents/` |
| Experiment Workspace (product description, target audience, objectives) | `app/models/experiment.py`, `app/api/v1/endpoints/experiments.py` |
| Persona Generation Agent → visual persona cards | `app/agents/persona_agent.py`, `app/api/v1/endpoints/personas.py` |

Survey Mode, Interview Mode, Insight Extraction, and Report Generation are **not** part of this milestone — those land in Milestones 2-4 per the project plan. This backend is structured so those slot in without refactors (see "Where the next milestones plug in" below).

## Architecture

```
Client (frontend, separate repo)
        │  HTTP/JSON
        ▼
┌───────────────────────────────────────────────┐
│ FastAPI app (app/main.py)                     │
│  ├─ api/v1/endpoints/experiments.py           │  Experiment Workspace CRUD
│  ├─ api/v1/endpoints/personas.py              │  Trigger + list persona generation
│  └─ api/v1/deps.py                            │  DI (DB session, current user stub)
└───────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│ services/  (business logic, no HTTP concerns) │
│  ├─ experiment_service.py                     │
│  └─ persona_service.py  ── calls agent ↓, persists via repos
└───────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│ agents/persona_agent.py  (LangGraph)          │
│                                                │
│   generate ──▶ validate ──(ok)──▶ finalize ──▶ END
│      ▲            │(invalid, retries left)     │
│      └────────────┘                            │
│                    │(invalid, out of retries)   │
│                    ▼                            │
│            synthetic_fallback ──────────────────┘
└───────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│ ai/  (AI infrastructure)                      │
│  ├─ model_router.py   Gemini primary → Ollama fallback (config-driven)
│  ├─ llm_client.py     LiteLLM async wrapper, structured JSON output
│  └─ prompt_manager.py Loads/renders prompts from app/prompts/
└───────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│ models/ (SQLAlchemy ORM)  +  repositories/     │
│  ├─ user.py         (minimal, full auth = later milestone)
│  ├─ experiment.py    Experiment Workspace + status lifecycle
│  └─ persona.py       Persona data model (demographic/behavioral/psych)
└───────────────────────────────────────────────┘
        │
        ▼
   PostgreSQL (prod/staging) / SQLite (local dev, zero setup)
```

### Agent roles

- **Persona Generation Agent** (`app/agents/persona_agent.py`) — the only agent built in this milestone. Given an experiment's product description, target audience, and research objectives, it produces N structurally-validated `PersonaProfile` objects. It is provider-agnostic: it calls whichever model `ModelRouter` resolves to, and if no LLM is reachable at all, it degrades to a Faker-driven synthetic generator so the platform is fully demoable offline (important for the "no research budget" early-stage-startup use case the project targets).
- **Survey Agent / Insight Agent** — stubbed as future modules only (not implemented yet); `app/agents/` is where they'll live in Milestone 2/3, following the same LangGraph pattern.

### Persona data model

A persona has three profile layers, matching the milestone spec exactly:

1. **Demographic** — name, age, gender, occupation, location, income bracket, education
2. **Behavioral** — personality traits, behavioral patterns, tech savviness, daily habits
3. **Psychological** — core values, motivations, pain points, risk tolerance

Plus narrative/display fields (`bio`, `quote`, `avatar_seed`) for rendering persona cards on the frontend, and consistency fields (`persona_hash`, `consistency_seed`) that the Milestone-2 Persona Memory module will use to keep a persona's opinions stable across Survey/Interview turns.

### Experiment workflow (state machine)

`Experiment.status` moves: `draft → personas_ready → running → completed` (`archived` is a terminal side-state). This milestone implements `draft` (on creation) and the transition to `personas_ready` (after persona generation succeeds). `running`/`completed` are set by Milestones 2-4.

## Where the next milestones plug in

- **Milestone 2** (Survey Mode, Memory): add `app/memory/`, `app/agents/survey_agent.py`, and a `SurveyResponse` model FK'd to `Persona` + `Experiment`. `PersonaService` already returns fully-formed `Persona` rows to build against.
- **Milestone 3** (Interview Mode, Insight Agent): add `app/agents/insight_agent.py`; `Persona.product_fit_score` column already exists (currently nullable/unused) for the "would use this product" scoring.
- **Milestone 4** (Dashboard, Reports): add `app/tasks/report_tasks.py` (Celery + ReportLab) and a `reports.py` endpoint; no changes needed to Milestone-1 models.

## Running locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive Swagger docs.

By default `GEMINI_API_KEY` is empty, so persona generation runs entirely on the offline synthetic fallback — useful for the other developer building the frontend to integrate against without needing an API key. Set `GEMINI_API_KEY` in `.env` to switch to real LLM-generated personas.

## API surface (Milestone 1)

```
POST   /api/v1/experiments                          Create an experiment workspace
GET    /api/v1/experiments                          List your experiments
GET    /api/v1/experiments/{id}                      Get one experiment
PATCH  /api/v1/experiments/{id}                      Update product/audience/objectives
DELETE /api/v1/experiments/{id}                      Delete an experiment

POST   /api/v1/experiments/{id}/personas/generate    Generate persona cards (body: {persona_count?, regenerate?})
GET    /api/v1/experiments/{id}/personas             List persona cards for an experiment
```

`PersonaListResponse.items[]` is the exact shape the frontend should render as persona cards — see `app/schemas/response/persona.py`.

## Testing

```bash
cd backend
pytest
```

`tests/` includes a smoke test that runs the Persona Generation Agent end-to-end against the synthetic fallback path (no API key required) and asserts the returned personas satisfy the data model.
