from datetime import datetime, timedelta
from pathlib import Path
from commonfunctions import *
from technicalanalysis import *

# To get futures and options data
# https://www1.nseindia.com/products/content/derivatives/equities/historical_fo.htm
# https://stockcharts.com/h-sc/ui?s=RELIANCE.IN

keepAlive = True
listed_companies = get_nse_listed_companies()
coff_day = 7
day_or_hour = 'D'

while keepAlive:

    clear_screen()
    prompt_msg = "Enter the Symbol of the Company (Ex: POWERGRID) or "
    prompt_msg += "Q to quit: "

    company_name = input(prompt_msg).upper().strip()

    if company_name == 'Q':
        keepAlive = False
        break
    elif company_name in listed_companies:

        stock_dates = get_start_end_date()

        csv_file_name = 'data/yfinance/csv/{}-day.csv'.format(company_name)
        company_full_name = listed_companies[company_name][1]

        if Path(csv_file_name).is_file():
            start_date = stock_dates['start_date'][0]
            end_date = stock_dates['end_date'][0]

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            clear_screen()

            # Creating the dataframe
            csv_data = pd.read_csv(csv_file_name)
       
            csv_data['DATE'] = csv_data['Date']

            csv_data['OPEN'] = csv_data['Open'].apply(
                lambda x: round(float(x), 2))

            csv_data['HIGH'] = csv_data['High'].apply(
                lambda x: round(float(x), 2))

            csv_data['LOW'] = csv_data['Low'].apply(
                lambda x: round(float(x), 2))

            csv_data['CLOSE'] = csv_data['Close'].apply(
                lambda x: round(float(x), 2))

            csv_data['VOLUME'] = csv_data['Volume']

            sw = start_date.strftime('%Y-%m-%d')
            ew = end_date.strftime('%Y-%m-%d')

            mask = (csv_data['DATE'] >= sw) & (
                csv_data['DATE'] <= ew)

            csv_data = csv_data.loc[mask]
            
            range_high = csv_data['HIGH'].max()
            range_low = csv_data['LOW'].min()

            low_gain = 0
            low_gain_total = 0

            high_gain = 0
            high_gain_total = 0

            while start_date < end_date:
                clear_screen()

                start_of_week = start_date - \
                    timedelta(days=start_date.weekday())
                end_of_week = start_of_week + timedelta(days=4)

                start_date = end_of_week + timedelta(days=3)

                sw = start_of_week.strftime('%A %d %b, %Y')
                ew = end_of_week.strftime('%A %d %b, %Y')

                print('Company: {},  {} - {}'.format(company_name, sw, ew))

                sw = start_of_week.strftime('%Y-%m-%d')
                ew = end_of_week.strftime('%Y-%m-%d')

                csv_data.set_index('DATE')

                mask = (csv_data['DATE'] >= sw) & (
                    csv_data['DATE'] <= ew)

                data = csv_data.loc[mask]

                for index, row in data.iterrows():
                    curr_date = datetime.strptime(row.loc['DATE'], '%Y-%m-%d')
                    curr_date = curr_date.strftime('%A %d %b, %Y')

                    msg = "OPEN: {}, CLOSE: {}, HIGH: {}, LOW: {}, VOLUME: {}".format(
                        row.loc['OPEN'], row.loc['CLOSE'], row.loc['HIGH'],
                        row.loc['LOW'], row.loc['VOLUME']
                    )

                    # calculated based on open and close
                    close_price_diff = round(
                        row.loc['CLOSE'] - row.loc['OPEN'], 2)
                    close_change_percentage = round((close_price_diff /
                                                     row.loc['OPEN']) * 100, 2)

                    msg_2 = "(OPEN - CLOSE) Price Diff: {}, Change: {}%".format(
                        close_price_diff, close_change_percentage)

                    # calculated based on open and high
                    high_price_diff = round(
                        row.loc['HIGH'] - row.loc['OPEN'], 2)
                    high_change_percentage = round((high_price_diff /
                                                    row.loc['OPEN']) * 100, 2)

                    msg_2 += "\n(OPEN - HIGH) Price Diff: {}, Change: {}%".format(
                        high_price_diff, high_change_percentage)

                    # calculated based on open and high
                    low_price_diff = round(row.loc['LOW'] - row.loc['OPEN'], 2)
                    low_change_percentage = round((low_price_diff /
                                                   row.loc['OPEN']) * 100, 2)

                    msg_2 += "\n(OPEN - LOW) Price Diff: {}, Change: {}%".format(
                        low_price_diff, low_change_percentage)

                    if (high_change_percentage >= 0.0 and
                            high_change_percentage <= 0.50):

                        if close_change_percentage <= 0.0:
                            high_gain += 1

                        high_gain_total += 1

                    if (low_change_percentage >= -0.50 and
                            low_change_percentage <= 0.0):
                        if close_change_percentage >= 0.0:
                            low_gain += 1

                        low_gain_total += 1

                    print("\n")
                    print(curr_date)
                    print(msg)
                    print(msg_2)

                success_rate = 0
                if high_gain > 0 and high_gain_total > 0:
                    success_rate = round(
                        (high_gain / high_gain_total) * 100, 2)

                print("\n\nINTRADAY")
                print("[SELL] [OPEN - HIGH STRATEGY] TOTAL: {}, HIGH GAIN (0% - 0.50%): {}, Success Rate: {}".format(
                    high_gain_total, high_gain, success_rate
                ))

                success_rate = 0
                if low_gain > 0 and low_gain_total > 0:
                    success_rate = round((low_gain / low_gain_total) * 100, 2)

                print("[BUY] [OPEN - LOW STRATEGY] TOTAL: {}, LOW GAIN (0% - 0.50%): {}, Success Rate: {}".format(
                    low_gain_total, low_gain, success_rate
                ))

                input("Press any key to continue...")
            
            range_diff = range_high - range_low
            Level_0 = range_high
            Level_1 = round(range_high - (range_diff * 0.236), 2)
            Level_2 = round(range_high - (range_diff * 0.382), 2)
            Level_3 = round(range_high - (range_diff * 0.50), 2)            
            Level_4 = round(range_high - (range_diff * 0.618), 2)
            Level_5 = round(range_high - (range_diff * 0.786), 2)
            Highest_Level = range_low

            print("Range High: {}, Range Low: {}".format(range_high, range_low))
            print("Level 1 (0.236): {}".format(Level_1))
            print("Level 2 (0.382): {}".format(Level_2))
            print("Level 3 (0.50): {}".format(Level_3))
            print("Level 4 (0.618): {}".format(Level_4))
            print("Level 5 (0.786): {}".format(Level_5))
            input("Press any key to continue...")

        else:
            print("Company data not found")
    else:
        print("Company Not found.")

    input("Press any key to continue....")
