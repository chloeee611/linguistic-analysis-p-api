from analysis.helpers.utterance import *
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY") or ""
supabase: Client = create_client(url, key)

def analyse_transcript_metadata(payload):
    files_reference = {}

    for url in payload.urls:
        metadata = {}

        response = supabase.storage.from_("transcripts").download(url)
        data = response.decode("utf-8")

        # Iterate each line of the text
        for line in data.split("\n"):
            # Metadata starts with @, followed by the property name
            if line.startswith("@"):
                split_line = line.split("\t")

                if(len(split_line) > 1):
                    property, value = split_line 
                    parsed_property = property.replace(":", "").replace("@", "").replace(' ', '_').lower()
                    parsed_value = ''

                    match parsed_property:
                        case "date" | "birth_of_chi":
                            parsed_value = datetime.strptime(value, '%d-%b-%Y').isoformat()
                        case "languages" | "types" | "transcriber":
                            parsed_value = value.split(', ')
                        case "tape_location" | "media" | "situation":
                            parsed_value = value
                        case "comment":
                            if (parsed_property in metadata):
                                metadata[parsed_property].append(value)
                            else:
                                metadata[parsed_property] = [value]

                            continue
                        case "participants":
                            participants = {}
                            for speaker in value.split(', '):
                                split_speaker = speaker.split(' ')
                                if (len(split_speaker) > 1):
                                    participants[split_speaker[0]] = split_speaker[1]
                            parsed_value = participants
                        case "time_duration":
                            duration_values = {}
                            split_value = value.split('-')
                            if (len(split_value) > 1):
                                duration_values["start"] = split_value[0]
                                duration_values["end"] = split_value[1]
                            parsed_value = duration_values
                        case "id":
                            id_dict = parse_id(value)

                            if (parsed_property in metadata):
                                metadata[parsed_property][id_dict["participant_code"]] = id_dict
                            else:
                                metadata[parsed_property] = { id_dict["participant_code"]: id_dict }
                            continue
                        case "pid":
                            continue


                    metadata[parsed_property] = parsed_value

            else:
                # As far as I can see, metadata is always at the top
                # Therefore when we hit something that isn't @, we can break early
                break
                        
        files_reference[url] = metadata
    
    return files_reference


ID_PROPERTY_LOOKUP = [
    "languages_spoken",
    "corpus",
    "participant_code",
    "age",
    "sex",
    "5",
    "6",
    "role",
    "8",
    "9"
]

def parse_id(value: str):
    id_reference = {}

    for i, value in enumerate(value.split('|')):
        if (value is not None and value is not ''):
            if (i == 0):
                id_reference[ID_PROPERTY_LOOKUP[i]] = value.split(', ')
            else:
                id_reference[ID_PROPERTY_LOOKUP[i]] = value

    return id_reference
