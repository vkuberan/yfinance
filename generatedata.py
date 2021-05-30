# run this file often to get the fresh day. Run atleast once
# during trading days.
import glob
import time
from datetime import datetime
import pandas as pd

from commonfunctions import *
from networkfunctions import *
from nsefunctions import *

clear_screen()


if is_time_between((9, 15), (11, 29)):
    print("Sorry You cann't run this script between 9:30 AM to 11:59PM")
    exit()


# Step 1: GET NSE 50, etc., data from https://www.nseindia.com/
print("STEP 1: Fetching feed DATA from NSE.")
fetch_nse_data_from_endpoints()

# Step 2: Clean the CSV header of the CSV and move to cleaned
# file to current-analysis folder
print("\nSTEP 2: Cleanup the feed DATA got from NSE.")
clean_nse_data_fetched_from_nse_api()


print("\nSTEP 3: Going to fetch Data from Yahoo Financial Server.")

files = glob.glob("data/current-analysis/*.csv")

for file in files:
    data = pd.read_csv(file)
    data.set_index('SYMBOL')

    for index, row in data.iterrows():
        now = custom_strftime('{S} %B, %Y %H:%M:%S', datetime.now())
        symbol = row['SYMBOL'].strip()
        time_intervel = '1h'

        temp_file_name = symbol.replace(' ', '-')
        file_name_full_day = 'data/yfinance/csv/{}-day.csv'.format(
            temp_file_name)
        file_name_time_intervel = 'data/yfinance/json/{}-{}.json'.format(
            temp_file_name, time_intervel)

        # print(file_name_full_day, file_name_time_intervel)
        print("\n[{:<24}] Fetching {} data from Yahoo Finance Sever.".format(
            now, symbol))

        if ((symbol == 'NIFTY 50') or (symbol == 'NIFTY 100')
                or (symbol == 'NIFTY 200')):
            symbol = '%5ENSEI'
        else:
            symbol = symbol + '.NS'

        # print("{:>24}   {}".format('', historical_data_url))
        # print("{:>24}   {}".format('', historical_one_hour_char))

        # Fetch last 1 year one day data
        historical_data_url = generate_yfinance_url(
            symbol, round(YEAR_BEFORE_TS), round(CURRENT_DAY_TS))

        content = fetch_data_from_url(historical_data_url)

        if content is not None:
            with open(file_name_full_day, 'w') as writer:
                writer.write(content)

        historical_one_hour_char = generate_yfinance_url(
            symbol, round(YEAR_BEFORE_TS), round(CURRENT_DAY_TS), time_intervel)

        content = fetch_data_from_url(historical_one_hour_char)

        if content is not None:
            with open(file_name_time_intervel, 'w') as writer:
                writer.write(content)

        time.sleep(1)
