from analysis.helpers.utterance import *
from analysis.types.kwal_types import *
from analysis.helpers.mor import * 
from analysis.helpers.gra import * 
from analysis.types.api_types import KwalBody
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

def kwal(payload: KwalBody):
    files_reference = {}
    # file_analysis = {}
    # speaker_summaries = {}

    for transcript in payload.urls:
        response = supabase.storage.from_("transcripts").download(transcript.file_url)
        data = response.decode("utf-8")
        kwal_summary: list[KwalMatch] = []

        # Iterate each line of the text
        lines = data.split("\n")
        for i, line in enumerate(lines):
            line_split = line.split("\t")

            # Utterances start with * in the transcripts
            # Other lines are ignored for the FREQ analysis
            if line.startswith("*"):
                current_speaker = line_split[0].replace(":", "").replace('*', '')

                mor_line = None
                gra_line = None

                if (payload.mor_filters):
                    for line_tracker in range(i + 1, len(lines)):
                        if lines[line_tracker].startswith('%mor'):
                            mor_line = analyse_mor_line(lines[line_tracker].split('\t')[1])
                            break
                        elif lines[line_tracker].startswith('*'):
                            break

                if (payload.gra_filters):
                    for line_tracker in range(i + 1, len(lines)):
                        if lines[line_tracker].startswith('%gra'):
                            gra_line = analyse_gra_line(lines[line_tracker].split('\t')[1])
                            break
                        elif lines[line_tracker].startswith('*'):
                            break

                search_terms = KwalSearch(payload.search_utterance, payload.mor_filters, payload.gra_filters)
                
                process_utterance_line(line_split[1], 
                        match_word(search_terms, line, gra_line, mor_line, i + 1, current_speaker, kwal_summary))

        files_reference[transcript.id] = kwal_summary
    
    return files_reference