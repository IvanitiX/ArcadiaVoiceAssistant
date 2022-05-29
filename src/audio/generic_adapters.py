"""
Archivo con las interfaces para adaptar al programa la comunicación del audio a E/S.
@author Iván Valero Rodríguez
"""
class AudioRecorderAdapter():
    """
        Interfaz genérica de grabación de audio.
        Sirve para especificar los métodos a implementar en adaptadores
        de sistemas de audio, heredando de estas clases y sobrecargándolos.
    """
    def record_voice(self):
        """
            Graba un audio con el micrófono
            (Se debe implementar en el adaptador específico)
        """

    def stream_voice(self):
        """
            Inicia una comunicación entre el micrófono y el dispositivo
            (Se debe implementar en el adaptador específico)
        """

class AudioPlayerAdapter():
    """
        Interfaz genérica de reproducción de audio.
        Sirve para especificar los métodos a implementar en adaptadores
        de sistemas de audio, heredando de estas clases y sobrecargándolos.
    """

    def play(self,audio):
        """
            Reproduce un archivo de audio
            :param: audio Archivo de audio o stream en cualquier formato
            (Se debe implementar en el adaptador específico)
        """
