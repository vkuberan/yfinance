import json
from datetime import datetime, timedelta
import pandas as pd
from commonfunctions import *


# https://www.nirmalbang.com/knowledge-center/open-high-low-strategy.html
# Unless the Nifty50 index is over 0.25 %, go on the buy side, and if this is below 0.25 %,
# go on the sell-side. Although it depends as some people even keep the criteria at 0.5%.
def ohl_analysis(start_date, end_date, stock_name, company_full_name=''):
    sw = start_date.strftime('%Y-%m-%d')
    ew = end_date.strftime('%Y-%m-%d')

    one_hour_file = 'data/yfinance/json/{}-1h.json'.format(stock_name)

    clear_screen()

    try:
        data = False

        with open(one_hour_file) as f:
            data = json.load(f)

        if data is not False:

            timestamps = data['chart']['result'][0]['timestamp']
            stock_open = data['chart']['result'][0]['indicators']['quote'][0]['open']
            stock_close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            stock_high = data['chart']['result'][0]['indicators']['quote'][0]['high']
            stock_low = data['chart']['result'][0]['indicators']['quote'][0]['low']
            stock_volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']

            # Creating the dataframe
            stock_data = pd.DataFrame(
                {
                    "DATETIME": timestamps,
                    "OPEN": stock_open,
                    "HIGH": stock_high,
                    "LOW": stock_low,
                    "CLOSE": stock_close,
                    "VOLUME": stock_volume
                }
            )

            stock_data['DATETIME'] = stock_data['DATETIME'].apply(
                lambda x: datetime.fromtimestamp(x))

            stock_data['OPEN'] = stock_data['OPEN'].apply(
                lambda x: round(float(x), 2))

            stock_data['CLOSE'] = stock_data['CLOSE'].apply(
                lambda x: round(float(x), 2))

            stock_data['HIGH'] = stock_data['HIGH'].apply(
                lambda x: round(float(x), 2))

            stock_data['LOW'] = stock_data['LOW'].apply(
                lambda x: round(float(x), 2))

            mask = (stock_data['DATETIME'] >= sw) & (
                stock_data['DATETIME'] <= ew)

            start_week = start_date.strftime('%A %d %b, %Y')
            end_week = end_date.strftime('%A %d %b, %Y')

            header = ''
            if company_full_name is not '':
                header = "COMPANY NAME: {}\n".format(company_full_name)

            header += "SYMBOL: {}\n".format(stock_name)
            header += "DATE: {} - {}".format(
                start_week, end_week)

            # Get 1 hour data from and to date
            one_hr_data = stock_data.loc[mask]

            iCnt = 0
            buy_data = {}
            sell_data = {}
            other_data = {}
            buyCnt = 0
            sellCnt = 0
            otherCnt = 0

            for index, row in one_hr_data.iterrows():
                timestamp = row["DATETIME"]
                timestamp = str(timestamp)
                open_price = row['OPEN']
                high_price = row['HIGH']
                low_price = row['LOW']
                close_price = row['CLOSE']

                msg = "Date: {}, Open: {}, Close: {}, High: {}, Low: {}".format(
                    timestamp, open_price, high_price,
                    low_price, close_price)

                if "09:15:00" in timestamp:
                    get_date = timestamp.split(" ")[0]

                    if open_price == high_price:
                        # print("SELL: {}".format(msg))
                        sell_data[sellCnt] = get_date
                        sellCnt += 1
                    elif open_price == low_price:
                        # print("BUY: {}".format(msg))
                        buy_data[buyCnt] = get_date
                        buyCnt += 1
                    else:
                        other_data[otherCnt] = get_date
                        otherCnt += 1

            clear_screen()
            buy_success_msg, buy_failed_msg, gain_msg = analyze_buy_call(
                buy_data, stock_data)

            print(header, "\n")
            print(gain_msg)
            print(buy_success_msg)
            print(buy_failed_msg)
            input("Press any key to continue...")

            clear_screen()
            sell_success_msg, sell_failed_msg, sell_gain_msg = analyze_sell_call(
                sell_data, stock_data)

            print(header, "\n")
            print(sell_gain_msg)
            print(sell_success_msg)
            print(sell_failed_msg)
            input("Press any key to continue...")

            clear_screen()
            print(header, "\n")
            print("BUY")
            print(gain_msg)

            print("\nSELL")
            print(sell_gain_msg)

        else:
            print("Something went wrong with data")

    except Exception as e:
        print('Error Occurred: ', e)


def analyze_buy_call(buy_data, stock_data):
    total_buy = 0
    total_buy_success = 0
    buy_success_msg = ''
    buy_failed_msg = ''
    buy_success_index = 1
    buy_failed_index = 1
    gained_above_1_perc = 0
    gained_above_in_first_1_hour_perc = 0

    for key, buy in buy_data.items():
        start_date = '{} 09:15:00'.format(buy)
        end_date = '{} 15:15:00'.format(buy)

        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        mask = (stock_data['DATETIME'] >= start_date) & (
            stock_data['DATETIME'] <= end_date)
        day_data = stock_data.loc[mask]

        last_index = len(day_data) - 1

        open_price = day_data['OPEN'].iloc[0]
        open_low_price = day_data['LOW'].iloc[0]
        open_high_price = day_data['HIGH'].iloc[0]
        close_price = day_data['CLOSE'].iloc[last_index]
        day_high_price = day_data['HIGH'].max()
        day_low_price = day_data['LOW'].min()

        days_low = stock_data.loc[stock_data['LOW']
                                  > open_price]
        temp_days_low_time = str(
            days_low['DATETIME'].iloc[0]).split(" ")[1]

        human_readable_days_low = "DAY's LOW: [{:<10} TIME: {:8}]".format(
            day_low_price, temp_days_low_time
        )

        open_low_perc_diff = round(
            ((open_price - day_low_price) / open_price) * 100, 2)

        open_close_perc_diff = round(
            ((close_price - open_price) / open_price) * 100, 2)

        open_high_first_one_hour_gain = round(
            ((open_high_price - open_price) / open_price) * 100, 2)

        if open_close_perc_diff >= 1.0:
            gained_above_1_perc += 1

        if open_high_first_one_hour_gain >= 1.0:
            gained_above_in_first_1_hour_perc += 1

        human_readble_date = datetime.strptime(
            buy, '%Y-%m-%d')
        human_readble_date = human_readble_date.strftime(
            '%a %d %b, %Y')

        if close_price > open_price:
            total_buy_success += 1

            tmp_msg = "SUCCESS {:>2}: DATE: {}\n\n".format(
                buy_success_index, human_readble_date,
            )
            tmp_msg += "{:<11} OPEN: {:<10} LOW: {:<10} {:<18} ".format(
                ' ', open_price, open_low_price,
                human_readable_days_low
            )
            tmp_msg += "CLOSE: {:<10} HIGH: {:<10}\n\n".format(
                close_price, day_high_price
            )
            tmp_msg += "{:<11} OPEN-LOW Diff (%): {:<10} GAIN (%): {:<10}\n\n".format(
                ' ', open_low_perc_diff, open_close_perc_diff
            )

            msg = 'GAIN MADE IN FIRST HOUR HIGH-OPEN DIFF (%)'
            tmp_msg += "{:<11} HIGH [9:15 - 10:15]: {}, {}: {:<10}\n\n".format(
                ' ', open_high_price, msg, open_high_first_one_hour_gain
            )

            buy_success_msg += tmp_msg
            buy_success_index += 1
        else:
            tmp_msg = "FAILED {:>2}: DATE: {}\n\n".format(
                buy_failed_index, human_readble_date,
            )
            tmp_msg += "{:<10} OPEN: {:<10} LOW: {:<10} {:<18} ".format(
                ' ', open_price, open_low_price,
                human_readable_days_low
            )
            tmp_msg += "CLOSE: {:<10} HIGH: {:<10}\n\n".format(
                close_price, day_high_price
            )
            tmp_msg += "{:<10} OPEN-LOW Diff (%): {:<10} GAIN (%): {:<10}\n\n".format(
                ' ', open_low_perc_diff, open_close_perc_diff
            )

            msg = 'GAIN MADE IN FIRST HOUR HIGH-OPEN DIFF (%)'
            tmp_msg += "{:<10} HIGH [9:15 - 10:15]: {}, {}: {:<10}\n\n".format(
                ' ', open_high_price, msg, open_high_first_one_hour_gain
            )

            buy_failed_msg += tmp_msg
            buy_failed_index += 1

        total_buy += 1

    gain_msg = ''
    percentage = round((total_buy_success / total_buy) * 100, 2)
    gain_percentage = round((gained_above_1_perc / total_buy) * 100, 2)
    gain_first_hour_percentage = round(
        (gained_above_in_first_1_hour_perc / total_buy) * 100, 2)

    gain_msg = ("Total 'Buy Call': {}\n".format(total_buy))
    gain_msg += ("Total 'Buy Call' Hold till End: {}\n".format(
        total_buy_success))
    gain_msg += ("Success Percentage: {}\n".format(percentage))
    gain_msg += ("Gained above 1%: {} ({}%), ".format(
        gained_above_1_perc, gain_percentage))
    gain_msg += ("Gained above 1% in first hour of trade: {} ({}%)\n\n".format(
        gained_above_in_first_1_hour_perc,
        gain_first_hour_percentage))

    return [buy_success_msg, buy_failed_msg, gain_msg]


def analyze_sell_call(sell_data, stock_data):
    total_sell = 0
    total_sell_success = 0
    sell_success_msg = ''
    sell_failed_msg = ''
    sell_success_index = 1
    sell_failed_index = 1
    gained_above_1_perc = 0
    gained_above_in_first_1_hour_perc = 0

    for key, buy in sell_data.items():
        start_date = '{} 09:15:00'.format(buy)
        end_date = '{} 15:15:00'.format(buy)

        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        mask = (stock_data['DATETIME'] >= start_date) & (
            stock_data['DATETIME'] <= end_date)
        day_data = stock_data.loc[mask]

        last_index = len(day_data) - 1

        open_price = day_data['OPEN'].iloc[0]
        open_low_price = day_data['LOW'].iloc[0]
        open_high_price = day_data['HIGH'].iloc[0]
        close_price = day_data['CLOSE'].iloc[last_index]
        day_high_price = day_data['HIGH'].max()
        day_low_price = day_data['LOW'].min()

        days_high = stock_data.loc[stock_data['HIGH']
                                   > open_price]
        temp_days_high_time = str(
            days_high['DATETIME'].iloc[0]).split(" ")[1]

        human_readable_days_low = "DAY's HIGH: [{:<10} TIME: {:8}]".format(
            day_low_price, temp_days_high_time
        )

        open_low_perc_diff = round(
            ((open_price - day_low_price) / open_price) * 100, 2)

        open_close_perc_diff = round(
            ((close_price - open_price) / open_price) * 100, 2)

        open_high_first_one_hour_gain = round(
            ((open_price - open_low_price) / open_price) * 100, 2)

        if open_close_perc_diff <= 1.0:
            gained_above_1_perc += 1

        if open_high_first_one_hour_gain <= 1.0:
            gained_above_in_first_1_hour_perc += 1

        human_readble_date = datetime.strptime(
            buy, '%Y-%m-%d')
        human_readble_date = human_readble_date.strftime(
            '%a %d %b, %Y')

        if close_price < open_price:
            total_sell_success += 1

            tmp_msg = "SUCCESS {:>2}: DATE: {}\n\n".format(
                sell_success_index, human_readble_date,
            )
            tmp_msg += "{:<11} OPEN: {:<10} LOW: {:<10} {:<18} ".format(
                ' ', open_price, open_low_price,
                human_readable_days_low
            )
            tmp_msg += "CLOSE: {:<10} HIGH: {:<10}\n\n".format(
                close_price, day_high_price
            )
            tmp_msg += "{:<11} OPEN-LOW Diff (%): {:<10} GAIN (%): {:<10}\n\n".format(
                ' ', open_low_perc_diff, open_close_perc_diff
            )

            msg = 'GAIN MADE IN FIRST HOUR HIGH-OPEN DIFF (%)'
            tmp_msg += "{:<11} HIGH [9:15 - 10:15]: {}, {}: {:<10}\n\n".format(
                ' ', open_high_price, msg, open_high_first_one_hour_gain
            )

            sell_success_msg += tmp_msg
            sell_success_index += 1
        else:
            tmp_msg = "FAILED {:>2}: DATE: {}\n\n".format(
                sell_failed_index, human_readble_date,
            )
            tmp_msg += "{:<10} OPEN: {:<10} LOW: {:<10} {:<18} ".format(
                ' ', open_price, open_low_price,
                human_readable_days_low
            )
            tmp_msg += "CLOSE: {:<10} HIGH: {:<10}\n\n".format(
                close_price, day_high_price
            )
            tmp_msg += "{:<10} OPEN-LOW Diff (%): {:<10} GAIN (%): {:<10}\n\n".format(
                ' ', open_low_perc_diff, open_close_perc_diff
            )

            msg = 'GAIN MADE IN FIRST HOUR HIGH-OPEN DIFF (%)'
            tmp_msg += "{:<10} HIGH [9:15 - 10:15]: {}, {}: {:<10}\n\n".format(
                ' ', open_high_price, msg, open_high_first_one_hour_gain
            )

            sell_failed_msg += tmp_msg
            sell_failed_index += 1

        total_sell += 1

    gain_msg = ''
    percentage = round((total_sell_success / total_sell) * 100, 2)
    gain_percentage = round((gained_above_1_perc / total_sell) * 100, 2)
    gain_first_hour_percentage = round(
        (gained_above_in_first_1_hour_perc / total_sell) * 100, 2)

    gain_msg = ("Total 'Sell Call': {}\n".format(total_sell))
    gain_msg += ("Total 'Sell Call' Hold till End: {}\n".format(
        total_sell_success))
    gain_msg += ("Success Percentage: {}\n".format(percentage))
    gain_msg += ("Gained above 1%: {} ({}%), ".format(
        gained_above_1_perc, gain_percentage))
    gain_msg += ("Gained above 1% in first hour of trade: {} ({}%)\n\n".format(
        gained_above_in_first_1_hour_perc,
        gain_first_hour_percentage))

    return [sell_success_msg, sell_failed_msg, gain_msg]
