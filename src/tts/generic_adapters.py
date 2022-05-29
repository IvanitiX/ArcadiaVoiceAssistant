"""
Archivo con la interfaz genérica de Text-to-Speech
@author Iván Valero Rodríguez
"""
class TTSGenericAdapter():
    """
    Clase genérica de síntesis de voz
    """
    def generate_voice(self,text):
        """
            Genera un audio narrado por una voz sintética
            @param text Texto a leer
        """
