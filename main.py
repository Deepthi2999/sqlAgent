from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_query
import subprocess
import os

if not os.path.exists("business.db"):
    subprocess.run(["python","setup_db.py"])

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    question:str

@app.get("/")
def root():
    return {"status":"SQL Agent is runnig"}

@app.post("/ask")
def ask_question(body:Question):
    answer=ask_query(body.question)
    return {"answer":answer}
