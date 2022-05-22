from time import sleep
import wave
from tts import nanotts_adapter
from arcadia import settings
from audio.pyaudio_adapters import PyAudioPlayerAdapter

def test_playttsaudio_pyaudio():
    tts = nanotts_adapter.NanoTTSAdapter()
    player = PyAudioPlayerAdapter()

    tts.generate_voice("Hola, buenas tardes desde PyAudio")
    sleep(3)
    path = '{0}/nano.wav'.format(settings.TESTING_FILES)

    wav = wave.open(path)
    assert (wav.getnframes() > 0)

    player.play(path)
    assert True

def test_playttsaudio_ffmpeg():
    tts = nanotts_adapter.NanoTTSAdapter()
    player = PyAudioPlayerAdapter()

    tts.generate_voice("Hola, buenas tardes desde ffmpeg")
    sleep(3)
    path = '{0}/nano.wav'.format(settings.TESTING_FILES)

    wav = wave.open(path)
    assert (wav.getnframes() > 0)

    player.play(path)
    assert True



