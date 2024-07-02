from .football_data_wrapper import FootballDataWrapper
from datetime import datetime, timedelta

STAGE_DICT = {
    'GROUP_STAGE' : 'Grupo',
    'LAST_16' : 'Octavos',
    'QUARTER_FINALS': 'Cuartos',
    'SEMI_FINALS': 'Semifinales',
    'FINAL': 'Final'
}

POSITIONS = {
    'Goalkeeper' : 'POR',
    'Centre-Back': 'DFC',
    'Defence': 'DFC',
    'Left-Back' : 'LI',
    'Right-Back': 'LD',
    'Central Midfield': 'MC',
    'Defensive Midfield': 'MCD',
    'Attacking Midfield': 'MCO',
    'Right Midfield' : 'MD',
    'Left Midfield' : 'MI',
    'Right Winger': 'ED',
    'Left Winger': 'EI',
    'Centre-Forward': 'DC',
    'Offence' : 'SD'
}

TEAMS_MAP = {
    'Germany': 'Alemania',
    'Scotland': 'Escocia',
    'Hungary': 'Hungría',
    'Switzerland': 'Suiza',
    'Spain' : 'España',
    'Croatia': 'Croacia',
    'Italy': 'Italia',
    'Albania': 'Albania',
    'Slovenia': 'Eslovenia',
    'Denmark': 'Dinamarca',
    'Serbia': 'Serbia',
    'England': 'Inglaterra',
    'Poland': 'Polonia',
    'Netherlands': 'Países Bajos',
    'Austria': 'Austria',
    'France': 'Francia',
    'Belgium': 'Bélgica',
    'Slovakia': 'Eslovaquia',
    'Romania': 'Rumanía',
    'Ukraine': 'Ucrania',
    'Türkiye': 'Turquía / Türkiye',
    'Georgia': 'Georgia',
    'Portugal': 'Portugal',
    'Czechia': 'República Checa / Chequia'
}

def get_current_matches(competition_code):
    footdata = FootballDataWrapper()

    matches = footdata.competition_matches(competition_code)
    all_matches = []

    for match_entry in matches.get('matches'):
        stage = match_entry.get('stage')
        group = match_entry.get('group').replace('GROUP_','') if match_entry.get('group') else ''
        team1 = match_entry.get('homeTeam').get('tla')
        team2 = match_entry.get('awayTeam').get('tla')
        goals_team1 = match_entry.get('score').get('fullTime').get('home') if match_entry.get('score').get('fullTime').get('home') else ''
        goals_team2 = match_entry.get('score').get('fullTime').get('away') if match_entry.get('score').get('fullTime').get('away') else ''

        if goals_team1 != '' and goals_team2 == '':
            goals_team2 = 0
        
        if goals_team1 == '' and goals_team2 != '':
            goals_team1 = 0

        timestamp = datetime.strptime(match_entry.get('utcDate'),'%Y-%m-%dT%H:%M:%SZ')

        if datetime.now() > (timestamp + timedelta(hours=2, minutes=30)) and goals_team1 == '' and goals_team2 == '':
            goals_team1 = 0
            goals_team2 = 0

        if team1 and team2:
            str_a = f'{STAGE_DICT[stage]} {group}. {team1} {goals_team1} - {team2} {goals_team2}'

            all_matches.append(str_a)

    return all_matches

def get_matches_string(competition_code):
    matches = get_current_matches(competition_code)

    str_matches = ''

    for match in matches:
        str_matches += f'{match}\n'

    return str_matches

def get_team_info(team):
    footdata = FootballDataWrapper()

    team_info = footdata.team_data(team)
    team_matches = footdata.team_matches(team)

    team_dict = {
        'name': '',
        'short_name': '',
        'coach': '',
        'players': {
            'POR': [],
            'LD': [],
            'CAD': [],
            'DFC': [],
            'LI': [],
            'CAI': [],
            'MCD': [],
            'MC': [],
            'MCO': [],
            'MD': [],
            'ED': [],
            'MI': [],
            'EI': [],
            'SDD': [],
            'SD': [],
            'SDI': [],
            'DC': []
        },
        'matches': []
    }

    team_dict['name'] = TEAMS_MAP.get(team_info.get('name'))
    team_dict['short_name'] = team_info.get('tla')
    team_dict['coach'] = team_info.get('coach').get('name')

    for player in team_info.get('squad'):
        team_dict.get('players').get(POSITIONS.get(player.get('position'))).append(player.get('name'))

    for match_entry in team_matches.get('matches'):
        stage = match_entry.get('stage')
        group = match_entry.get('group').replace('GROUP_','') if match_entry.get('group') else ''
        team1 = match_entry.get('homeTeam').get('tla')
        team2 = match_entry.get('awayTeam').get('tla')
        goals_team1 = match_entry.get('score').get('fullTime').get('home') if match_entry.get('score').get('fullTime').get('home') else ''
        goals_team2 = match_entry.get('score').get('fullTime').get('away') if match_entry.get('score').get('fullTime').get('away') else ''

        if goals_team1 != '' and goals_team2 == '':
            goals_team2 = 0

        if goals_team1 == '' and goals_team2 != '':
            goals_team1 = 0

        timestamp = datetime.strptime(match_entry.get('utcDate'),'%Y-%m-%dT%H:%M:%SZ')

        if datetime.now() > (timestamp + timedelta(hours=2, minutes=30)) and goals_team1 == '' and goals_team2 == '':
            goals_team1 = 0
            goals_team2 = 0

        if team1 and team2:
            str_a = f'{STAGE_DICT[stage]} {group}. {team1} {goals_team1} - {team2} {goals_team2}'

            team_dict['matches'].append(str_a)


    return team_dict

def get_team_info_str(team):

    info_dict = get_team_info(team)

    print(info_dict)

    matches = ''
    players = ''

    for player_position in info_dict.get('players').keys():
        if len(info_dict.get('players').get(player_position)) > 0:
            for player in info_dict.get('players').get(player_position):
                players += f"{player_position} . {player} \n"

    for match in info_dict.get('matches'):
        matches = matches + match + '\n'

    info_str = f"Aquí tienes toda la info de {info_dict.get('name')} ({info_dict.get('short_name')}): \n \
        Entrenador : {info_dict.get('coach')} \n \
        Equipo: \n \
        {players} \n \
        Partidos : \n \
        {matches} \
    "

    info_str.replace('\t','')

    return info_str

