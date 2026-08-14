from unittest.mock import MagicMock
from analysis.types.api_types import KwalBody
from analysis.types.api_types import TranscriptInstance

import analysis.kwal as kwal_module

def test_kwal_find_word(monkeypatch):
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
        kwal_module,
        "supabase",
        mock_supabase
    )

    payload = KwalBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        search_utterance=["wine"]
    )

    result = kwal_module.kwal(payload)

    matches = result["test_transcript"]

    assert len(matches) == 2

    match = matches[0]

    assert match.keyword == "wine"
    assert match.line_number == 5
    assert match.speaker == "CHI"
    assert match.utterance == "*CHI:\tthis wine and this ..."

def test_kwal_return_no_match_for_missing_word(monkeypatch):
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
        kwal_module,
        "supabase",
        mock_supabase
    )

    payload = KwalBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ],
        search_utterance=["apple"]
    )

    result = kwal_module.kwal(payload)

    assert result["test_transcript"] == []