##**vosk\_adapter** 


Archivo con la interfaz genérica de Reconocimiento de Voz usando Vosk  

 --- 

 
### Clase **PyAudioStreamOnVosk**
(implementa los métodos de [sr.generic\_adapters.StreamingRecognizerAdapter](generic_adapters.md#StreamingRecognizerAdapter)) 
      Clase genérica de reconocimiento de voz en Streaming desde PyAudio hasta Vosk  

#### Métodos
**recognize\_stream**(self, recognizer)Reconoce un streaming de audio
**Parámetro** recognizer Reconocedor de audio
**Devuelve** transcript Transcripción

 --- 
 
### Clase **VoskAdapter**
(implementa los métodos de [sr.generic\_adapters.SpeechRecognizerGenericAdapter](generic_adapters.md#SpeechRecognizerGenericAdapter)) 
      Clase genérica de reconocimiento de voz usando Vosk  

#### Métodos
**\_\_init\_\_**(self)
Initialize self.  See help(type(self)) for accurate signature.

**get\_last\_transcript**(self)
Devuelve la última transcripción
**Devuelve** last\_transcript Última transcripción

**recognize**(self, audio)
Reconoce un audio
**Parámetro** audio Un archivo de sonido
**Devuelve** last\_transcript Última transcripción

**recognize\_stream**(self)
Reconoce un streaming de audio
**Devuelve** last\_transcript Última transcripción

**reset\_transcript**(self)
Elimina la última transcripción

