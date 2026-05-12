<div align="center">
  <img src="../frontend/public/favicon.png" alt="MeloTech Logo" width="120" />
  <h1>MeloTech Backend</h1>
  <p>A small FastAPI backend that generates thoughtful interview questions using AI.</p>
</div>

---

## What does this do?

This backend powers the MeloTech application. When the frontend sends a job title (like "Customer Success Manager"), this server:

1. Validates and cleans the input.
2. Checks for any suspicious or malicious content.
3. Asks an AI model (Google Gemini) to generate 3 interview questions.
4. If Gemini is unavailable, it automatically tries a backup AI model (Groq).
5. Returns the questions in a clean, structured format the frontend can display.

---

## How to set it up locally

### 1. Prerequisites

- **Python 3.11 or newer** installed on your machine.
- A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/).
- A **Groq API key** from [Groq Console](https://console.groq.com/) (for the fallback).

### 2. Install dependencies

Open your terminal, navigate to the `backend/` folder, and run:

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

Copy the example environment file:

```bash
cp .env.example .env
```

Then open the new `.env` file and replace the placeholder values with your real API keys:

```
GEMINI_API_KEY=your_real_gemini_key
GROQ_API_KEY=your_real_groq_key
```

### 4. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`.

---

## How to verify it works

### Check the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

### Generate interview questions

```bash
curl -X POST http://localhost:8000/questions \
  -H "Content-Type: application/json" \
  -d '{"job_title": "Customer Success Manager"}'
```

Expected response:
```json
{
  "questions": [
    {"category": "Behavioral", "question": "..."},
    {"category": "Situational", "question": "..."},
    {"category": "Technical", "question": "..."}
  ]
}
```

### Explore the API docs

Visit `http://localhost:8000/docs` in your browser for the interactive Swagger UI.

---

## How to run the tests

```bash
pytest tests/ -v
```

---

## Project structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py           # Environment variable loading
│   │   ├── logging.py          # Logger setup
│   │   └── security.py         # Prompt injection detection
│   ├── schemas/
│   │   ├── common.py           # Shared response schemas
│   │   └── questions.py        # Request/response models for /questions
│   ├── services/
│   │   ├── ai_orchestrator.py  # Gemini → Groq fallback logic
│   │   ├── gemini_client.py    # Google Gemini API wrapper
│   │   ├── groq_client.py      # Groq API wrapper
│   │   ├── prompt_builder.py   # System prompt construction
│   │   ├── response_parser.py  # AI response → structured JSON
│   │   └── sanitization.py     # Input text cleaning
│   └── routes/
│       ├── health.py           # GET /health
│       └── questions.py        # POST /questions
├── tests/
│   ├── test_health.py          # Health endpoint tests
│   └── test_questions.py       # Question generation tests
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
