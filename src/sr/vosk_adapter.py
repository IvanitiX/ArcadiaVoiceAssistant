"""
Archivo con la interfaz genérica de Reconocimiento de Voz usando Vosk
@author Iván Valero Rodríguez
"""
import json
from vosk import Model, KaldiRecognizer
from arcadia import settings
from sr.generic_adapters import SpeechRecognizerGenericAdapter, StreamingRecognizerAdapter

class PyAudioStreamOnVosk(StreamingRecognizerAdapter):
    """
    Clase genérica de reconocimiento de voz en Streaming desde PyAudio hasta Vosk
    """
    def recognize_stream(self, recognizer):
        """
        Reconoce un streaming de audio
        @param recognizer Reconocedor de audio
        @return transcript Transcripción
        """
        from audio.pyaudio_adapters import PyAudioRecordingAdapter
        adapter = PyAudioRecordingAdapter()
        stream = adapter.stream_voice()
        transcript = ''

        while True:
            data = stream.read(4000)
            stream_silenced = adapter.check_silence(data)
            if stream_silenced or len(data) == 0:
                stream.stop_stream()
                break
            if len(data) == 0:
                stream.stop_stream()
                break
            if recognizer.AcceptWaveform(data):
                transcript = transcript + json.loads(recognizer.Result())['text'] + " "
        transcript = transcript + json.loads(recognizer.FinalResult())['text']
        return transcript

class VoskAdapter(SpeechRecognizerGenericAdapter):
    """
    Clase genérica de reconocimiento de voz usando Vosk
    """
    def __init__(self):
        self.model = Model(settings.VOSK_MODEL_PATH)
        self.rate = settings.VOSK_RATE
        self.recognizer = KaldiRecognizer(self.model, self.rate)
        self.last_transcript = ''
        self.recorder_adapter = settings.RECORDER_ADAPTER

    def get_last_transcript(self):
        """
        Devuelve la última transcripción
        @return last_transcript Última transcripción
        """
        return self.last_transcript

    def reset_transcript(self):
        """
        Elimina la última transcripción
        """
        self.last_transcript = ''

    def recognize(self,audio):
        """
        Reconoce un audio
        @param audio Un archivo de sonido
        @return last_transcript Última transcripción
        """
        print(':: Reconociendo audio...')
        print(audio)
        self.reset_transcript()
        audio_stream = open(audio,"rb")
        audio_stream.read(44)

        while True:
            data = audio_stream.read(4000)
            print(len(data))
            if len(data) == 0:
                break

            if self.recognizer.AcceptWaveform(data):
                self.last_transcript = self.last_transcript \
                    + json.loads(self.recognizer.Result())['text'] + " "
                print(f'Parcial: {self.last_transcript}')
            else:
                print('No se reconoce')

        self.last_transcript = self.last_transcript \
            + json.loads(self.recognizer.FinalResult())['text']
        print(f'Final: {self.last_transcript}')
        return self.get_last_transcript()

    def recognize_stream(self):
        """
        Reconoce un streaming de audio
        @return last_transcript Última transcripción
        """
        print(':: Reconociendo stream...')
        self.reset_transcript()

        return self.recorder_adapter.recognize_stream(self.recognizer)
