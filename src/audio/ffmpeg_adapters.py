"""
Archivo con las interfaz de FFMpeg para adaptar al programa la comunicación del audio a Saslida.
@author Iván Valero Rodríguez
"""
import subprocess
from audio.generic_adapters import AudioPlayerAdapter

class FFMpegPlayerAdapter(AudioPlayerAdapter):
    """
        Interfaz de reproducción de audio a través de FFMpeg
    """
    def play(self, audio):
        """
            Reproduce un archivo de audio (en cualquier formato) o un stream m4a
            :param: audio Archivo de audio o stream en cualquier formato
        """
        subprocess.call(['ffplay','-nodisp','-autoexit',audio])
