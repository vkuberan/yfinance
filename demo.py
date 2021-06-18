from ohlanalysis import *
from datetime import datetime, time, timedelta

start_date = datetime.strptime(
    '2021-01-01', '%Y-%m-%d')
end_date = datetime.strptime(
    '2021-06-17', '%Y-%m-%d')

stock_name = 'POWERGRID'

ohl_analysis(start_date, end_date, stock_name)
