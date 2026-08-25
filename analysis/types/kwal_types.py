# Summarises KWAL results if a match is found
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

# Building up the search request which is passed to the match_words function
class KwalSearch:
    utterance_word: list[str] | None
    mor_word_class: list[str] | None
    gra_relation: list[str] | None

    def __init__(self, utterance_word: list[str] | None, mor_word_class: list[str] | None, gra_relation: list[str] | None):
            self.utterance_word = utterance_word
            self.mor_word_class = mor_word_class
            self.gra_relation = gra_relation