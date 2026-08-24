class FreqSpeakerTracker:
    unique_words_lookup: set 
    unique_words_count: int 
    total_count: int 

    def __init__(self):
        self.unique_words_lookup = set()
        self.unique_words_count = 0
        self.total_count = 0

    def get_unique_word_ratio(self):
        return float("{:.3f}".format(
                    self.unique_words_count
                    / self.total_count if self.total_count > 0 else 0
                ))

class FreqAnalysis:
    counts: dict[str, int]
    summary: FreqSpeakerSummary

    def __init__(self):
        self.counts = {}

class FreqSpeakerSummary:
    total_unique_words: int
    total_items: int
    unique_word_ratio: float

    def __init__(self,  total_unique_words: int, total_items: int, unique_word_ratio: float):
        self.total_unique_words = total_unique_words
        self.total_items = total_items
        self.unique_word_ratio = unique_word_ratio

