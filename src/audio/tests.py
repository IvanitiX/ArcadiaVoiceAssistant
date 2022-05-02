from arcadia.settings import TESTING_FILES
from .pyaudio_adapters import PyAudioPlayerAdapter, PyAudioRecordingAdapter

class TestPyAudio():
    def test_pyaudio_player(self):
        print(":: [T] Prueba de reproducción de audio")
        test_player = PyAudioPlayerAdapter()
        path = '{0}/input.wav'.format(TESTING_FILES)
        print(path)
        test_player.play(path)
        assert True

    def test_pyaudio_recorder(self):
        print(":: [T] Prueba de grabación de audio")
        test_recorder = PyAudioRecordingAdapter()
        sw, data = test_recorder.record_voice()
        print("DEBUG: Tamaño del stream de datos : {0}/ Ancho de muestreo : {1}\n".format(len(data),sw))
        assert (len(data) > 0)
        assert (sw > 0)

    def test_pyaudio_streaming(self):
        print(":: [T] Prueba de streaming de audio")
        test_recorder = PyAudioRecordingAdapter()
        test_recorder.stream_voice()

