import os

import requests
import json
import datetime


base = 'https://www.worldtradingdata.com/api/v1/history'
data_directory = os.path.join(os.getcwd(), 'sources', 'world_trading_data', 'data')


class WorldTradingData(object):

    def __init__(self, use_latest=False):
        # if true, then redownload the data if a new day
        self.use_latest = use_latest

    def update_data(self):

        if not os.path.exists(data_directory):
            os.mkdir(data_directory)

        with open('stock_tickers.json', 'r') as infile:
            tickers = json.load(infile)

        with open('api_keys.json', 'r') as infile:
            key = json.load(infile)['world-trading-data']

        for ticker in tickers:

            date_extension = f"_{datetime.datetime.today().strftime('%Y-%m-%d')}" if self.use_latest else '_no-date'

            file_name = f"{ticker}{date_extension}.json"
            file_path = os.path.join(data_directory, file_name)

            if not os.path.exists(file_path):

                r = requests.get(f'{base}?symbol={ticker}&sort=newest&api_token={key}')
                if r.status_code != 200:
                    raise ValueError('Request failed!')

                with open(file_path, 'w') as cache_file:
                    cache_file.write(r.text)

    def get_data(self):
        data = {}
        for filename in os.listdir(data_directory):
            ticker, end_date = filename.replace('.json', '').split('_')

            with open(os.path.join(data_directory, filename), 'r') as ticker_file:
                parsed_file = json.load(ticker_file)

            for date in parsed_file['history']:
                data.setdefault(date, {})[ticker] = parsed_file['history'][date]

        return data
