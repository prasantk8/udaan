# import os
# from fastapi import FastAPI
# from llama_cpp import Llama
# from pydantic import BaseModel
# import sqlite3
# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime

# # --- Configuration ---
# MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'mistral-7b-instruct-v0.2.Q4_K_M.gguf')
# SYSTEM_PROMPT = """
# You are a Socratic Math Tutor. Your purpose is to guide a 10th-grade student through learning algebra. Do not give direct answers. Instead, ask probing questions to help the student discover the solution on their own. Focus on one step at a time.
# """

# class PromptRequest(BaseModel):
#     prompt: str

# # --- FastAPI Application ---
# app = FastAPI()
# llm = None  # Will be initialized at startup

# # --- Database Setup ---
# DATABASE_URL = "sqlite:///../data/user_state.db"
# engine = create_engine(DATABASE_URL)
# Base = declarative_base()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class UserEmotion(Base):
#     __tablename__ = "user_emotions"
#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(String)
#     sentiment = Column(String)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# # --- New API Endpoint ---
# class CheckinRequest(BaseModel):
#     text: str

# @app.on_event("startup")
# async def startup_db_and_model():
#     Base.metadata.create_all(bind=engine)
# async def load_model():
#     global llm
#     print("Loading Mistral 7B model...")
#     llm = Llama(
#         model_path=MODEL_PATH,
#         n_ctx=2048,  # Context window size
#         n_gpu_layers=-1, # Offload all layers to GPU (M3 Max)
#         verbose=False
#     )
#     print("Model loaded successfully!")

# # --- API Endpoint ---
# @app.post("/tutor/ask")
# async def ask_tutor(request: PromptRequest):
#     global llm
#     if llm is None:
#         return {"error": "Model not loaded."}, 500

#     full_prompt = f"### System:\n{SYSTEM_PROMPT}\n### User:\n{request.prompt}\n### Assistant:\n"

#     output = llm(
#         full_prompt,
#         max_tokens=256,
#         stop=["### User:"],
#         echo=False
#     )

#     response_text = output['choices'][0]['text'].strip()
#     return {"response": response_text}
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from pydantic import BaseModel
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# --- Configuration ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'mistral-7b-instruct-v0.2.Q4_K_M.gguf')
SYSTEM_PROMPT = """
You are a Socratic Math Tutor. Your purpose is to guide a 10th-grade student through learning algebra. Do not give direct answers. Instead, ask probing questions to help the student discover the solution on their own. Focus on one step at a time.
"""

class PromptRequest(BaseModel):
    prompt: str

# --- FastAPI Application ---
app = FastAPI()

# Add CORS middleware to allow the frontend to communicate with the backend.
# The `allow_origins` list should include the URL of your frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Use a specific origin in production, e.g., ["http://localhost:PORT"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = None  # Will be initialized at startup

# --- Database Setup ---
DATABASE_URL = "sqlite:///../data/user_state.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserEmotion(Base):
    __tablename__ = "user_emotions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    sentiment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- New API Endpoint ---
class CheckinRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_db_and_model():
    # Create the database table on startup
    Base.metadata.create_all(bind=engine)
    
    # Load the LLM model
    global llm
    print("Loading Mistral 7B model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,  # Context window size
        n_gpu_layers=-1, # Offload all layers to GPU (M3 Max)
        verbose=False
    )
    print("Model loaded successfully!")

# --- API Endpoint ---
@app.post("/tutor/ask")
async def ask_tutor(request: PromptRequest):
    global llm
    if llm is None:
        return {"error": "Model not loaded."}, 500

    full_prompt = f"### System:\n{SYSTEM_PROMPT}\n### User:\n{request.prompt}\n### Assistant:\n"

    output = llm(
        full_prompt,
        max_tokens=256,
        stop=["### User:"],
        echo=False
    )

    response_text = output['choices'][0]['text'].strip()
    return {"response": response_text}

# This new endpoint will handle the emotional check-in from the frontend.
@app.post("/checkin/emotional")
async def emotional_checkin(request: CheckinRequest):
    # This is a placeholder for the sentiment analysis logic.
    # In a later step, we will use the fine-tuned model here.
    # For now, we'll return a static response.
    print(f"Received emotional check-in: {request.text}")
    return {"sentiment": "neutral"}
