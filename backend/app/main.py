from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="InfluenceOS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PostRequest(BaseModel):
    industry: str
    role: str
    interests: list[str] = []
    

@app.get("/")
def root():
    return {"message": "InfluenceOS backend is running!"}

@app.post("/generate_post")
def generate_post(req: PostRequest):
    """Generate a LinkedIn post using OpenAI"""
    prompt = (
        f"Write a professional LinkedIn post for someone in {req.role} "
        f"working in {req.industry}. Interests: {', '.join(req.interests)}. "
        f"Keep it short, engaging, and professional."
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return {"post": response.choices[0].message.content.strip()}
