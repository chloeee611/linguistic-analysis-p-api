from analysis.types.api_types import LexBody, TranscriptInstance
from unittest.mock import MagicMock

import analysis.lexrare as lexrare_module

def test_lexrare_common_word(monkeypatch):
    transcript = """@Begin
*CHI:\thello .
@End"""

    mock_supabase = MagicMock()

    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        lexrare_module,
        "supabase",
        mock_supabase
    )

    payload = LexBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        target_tier="utt"
    )

    result = lexrare_module.lexrare(payload)

    analysis = result["test_transcript"]["CHI"]

    assert analysis.num_common_words == 1
    assert analysis.num_rare_words == 0
    assert analysis.num_total_words == 1

def test_lexrare_rare_word(monkeypatch):
    transcript = """@Begin
*CHI:\thedgehog .
@End"""

    mock_supabase = MagicMock()
    
    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        lexrare_module,
        "supabase",
        mock_supabase
    )

    payload = LexBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        target_tier="utt"
    )

    result = lexrare_module.lexrare(payload)

    analysis = result["test_transcript"]["CHI"]

    assert analysis.num_common_words == 0
    assert analysis.num_rare_words == 1
    assert analysis.num_total_words == 1

def test_lexrare_percent_rare_word(monkeypatch):
    transcript = """@Begin
*CHI:\tthis is my hedgehog .
@End"""

    mock_supabase = MagicMock()
    
    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        lexrare_module,
        "supabase",
        mock_supabase
    )

    payload = LexBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        target_tier="utt"
    )

    result = lexrare_module.lexrare(payload)

    analysis = result["test_transcript"]["CHI"]

    assert analysis.num_common_words == 3
    assert analysis.num_rare_words == 1
    assert analysis.num_total_words == 4
    assert analysis.percent_rare_words == 0.25