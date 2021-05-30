import json
from datetime import datetime
import pandas as pd
from commonfunctions import *
from stdfunctions import *


def technical_analysis_day(symbol, company_name, csv_file_name,
                           stock_dates):
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

    csv_data.set_index('DATE')

    start_date = stock_dates['start_date'][0]
    start_date_human_readble = stock_dates['start_date'][1]

    end_date = stock_dates['end_date'][0]
    end_date_human_readble = stock_dates['end_date'][1]

    mask = (csv_data['DATE'] >= start_date) & (
        csv_data['DATE'] <= end_date)

    data = csv_data.loc[mask]

    # Std and Mean data;
    temp_msg = find_std_and_mean(data)
    header = "SYMBOL: {}\n".format(symbol)
    header += "Company: {}\n".format(company_name)
    header += "From: {} - TO: {}\n\n".format(start_date_human_readble,
                                             end_date_human_readble)
    header += "{}\n".format(temp_msg)

    print(header)


def technical_analysis(symbol, company_name, csv_file_name, json_file_name,
                       stock_dates):

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

    csv_data.set_index('DATE')

    start_date = stock_dates['start_date'][0]
    start_date_human_readble = stock_dates['start_date'][1]

    end_date = stock_dates['end_date'][0]
    end_date_human_readble = stock_dates['end_date'][1]

    mask = (csv_data['DATE'] >= start_date) & (
        csv_data['DATE'] <= end_date)

    csv_tail = csv_data.tail(coff_day)

    cutoff_date = csv_tail.iloc[0]['Date']

    with open(json_file_name) as f:
        data = json.load(f)

    # print(json.dumps(data, indent=4, sort_keys=True))
    stock_open = data['chart']['result'][0]['indicators']['quote'][0]['open']
    stock_close = data['chart']['result'][0]['indicators']['quote'][0]['close']
    stock_high = data['chart']['result'][0]['indicators']['quote'][0]['high']
    stock_low = data['chart']['result'][0]['indicators']['quote'][0]['low']
    timestamps = data['chart']['result'][0]['timestamp']

    # Creating the dataframe
    data = pd.DataFrame(
        {
            "TIMESTAMP": timestamps,
            "OPEN": stock_open,
            "HIGH": stock_high,
            "LOW": stock_low,
            "CLOSE": stock_close
        }
    )

    data['TIMESTAMP'] = data['TIMESTAMP'].apply(
        lambda x: datetime.fromtimestamp(x))

    data['OPEN'] = data['OPEN'].apply(
        lambda x: round(float(x), 2))

    data['CLOSE'] = data['CLOSE'].apply(
        lambda x: round(float(x), 2))

    data['HIGH'] = data['HIGH'].apply(
        lambda x: round(float(x), 2))

    data['LOW'] = data['LOW'].apply(
        lambda x: round(float(x), 2))

    iCnt = 0
    buy_data = {}
    sell_data = {}
    other_data = {}
    buyCnt = 0
    sellCnt = 0
    otherCnt = 0

    start_date = datetime.strptime(cutoff_date, '%Y-%m-%d')
    mask = (data['TIMESTAMP'] >= start_date)
    ohl_date = data.loc[mask]

    # Std and Mean data;
    temp_msg = find_std_and_mean(ohl_date)
    header = "SYMBOL: {}\n".format(symbol)
    header += "Company: {}\n".format(company_name)
    header += "Analysis of last {} Day(s) \n\n{}\n".format(coff_day, temp_msg)

    # dont' use iterrows () it returns series so it will change the
    # datatype
    for index, row in ohl_date.iterrows():
        timestamp = row["TIMESTAMP"]
        timestamp = str(timestamp)
        open_price = row['OPEN']
        high_price = row['HIGH']
        low_price = row['LOW']
        close_price = row['CLOSE']

        msg = "{} Date: {}, Open: {}, Close: {}, High: {}, Low: {}".format(
            iCnt, timestamp, open_price, high_price, low_price, close_price)

        if "09:15:00" in timestamp:
            get_date = timestamp.split(" ")[0]

            if open_price == high_price:
                sell_data[sellCnt] = get_date
                sellCnt += 1
            elif open_price == low_price:
                buy_data[buyCnt] = get_date
                buyCnt += 1
            else:
                other_data[otherCnt] = get_date
                otherCnt += 1

        iCnt += 1

    total_buy = 1
    total_buy_success = 0
    for key, buy in buy_data.items():
        start_date = '{} 09:15:00'.format(buy)
        end_date = '{} 15:15:00'.format(buy)
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        mask = (data['TIMESTAMP'] >= start_date) & (
            data['TIMESTAMP'] <= end_date)
        ohl_date = data.loc[mask]
        msg = find_std_and_mean(ohl_date)

        print(header)
        print("BUY")
        print(ohl_date, "\n")
        print(msg)

        input("Press any key to continue...")
        clear_screen()

    for key, sell in sell_data.items():

        start_date = '{} 09:15:00'.format(sell)
        end_date = '{} 15:15:00'.format(sell)
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        mask = (data['TIMESTAMP'] >= start_date) & (
            data['TIMESTAMP'] <= end_date)
        ohl_date = data.loc[mask]
        msg = find_std_and_mean(ohl_date)

        print(header)
        print("SELL")
        print(ohl_date, "\n")
        print(msg)

        input("Press any key to continue...")
        clear_screen()

    for key, other in other_data.items():

        start_date = '{} 09:15:00'.format(other)
        end_date = '{} 15:15:00'.format(other)
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        mask = (data['TIMESTAMP'] >= start_date) & (
            data['TIMESTAMP'] <= end_date)
        ohl_date = data.loc[mask]
        msg = find_std_and_mean(ohl_date)

        print(header)
        print("OTHER")
        print(ohl_date, "\n")
        print(msg)

        input("Press any key to continue...")
        clear_screen()
