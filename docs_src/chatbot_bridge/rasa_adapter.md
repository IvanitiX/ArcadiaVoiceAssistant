
## **rasa\_adapter**

Archivo para adaptar la comunicación de chatbots usando Rasa.  

### Clase **RasaChatbotAdapter**
(hereda de [chatbot\_bridge.generic\_adapters.ChatbotGenericAdapter](chatbot_bridge.generic_adapters.html#ChatbotGenericAdapter)) 
      Interfaz de comunicación de chatbots con Rasa.  

#### Métodos
**\_\_init\_\_**(self)
Inicializador de parámetros

**get\_last\_result**(self)
Devuelve la respuesta de la última petición.
**Devuelve** last\_result Ultima respuesta de Rasa a la petición solicitada.

**make\_petition**(self, query)
Envía un texto a Rasa para analizarlo, devolviendo una respuesta.
**Parámetro** *query* Texto para consultar.
**Devuelve** *last\_result* Respuesta de Rasa a la petición solicitada.

**no\_connection\_to\_knowledge\_server**(self)
Retorna el mensaje para avisar que no puede conectarse a Rasa.
**Devuelve** *settings.NO\_CONNECTION\_TO\_CHATBOT\_MESSAGE* Mensaje de aviso.
