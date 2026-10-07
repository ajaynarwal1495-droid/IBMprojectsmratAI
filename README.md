# SmartStudy AI

**AI-powered Smart Study Generator — Problem Statement No. 13**

SmartStudy AI is an agentic, IBM Granite-powered study assistant that accepts student study material (PDF, DOCX, TXT, and images) and generates personalised study resources: structured notes, concise summaries, key topics, flashcards, MCQ quizzes, personalised study plans, and a learning progress dashboard.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite 5, React Router 6, Axios, Recharts, CSS |
| Backend | Python 3.11, FastAPI, Pydantic v2, Uvicorn |
| AI | IBM Granite via IBM watsonx.ai |
| Cloud | IBM Cloud, IBM Cloud Object Storage, IBM Cloud Code Engine |
| Database | SQLite (local dev) → IBM Cloudant (production) via SQLAlchemy |
| Source Control | Git, GitHub |

---

## Project Structure

```
smart-study-ai/
├── frontend/               React + Vite frontend application
│   └── src/
│       ├── assets/         Static assets (images, icons)
│       ├── components/     Shared UI components (Navbar, etc.)
│       ├── context/        React context providers (AppContext)
│       ├── hooks/          Custom React hooks (useApi)
│       ├── pages/          One component per page/route
│       ├── services/       Axios-based API service modules
│       ├── utils/          Pure utility functions (formatters, validators)
│       ├── App.jsx         Root component with routing
│       ├── main.jsx        React DOM entry point
│       └── index.css       Global styles and design tokens
│
├── backend/                Python FastAPI backend
│   ├── main.py             FastAPI app entry point (keeps this file small)
│   ├── requirements.txt    Python dependencies
│   ├── Dockerfile          Multi-stage production Docker image
│   └── app/
│       ├── api/            Route handlers (one file per domain)
│       ├── agents/         AI agents (study, planner, exam, progress)
│       ├── core/           Config, logging, exceptions
│       ├── integrations/   IBM watsonx.ai, IBM COS, database
│       ├── models/         SQLAlchemy ORM models
│       ├── schemas/        Pydantic request/response schemas
│       ├── services/       Business logic services
│       └── utils/          File parsers, text cleaner, chunker
│
├── docs/                   Project documentation
├── tests/                  Backend test suite (pytest)
├── .github/                GitHub Actions CI/CD workflows
├── .env.example            Environment variable template
├── .gitignore
├── docker-compose.yml      Production Docker Compose
├── docker-compose.dev.yml  Local development Docker Compose
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- (Optional) Docker and Docker Compose

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-study-ai.git
cd smart-study-ai
```

---

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your IBM watsonx.ai and IBM Cloud Object Storage credentials.  
For local development, you only need to set `DEBUG=True`. IBM credentials are required only when using AI generation features.

---

### 3. Run the Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload --port 8000
```

The backend will be available at: **http://localhost:8000**  
API documentation (Swagger UI): **http://localhost:8000/api/docs**  
Health check: **http://localhost:8000/api/health**

---

### 4. Run the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

The Vite dev server automatically proxies all `/api/*` requests to `http://localhost:8000`, so no CORS configuration is needed during development.

---

### 5. Run with Docker Compose (Optional)

```bash
# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Backend health check |
| POST | `/api/documents/upload` | Upload a study document |
| GET | `/api/documents` | List uploaded documents |
| POST | `/api/study/generate` | Generate notes and summary |
| POST | `/api/quiz/generate` | Generate MCQ quiz |
| POST | `/api/quiz/submit` | Submit quiz answers |
| POST | `/api/flashcards/generate` | Generate flashcards |
| POST | `/api/planner/generate` | Generate study plan |
| GET | `/api/progress/summary` | Get progress dashboard data |

Full interactive API documentation is available at `/api/docs` when the backend is running.

---

## Environment Variables Reference

See [`.env.example`](.env.example) for the full list of variables with descriptions.

| Variable | Description |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud API key for watsonx.ai |
| `WATSONX_PROJECT_ID` | watsonx.ai project ID |
| `WATSONX_URL` | watsonx.ai regional endpoint |
| `IBM_COS_API_KEY` | IBM Cloud Object Storage API key |
| `IBM_COS_INSTANCE_CRN` | COS service instance CRN |
| `IBM_COS_BUCKET` | COS bucket name for document storage |
| `DATABASE_URL` | SQLAlchemy database URL (SQLite for dev) |
| `DEBUG` | Enable verbose logging (`True` / `False`) |
| `ALLOWED_ORIGINS` | Comma-separated CORS allowed origins |

---

## Security Notes

- **Never commit your `.env` file.** It is listed in `.gitignore`.
- IBM API keys are read exclusively from environment variables — they are never hardcoded in source code and are never sent to the frontend.
- The frontend has no access to IBM credentials. All AI calls go through the backend.

---

## Deployment (IBM Cloud Code Engine)

1. Build and push the backend Docker image to IBM Container Registry.
2. Create a Code Engine application pointing to the image.
3. Set all environment variables from `.env.example` as Code Engine secrets/config maps.
4. Deploy the frontend `dist/` folder to IBM Cloud Object Storage + CDN, or as a separate Code Engine application.

---

## License

MIT License — see [LICENSE](LICENSE)
