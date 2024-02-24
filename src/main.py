from datetime import datetime
from import_data import fetch_data
import os

DATA_TYPE = os.getenv('DATA_TYPE', 'fixtures')

if __name__ == '__main__':
    print(f'[INFO] -- {datetime.now()} -- starting program')
    fetch_data(DATA_TYPE)
    print(f'[INFO] -- {datetime.now()} -- ending program')
