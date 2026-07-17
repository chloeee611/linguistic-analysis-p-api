from analysis.helpers.utterance import *
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

def mlu(payload):
    files_reference = {}
    file_analysis = {"counts": {}}
    morph_count = {}
    file_scan = {"gra": [], "wor": [], "mor": []}

    for url in payload.urls:
        file_url = url

        response = supabase.storage.from_("transcripts").download(url)
        data = response.decode("utf-8")