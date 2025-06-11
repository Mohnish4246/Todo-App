# 📝 Todo App – FastAPI + SQLite + Streamlit

A full-stack Todo application built with a FastAPI backend, Streamlit frontend, and SQLite database.  
Dockerized and deployed easily via Render.

---

## 🚀 Features

- ✅ Create, Read, Update, Delete (CRUD) Todos
- 🎯 Task filters: Completed, Pending
- 🕒 Add due dates & optional tags
- 📦 SQLite as local database
- 🌐 Streamlit web frontend
- ⚡ FastAPI REST API backend
- 🐳 Docker support
- ☁️ Easily deployable on Render or Railway

---

## 📁 Project Structure

├── main.py # FastAPI app
├── models.py # DB models (SQLAlchemy)
├── database.py # DB setup (SQLite)
├── crud.py # Database operations
├── streamlit_app.py # Streamlit frontend
├── requirements.txt # Python dependencies
├── Dockerfile # Docker config
└── render.yaml # Render deployment config (optional)
