from analysis.helpers.clean_word import clean_word
from analysis.types.kwal_types import KwalMatch
from analysis.types.lexrare_types import LexAnalysis

INVALID_STARTS = ['0', '&', '+', '-', '#', '‡']
IGNORED_MORPHS = ['xxx', 'www', '?', '!', '„', '.', ',', '(.)']

# Validates that a word is not empty or invalid
validate = lambda w: w is not None and w != '' and not w.isspace() and  not w.startswith('\x15') and w[0] not in INVALID_STARTS and w not in IGNORED_MORPHS

def process_utterance_line(line: str, callback_func):

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
            next_word = line_list[current_index + 1]
        else:
            next_word = None

        # Sections between angled brackets are ignored
        if word.startswith('<') and not word.endswith('>'):
            angle_ignore = True
        
        # Skips words which start and end with an angled bracket
        elif word.startswith('<'):
            current_index += 1
            continue

        # Ends the angle_ignore if it has been previously set to true
        elif word.endswith('>'):
            angle_ignore = False

        # Noises or malformed words are skipped
        if next_word and next_word in ['[/]', '[//]', '[///]', '[/?]', '[/-]']:
            current_index += 2
            next_word = clean_word(line_list[current_index])
            continue

        # There are instances of mispronounced words where the transcriber uses square brackets
        # after the word to indicate what the word should have been. This handles these instances 
        # by skipping the unclear word and using the substituted word in the analysis instead
        elif next_word == '[:':
            word = line_list[current_index + 2].replace(']', '')
            if validate(word):
                callback_func(word)
            current_index += 3
            next_word = line_list[current_index]
            continue

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
            word = clean_word(word)

            if validate(word):
                callback_func(word)

        current_index += 1

def count_words(search_word: list[str] | None, speaker_dict: dict[str, int], summary: dict[str, int | set]):
    def count(word: str):
        if not search_word or word in search_word:
            # If word isn't in counts yet, initialise it
            # Otherwise, add 1 to existing word entry
            if word in speaker_dict['counts']:
                speaker_dict['counts'][word] += 1
            else:
                speaker_dict['counts'][word] = 1

            if word not in summary['unique_words_lookup']:
                summary['unique_words_lookup'].add(word)
                summary['unique_words_count'] += 1
            
            summary['total_count'] += 1
    
    return count

def match_word(search_word: list[str] | None, line: str, line_number: int, current_speaker: str, kwal_summary: list[KwalMatch]):
    def match(word: str):
        if search_word and word in search_word:
            # If word isn't in counts yet, initialise it
            # Otherwise, add 1 to existing word entry
            kwal_summary.append(KwalMatch(word, line_number, current_speaker, line))
    
    return match

def count_morphemes(counts: dict[str, int]):
    def count(word: str):
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return count

def is_utt_rare(common_words: set[str], speaker_summary: LexAnalysis):
    def compare_common_words(word: str):
        if not word:
            return

        if word in common_words:
            speaker_summary.num_common_words += 1
        else:
            speaker_summary.num_rare_words += 1

        speaker_summary.num_total_words += 1

    return compare_common_words