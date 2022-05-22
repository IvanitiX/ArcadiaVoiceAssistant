from time import sleep
from tts import nanotts_adapter
from arcadia import settings
import wave

class TestTTS():
    def test_generate_tts(self):
        tts = nanotts_adapter.NanoTTSAdapter()
        tts.generate_voice("Hola, buenas tardes")
        sleep(3)
        wav = wave.open('{0}/nano.wav'.format(settings.TESTING_FILES))
        assert (wav.getnframes() > 0)