from commonfunctions import *
from datetime import datetime, time, timedelta


stock_dates = get_start_end_date()

print(stock_dates['start_date'])
print(stock_dates['end_date'])

exit()

csv_data = pd.read_csv('data/yfinance/csv/AXISBANK-day.csv')

csv_data.set_index('Date')

csv_data['DATE'] = csv_data['Date']

csv_data['OPEN'] = csv_data['Open'].apply(
    lambda x: round(float(x), 2))

csv_data['HIGH'] = csv_data['High'].apply(
    lambda x: round(float(x), 2))

csv_data['LOW'] = csv_data['Low'].apply(
    lambda x: round(float(x), 2))

csv_data['CLOSE'] = csv_data['Close'].apply(
    lambda x: round(float(x), 2))

print(csv_data)

mask = (csv_data['DATE'] >= start_date) & (
    csv_data['DATE'] <= end_date)
ohl_date = csv_data.loc[mask]

print(ohl_date)
