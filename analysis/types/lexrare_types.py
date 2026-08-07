class LexAnalysis:
    code: str
    num_common_words: int = 0
    num_rare_words: int = 0
    num_total_words: int = 0
    percent_rare_words: float = 0

    def __init__(self, code: str):
        self.code = code
