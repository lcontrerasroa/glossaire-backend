from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

# Autoriser les appels depuis ton app Streamlit (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TermRequest(BaseModel):
    term: str
    lang: str = "en"

@app.post("/define")
def define_term(req: TermRequest):
    term = req.term.strip()
    lang = req.lang

    # Recherche simplifiée sur Wikipedia
    search_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{term.replace(' ', '_')}"
    r = requests.get(search_url)

    if r.status_code == 200:
        data = r.json()
        if "extract" in data:
            return {"definition": data["extract"]}
    
    # Fallback générique
    return {
        "definition": f"{term.capitalize()} is a concept used in linguistics, education, or translation."
    }
