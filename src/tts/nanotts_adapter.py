"""
Archivo con la interfaz genérica de Text-to-Speech
@author Iván Valero Rodríguez
"""
import nanotts
from arcadia import settings
from tts.generic_adapters import TTSGenericAdapter


class NanoTTSAdapter(TTSGenericAdapter):
    """
    Clase de síntesis de voz usando NanoTTS
    """
    def __init__(self):
        self.nano_tts = nanotts.NanoTTS(
            voice=settings.VOICE_TTS,
            outputFile=f'{settings.TESTING_FILES}/nano.wav',
            speed=settings.SPEED_TTS,
            pitch=settings.PITCH_TTS
        )
        print(f'{settings.TESTING_FILES}/nano.wav')

    def generate_voice(self, text):
        """
            Genera un audio narrado por una voz sintética
            @param text Texto a leer
            @return nano_wav Referencia al audio exportado.
        """
        self.nano_tts.speaks(text)
