# backend_leads
# 🚀 Lead Scoring Backend Assignment

This project implements a backend service for uploading leads, adding product offers, and scoring the leads based on rules + AI classification.  
Built with **FastAPI**, **SQLite**, and **OpenAI API**.

---

## 📌 Features
- Upload leads via CSV (`/leads/upload`)
- Add product offers (`/offer`)
- Score leads using rules + AI (`/score`)
- Fetch results (`/results`)
- Interactive API docs available at `/docs` (Swagger UI)

---

## ⚙️ Tech Stack
- **FastAPI** (Python backend framework)
- **SQLite** (local database)
- **SQLAlchemy** (ORM)
- **Pandas** (CSV parsing)
- **OpenAI API** (AI classification)
- **Uvicorn** (ASGI server)

---
#direct command
start chrome "http://127.0.0.1:8001/docs"; uvicorn main:app --reload --port 8001
https://backend-leads-gg2u.onrender.com/docs

## 🛠️ Setup Instructions

### 1. Clone repository
```bash
git remote set-url origin https://github.com/aryasohani/backend_leads.git
cd backend-leads-assignment
