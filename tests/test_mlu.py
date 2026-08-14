from analysis.types.api_types import MluBody, TranscriptInstance
from unittest.mock import MagicMock

import analysis.mlu as mlu_module

def test_mlu_calculate_mean_length_utterance(monkeypatch):
    transcript = """@Begin
*CHI:\tyes .
*CHI:\tthis is okay .
@End"""

    mock_supabase = MagicMock()

    mock_supabase.storage.from_.return_value.download.return_value = (
        transcript.encode("utf-8")
    )

    monkeypatch.setattr(
        mlu_module,
        "supabase",
        mock_supabase
    )

    payload = MluBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ]
    )

    result = mlu_module.mlu(payload)

    analysis = result["test_transcript"]["counts"]["CHI"]

    assert analysis["utterances"] == 2
    assert analysis["morphs"] == 4
    assert analysis["mlu"] == 2.0

def test_mlu_separates_speakers(monkeypatch):
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
        mlu_module,
        "supabase",
        mock_supabase
    )

    payload = MluBody(
        urls=[
            TranscriptInstance(
                id="test_transcript",
                file_url="test.cha"
            )
        ]
    )

    result = mlu_module.mlu(payload)

    chi = result["test_transcript"]["counts"]["CHI"]
    bel = result["test_transcript"]["counts"]["BEL"]

    assert chi["utterances"] == 2
    assert chi["morphs"] == 5
    assert chi["mlu"] == 2.5

    assert bel["utterances"] == 2
    assert bel["morphs"] == 8
    assert bel["mlu"] == 4.0