"""
    Archivo de instanciación de clases para gestionar el loop principal.
"""

from audio import pyaudio_adapters, ffmpeg_adapters
from sr import vosk_adapter
from tts import nanotts_adapter
from chatbot_bridge import rasa_adapter

print("Cargando PyAudio")
RECORDER = pyaudio_adapters.PyAudioRecordingAdapter()
RESPONSE_PLAYER = pyaudio_adapters.PyAudioPlayerAdapter()
print("Cargando PyAudio")
print("Cargando FFMpeg")
MEDIA_PLAYER = ffmpeg_adapters.FFMpegPlayerAdapter()
print("Cargando FFMpeg")
print("Cargando Vosk")
SPEECH_RECOGNIZER = vosk_adapter.VoskAdapter()
print("Cargando Vosk")
print("Cargando NanoTTS")
TEXT_TO_SPEECH_GENERATOR = nanotts_adapter.NanoTTSAdapter()
print("Cargando NanoTTS")
print("Cargando Rasa")
CHATBOT = rasa_adapter.RasaChatbotAdapter()
print("Cargando Rasa")
