"""
Archivo para adaptar la comunicación de chatbots usando Rasa.
@author Iván Valero Rodríguez
"""
import requests
from arcadia import settings
from chatbot_bridge.generic_adapters import ChatbotGenericAdapter

class RasaChatbotAdapter(ChatbotGenericAdapter):
    """
        Interfaz genérica de comunicación de chatbots con Rasa.
    """
    def __init__(self):
        self.last_result = []
    
    def no_connection_to_knowledge_server(self):
        """
            Retorna el mensaje para avisar que no puede conectarse a Rasa.
            @return settings.NO_CONNECTION_TO_CHATBOT_MESSAGE Mensaje de aviso.
        """
        return settings.NO_CONNECTION_TO_CHATBOT_MESSAGE

    def make_petition(self, query):
        """
            Envía un texto a Rasa para analizarlo, devolviendo una respuesta.
            @param query Texto para consultar.
            @return last_result Respuesta de Rasa a la petición solicitada.
        """
        self.last_result = []
        request = None
        try:
            request = requests.post('http://{0}:5005/webhooks/rest/webhook'.format(settings.RASA_IP), \
            json={"sender": '', "message": query})
        except requests.exceptions.ConnectionError:
            self.last_result = [self.no_connection_to_knowledge_server(),]

        if request is not None:
            print(f"Bot says, {request.json()}")
            for i in request.json():
                try:
                    self.last_result.append(i['text'])
                except KeyError:
                    try:
                        if i['custom']['text']:
                            text = i['custom']['text']
                            self.last_result.append(f'{text}')
                        if 'audio' in i['custom']:
                            source = str(i['custom']['audio'])
                            self.last_result.append(f'[>] {source}')
                        if 'source' in i['custom']:
                            self.last_result.append(f"[<>] {i['custom']['source']}")
                    except KeyError:
                        pass
        print(f"{self.last_result}")

        return self.get_last_result()

    def get_last_result(self):
        """
            Devuelve la respuesta de la última petición.
            @return last_result Ultima respuesta de Rasa a la petición solicitada.
        """
        return self.last_result
