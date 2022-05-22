import requests
from arcadia import settings
from .generic_adapters import ChatbotGenericAdapter

class RasaChatbotAdapter(ChatbotGenericAdapter):
    def __init__(self):
        self.last_result = ''

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
        self.last_result = ''
        r = None
        try:
            r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": '', "message": query})
        except requests.exceptions.ConnectionError as e:
            self.last_result = self.no_connection_to_knowledge_server()

        if r is not None:
            print("Bot says, ")
            for i in r.json():
                try:
                    self.last_result += i['text']
                except KeyError:
                    self.last_result += ''
        print(f"{self.last_result}")

        return self.get_last_result()

    def get_last_result(self):
        """
            Envía un texto a Rasa para analizarlo, devolviendo una respuesta.
            @param query Texto para consultar.
            @return last_result Respuesta de Rasa a la petición solicitada.
        """
        return self.last_result