from datetime import datetime, timedelta

start_date = '2021-01-01'
end_date = '2021-06-01'

start_date = datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.strptime(end_date, '%Y-%m-%d')

while start_date < end_date:

    start_of_week = start_date - timedelta(days=start_date.weekday())
    end_of_week = start_of_week + timedelta(days=4)

    start_date = end_of_week + timedelta(days=3)

    sw = start_of_week.strftime('%A %d %b, %Y')
    ew = end_of_week.strftime('%A %d %b, %Y')

    print('{} - {}'.format(sw, ew))


# use this code to get data from monday to friday
# data['DATE'] = pd.to_datetime(data['DATE'])

# stock_peak = data.resample(
#     'W-Mon', on='DATE')['DATE', 'OPEN', 'CLOSE'].max()
# # stock_peak.reset_index().set_index('DATE')

# stock_valley = data.resample(
#     'W-Mon', on='DATE')['DATE', 'OPEN', 'CLOSE'].min()

# msg = "{:<20} {:<15} {:<15} {:<20} {:<15} {:<15}".format(
#     'Max Date', 'Max Open', 'Max Close', 'Min Date', 'Min Open', 'Min Close')
# print(msg)
# iCnt = 0
# for index, row in stock_peak.iterrows():
#     peak_date = row['DATE']
#     peak_open = row['OPEN']
#     peak_close = row['CLOSE']

#     valley = stock_valley.iloc[iCnt]
#     valley_date = valley.loc['DATE']
#     valley_open = valley.loc['OPEN']
#     valley_close = valley.loc['CLOSE']

#     # print(peak_date, valley_date)

#     msg = "{} {:<15} {:<15} {} {:<15} {:<15}".format(
#         peak_date, peak_open, peak_close, valley_date, valley_open, valley_close)
#     print(msg)

#     iCnt += 1
