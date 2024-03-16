from datetime import datetime
from import_data import fetch_data, fetch_fixtures, fetch_statistics
import pandas as pd
import os

DATA_TYPE = os.getenv('DATA_TYPE', 'fixtures')
LEAGUE_ID = os.getenv('LEAGUE_ID', '39')
SEASON = os.getenv('SEASON', '2024')
# TEAM_ID = os.getenv('TEAM_ID', '33')

if __name__ == '__main__':
    print(f'[INFO] -- {datetime.now()} -- starting program')
    data = fetch_fixtures(LEAGUE_ID, SEASON)
    # print('[INFO] -- {datetime.now()} -- data', data)
    fixture_containers = data['response']
    dict_fixtures: dict = {
        'technical_id': [],
        'id_fixture': [],
        'id_team_1': [],
        'id_team_2': [],
        'wins_team_1': [],
        'draws_team_1': [],
        'loses_team_1': [],
        'wins_team_2': [],
        'draws_team_2': [],
        'loses_team_2': []
    }
    df = pd.DataFrame()
    i = 0
    for fixture_container in fixture_containers:
        # print('fixture', fixture)
        dict_fixtures['technical_id'].append(i)
        dict_fixtures['id_fixture'].append(fixture_container['fixture']['id'])
        id_team_1 = fixture_container['teams']['home']['id']
        dict_fixtures['id_team_1'].append(id_team_1)
        id_team_2 = fixture_container['teams']['away']['id']
        dict_fixtures['id_team_2'].append(id_team_2)
        dict_fixtures['wins_team_1'].append(fixture_container['teams']['home']['id'])
        data = fetch_statistics(id_team_1, LEAGUE_ID, SEASON)
        data_team_1 = fetch_statistics()
        i += 1
    print('nb fixtures', i)
    print(f'[INFO] -- {datetime.now()} -- ending program')
