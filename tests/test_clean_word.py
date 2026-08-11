from analysis.helpers.clean_word import clean_word

def test_clean_word_remove_brackets():
    assert clean_word("(linguistics)") == "linguistics"

def test_clean_word_remove_comma():
    assert clean_word("linguistics,") == "linguistics"

def test_clean_word_remove_colon():
    assert clean_word("linguistics:") == "linguistics"

def test_clean_word_remove_multiple_characters():
    assert clean_word("(linguistics),") == "linguistics"

def test_clean_word_unchanged_normal_word():
    assert clean_word("linguistics") == "linguistics"