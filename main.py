from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_query

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
