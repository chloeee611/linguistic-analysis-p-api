import analysis.freq as freq_module
from unittest.mock import MagicMock
from analysis.types.api_types import FreqBody, TranscriptInstance

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

    analysis = result["test_transcript"]["CHI"]

    assert analysis["counts"]["this"] == 3
    assert analysis["counts"]["wine"] == 1
    assert analysis["counts"]["and"] == 1

