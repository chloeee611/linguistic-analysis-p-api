from analysis.helpers.mor import analyse_mor

def test_analyse_mor_word_class():
    result = analyse_mor("noun|apple")

    assert result.word_class == "noun"
    assert result.word == "apple"

def test_analyse_mor_word_modifier():
    result = analyse_mor("propn|Christmas-Acc")

    assert result.word_class == "propn"
    assert result.word == "Christmas"
    assert result.word_modifiers == ["Acc"]

def test_analyse_mor_multiple_word_modifiers():
    result = analyse_mor("verb|cut-Inf-S")

    assert result.word_class == "verb"
    assert result.word == "cut"
    assert result.word_modifiers == ["Inf", "S"]

def test_analyse_mor_three_part_entry():
    result = analyse_mor(
        "pron|we-Prs-Nom-P1~aux|be-Fin-Ind-Pres-P1"
    )

    assert result.word_class == "pron"
    assert result.conjunction_word == "we-Prs-Nom-P1"
    assert result.conjunction_type == "aux"
    assert result.word == "be"
    assert result.word_modifiers == ["Fin", "Ind", "Pres", "P1"]