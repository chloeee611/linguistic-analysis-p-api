from analysis.helpers.clean_word import clean_word

INVALID_STARTS = ['0', '&', '+', '-', '#', '‡']
IGNORED_MORPHS = ['xxx', 'www', '?', '!', '„', '.', ',', '(.)']

# Validates that a word is not empty or invalid
validate = lambda w: w is not None and w is not '' and not w.isspace() and  not w.startswith('\x15') and w[0] not in INVALID_STARTS and w not in IGNORED_MORPHS

def process_line(line: str, callback_func):

    # Track ignored bracketed sections
    angle_ignore = False
    square_ignore = False

    current_index = 0

    # Array of all the words in a line
    line_list = line.split(' ')

    # Keeps track of and cleans the next word in the line
    next_word = clean_word(line_list[0])

    # Iterate through each word in the line
    while current_index < len(line_list):
        word = next_word

        if word is None:
            continue

        # If current word is the last, set next word to empty, otherwise populate next word
        if len(line_list) != current_index + 1:
            next_word = clean_word(line_list[current_index + 1])
        else:
            next_word = None

        # Sections between angled brackets are ignored
        if word.startswith('<'):
            angle_ignore = True
        elif word.endswith('>'):
            angle_ignore = False
            continue

        # Noises or malformed words are skipped
        if next_word and next_word in ['[/]', '[//]', '[///]', '[/?]', '[/-]']:
            current_index += 2
            next_word = clean_word(line_list[current_index])
            continue

        # There are instances of mispronounced words where the transcriber uses square brackets
        # after the word to indicate what the word should have been. This handles these instances 
        # by skipping the unclear word and using the substituted word in the analysis instead
        elif next_word == '[:':
            word = clean_word(line_list[current_index + 2]).replace(']', '')
            if validate(word):
                callback_func(word)
            square_ignore = True

        # Handles other instances of square brackets
        elif word.startswith('[') and not word.endswith(']'):
            square_ignore = True

        # Skips words which start and end with a square bracket
        elif word.startswith('['):
            current_index += 1
            continue

        # Ends the square_ignore if it has been previously set to true
        elif word.endswith(']'):
            square_ignore = False
        
        # Skip if currently ignoring text because of brackets
        elif not (square_ignore or angle_ignore):
            if validate(word):
                callback_func(word)

        current_index += 1

def count_words(search_word: list[str], speaker_dict: dict[str, int], summary: dict[str, int | set], line: str):
    def count(word: str):
        if not search_word or word in search_word:
            # If word isn't in counts yet, initialise it
            # Otherwise, add 1 to existing word entry
            if word in speaker_dict['counts']:
                speaker_dict['counts'][word] += 1
            else:
                speaker_dict['counts'][word] = 1
            
            summary['total_count'] += 1
    
    return count

def count_morphemes(counts: dict[str, int]):
    def count(word: str):
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return count