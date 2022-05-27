from audio.generic_adapters import AudioRecorderAdapter, AudioPlayerAdapter
from arcadia import settings

from array import array
from sys import byteorder
from pyaudio import PyAudio
import wave

class PyAudioRecordingAdapter(AudioRecorderAdapter):
    def __init__(self):
        self.recorder = PyAudio()
        self.silenced_chunks = 0
        self.audio_started = False
        self.audio_finished = False

        self.THRESHOLD = settings.THRESHOLD 
        self.CHUNK_SIZE = settings.CHUNK_SIZE
        self.RATE = settings.RATE
        self.SILENT_CHUNKS = 1 * self.RATE / self.CHUNK_SIZE  # about 3sec
        self.FORMAT = settings.FORMAT
        self.FRAME_MAX_VALUE = settings.FRAME_MAX_VALUE
        self.NORMALIZE_MINUS_ONE_dB = settings.NORMALIZE_MINUS_ONE_dB
        self.CHANNELS = settings.CHANNELS
        self.TRIM_APPEND = settings.TRIM_APPEND
        self.AUDIO_FOLDER_PATH = settings.AUDIO_FOLDER_PATH

    def is_silent(self, audio_data_chunk):
        """
            Comprueba que un array de datos extraídos de la graabción
            esté en silencio
            @return Devuelve un booleano en función de si sobrepasa el THRESHOLD
        """
        print(max(audio_data_chunk))
        return max(audio_data_chunk) < self.THRESHOLD

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
                    if self.silenced_chunks > self.SILENT_CHUNKS:
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
            format=self.FORMAT,
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            output=True,
            frames_per_buffer=self.CHUNK_SIZE
        )

        data_all = array('h')

        while True:
            data_chunk = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)

            if self.check_silence(data_chunk):
                break            

        sample_width = self.recorder.get_sample_size(self.FORMAT)
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
            format=self.FORMAT,
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            frames_per_buffer=self.CHUNK_SIZE
        )

        stream.start_stream()

        return stream


class PyAudioPlayerAdapter(AudioPlayerAdapter):
    def __init__(self):
        self.player = PyAudio()
        self.CHUNK_SIZE = settings.PLAYER_CHUNK_SIZE

    def play(self,audio):
        """
            Reproduce un archivo en .WAV
        """
        audio_binary = wave.open(audio,'rb')

        audio_stream = self.player.open(
            format=self.player.get_format_from_width(audio_binary.getsampwidth()),
            channels=audio_binary.getnchannels(),
            rate=audio_binary.getframerate(),
            output=True
        )

        audio_chunk_data = audio_binary.readframes(self.CHUNK_SIZE)
        while (len(audio_chunk_data) > 0) :
            audio_stream.write(audio_chunk_data)
            audio_chunk_data = audio_binary.readframes(self.CHUNK_SIZE)

        self.player.close(audio_stream)
        audio_binary.close()
