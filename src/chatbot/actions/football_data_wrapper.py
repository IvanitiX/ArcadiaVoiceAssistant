import requests
from .action_settings import FOOTBALL_DATA_API_KEY

class FootballDataWrapper:

    def __init__(self) -> None:
        self.base_url = 'https://api.football-data.org/v4'
        self.headers = {'X-Auth-Token': FOOTBALL_DATA_API_KEY}

    def mount_request(self, endpoint_name : str, fn_args : dict = None):
        uri = f'{self.base_url}/{endpoint_name}'

        response = requests.get(uri, headers=self.headers)

        return response.json()
    

    def competition_standings(self, competition_code : str):
        return self.mount_request(f'competitions/{competition_code}/standings')
    
    def competition_matches(self, competition_code : str):
        return self.mount_request(f'competitions/{competition_code}/matches')
    
    def competition_teams(self, competition_code : str):
        return self.mount_request(f'competitions/{competition_code}/teams')
    
    def competition_scorer(self, competition_code : str):
        return self.mount_request(f'competitions/{competition_code}/scorers')
    
    def team_data(self, team_code : str):
        return self.mount_request(f'teams/{team_code}/')
    
    def team_matches(self, team_code : str):
        return self.mount_request(f'teams/{team_code}/matches/')
