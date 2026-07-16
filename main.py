from supabase import create_client, Client
from analysis.freq import freq
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)
app = FastAPI()

class Item(BaseModel):
    urls: list[str]

@app.post("/analysis/frequency")
def read_root(item: Item):
    response = freq(item)
    return response