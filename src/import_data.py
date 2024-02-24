from datetime import datetime
import json
import os
import requests

# API settings
BASE_URL = os.getenv('API_FOOTBALL_URL')
HEADERS = {
	"X-RapidAPI-Key": os.getenv('API_FOOTBALL_KEY'),
	"X-RapidAPI-Host": os.getenv('API_FOOTBALL_HOST')
}
NB_MAX_DAILY_API_REQUESTS = os.getenv('NB_MAX_DAILY_API_REQUESTS')

# API parameters
LEAGUE_ID = os.getenv('LEAGUE_ID')
TEAM_ID = os.getenv('TEAM_ID')
SEASON = os.getenv('SEASON')

# Data settings
DATA_FILENAME_PREFIX = f'{os.getenv("DATA_FOLDER")}/'
DATA_FILENAME_SUFFIX = os.getenv('DATA_FILENAME_SUFFIX')

# Logs settings
LOGS_NB_DAILY_REQUESTS_FILENAME = os.getenv('LOGS_FILENAME', '/logs/nb_daily_requests.log')

endpoints = {
        'timezone': {
            'filename': 'timezones',
            'query_string': {},
            'url': 'timezone'
            },
        'teams': {
            'filename': f'team_{TEAM_ID}',
            'query_string': { 'id': TEAM_ID },
            'url': 'teams'
            },
        'statistics': {
            'filename': f'team_{TEAM_ID}_statistics_for_league_{LEAGUE_ID}_and_season_{SEASON}',
            'query_string': { 'league': LEAGUE_ID, 'season': SEASON, 'team': TEAM_ID },
            'url': 'teams/statistics'
            },
        'fixtures': {
            'filename': f'fixtures_for_league_{LEAGUE_ID}_and_season_{SEASON}',
            'query_string': { 'league': LEAGUE_ID, 'season': SEASON },
            'url': 'fixtures'
            }
        }

def fetch_data(endpoint):
    nb_requests = NB_MAX_DAILY_API_REQUESTS
    data_type = endpoints[endpoint]
    filename = f'{DATA_FILENAME_PREFIX}{data_type["filename"]}{DATA_FILENAME_SUFFIX}'
    query_string = data_type['query_string']
    url = f'{BASE_URL}{data_type["url"]}'

    print(f'[INFO] -- {datetime.now()} -- fetching data if necessary at url {url} with headers {HEADERS} and query string {query_string}')

    if not os.path.isfile(filename):
     response = requests.get(url, headers=HEADERS, params=query_string)
     json_object = response.json()
     serialized_data = json.dumps(json_object, indent=4)
     with open(filename, 'w') as outfile:
        print(f'[INFO] -- {datetime.now()} -- saving data in {filename}')
        outfile.write(serialized_data)
     with open(LOGS_NB_DAILY_REQUESTS_FILENAME, 'r') as logfile:
         content = logfile.readline()
         nb_requests = int(content)
     with open(LOGS_NB_DAILY_REQUESTS_FILENAME, 'w+') as logfile:
         print(f'[INFO] -- {datetime.now()} -- {nb_requests + 1} requests made today')
         logfile.write(str(nb_requests + 1))
         print(f'[INFO] -- {datetime.now()} -- data has been fetched and saved')
    else:
        print(f'[INFO] -- {datetime.now()} -- no data has been fetched, an existing version can be found at {filename}')

def fetch_fixtures():
    return fetch_data('fixtures')

def fetch_teams():
    return fetch_data('teams')

def fetch_timezone():
    return fetch_data('timezone')

def fetch_statistics():
    return fetch_data('statistics')
