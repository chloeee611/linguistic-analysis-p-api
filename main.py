from fastapi import FastAPI
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)
app = FastAPI()


@app.post("/analysis/frequency/{transcript_name}")
def read_root(transcript_name: str):
    response = supabase.storage.from_("transcripts").download(transcript_name)
    transcript = response.decode("utf-8")
    return {
        "transcript": transcript
    }