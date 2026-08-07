from pydantic import BaseModel

class FreqBody(BaseModel):
    urls: list[str]
    search: list[str] | None = None

class KwalBody(BaseModel):
    urls: list[str]
    search_utterance: list[str] | None = None

class MetadataBody(BaseModel):
    urls: list[str]

class MluBody(BaseModel):
    urls: list[str]

class LexBody(BaseModel):
    urls: list[str]
    target_tier: str