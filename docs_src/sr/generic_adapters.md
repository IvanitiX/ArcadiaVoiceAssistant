## **generic\_adapters**


Archivo con la interfaz genérica de Reconocimiento de Voz  

 --- 
 
### Clase **SpeechRecognizerGenericAdapter**
      Clase genérica de reconocimiento de voz  
  #### Métodos
**get\_last\_transcript**(self)
Devuelve la última transcripción

**recognize**(self, audio)
Reconoce un audio
**Parámetro** audio Un archivo de sonido

 --- 
 
### Clase **StreamingRecognizerAdapter**
      Clase genérica de reconocimiento de voz en Streaming  
  #### Métodos
**recognize\_stream**(self, recognizer)
Reconoce un streaming de audio
**Parámetro** recognizer Reconocedor de audio
