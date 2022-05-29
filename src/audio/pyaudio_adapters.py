"""
Archivo con las interfaz de PyAudio para adaptar al programa la comunicación del audio a E/S.
@author Iván Valero Rodríguez
"""
from array import array
from sys import byteorder
import wave
from pyaudio import PyAudio

from arcadia import settings
from audio.generic_adapters import AudioRecorderAdapter, AudioPlayerAdapter

class PyAudioRecordingAdapter(AudioRecorderAdapter):
    """
        Interfaz de grabación de audio a través de PyAudio
    """
    def __init__(self):
        self.recorder = PyAudio()
        self.silenced_chunks = 0
        self.audio_started = False
        self.audio_finished = False
        self.last_stream = array('h')
        self.threshold = settings.THRESHOLD
        self.chunk_size = settings.CHUNK_SIZE
        self.rate = settings.RATE
        self.silent_chunks = 1 * self.rate / self.chunk_size  # about 3sec
        self.format = settings.FORMAT
        self.frame_max_value = settings.FRAME_MAX_VALUE
        self.normalize_minus_one_db = settings.NORMALIZE_MINUS_ONE_DB
        self.channels = settings.CHANNELS
        self.trim_append = settings.TRIM_APPEND
        self.audio_folder_path = settings.AUDIO_FOLDER_PATH

    def is_silent(self, audio_data_chunk):
        """
            Comprueba que un array de datos extraídos de la graabción
            esté en silencio
            @return Devuelve un booleano en función de si sobrepasa el THRESHOLD
        """
        print(max(audio_data_chunk))
        return max(audio_data_chunk) < self.threshold

    def check_silence(self, stream_data):
        """
            Comprueba que una grabación o streaming esté en silencio.
            @param stream_data Un fragmento de la grabación o streaming
            @return Devuelve un booleano en función de si está en silencio o no
        """
        data_chunk = array('h', stream_data)
        if byteorder == 'big':
            data_chunk.byteswap()

        silent = self.is_silent(data_chunk)

        if self.audio_started:
            if silent:
                self.silenced_chunks += 1
                if self.silenced_chunks > self.silent_chunks:
                    self.audio_started = False
                    self.last_stream = array('h')
                    return True
            else:
                self.silenced_chunks = 0
        elif not silent:
            self.audio_started = True
        return False

    def record_voice(self):
        """
            Graba un audio con el micrófono
            @return sample_width Tamaño de muestra de un audio
            @return data_all La grabación del micrófono en formato binario.
        """
        stream = self.recorder.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk_size
        )

        data_all = array('h')

        while True:
            data_chunk = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)

            if self.check_silence(data_chunk):
                break

        sample_width = self.recorder.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        self.audio_started = False
        self.silenced_chunks = 0
        self.recorder.terminate()

        return sample_width, data_all

    def stream_voice(self):
        """
            Inicia una comunicación entre el micrófono y el dispositivo
            @return stream Comunicación de lo que recibe el micrófono en el dispositivo.
        """
        stream = self.recorder.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        stream.start_stream()

        return stream


class PyAudioPlayerAdapter(AudioPlayerAdapter):
    """
        Interfaz de reproducción de audio a través de PyAudio
    """
    def __init__(self):
        self.player = PyAudio()
        self.chunk_size = settings.PLAYER_CHUNK_SIZE

    def play(self,audio):
        """
            Reproduce un archivo en .WAV
            :param: audio Archivo de audio en formato .wav
        """
        audio_binary = wave.open(audio,'rb')

        audio_stream = self.player.open(
            format=self.player.get_format_from_width(audio_binary.getsampwidth()),
            channels=audio_binary.getnchannels(),
            rate=audio_binary.getframerate(),
            output=True
        )

        audio_chunk_data = audio_binary.readframes(self.chunk_size)
        while len(audio_chunk_data) > 0 :
            audio_stream.write(audio_chunk_data)
            audio_chunk_data = audio_binary.readframes(self.chunk_size)

        self.player.close(audio_stream)
        audio_binary.close()
