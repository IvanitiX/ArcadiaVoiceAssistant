from pydantic import BaseModel

from sr import vosk_adapter
from tts import nanotts_adapter

AVAILABLE_SR_MODELS = {
    'vosk' : vosk_adapter.VoskAdapter()
    #'whisper' : whisper_adapter.WhisperAdapter()
}
AVAILABLE_TTS_MODELS = {
    'nanotts' : nanotts_adapter.NanoTTSAdapter()
}


class ArcadiaPetition(BaseModel):
    query: str

class TTSQuery(BaseModel):
    text_to_read: str