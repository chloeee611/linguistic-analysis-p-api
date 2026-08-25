from analysis.types.lexrare_types import LexAnalysis

# Adds each part of a mor line to mor_list 
def analyse_mor_line(line: str):
    line_list = line.split(' ')

    mor_list: list[MorEntry] = []
    
    # Iterate through each word in the line
    for mor in line_list:
        if mor is None:
            continue

        mor_list.append(analyse_mor(mor))

    return mor_list

def process_mor_line(line: str, callback_func):
    # Array of all the words in a line
    line_list = line.split(' ')

    # Iterate through each word in the line
    for mor in line_list:
        if mor is None:
            continue

        mor_entry = analyse_mor(mor)

        callback_func(mor_entry)

class MorEntry:
    word_class_type: str = ''
    word_class: str = ''
    word_modifiers: list[str] = []
    word: str = ''
    conjunction_type: str = ''
    conjunction_word: str = ''

# Processes each part of the mor tier and adds it to the relevant class variables in MorEntry
# E.g. in a transcript, a speaker says "ears" and this is marked as "noun|ear-Plur" in the mor tier
# The function will process this by adding "noun" to word_class, "ear" to word, and "Plur" to word_modifiers
def analyse_mor(mor:str) -> MorEntry:
    mor_desc = MorEntry()
    mor_split = mor.split('|')

    if len(mor_split) == 2 or len(mor_split) == 3:
        word_class_split = mor_split[0].split(':')
        if len(word_class_split) > 1:
            mor_desc.word_class_type = word_class_split[1]
        mor_desc.word_class = word_class_split[0]

    if len(mor_split) == 2:
        word_split = mor_split[1].split('-')
        if len(word_split) > 1:
            mor_desc.word_modifiers = word_split[1:]
        mor_desc.word = word_split[0]
    elif len(mor_split) == 3:
        middle_split = mor_split[1].split('~')
        if len(middle_split) > 1:
            mor_desc.conjunction_type = middle_split[1]
        mor_desc.conjunction_word = middle_split[0]

        end_split = mor_split[2].split('-')
        if len(end_split) > 1:
            mor_desc.word_modifiers = end_split[1:]
        mor_desc.word = end_split[0]

    return mor_desc 

# Compares words with the rare words list for lexrare analysis
def is_mor_rare(common_words: set[str], speaker_summary: LexAnalysis):
    def compare_common_words(mor: MorEntry):
        if not mor.word:
            return

        if mor.word in common_words:
            speaker_summary.num_common_words += 1
        else:
            speaker_summary.num_rare_words += 1

        speaker_summary.num_total_words += 1

    return compare_common_words