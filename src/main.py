from datetime import datetime
from import_data import fetch_data, fetch_fixtures, fetch_statistics
import pandas as pd
import os

DATA_TYPE = os.getenv('DATA_TYPE', 'fixtures')
LEAGUE_ID = os.getenv('LEAGUE_ID', '39')
SEASON = os.getenv('SEASON', '2024')
DATA_FOLDER = os.getenv('DATA_FOLDER')
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
        'loses_team_2': [],
        'is_team1_winner': []
    }

    technical_id = 0
    for fixture_container in fixture_containers:
        # print('fixture', fixture)
        dict_fixtures['technical_id'].append(technical_id)
        dict_fixtures['id_fixture'].append(fixture_container['fixture']['id'])
        id_team_1 = fixture_container['teams']['home']['id']
        dict_fixtures['id_team_1'].append(id_team_1)
        id_team_2 = fixture_container['teams']['away']['id']
        dict_fixtures['id_team_2'].append(id_team_2)

        data_team_1 = fetch_statistics(id_team_1, LEAGUE_ID, SEASON)
        data_team_2 = fetch_statistics(id_team_2, LEAGUE_ID, SEASON)

        dict_fixtures['wins_team_1'].append(data_team_1['response']['fixtures']['wins']['total'])
        dict_fixtures['draws_team_1'].append(data_team_1['response']['fixtures']['draws']['total'])
        dict_fixtures['loses_team_1'].append(data_team_1['response']['fixtures']['loses']['total'])

        dict_fixtures['wins_team_2'].append(data_team_2['response']['fixtures']['wins']['total'])
        dict_fixtures['draws_team_2'].append(data_team_2['response']['fixtures']['draws']['total'])
        dict_fixtures['loses_team_2'].append(data_team_2['response']['fixtures']['loses']['total'])

        winner = fixture_container['teams']['home']['winner']
        dict_fixtures['is_team1_winner'].append("0" if winner is None else "1" if winner else "2")

        technical_id += 1

    df_fixtures = pd.DataFrame(dict_fixtures)
    df_fixtures.to_csv(f'{DATA_FOLDER}/dataframe_fixtures_{LEAGUE_ID}_{SEASON}.csv', index=False)

    print('nb fixtures', len(df_fixtures))
    print(df_fixtures.head())
    print(df_fixtures[df_fixtures['id_team_1'] == 44].value_counts())
    print(df_fixtures[df_fixtures['id_team_2'] == 44].value_counts())
    print(df_fixtures['is_team1_winner'].value_counts())

    print(f'[INFO] -- {datetime.now()} -- ending program')
