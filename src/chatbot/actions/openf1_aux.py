from datetime import datetime
from time import sleep

from .openf1_wrapper import OpenF1

SESSION_TYPES = {
    'Practice' : 'las prácticas',
    'Qualifying' : 'la clasificación',
    'Race' : 'la carrera',
    'Sprint Qualifying': 'la clasificación para el Sprint',
    'Sprint': 'la carrera al Sprint'
}

def is_live_event():
    openf1 = OpenF1()

    latest_event = openf1.sessions()[-1]
    event_start_datetime = datetime.fromisoformat(latest_event.get('date_start'))
    event_end_datetime = datetime.fromisoformat(latest_event.get('date_end'))

    if datetime.now().astimezone() >= event_end_datetime:
        return False
    elif datetime.now().astimezone() >= event_start_datetime and datetime.now() >= event_end_datetime:
        return True
    
def get_session_data():
    openf1 = OpenF1()

    latest_event = openf1.sessions()[-1]
    latest_meeting = openf1.meetings()[-1]
    live_text = 'en vivo ' if is_live_event() else ''
    event_text = f"Esta es la información {live_text}de {SESSION_TYPES.get(latest_event.get('session_type'))} en el {latest_meeting.get('meeting_official_name')}."

    return event_text

def get_top_drivers(drivers: int = 10):
    openf1 = OpenF1()
    top_drivers_str = f'Este es el Top {drivers}:\n '

    for iterator in range(1,drivers+1):
        if len(openf1.position(position=iterator)):
            latest_update_in_position =  openf1.position(position=iterator)[-1]
            latest_driver_in_position = openf1.drivers(driver_number=latest_update_in_position.get('driver_number'))[-1]
            top_drivers_str += f"{iterator}. {latest_driver_in_position.get('full_name')} \n"
        sleep(0.5)

    return top_drivers_str

def get_race_control_info():
    openf1 = OpenF1()

    race_control = {
        'Flag': {
            'GREEN': [],
            'RED': [],
            'YELLOW': [],
            'DOUBLE YELLOW': [],
            'CLEAR': [],
            'BLUE': [],
            'CHEQUERED': []
        },
        'FIA Notifs': []
    }

    for notif in openf1.race_control():
        if notif.get('category') == 'Flag':
            if notif.get('flag') in race_control.get('Flag').keys():
                race_control.get('Flag').get(notif.get('flag')).append(f"{datetime.fromisoformat(notif.get('date')).strftime('%H:%M:%S')} - {notif.get('message')}")
        elif notif.get('category') == 'Other':
            race_control.get('FIA Notifs').append(notif.get('message'))

    return race_control

def get_race_control_count():
    race_control_count = {
        'Flag': {
            'GREEN': 0,
            'RED': 0,
            'YELLOW': 0,
            'DOUBLE YELLOW': 0,
            'CLEAR': 0,
            'BLUE': 0,
            'CHEQUERED': 0
        },
        'FIA Notifs': 0
    }

    race_control_dict = get_race_control_info()

    for flag_type in race_control_dict.get('Flag').keys():
        race_control_count.get('Flag')[flag_type] = len(race_control_dict.get('Flag').get(flag_type))

    race_control_count['FIA Notifs'] = len(race_control_dict.get('FIA Notifs'))

    return race_control_count

def get_race_control_string():
    race_control = get_race_control_count()
    live_str = 'hasta ahora ' if is_live_event() else ''

    return f"Los comisarios han emitido {live_str} {race_control.get('FIA Notifs')} notificaciones y se han levantado las siguientes banderas: {race_control.get('Flag').get('YELLOW')} de amarillo, {race_control.get('Flag').get('DOUBLE YELLOW')} de doble amarillo y {race_control.get('Flag').get('RED')} de rojo."

def get_weather_info():
    openf1 = OpenF1()

    weather = openf1.weather()[-1]

    live_str = 'El último parte meteorológico dice' if not is_live_event() else 'En este momento se reporta'
    is_raining = 'Está lloviendo.' if weather.get('rainfall') == 1 else ''

    return f"{live_str} que el aire está a {weather.get('air_temperature')} grados y la pista a {weather.get('track_temperature')}, con una humedad del {weather.get('humidity')} % y el viento está a {weather.get('wind_speed')} kilómetros por hora con dirección {weather.get('wind_direction')} grados. {is_raining}"


def get_all_event_data():
    try:
        return f'{get_session_data()} \n {get_top_drivers()} \n {get_race_control_string()} \n {get_weather_info()}'
    except Exception as e:
        return 'Ahora mismo no puedo obtener información de la última carrera. '
    