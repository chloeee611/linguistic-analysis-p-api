from analysis.types.lexrare_types import LexAnalysis

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