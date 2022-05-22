import subprocess 
from .generic_adapters import AudioPlayerAdapter

class FFMpegPlayerAdapter(AudioPlayerAdapter):
    def play(self, audio):
        """
            Reproduce un archivo de audio (en cualquier formato) o un stream m4a
        """
        subprocess.call(['ffplay','-nodisp','-autoexit',audio])