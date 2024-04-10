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
import re
from os import environ

import wikipedia
from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionsSettings():
    """
    Clase para la configuración de variables necesarias en las acciones
    """
    load_dotenv('../../.envs/.actions.env')

    NO_CONNECTION_TO_INTERNET = 'No me puedo conectar a Internet ahora mismo, lo siento.\
         Comprueba por si acaso la conexión.'
    OPENWEATHERMAP_API_KEY = environ.get('OPENWEATHERMAP_API_KEY')
    FOOTBALL_STATS_API_KEY = environ.get('FOOTBALL_STATS_API_KEY')


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
        96 : ", está en medio de una tormenta, y además lloviendo",
        99 : ", está en medio de una tormenta lloviendo a cántaros",
        95 : ", está en medio de una tormenta",

        51 : ", está cayendo algo de llovizna",
        53 : ", está llovizneando",
        55 : ", está cayendo una fuerte llovizna",
        56 : ", está cayendo algo de llovizna y encima helando",
        57 : ", está cayendo una llovizna y encima para quedarse pínfano",

        61 : ", está lloviendo ligeramente. Llévate un paraguas.",
        63 : ", está lloviendo. Llévate un paraguas.",
        65 : ", está lloviendo fuertemente. Llévate un paraguas.",
        66 : ", está lloviendo y helando.",
        67 : ", está lloviendo y helando para quedarse polito.",

        71 : ", está nevando ligeramente.",
        73 : ", está nevando.",
        75 : ", está nevando fuertemente.",
        85 : ", está cayendo algo de nieve.",
        86 : ", están cayendo montones de nieve.",
        77 : ", está granizando. ¡Ponte a salvo!",

        45 : ", está rodeada de neblina.",
        48 : ", está rodeada de bruma.",

        0 : ", el cielo está despejado",

        1 : ", podremos ver alguna que otra nube",
        2 : ", el cielo tendrá más nubes que claros",
        3 : ", no parece que vayas a ver el sol, todo serán nubes",
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

        if code in self.CODES:
            weather_report = self.CODES[code]
            return weather_report
        else:
            return ', se deconoce cómo va.'
    
    def geocoding(self, prompt):
        if len(prompt) < 2:
            return None
        
        uri = 'https://geocoding-api.open-meteo.com/'
        path = 'v1/search/'
        get_parameters = f'?name={prompt}&count=1&language=es&format=json'

        url = f'{uri}{path}{get_parameters}'
        try:
            request = requests.get(url)
            if request is not None:
                req_json = request.json()
                print(req_json)
                return (req_json['results'][0]['latitude'],req_json['results'][0]['longitude'])
            return None
        except Exception:
            return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Ejecución de la acción.
        Extrae de la API de OpenMeteo a través de Internet
        y fabrica el reporte del tiempo en la ciudad pasada como entidad.
        @utter_message Devuelve el reporte del tiempo para la ciudad.
        """

        city = next(tracker.get_latest_entity_values('city'),None)
        coordinates = self.geocoding(city)
        if coordinates is not None:
            url = f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min'
            try:
                request = requests.get(url)
                if request is not None:
                    req_json = request.json()
                    print(req_json)
                    city_name = city
                    current_temp = ceil(req_json['current']['temperature_2m'])
                    max_temp = ceil(req_json['daily']['temperature_2m_max'][0])
                    min_temp = ceil(req_json['daily']['temperature_2m_min'][0])
                    pronostic = self.weather_report_sky(req_json['current']['weather_code'])

                    sky = f'En {city_name} {pronostic}.'
                    temp = f'Ahora mismo se está a {current_temp} grados,\
                        con máximas de {max_temp} y mínimas de {min_temp}.'

                    dispatcher.utter_message(text=f'{sky} {temp}')

            except requests.exceptions.ConnectionError as error:
                dispatcher.utter_message(text=f'Ahora mismo no te puedo decir mucho del tiempo\
                    que hace en {city}. Consulta a tu meteorólogo.')
                print(error)

        else:
            dispatcher.utter_message(text=f'Ahora mismo no te puedo decir mucho del tiempo\
                que hace en {city} porque no encuentro las coordenadas. Consulta a tu meteorólogo.')

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
        url = ''

        search_term = next(tracker.get_latest_entity_values('wiki_search_term'),None)

        if search_term:
            try:
                wikipedia_response = wikipedia.page(search_term)
                response = f"Según Wikipedia, {wikipedia_response.summary}"
                response = re.sub('\[(.*?)\]','',response)
                response = response.replace('\n','')
                # Por razones de limitación con Telegram, sólo se pueden poner 4096 caracteres.
                response = response[:4096]
                # Pero está feo cortarlo, así que vamos a dejarlo en el último punto antes del corte.
                response = response.rsplit('.',1)[0]
                url = wikipedia_response.url
            except wikipedia.exceptions.DisambiguationError as error:
                options = error.options
                response = f"Hay mucha info parecida en Wikipedia, quizás puedes preguntarme de esta forma:\
                            {','.join(options)}"
            except wikipedia.exceptions.PageError as e:
                response = f"No encuentro nada de eso en Wikipedia, ni nada parecido."
            except requests.exceptions.ConnectionError:
                response = ActionsSettings.NO_CONNECTION_TO_INTERNET
        print(f'Wikipedia -> {url} {response}')

        dispatcher.utter_message(custom={'text':response,'source':url})

        return []

