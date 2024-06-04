import requests

class OpenF1:

    def __init__(self) -> None:
        self.base_url = 'https://api.openf1.org/v1'

    def function_args_to_url_args(self, fn_args : dict):
        args_str = ''
        for arg in fn_args.keys():
            if arg != 'self' and fn_args[arg]:
                args_str += f'{arg}={fn_args[arg]}&'
        
        return args_str
    
    def mount_request(self, endpoint_name : str, fn_args : dict):
        uri = f'{self.base_url}/{endpoint_name}?{self.function_args_to_url_args(fn_args)}'

        response = requests.get(uri)

        return response.json()


    def car_data(
            self,
            brake : int = None,
            date: str = None,
            driver_number: int = None,
            drs: int = None,
            meeting_key: str = 'latest',
            n_gear: int = None,
            session_key: str = 'latest',
            speed: int = None,
            throttle: int = None
    ) -> list:
        return self.mount_request('car_data',locals())
    
    def drivers(
            self,
            broadcast_name : str = None,
            country_code : str = None,
            driver_number : int = None,
            first_name : int = None,
            full_name : int = None,
            last_name : int = None,
            meeting_key: str = 'latest',
            name_acronym : str = None,
            session_key: str = 'latest',
            team_name : str = None
    ) -> list:
        return self.mount_request('drivers',locals())
    
    def intervals(
            self,
            driver_number : int = None,
            meeting_key: str = 'latest',
            session_key: str = 'latest'
        ) -> list:
        return self.mount_request('intervals',locals())

    def laps(
            self,
            driver_number : int = None,
            meeting_key: str = 'latest',
            session_key: str = 'latest',
            lap_number : int = None
        ) -> list:
        return self.mount_request('laps',locals())

    def location(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest'
    ) -> list:
        return self.mount_request('location',locals())

    def meetings(
            self,
            circuit_short_name: str = None,
            country_code: str = None,
            country_name: str = None,
            meeting_name: str = None,
            meeting_key: str = 'latest',
            year: int = None
        ) -> list:
        return self.mount_request('meetings',locals())

    def pit(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest',
        lap_number : int = None
    ) -> list:
        return self.mount_request('pit',locals())

    def position(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest',
        position : int = None
    ) -> list:
        return self.mount_request('position',locals())

    def race_control(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest',
        category : str = None,
        flag : str = None,
        scope : str = None,
        sector : int = None
    ) -> list:
        return self.mount_request('race_control',locals())

    def sessions(
            self,
            circuit_short_name: str = None,
            country_code: str = None,
            country_name: str = None,
            meeting_name: str = None,
            meeting_key: str = 'latest',
            session_key: str = 'latest',
            year: int = None,
            session_name: int = None,
            session_type: int = None
        ) -> list: 
        return self.mount_request('sessions',locals())

    def stints(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest',
        stint_number : int = None,
        lap_start : int = None,
        lap_end : int = None,
        compound : str = None
    ) -> list:
        return self.mount_request('stints',locals())

    def team_radio(
        self,
        driver_number : int = None,
        meeting_key: str = 'latest',
        session_key: str = 'latest'
    ) -> list:
        return self.mount_request('team_radio',locals())

    def weather(
        self,
        meeting_key: str = 'latest',
        session_key: str = 'latest',
    ) -> list:
        return self.mount_request('weather',locals())