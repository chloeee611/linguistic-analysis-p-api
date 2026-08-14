from unittest.mock import MagicMock
from analysis.types.api_types import FreqBody, TranscriptInstance

import analysis.freq as freq_module

# Tests that FREQ will count words correctly
def test_freq_counts_words(monkeypatch):
    transcript = """@Begin
*BEL:\twhere is lemon juice .
*CHI:\tthis .
*BEL:\tand what is this .
*CHI:\tthis wine and this ...
*LIN:\twine &=laugh .
*LIN:\tthis is lemon juice .
@End"""

    mock_supabase = MagicMock()

    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        freq_module,
        "supabase",
        mock_supabase
    )

    payload = FreqBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        search=[]
    )

    result = freq_module.freq(payload)

    analysis = result["test_transcript"]

    assert "CHI" in analysis
    assert "LIN" in analysis

    assert analysis["CHI"]["counts"]["this"] == 3
    assert analysis["CHI"]["counts"]["wine"] == 1
    assert analysis["CHI"]["counts"]["and"] == 1

    assert analysis["LIN"]["counts"]["this"] == 1
    assert analysis["LIN"]["counts"]["juice"] == 1

# Tests that FREQ will calculate the unique words ratio correctly
def test_freq_calculate_unique_words_ratio(monkeypatch):
    transcript = """@Begin
*BEL:\twhere is lemon juice .
*CHI:\tthis .
*BEL:\tand what is this .
*CHI:\tthis wine and this ...
*LIN:\twine &=laugh .
*LIN:\tthis is lemon juice .
@End"""
    
    mock_supabase = MagicMock()

    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        freq_module,
        "supabase",
        mock_supabase
    )

    payload = FreqBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        search=[]
    )

    result = freq_module.freq(payload)

    analysis = result["test_transcript"]["CHI"]["summary"]

    assert analysis["total_unique_words"] == 3
    assert analysis["total_items"] == 5
    assert analysis["unique_word_ratio"] == 0.6