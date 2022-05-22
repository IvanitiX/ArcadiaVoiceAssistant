from audio.ffmpeg_adapters import FFMpegPlayerAdapter
from arcadia.settings import TESTING_FILES

class TestFFMpeg():
    def test_pyaudio_player(self):
        print(":: [T] Prueba de reproducción de audio")
        test_player = FFMpegPlayerAdapter()
        path = '{0}/input.wav'.format(TESTING_FILES)
        print(path)
        test_player.play(path)
        assert True