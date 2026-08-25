from analysis.helpers.utterance import *
from analysis.types.api_types import MluBody
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

# Handles the MLU analysis
def mlu(payload: MluBody):
    # Stores the data in the below dictionary objects as it iterates through each line of the transcript
    files_reference = {}
    file_analysis = {"counts": {}}
    morph_count = {}
    file_scan = {"gra": [], "wor": [], "mor": []}

    for transcript in payload.urls:
        # Requests the .cha file from storage and decodes into text format
        response = supabase.storage.from_("transcripts").download(transcript.file_url)
        data = response.decode("utf-8")

        # Iterate through each line of the transcript
        for line in data.split("\n"):
            line_split = line.split("\t")

            # The lines that start with an asterisk denotes a normal utterance
            if line.startswith("*"):
                # The word that follows the asterisk is always the speaker name
                current_speaker = line_split[0].replace(":", "").replace('*', '')

                if current_speaker not in file_analysis["counts"]:
                    # A new file_analysis object is created for all new speakers to track their utterance stats
                    file_analysis["counts"][current_speaker] = {"utterances": 0, "morphs": 0, "mlu": 0, "std": 0}

                # The file_analysis object is assigned to the relevant speaker and it uses process_utterance_line to count the words 
                speaker = file_analysis["counts"][current_speaker]
                process_utterance_line(line_split[1], count_morphemes(morph_count))
                speaker["morphs"] += sum(morph_count.values())

                if len(morph_count) >= 1:
                    speaker["utterances"] += 1

                morph_count = {}

                # Calculates the MLU by doing total number of words divided by total utterances
                # If the speaker has no utterances, this logic does not run as it will cause a ZeroDivisionError
                if speaker["utterances"] > 0:
                    speaker["mlu"] = round(speaker["morphs"] / speaker["utterances"], 3)

            # If a line does not start with asterisk, then it is always one of the below tiers    
            else:
                match line_split[0].replace("%", ""):
                    case "gra:":
                        file_scan["gra"].append(line)
                    case "wor:":
                        file_scan["wor"].append(line)
                    case "mor:":
                        file_scan["mor"].append(line)
            
        files_reference[transcript.id] = file_analysis

    return files_reference