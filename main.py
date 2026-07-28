from supabase import create_client, Client
from analysis.freq import freq
from analysis.transcript import analyse_transcript_metadata
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    urls: list[str]

@app.post("/analysis/frequency")
def read_root(item: Item):
    response = freq(item)
    return response

@app.post("/transcript/metadata")
def transcript_metadata(item: Item):
    response = analyse_transcript_metadata(item)
    return response
