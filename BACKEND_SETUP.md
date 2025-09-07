# ⚙️ Backend Setup (FastAPI)

This guide explains how to set up and run the **Socratic Tutor backend** using FastAPI.

-----

## 1️⃣ System Requirements

  * **Python 3.10+**
  * **Virtualenv** (`python3 -m venv`)

-----

## 2️⃣ Setup Virtual Environment

Navigate to the project directory:

```bash
cd backend
```

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

-----

## 3️⃣ Install Dependencies

Install the required packages:

```bash
pip install fastapi uvicorn
```

-----

## 4️⃣ Project Files

  * **`main.py`** → entrypoint for the FastAPI application

### API Endpoint:

  * **`POST /tutor/ask`** → receives a prompt and returns a response

-----

## 5️⃣ Run Server

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

-----

## 6️⃣ Verify API

Send a test request to the endpoint:

```bash
curl http://localhost:8000/tutor/ask \
 -X POST \
 -H "Content-Type: application/json" \
 -d '{"prompt": "hello"}'
```

### Expected response:

```json
{"response": "some answer"}
```

-----

## ✅ Verification Checklist

  * Server runs at `http://localhost:8000`.
  * `/tutor/ask` accepts input and returns a JSON response.
  * No Python errors occur during server startup.

