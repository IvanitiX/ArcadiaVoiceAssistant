"""
    Archivo de instanciación de clases para gestionar el loop principal.
"""

from audio import pyaudio_adapters, ffmpeg_adapters
from sr import vosk_adapter
from tts import nanotts_adapter
from chatbot_bridge import rasa_adapter

RECORDER = pyaudio_adapters.PyAudioRecordingAdapter()
RESPONSE_PLAYER = pyaudio_adapters.PyAudioPlayerAdapter()
MEDIA_PLAYER = ffmpeg_adapters.FFMpegPlayerAdapter()
SPEECH_RECOGNIZER = vosk_adapter.VoskAdapter()
TEXT_TO_SPEECH_GENERATOR = nanotts_adapter.NanoTTSAdapter()
CHATBOT = rasa_adapter.RasaChatbotAdapter()
