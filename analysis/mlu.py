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
        response = supabase.storage.from_("transcripts").download(url)
        data = response.decode("utf-8")

        for line in data.split("\n"):
            line_split = line.split("\t")

            if line.startswith("*"):
                if line_split[0] not in file_analysis["counts"]:
                    file_analysis["count"][line_split[0]] = {"utterances": 1, "morphs": 0, "mlu": 0, "std": 0}

                speaker = file_analysis["counts"][line_split[0]]
                process_line(line_split[0], count_morphemes(morph_count))
                speaker["morphs"] += sum(morph_count.values())

                if len(morph_count) >= 1:
                    speaker["utterances"] += 1

                morph_count = {}

                speaker["mlu"] = round(speaker["morphs"] / speaker["utterances"], 3)
            else:
                match line_split[0].replace("%", ""):
                    case "gra:":
                        file_scan["gra"].append(line)
                    case "wor:":
                        file_scan["wor"].append(line)
                    case "mor:":
                        file_scan["mor"].append(line)
            
        files_reference[url.split("/")[-1]] = file_analysis

    return files_reference