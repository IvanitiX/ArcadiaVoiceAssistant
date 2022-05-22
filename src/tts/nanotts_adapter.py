from .generic_adapters import TTSGenericAdapter
from arcadia import settings
import nanotts

class NanoTTSAdapter(TTSGenericAdapter):
    def __init__(self):
        self.nano_tts = nanotts.NanoTTS(
            voice=settings.VOICE_TTS,
            outputFile='{0}/nano.wav'.format(settings.TESTING_FILES),
            speed=settings.SPEED_TTS, 
            pitch=settings.PITCH_TTS
        )
        print('{0}/nano.wav'.format(settings.TESTING_FILES))

    def generate_voice(self, text):
        """
            Genera un audio narrado por una voz sintética
            @param text Texto a leer
            @return nano_wav Referencia al audio exportado. 
        """
        nano_wav = self.nano_tts.speaks(text)
        return nano_wav