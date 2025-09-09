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
import json
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from fuzzywuzzy import fuzz  # Note: `fuzzywuzzy` is for fuzzy string matching, useful for robust keyword identification.
from typing import List

# --- Configuration ---
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'models', 'mistral-7b-instruct-v0.2.Q4_K_M.gguf'
)
SYSTEM_PROMPT = """
You are a Socratic Math Tutor. Your purpose is to guide a 10th-grade student through learning algebra. 
Do not give direct answers. Instead, ask probing questions to help the student discover the solution on their own. 
Focus on one step at a time.
"""

class PromptRequest(BaseModel):
    prompt: str

class CheckinRequest(BaseModel):
    text: str

# For the new GET endpoint, we will use a path parameter for tags
# class FeedRequest(BaseModel):
#     tags: list[str]

# --- FastAPI Application ---
app = FastAPI()

# Add CORS middleware to allow the frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use a specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = None         # Will be initialized at startup
explore_feed = []  # Will hold curated content

# --- Database Setup ---
DATABASE_URL = "sqlite:///../data/user_state.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserEmotion(Base):
    __tablename__ = "user_emotions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    sentiment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- Startup: DB + Model + Explore Feed ---
@app.on_event("startup")
async def startup_db_and_model():
    global llm, explore_feed

    # Create the database table on startup
    Base.metadata.create_all(bind=engine)

    # Load the LLM model
    print("Loading Mistral 7B model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_gpu_layers=-1,  # Offload all layers to GPU (M3 Max)
        verbose=False
    )
    print("Model loaded successfully!")

    # Load Explore Feed
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'explore_feed.json'), 'r') as f:
            explore_feed = json.load(f)
        print("Explore feed loaded successfully.")
    except FileNotFoundError:
        print("Warning: explore_feed.json not found. The Explore Feed will be empty.")

# --- Concept Weaving Logic ---
def weave_concepts(response_text: str):
    """
    Parses a tutor's response to identify key mathematical concepts.
    Uses fuzzy string matching (`fuzzywuzzy`) for robustness.
    """
    found_tags = set()
    response_lower = response_text.lower()

    # Simple keyword list for MVP
    keywords = ["algebra", "equations", "variables", "quadratic", "factoring", "polynomials"]

    # Direct keyword match
    for keyword in keywords:
        if keyword in response_lower:
            found_tags.add(keyword)

    # Fuzzy matching against the tags in our curated content
    for item in explore_feed:
        for tag in item["tags"]:
            for keyword in keywords:
                if fuzz.ratio(tag.lower(), keyword) > 80:
                    found_tags.add(tag)

    return list(found_tags)

# --- Tutor Ask Endpoint ---
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

    # Weave concepts from response
    relevant_tags = weave_concepts(response_text)

    return {"response": response_text, "tags": relevant_tags}

# --- Emotional Check-in Endpoint ---
# We use a dependency injection approach for the database session, which is a best practice.
@app.post("/checkin/emotional")
async def emotional_checkin(request: CheckinRequest, db: Session = Depends(get_db)):
    """
    Placeholder endpoint to record a user's text-based check-in.
    NOTE: The sentiment is hardcoded for the MVP. The fine-tuned DistilBERT model logic will be added here in the future.
    """
    sentiment = "neutral"  # Placeholder for MVP

    db_entry = UserEmotion(text=request.text, sentiment=sentiment)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return {"sentiment": sentiment, "message": "Check-in recorded."}

# --- Explore Feed Endpoint ---
from fastapi import Query
from typing import List

# --- Explore Feed Endpoint ---
@app.get("/feed/explore")
async def get_explore_feed(tags: List[str] = Query(default=[])):
    """
    Retrieves curated content from the explore feed based on query params (?tags=algebra&tags=quadratic).
    Returns all items if no tags are provided.
    """
    curated_feed = []
    curated_ids = set()

    if not tags:  # return all if no tags provided
        return {"feed_items": explore_feed}

    tags_lower = {tag.lower() for tag in tags}  # optional: convert to set for efficiency

    for item in explore_feed:
        item_tags_lower = {t.lower() for t in item["tags"]}
        if tags_lower & item_tags_lower and item["id"] not in curated_ids:
            curated_feed.append(item)
            curated_ids.add(item["id"])

    return {"feed_items": curated_feed}