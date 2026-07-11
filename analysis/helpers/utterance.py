from analysis.helpers.clean_word import clean_word

def process_line(line: str):

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