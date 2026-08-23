from pydantic import BaseModel

class TranscriptInstance(BaseModel):
    id: str
    file_url: str

class FreqBody(BaseModel):
    urls: list[TranscriptInstance]
    search: list[str] | None = None

class KwalBody(BaseModel):
    urls: list[TranscriptInstance]
    search_utterance: list[str] | None = None
    gra_filters: list[str] | None = None
    mor_filters: list[str] | None = None

class MetadataBody(BaseModel):
    urls: list[TranscriptInstance]

class MluBody(BaseModel):
    urls: list[TranscriptInstance]

class LexBody(BaseModel):
    urls: list[TranscriptInstance]
    target_tier: str