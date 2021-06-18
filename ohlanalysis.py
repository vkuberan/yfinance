import json
from datetime import datetime, timedelta
import pandas as pd
from commonfunctions import *


def ohl_analysis(start_date, end_date, stock_name):
    sw = start_date.strftime('%Y-%m-%d')
    ew = end_date.strftime('%Y-%m-%d')

    one_hour_file = 'data/yfinance/json/{}-1h.json'.format(stock_name)

    clear_screen()

    try:
        data = False

        with open(one_hour_file) as f:
            data = json.load(f)

        if data is not False:
            print('Range: {} - {}, Stock Name: {}'.format(
                sw, ew, stock_name))

            timestamps = data['chart']['result'][0]['timestamp']
            stock_open = data['chart']['result'][0]['indicators']['quote'][0]['open']
            stock_close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            stock_high = data['chart']['result'][0]['indicators']['quote'][0]['high']
            stock_low = data['chart']['result'][0]['indicators']['quote'][0]['low']
            stock_volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']

            # Creating the dataframe
            stock_data = pd.DataFrame(
                {
                    "TIMESTAMP": timestamps,
                    "OPEN": stock_open,
                    "HIGH": stock_high,
                    "LOW": stock_low,
                    "CLOSE": stock_close,
                    "VOLUME": stock_volume
                }
            )

            stock_data['TIMESTAMP'] = stock_data['TIMESTAMP'].apply(
                lambda x: datetime.fromtimestamp(x))

            stock_data['OPEN'] = stock_data['OPEN'].apply(
                lambda x: round(float(x), 2))

            stock_data['CLOSE'] = stock_data['CLOSE'].apply(
                lambda x: round(float(x), 2))

            stock_data['HIGH'] = stock_data['HIGH'].apply(
                lambda x: round(float(x), 2))

            stock_data['LOW'] = stock_data['LOW'].apply(
                lambda x: round(float(x), 2))

            print(stock_data)
            print(stock_data.head())
            print(stock_data.tail())

        else:
            print("Something went wrong with data")

    except Exception as e:
        print(e)
