"""
Archivo con la interfaz genérica de Text-to-Speech
@author Iván Valero Rodríguez
"""
import subprocess, shutil
from arcadia import settings
from tts.generic_adapters import TTSGenericAdapter


class NanoTTSAdapter(TTSGenericAdapter):
    """
    Clase de síntesis de voz usando NanoTTS
    """
    def __init__(self):
        self.nano_tts = {
            'voice': settings.VOICE_TTS,
            'outputFile':f'test_files/nano.wav',
            'speed':settings.SPEED_TTS,
            'pitch':settings.PITCH_TTS,
            'play': None,
            'volume': None
        }

        if shutil.which("nanotts") is None:
            raise Exception(
                "Can't find nanotts executable. Make sure to add it to the $PATH."
            )
        self._path = shutil.which("nanotts")[:-7]

    def generate_voice(self, text):
        """
            Genera un audio narrado por una voz sintética
            @param text Texto a leer
            @return nano_wav Referencia al audio exportado.
        """
        command = ['/code/tts/nanotts.sh',text,self.nano_tts['voice'],self.nano_tts['outputFile'],
                   str(self.nano_tts['pitch']), str(self.nano_tts['speed'])]
        # command.append("-i")
        # command.append(f'\"{text}\"')

        # if self.nano_tts['voice'] is not None:
        #     command.append("--voice")
        #     command.append(self.nano_tts['voice'])
        # if self.nano_tts['outputFile'] is not None:
        #     command.append("-o")
        #     command.append(self.nano_tts['outputFile'])
        # if self.nano_tts['play']:
        #     command.append("-p")
        # if self.nano_tts['speed'] is not None:
        #     command.append("--speed")
        #     command.append(str(self.nano_tts['speed']))
        # if self.nano_tts['pitch'] is not None:
        #     command.append("--pitch")
        #     command.append(str(self.nano_tts['pitch']))
        # if self.nano_tts['volume'] is not None:
        #     command.append("--volume")
        #     command.append(str(self.nano_tts['volume']))
        
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
