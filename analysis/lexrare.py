from analysis.helpers.mor import *
from analysis.helpers.utterance import *
from analysis.types.api_types import LexBody
from analysis.types.lexrare_types import LexAnalysis
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import json

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

with open('./analysis/data/thorndike_lorge.json', 'r') as file:
    common_word_set: set[str] = set(json.load(file))

def lexrare(payload: LexBody):
    files_reference = {}

    for transcript in payload.urls:
        response = supabase.storage.from_("transcripts").download(transcript.file_url)
        data = response.decode("utf-8")

        speaker_summaries: dict[str, LexAnalysis] = {}
        current_speaker = ''

        for line in data.split("\n"):
            line_split = line.split("\t")

            if line.startswith("*"):
                current_speaker = line_split[0].replace(":", "").replace('*', '')

                if (current_speaker not in speaker_summaries):
                    speaker_summaries[current_speaker] = LexAnalysis(current_speaker)

                if payload.target_tier == 'utt':
                    process_utterance_line(line_split[1], 
                            is_utt_rare(common_word_set, speaker_summaries[current_speaker]))
            elif line.startswith('%mor') and payload.target_tier == 'mor':
                process_mor_line(line_split[1], 
                        is_mor_rare(common_word_set, speaker_summaries[current_speaker]))

        for key in speaker_summaries:
            speaker_summaries[key].percent_rare_words = float("{:.3f}".format(
                    speaker_summaries[key].num_rare_words
                    / speaker_summaries[key].num_total_words if speaker_summaries[key].num_total_words > 0 else 0
                ))
                
        files_reference[transcript.id] = speaker_summaries

    
    return files_reference