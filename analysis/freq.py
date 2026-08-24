from analysis.helpers.utterance import *
from analysis.types.freq_types import *
from analysis.types.api_types import FreqBody
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

def freq(payload: FreqBody):
    files_reference: dict[str, dict[str, FreqAnalysis]] = {}
    file_analysis: dict[str, FreqAnalysis] = {}
    speaker_trackers: dict[str, FreqSpeakerTracker] = {}

    for transcript in payload.urls:
        response = supabase.storage.from_("transcripts").download(transcript.file_url)
        data = response.decode("utf-8")

        # Iterate each line of the text
        for i, line in enumerate(data.split("\n")):
            line_split = line.split("\t")

            # Utterances start with * in the transcripts
            # Other lines are ignored for the FREQ analysis
            if line.startswith("*"):
                current_speaker = line_split[0].replace(":", "").replace('*', '')

                # If first time encountering this speaker, add an entry for them in file_analysis
                if current_speaker not in file_analysis:
                    file_analysis[current_speaker] = FreqAnalysis()

                    # Speaker_summaries contains stats for each speaker
                    speaker_trackers[current_speaker] = FreqSpeakerTracker()
                
                process_utterance_line(line_split[1], 
                        count_words(payload.search,
                                    file_analysis[current_speaker],
                                    speaker_trackers[current_speaker]))

        # After processing every line, move speaker_summaries into file_analysis for each speaker
        for key in speaker_trackers:
            file_analysis[key].summary = FreqSpeakerSummary(
                speaker_trackers[key].unique_words_count, 
                speaker_trackers[key].total_count, 
                speaker_trackers[key].get_unique_word_ratio()
            )
        
        files_reference[transcript.id] = file_analysis
    
    return files_reference