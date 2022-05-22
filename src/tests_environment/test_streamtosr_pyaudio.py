from sr.vosk_adapter import VoskAdapter
from chatbot_bridge.rasa_adapter import RasaChatbotAdapter
from arcadia import settings

class TestStreamtoSR():
    def test_sr_stream(self):
        sr = VoskAdapter()
        text = sr.recognize_stream()
        print(f':: Texto del stream : {text}')
        assert (len(text) > 0)

    def test_send_stream_sr(self):
        sr = VoskAdapter()
        chatbot = RasaChatbotAdapter()

        text = sr.recognize_stream()
        print(f':: Texto del stream : {text}')
        assert (len(text) > 0)

        response = chatbot.make_petition(text)
        assert(len(response) > 0)
        assert(response != None)
        assert(response != settings.NO_CONNECTION_TO_CHATBOT_MESSAGE)

        