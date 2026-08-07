class KwalMatch:
    keyword: str
    line_number: int
    speaker: str
    utterance: str

    def __init__(self, keyword: str, line_number: int, speaker: str, utterance: str):
        self.keyword = keyword
        self.line_number = line_number
        self.speaker = speaker
        self.utterance = utterance