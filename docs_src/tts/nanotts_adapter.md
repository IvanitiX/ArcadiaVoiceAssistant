## **nanotts\_adapter**


Archivo con la interfaz genérica de Text-to-Speech  

 
class **NanoTTSAdapter**
(implementa los métodos de [tts.generic\_adapters.TTSGenericAdapter](generic_adapters.md#TTSGenericAdapter)) 
      Clase de síntesis de voz usando NanoTTS  

#### Métodos

**\_\_init\_\_**(self)
Initialize self.  See help(type(self)) for accurate signature.

**generate\_voice**(self, text)
Genera un audio narrado por una voz sintética
**Parámetro** *text* Texto a leer
**Devuelve** *nano\_wav* Referencia al audio exportado.
