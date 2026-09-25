# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant built with FastAPI and Google Gemini. It helps students learn through clear answers, simple explanations, quizzes, summaries, and personalized learning paths.

## Features

- Question answering
- Beginner-friendly concept explanations
- 1–10 question MCQ generation
- Passage summarization
- Personalized learning paths

## Architecture

Browser → FastAPI backend → Learning services → Gemini API

## Requirements

- Python 3.10+
- A Gemini API key
- VS Code recommended

## Setup

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `your_gemini_api_key_here` with your Gemini API key.

## Run

```powershell
python -m uvicorn backend.main:app --reload
```

Open:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

API documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Test

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Question answering:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/qa `
  -ContentType "application/json" `
  -Body '{"question":"What is photosynthesis?"}'
```

## Security

Never commit `.env` or an API key. The browser communicates with the FastAPI backend, and your Gemini API key stays on the server.
