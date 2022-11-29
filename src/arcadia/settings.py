"""
    Archivo de parámetros y configuraciones del Asistente.
"""
import os
from pyaudio import paInt16
from sr.vosk_adapter import PyAudioStreamOnVosk

# Configuraciones para IP de conexión a Rasa
RASA_IP = os.getenv('RASA_IP');

#Configuraciones para el grabador de PyAudio
THRESHOLD = 10000
CHUNK_SIZE = 1024
RATE = 16000
SILENT_CHUNKS = 1 * RATE / CHUNK_SIZE  # about 3sec
FORMAT = paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_DB = 10 ** (-1.0 / 20)
CHANNELS = 1
TRIM_APPEND = RATE / 4

# Configuraciones para el reproductor en PyAudio
PLAYER_CHUNK_SIZE = 1024

#Configuraciones para Vosk
VOSK_MODEL_PATH = os.path.abspath('model_files/model/')
VOSK_RATE = 16000
RECORDER_ADAPTER = PyAudioStreamOnVosk()

# Configuraciones para Whisper
WHISPER_MODEL = 'base'

#Configuraciones para el chatbot
BOT_NAME_VARIANTS = ['arcadia', 'arabia',]
NO_CONNECTION_TO_CHATBOT_MESSAGE = '¡Oh, no! No puedo atenderte en este momento porque no puedo acceder a mis conocimientos, lo siento.'

#Configuraciones de NanoTTS
VOICE_TTS = 'es-ES'
SPEED_TTS = 1.25
PITCH_TTS = 1.1

# Configuraciones para testing
TESTING_FILES = os.path.abspath('test_files')
AUDIO_FOLDER_PATH = TESTING_FILES
