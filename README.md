# Linguistic Analysis Python API

A FastAPI service for analysing transcript files stored in Supabase. The API extracts transcript metadata and handles common linguistic analyses such as word frequency, keyword analysis, lexical rarity, and mean length of utterance (MLU).

## Features

- Transcript metadata parsing from `.cha` files
- Word frequency analysis by speaker
- Keyword analysis with utterance, MOR, and GRA filtering
- Lexical rarity analysis against the Thorndike-Lorge word list
- MLU calculation from utterances
- Built with Python, FastAPI, Pydantic, and Supabase

## Requirements

- Python 3.10+
- A Supabase project with a `transcripts` storage bucket containing `.cha` transcript files

## Installation

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory.

Example:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_PUBLISHABLE_KEY=your-anon-key
SUPABASE_SECRET_KEY=your-secret-key
SUPABASE_JWKS_URL=https://your-jwks.link.supabase.co/auth/v1/.well-known/jwks.json
```

## Running the API

Start the FastAPI app in development mode:

```bash
fastapi dev
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## Example API Endpoints

### POST /analysis/freq

Analyse word frequency by speaker.

Request body:

```json
{
    "urls": [
        {
            "id": "transcript-1",
            "file_url": "path/to/transcript.cha"
        }
    ]
}
```

### POST /analysis/kwal

Run keyword analysis using utterance, MOR, and/or GRA filters.

Request body:

```json
{
    "urls": [
        {
            "id": "transcript-1",
            "file_url": "path/to/transcript.cha"
        },
        {
            "id": "transcript-2",
            "file_url": "path/to/transcript-2.cha"
        }
    ],
    "search_utterance": ["want", "go"],
    "gra_filters": ["VERB"],
    "mor_filters": ["V"]
}
```

## Data assumptions

This project expects transcript files in the CHAT `.cha` format, with speaker utterances such as:

```text
*BEL: where is lemon juice .
*CHI: this is lemon juice .
```

The API reads transcript files from the configured Supabase storage bucket and processes each utterance line to compute the requested analyses.

## Testing

The project includes pytest tests for the analysis functions:

```bash
python -m pytest
```

## Notes

- The application expects transcript storage paths to be valid keys in the `transcripts` bucket.
- This project is intended as a backend analysis API and is designed to integrate with other services or front-end applications.
