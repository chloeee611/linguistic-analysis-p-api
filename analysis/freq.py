from analysis.helpers.utterance import *
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

def freq(payload):
    files_reference = {}
    file_analysis = {}
    speaker_summaries = {}

    for url in payload.urls:
        file_url = url

        response = supabase.storage.from_("transcripts").download(url)
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
                
                process_line(line_split[1], 
                        count_words(payload["search"] if "search" in payload else None,
                                    file_analysis[current_speaker],
                                    speaker_summaries[current_speaker],
                                    i))

        # After processing every line, move speaker_summaries into file_analysis for each speaker
        for key in speaker_summaries:
            file_analysis[key]["summary"] = {
                "total_unique_words": str(speaker_summaries[key]["unique_words_count"]),
                "total_items": str(speaker_summaries[key]["total_count"]),
                "unique_word_ratio": "{:.3f}".format(
                    speaker_summaries[key]["unique_words_count"] 
                    / speaker_summaries[key]["total_count"] if speaker_summaries[key]["total_count"] > 0 else 0
                ),
            }
        
        files_reference[url.split("/")[-1].replace(".cha", "")] = file_analysis
    
    return files_reference