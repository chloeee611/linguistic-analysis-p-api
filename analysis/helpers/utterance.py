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

        # There are instances of words that are not fully pronounced where the transcriber uses square 
        # brackets after the word to indicate what the word should have been. This handles these instances 
        # by skipping the unclear word and using the substituted word in the analysis instead
        elif next_word == '[:':
            word = clean_word(line_list[current_index + 2]).replace(']', '')
            if validate(word):
                callback_func(word)
            square_ignore = True