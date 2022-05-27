# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import datetime
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from requests import request
import requests

class ActionsSettings():
    NO_CONNECTION_TO_INTERNET = 'No me puedo conectar a Internet ahora mismo, lo siento. Comprueba por si acaso la conexión.'
    OPENWEATHERMAP_API_KEY = '831587653e5df6adadd7d236ea88f6d6'


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=u"Son las {0}".format(datetime.datetime.now().strftime('%H horas y %M minutos')))

        return []

class ActionThrowDice(Action):

    def name(self) -> Text:
        return "action_throw_dice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        value = random.Random().randint(1,6)

        dispatcher.utter_message(text=u"Acabo de tirar un dado y ha salido el {0}".format(value))

        return []


class ActionLightPrice(Action):
    def name(self) -> Text:
        return "action_light_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            request = requests.get('https://api.preciodelaluz.org/v1/prices/now?zone=PCB')
            if request is not None:
                price_now = u'{0} euros el megavatio hora'.format(request.json()['price'])
            request = requests.get('https://api.preciodelaluz.org/v1/prices/avg?zone=PCB')
            if request is not None:
                avg_price = u'{0} euros el megavatio hora'.format(request.json()['price'])
            request = requests.get('https://api.preciodelaluz.org/v1/prices/max?zone=PCB')
            if request is not None:
                range_hours = str(request.json()['hour']).replace('-', ' a ')
                max_price = u'a {0} euros el megavatio hora de {1}'.format(request.json()['price'], range_hours)
            request = requests.get('https://api.preciodelaluz.org/v1/prices/min?zone=PCB')
            if request is not None:
                range_hours = str(request.json()['hour']).replace('-', ' a ')
                min_price = u'a {0} euros el megavatio hora de {1}'.format(request.json()['price'], range_hours)

            dispatcher.utter_message(text=u"En España, a esta hora, el precio es de {0}. De media, hoy pagaremos \
            {1}, siendo la hora más barata {2}; y la más cara {3}".format(price_now,avg_price,min_price,max_price))
        except requests.exceptions.ConnectionError as e:
            dispatcher.utter_message(ActionsSettings.NO_CONNECTION_TO_INTERNET)

        return []

class ActionTellWeather(Action):

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
        return "action_tell_weather"

    def weather_report_sky(self,code):
        weather_report = self.CODES[str(code)]
        print(weather_report)
        return weather_report

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = next(tracker.get_latest_entity_values('city'),None)
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={ActionsSettings().OPENWEATHERMAP_API_KEY}&units=metric&lang=es'
        print(url)
        try:
            request = requests.get(url)
            if request is not None:
                req_json = request.json()
                city_name = req_json.get('name')
                
                max_temp = req_json['main']['temp_max']
                min_temp = req_json['main']['temp_min']
                current_temp = req_json['main']['temp']

                print(req_json['weather'][0]['id'])
                pronostic = self.weather_report_sky(req_json['weather'][0]['id'])
                print(pronostic)

                sky = u'En {0} {1}.'.format(city_name, pronostic)
                print(sky)
                temp = f'Ahora mismo se está a {current_temp} grados, com máximas de {max_temp} y mínimas de {min_temp}.'

                dispatcher.utter_message(text=f'{sky} {temp}')

        except requests.exceptions.ConnectionError as e:
            dispatcher.utter_message(text=f'Ahora mismo no te puedo decir mucho del tiempo que hace en {city}. Consulta a tu meteorólogo.')
            print(e)

        return []

