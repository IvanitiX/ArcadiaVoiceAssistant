from arcadia import settings
from sr import generic_adapters

import whisper
import numpy as np

class WhisperStreamingRecognizer(generic_adapters.StreamingRecognizerAdapter):
    def recognize_stream(self, model):
        from audio.pyaudio_adapters import PyAudioRecordingAdapter
        adapter = PyAudioRecordingAdapter()
        stream = adapter.record_voice()
        data = np.frombuffer(bytes(stream[1]), np.int16).flatten().astype(np.float32) / 32768.0 

        transcription = str(model.transcribe(data)['text']).lower().replace(',','').replace('.','')
        print(transcription)
        return transcription

class WhisperAdapter(generic_adapters.SpeechRecognizerGenericAdapter):
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL) 
        self.last_transcript = ''
        self.recorder_adapter = WhisperStreamingRecognizer()

    def recognize(self, audio):
        """
        Reconoce un audio
        @param audio Un archivo de sonido
        @return last_transcript Última transcripción
        """
        print(':: Reconociendo audio...')
        print(audio)
        self.reset_transcript()
        self.last_transcript = self.model.transcribe(audio)
        return self.get_last_transcript()

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

    def recognize_stream(self):
        """
        Reconoce un streaming de audio
        @return last_transcript Última transcripción
        """
        print(':: Reconociendo stream...')
        self.reset_transcript()

        return self.recorder_adapter.recognize_stream(self.model)