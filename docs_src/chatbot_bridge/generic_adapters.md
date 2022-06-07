## **generic\_adapters**


Archivo para adaptar la comunicación de chatbots de forma genérica.  

 --- 
 
### Clase **ChatbotGenericAdapter**
      Interfaz genérica de comunicación de chatbots.
Sirve para especificar los métodos a implementar en adaptadores
de sistemas de chatbot, heredando de estas clases y sobrecargándolos.  
   #### Métodos
**get\_last\_result**(self)
Devuelve la respuesta de la última petición.
(Se debe implementar en el adaptador específico)

**make\_petition**(self, query)
Envía un texto para analizarlo.
(Se debe implementar en el a daptador específico)
##### Parámetros
**query** Texto para consultar.


