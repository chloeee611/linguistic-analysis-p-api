class FreqAnalysis:
    counts: dict[str, int]
    summary: FreqSpeakerSummary

    def __init__(self, counts: dict[str, int], summary: FreqSpeakerSummary):
        self.counts = counts
        self.summary = summary

class FreqSpeakerSummary:
    total_unique_words: str
    total_items: str
    unique_word_ratio: float

    def __init__(self,  total_unique_words: str, total_items: str, unique_word_ratio: float):
        self.total_unique_words = total_unique_words
        self.total_items = total_items
        self.unique_word_ratio = unique_word_ratio

