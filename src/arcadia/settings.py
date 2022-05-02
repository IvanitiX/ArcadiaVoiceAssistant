"""
    Archivo de parámetros y configuraciones del Asistente.
"""
import os
import pyaudio

#Configuraciones para el grabador de PyAudio
THRESHOLD = 1500 
CHUNK_SIZE = 1024
RATE = 16000
SILENT_CHUNKS = 1 * RATE / CHUNK_SIZE  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
CHANNELS = 1
TRIM_APPEND = RATE / 4

# Configuraciones para el reproductor en PyAudio
PLAYER_CHUNK_SIZE = 1024

# Configuraciones para testing
TESTING_FILES = os.path.abspath('test_files')
AUDIO_FOLDER_PATH = TESTING_FILES