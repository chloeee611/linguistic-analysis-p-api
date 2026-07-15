from analysis.helpers.utterance import process_line
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)


def freq(transcript_name: str):
    files_reference = {}
    file_analysis = {}
    speaker_summaries = {}

    response = supabase.storage.from_("transcripts").download(transcript_name)
    data = response.decode("utf-8")

    # Iterate each line of the text
    for i, line in enumerate(data.split("\n")):
        line_split = line.split("\t")

        # Utterances start with * in the transcripts
        # Other lines are ignored for the FREQ analysis
        if line.startswith("*"):
            current_speaker = line_split[0].replace(":", "")

            # If first time encountering this speaker, add an entry for them in file_analysis
            if current_speaker not in file_analysis:
                file_analysis[current_speaker] = {"counts": {}, "summary": {}}

                # Speaker_summaries contains stats for each speaker
                speaker_summaries[current_speaker] = {
                    "unique_words_lookup": set(),
                    "unique_words_count": 0,
                    "total_count": 0
                }
            
            # TODO: clean each line and implement count for specific words
