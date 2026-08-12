import pytest

from analysis.helpers.utterance import *

# Tests basic line processing
def test_process_utterance_line_process_normal_words():
    words = []

    process_utterance_line(
        "I saw a cat",
        lambda word: words.append(word)
    )

    assert words == ["I", "saw", "a", "cat"]

# Tests that empty lines are ignored
def test_process_utterance_line_ignore_empty_line():
    words = []

    process_utterance_line(
        "",
        lambda word: words.append(word)
    )

    assert words == []

# Tests that whitespace is ignored
def test_process_utterance_line_ignore_whitespace():
    words = []

    process_utterance_line(
        "   ",
        lambda word: words.append(word)
    )

    assert words == []

# Uses parametrize to test 6 examples of data that include invalid starts
@pytest.mark.parametrize(
    "invalid_word",
    ["0hello", "&hello", "+hello", "-hello", "#hello", "‡hello"]
)

def test_process_utterance_line_ignore_invalid_start(invalid_word):
    words = []

    process_utterance_line(
        invalid_word,
        lambda word: words.append(word)
    )

    assert words == []

# Uses parametrize to test 8 examples of ignored words
@pytest.mark.parametrize(
    "ignored_word",
    ["xxx", "www", "?", "!", "„", ".", ",", "(.)"]
)

def test_process_utterance_line_ignore_invalid_morph(ignored_word):
    words = []

    process_utterance_line(
        ignored_word,
        lambda word: words.append(word)
    )

    assert words == []

# Tests that valid words are processed when an utterance contains both valid and invalid words
def test_process_utterance_line_valid_and_invalid_words():
    words = []

    process_utterance_line(
        "I saw a xxx horse",
        lambda word: words.append(word)
    )

    assert words == ["I", "saw", "a", "horse"]

# Tests that the clean_word() call will clean the specified characters
def test_process_utterance_line_clean_words():
    words = []

    process_utterance_line(
        "where is (my) teddy,",
        lambda word: words.append(word)
    )

    assert words == ["where", "is", "my", "teddy"]

# Tests that text within angled brackets are ignored
def test_process_utterance_line_ignore_angle_bracketed_words():
    words = []

    process_utterance_line(
        "I love <fluffy> cats",
        lambda word: words.append(word)
    )

    assert words == ["I", "love", "cats"]

# Tests that text within squared brackets are ignored
def test_process_utterance_line_ignore_square_bracketed_words():
    words = []

    process_utterance_line(
        "I [don't] want carrots",
        lambda word: words.append(word)
    )

    assert words == ["I", "want", "carrots"]

# Tests that mispronounced words are replaced successfully
def test_process_utterance_line_use_replacement_word():
    words = []

    process_utterance_line(
        "I wn [: want] that",
        lambda word: words.append(word)
    )

    assert words == ["I", "want", "that"]

# Tests the count_morphemes() function
def test_count_morphemes_add_new_morpheme():
    counts = {}

    callback = count_morphemes(counts)

    callback("juice")

    assert counts["juice"] == 1