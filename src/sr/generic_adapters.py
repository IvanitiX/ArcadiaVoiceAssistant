"""
Archivo con la interfaz genérica de Reconocimiento de Voz
@author Iván Valero Rodríguez
"""
class StreamingRecognizerAdapter():
    """
    Clase genérica de reconocimiento de voz en Streaming
    """
    def recognize_stream(self, recognizer):
        """
        Reconoce un streaming de audio
        @param recognizer Reconocedor de audio
        """
class SpeechRecognizerGenericAdapter():
    """
    Clase genérica de reconocimiento de voz
    """

    def recognize(self,audio):
        """
        Reconoce un audio
        @param audio Un archivo de sonido
        """

    def get_last_transcript(self):
        """
        Devuelve la última transcripción
        """
