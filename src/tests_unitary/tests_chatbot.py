from chatbot_bridge.rasa_adapter import RasaChatbotAdapter
from arcadia import settings

class TestChatbot():
    def test_rasa_chatbot(self):
        rasa = RasaChatbotAdapter()
        res = rasa.get_last_result()
        assert (res == '')
        res = rasa.make_petition('hola')
        res_aux = rasa.get_last_result()
        assert (res == res_aux)
        assert (res != settings.NO_CONNECTION_TO_CHATBOT_MESSAGE), "[X_X] Parece que no has conectado el servidor de Rasa o lo has movido de puerto"

    def test_rasa_chatbot_disconnected(self):
        rasa = RasaChatbotAdapter()
        res = rasa.get_last_result()
        assert (res == '')
        res = rasa.make_petition('hola')
        res_aux = rasa.get_last_result()
        assert (res == res_aux)
        assert (res == settings.NO_CONNECTION_TO_CHATBOT_MESSAGE), "Para esta prueba tienes que desconectar Rasa"
