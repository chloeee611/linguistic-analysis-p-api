from analysis.helpers.mor import analyse_mor

def test_analyse_mor_word_class():
    result = analyse_mor("v|walk")

    assert result.word_class == "v"
    assert result.word == "walk"

def test_analyse_mor_word_modifier():
    result = analyse_mor("v|see-PAST")

    assert result.word_class == "v"
    assert result.word == "see"
    assert result.word_modifiers == ["PAST"]