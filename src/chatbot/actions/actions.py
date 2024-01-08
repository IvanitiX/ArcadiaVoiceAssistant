"""
Archivo de acciones en Rasa
This files contains your custom actions which can be used to run
custom Python code.
@author Iván Valero Rodriguez
@generated_by Rasa
@docs https://rasa.com/docs/rasa/custom-actions
"""

import datetime
from math import ceil
import random
from typing import Any, Text, Dict, List
import wikipedia
import re

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionsSettings():
    """
    Clase para la configuración de variables necesarias en las acciones
    """
    NO_CONNECTION_TO_INTERNET = 'No me puedo conectar a Internet ahora mismo, lo siento.\
         Comprueba por si acaso la conexión.'
    OPENWEATHERMAP_API_KEY = '831587653e5df6adadd7d236ea88f6d6'


class ActionTellTime(Action):
    """
    Clase para la acción de decir la hora
    """

    def name(self) -> Text:
        """
        Declaración de la acción
        @return string Nombre de la acción
        """
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Ejecución de la acción.
        Extrae el datetime de este instante y extrae la hora
        @utter_message Devuelve la hora en formato HH y MM (15:30 -> Son las 15 horas y 30 minutos)
        """
        dispatcher.utter_message(text=f"Son las \
            {datetime.datetime.now().strftime('%H horas y %M minutos')}")

        return []

class ActionThrowDice(Action):
    """
    Clase para la acción de tirar el dado
    """

    def name(self) -> Text:
        """
        Declaración de la acción
        @return string Nombre de la acción
        """
        return "action_throw_dice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Ejecución de la acción.
        Genera un número aleatorio entre 1 y 6
        @utter_message Devuelve una cadena con el valor generado entre 1 y 6
        """
        value = random.Random().randint(1,6)
        dispatcher.utter_message(text=f"Acabo de tirar un dado y ha salido el {value}")

        return []


class ActionLightPrice(Action):
    """
    Clase para la acción de decir el precio de la luz
    """
    def name(self) -> Text:
        """
        Declaración de la acción
        @return string Nombre de la acción
        """
        return "action_light_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Ejecución de la acción.
        Extrae de Internet, de la API de preciodelaluz.com, los valores máximos, mínimos
        y actuales del precio de la luz.
        @utter_message Devuelve la cadena explicando los valores anteriormente descritos.
        """

        try:
            request = requests.get('https://api.preciodelaluz.org/v1/prices/now?zone=PCB')
            if request is not None:
                price = request.json()['price']
                price_now = f'{price} euros el megavatio hora'
            request = requests.get('https://api.preciodelaluz.org/v1/prices/avg?zone=PCB')
            if request is not None:
                price = request.json()['price']
                avg_price = f'{price} euros el megavatio hora'
            request = requests.get('https://api.preciodelaluz.org/v1/prices/max?zone=PCB')
            if request is not None:
                price = request.json()['price']
                range_hours = str(request.json()['hour']).replace('-', ' a ')
                max_price = f'a {price} euros el megavatio hora de {range_hours}'
            request = requests.get('https://api.preciodelaluz.org/v1/prices/min?zone=PCB')
            if request is not None:
                price = request.json()['price']
                range_hours = str(request.json()['hour']).replace('-', ' a ')
                min_price = f'a {price} euros el megavatio hora de {range_hours}'

            dispatcher.utter_message(text=f"En España, a esta hora, el precio es de {price_now}.\
                 De media, hoy pagaremos {avg_price}, siendo la hora más barata {min_price};\
                 y la más cara {max_price}")
        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(ActionsSettings.NO_CONNECTION_TO_INTERNET)

        return []

class ActionTellWeather(Action):
    """
    Clase para la acción de decir el tiempo en una localidad
    """
    #Códigos de fenómenos meteorológicos, con la respuesta que debería dar.
    CODES = {
        "200" : ", está habiendo una tormenta con algo de lluvia.",
        "201" : ", está en medio de una tormenta, y además lloviendo",
        "202" : ", está en medio de una tormenta lloviendo a cántaros",
        "210" : ", se avecina una pequeña tormenta",
        "211" : ", está en medio de una tormenta",
        "212" : ", está en medio de una fuerte tormenta",
        "221" : ", hay una tormenta con nubes y claros",
        "230" : ", está en medio de una tormenta con algo de llovizna",
        "231" : ", está en medio de una tormenta y además llovizneando",
        "232" : ", está en medio de una tormenta con una llovizna fuerte",

        "300" : ", está cayendo algo de llovizna",
        "301" : ", está llovizneando",
        "302" : ", está cayendo una fuerte llovizna",
        "310" : ", está cayendo algo de llovizna",
        "311" : ", está empezando a llover seriamente",
        "312" : ", está a punto de llover muy fuertemente. Llévate un paraguas. ",
        "313" : ", está a punto de llover muchísimo. Llévate un paraguas. ",
        "314" : ", está a punto de llover a cántaros. Llévate un paraguas. ",
        "321" : ", está chispeando bastante fuertemente. Llévate un paraguas. ",

        "500" : ", está lloviendo ligeramente. ",
        "501" : ", está lloviendo.",
        "502" : ", está lloviendo fuertemente.",
        "503" : ", está lloviendo con intensidad.",
        "504" :  ", está lloviendo muy fuertemente.",
        "511" : ", está lloviendo y helando.",
        "520" : ", está lloviendo poquito pero a cántaros.",
        "521" : ", está lloviendo a cántaros.",
        "522" : ", está lloviendo a cántaros, pero mucho.",
        "531" : ", está lloviendo... más o menos.",

        "600" : ", está nevando ligeramente.",
        "601" : ", está nevando.",
        "602" : ", está nevando fuertemente.",
        "611" : ", está lloviendo aguanieve.",
        "612" : ", está lloviendo algo de aguanieve.",
        "613" : ", está lloviendo bastante aguanieve.",
        "615" :  ", está lloviendo un poco  a la vez que nieva.",
        "616" : ", está lloviendo y nevando.",
        "620" : ", está cayendo algo de nieve.",
        "621" : ", están cayendo montones de nieve.",
        "622" :  ", se viene un alud de nieve.",

        "701" : ", está rodeada de neblina.",
        "711" : ", está rodeada de humo.",
        "721" : ", está rodeada de bruma.",
        "731" : ", está rodeada de calima.",
        "741" : ", está rodeada de niebla.",
        "751" : ", está en una tormenta de arena.",
        "761" : ", está rodeada de polvo.",
        "762" : ", tiene el cielo cubierto de cenizas del volcán",
        "771" : ", se pasará por algunos chubascos.",
        "781" : "... ¡Oh, no! Un tornado, yo que tú me refugiaba ya.",

        "800" : ", el cielo está despejado",

        "801" : ", podremos ver alguna que otra nube",
        "802" : ", podemos ver nubes por el cielo",
        "803" : ", el cielo tendrá más nubes que claros",
        "804" : ", no parece que vayas a ver el sol, todo serán nubes",
    }

    def name(self) -> Text:
        """
        Declaración de la acción
        @return string Nombre de la acción
        """
        return "action_tell_weather"

    def weather_report_sky(self,code):
        """
        Método que asocia el código con el mensaje que debería añadir
        @return weather_report Mensaje a añadir al reporte
        """
        weather_report = self.CODES[str(code)]
        print(weather_report)
        return weather_report

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Ejecución de la acción.
        Extrae de la API de OpenWeatherMap a través de Internet
        y fabrica el reporte del tiempo en la ciudad pasada como entidad.
        @utter_message Devuelve el reporte del tiempo para la ciudad.
        """

        city = next(tracker.get_latest_entity_values('city'),None)
        uri = f'https://api.openweathermap.org/data/2.5/weather?q={city}'
        app_id = f'&appid={ActionsSettings().OPENWEATHERMAP_API_KEY}'
        units = '&units=metric'
        lang = '&lang=es'
        url = f'{uri}{app_id}{units}{lang}'
        try:
            request = requests.get(url)
            if request is not None:
                req_json = request.json()
                print(req_json)
                city_name = req_json.get('name')
                max_temp = ceil(req_json['main']['temp_max'])
                min_temp = ceil(req_json['main']['temp_min'])
                current_temp = ceil(req_json['main']['temp'])
                pronostic = self.weather_report_sky(req_json['weather'][0]['id'])

                sky = f'En {city_name} {pronostic}.'
                temp = f'Ahora mismo se está a {current_temp} grados,\
                     con máximas de {max_temp} y mínimas de {min_temp}.'

                dispatcher.utter_message(text=f'{sky} {temp}')

        except requests.exceptions.ConnectionError as error:
            dispatcher.utter_message(text=f'Ahora mismo no te puedo decir mucho del tiempo\
                 que hace en {city}. Consulta a tu meteorólogo.')
            print(error)

        return []

class ActionSearchOnWikipedia(Action):
    """"""

    def name(self) -> Text:
        return "action_search_on_wikipedia"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        wikipedia.set_lang("es")

        response = ''

        search_term = next(tracker.get_latest_entity_values('wiki_search_term'),None)

        if search_term:
            try:
                wikipedia_response = wikipedia.summary(search_term)
                response = f"Según Wikipedia, {wikipedia_response}"
                response = re.sub('\[(.*?)\]','',response)
                response = response.replace('\n','')
            except wikipedia.exceptions.DisambiguationError as error:
                options = error.options
                response = f"Hay mucha info parecida en Wikipedia, quizás puedes preguntarme de esta forma:\
                            {','.join(options)}"
            except wikipedia.exceptions.PageError as e:
                response = f"No encuentro nada de eso en Wikipedia, ni nada parecido."
            except requests.exceptions.ConnectionError:
                response = ActionsSettings.NO_CONNECTION_TO_INTERNET

        dispatcher.utter_message(text=response)

        return []

