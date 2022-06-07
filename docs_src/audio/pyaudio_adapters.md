## **generic\_adapters**


Archivo con las interfaces para adaptar al programa la comunicación del audio a E/S.  

  
 --- 
 
### Clase **AudioPlayerAdapter**
      Interfaz genérica de reproducción de audio.
Sirve para especificar los métodos a implementar en adaptadores
de sistemas de audio, heredando de estas clases y sobrecargándolos.  
#### Métodos
**play**(self, audio)
Reproduce un archivo de audio
##### Parámetros
 *audio* Archivo de audio o stream en cualquier formato
(Se debe implementar en el adaptador específico)

 --- 
 
### Clase **AudioRecorderAdapter** 
      Interfaz genérica de grabación de audio.
Sirve para especificar los métodos a implementar en adaptadores de sistemas de audio, heredando de estas clases y sobrecargándolos.  
#### Métodos
**record\_voice**(self)
Graba un audio con el micrófono
(Se debe implementar en el adaptador específico)
**stream\_voice**(self)Inicia una comunicación entre el micrófono y el dispositivo
(Se debe implementar en el adaptador específico)

 

 




