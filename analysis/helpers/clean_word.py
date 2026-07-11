CHARS_TO_CLEAN = ['(', ')', ',', ':']

# Cleans unused or invalid characters from a word
def clean_word(word: str) -> str:
    cleaned_word = word

    for exclusion in CHARS_TO_CLEAN:
        cleaned_word = cleaned_word.replace(exclusion, '')
    
    return cleaned_word