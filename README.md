# Udaan 🚀

Udaan is an open-source **MVP learning and emotional support platform**.  
It combines four key pillars into one cohesive app:  
- 📘 **Academic Compass** – Socratic tutor for 10th-grade mathematics (Algebra)  
- 💙 **Inner World** – Emotional GPS with daily text-based check-ins  
- 🌍 **World Navigator** – Curated "Explore Feed" of 5–10 content pieces  
- 🔗 **Launchpad** – Concept Weaving: connect learned concepts to real-world content  

The MVP is designed to run **locally on a modern laptop (16GB RAM)**, leveraging efficient open-source models.

---

## 📦 Prerequisites

Make sure you have the following installed on your system:

- **Flutter** (latest stable) → [Install Guide](https://docs.flutter.dev/get-started/install)  
- **Python 3.10+** with `pip`  
- **FastAPI** and Uvicorn for backend  
- **SQLite** (comes preinstalled on macOS/Linux)  
- **Ollama** for running Gemma 2B model → [Install Ollama](https://ollama.ai/)  
- **Git** for version control  

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/udaan.git
cd udaan

cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt


uvicorn main:app --reload

cd ../frontend
flutter pub get
flutter run


```



# 📘 Socratic Tutor - Setup Guide

Welcome! This repository contains both the **backend** (FastAPI) and **frontend** (Flutter) of the Socratic Tutor project.

---

## ⚙️ Setup Instructions

- [Backend Setup](BACKEND_SETUP.md)  
- [Frontend Setup](FRONTEND_SETUP.md)  

---

## ✅ Verification Checklist

- `flutter doctor` shows **no issues**  
- Backend FastAPI server is running at `http://localhost:8000`  
- Frontend app sends questions and displays tutor responses  
