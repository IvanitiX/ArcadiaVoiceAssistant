from sr import vosk_adapter
from arcadia import settings

class TestSR():
    def test_sr_audio(self):
        sr = vosk_adapter.VoskAdapter()
        path = path = '{0}/input.wav'.format(settings.TESTING_FILES)
        text = sr.recognize(path)

        assert (text is not None)
        assert (len(text) > 0)
