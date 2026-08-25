from analysis.types.lexrare_types import LexAnalysis

# Adds each part of a gra ine to gra_list
def analyse_gra_line(line: str):
    line_list = line.split(' ')

    gra_list: list[GraEntry] = []
    
    # Iterate through each word in the line
    for gra in line_list:
        if gra is None:
            continue

        gra_list.append(analyse_gra(gra))

    return gra_list

class GraEntry:
    head: int = 0
    position: int = 0
    relation: str = ''

# Each part of a gra line is always made up of three components, such as "4|3|OBJ"
# This function splits them into three separate lists
# "4" is its position in the utterance, "3" is the position of the head of the utterance, "OBJ" is the relation of the word to the head
def analyse_gra(gra:str):
    gra_desc = GraEntry()
    gra_split = gra.split('|')

    try:
        if len(gra_split) == 3:
            gra_desc.position = int(gra_split[0].strip())
            gra_desc.head = int(gra_split[1].strip())
            gra_desc.relation = gra_split[2]
    except:
        print(gra_split[0])

    return gra_desc