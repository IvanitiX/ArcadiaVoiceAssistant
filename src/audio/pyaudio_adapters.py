from time import sleep
from .generic_adapters import AudioRecorderAdapter, AudioPlayerAdapter
from arcadia import settings

from array import array
from sys import byteorder
from pyaudio import PyAudio, paContinue
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
        return max(audio_data_chunk) < self.THRESHOLD

    def parse_callback(self,input_data, frame_count, time_info, flags):
        data_chunk = array('h', input_data)
        if byteorder == 'big':
            data_chunk.byteswap()

        silent = self.is_silent(data_chunk)

        if self.audio_started:
            if silent:
                self.silenced_chunks += 1
                if self.silenced_chunks > self.SILENT_CHUNKS:
                    self.audio_finished = True
            else: 
                self.silenced_chunks = 0
        elif not silent:
            self.audio_started = True

        print(frame_count)
        print(time_info)
        print(flags)
        return input_data, paContinue


    def record_voice(self):
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

            silent = self.is_silent(data_chunk)

            if self.audio_started:
                if silent:
                    self.silenced_chunks += 1
                    if self.silenced_chunks > self.SILENT_CHUNKS:
                        break
                else: 
                    self.silenced_chunks = 0
            elif not silent:
                self.audio_started = True             

        sample_width = self.recorder.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        self.audio_started = False
        self.silenced_chunks = 0
        self.recorder.terminate()

        return sample_width, data_all

    def stream_voice(self):
        stream = self.recorder.open(
            format=self.FORMAT,
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            output=True,
            frames_per_buffer=self.CHUNK_SIZE,
            stream_callback=self.parse_callback
        )

        stream.start_stream()

        while stream.is_active():
            sleep(0.1)
            if self.audio_finished:
                stream.stop_stream()
                self.audio_finished = False
                self.audio_started = False
                self.silenced_chunks = 0


class PyAudioPlayerAdapter(AudioPlayerAdapter):
    def __init__(self):
        self.player = PyAudio()
        self.CHUNK_SIZE = settings.PLAYER_CHUNK_SIZE

    def play(self,audio):
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
