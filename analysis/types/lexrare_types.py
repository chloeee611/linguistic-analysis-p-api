# Summarises results for LEXRARE analysis
class LexAnalysis:
    code: str
    num_common_words: int 
    num_rare_words: int
    num_total_words: int 
    percent_rare_words: float 

    def __init__(self, code: str):
        self.code = code
        self.num_common_words = 0
        self.num_rare_words = 0
        self.num_total_words = 0
        self.percent_rare_words = 0
