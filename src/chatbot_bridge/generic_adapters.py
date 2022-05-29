"""
Archivo para adaptar la comunicación de chatbots de forma genérica.
@author Iván Valero Rodríguez
"""
class ChatbotGenericAdapter():
    """
        Interfaz genérica de comunicación de chatbots.
        Sirve para especificar los métodos a implementar en adaptadores
        de sistemas de chatbot, heredando de estas clases y sobrecargándolos.
    """
    def make_petition(self,query):
        """
            Envía un texto para analizarlo.
            @param query Texto para consultar.
            (Se debe implementar en el adaptador específico)
        """

    def get_last_result(self):
        """
            Devuelve la respuesta de la última petición.
            (Se debe implementar en el adaptador específico)
        """
