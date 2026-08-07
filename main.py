from analysis.transcript import analyse_transcript_metadata
from analysis.types.api_types import *
from analysis.freq import freq
from analysis.kwal import kwal
from analysis.lexrare import lexrare
from analysis.mlu import mlu
from fastapi import FastAPI

app = FastAPI()

@app.post("/transcript/metadata")
def transcript_metadata_endpoint(body: MetadataBody):
    response = analyse_transcript_metadata(body)
    return response

@app.post("/analysis/freq")
def freq_endpoint(body: FreqBody):
    response = freq(body)
    return response

@app.post("/analysis/kwal")
def kwal_endpoint(body: KwalBody):
    response = kwal(body)
    return response

@app.post("/analysis/lexrare")
def lexrare_endpoint(body: LexBody):
    response = lexrare(body)
    return response

@app.post("/analysis/mlu")
def mlu_endpoint(body: MluBody):
    response = mlu(body)
    return response