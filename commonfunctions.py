import os
import platform
import subprocess
from datetime import datetime, time, timedelta
import pandas as pd

CURRENT_DAY = datetime.today()
THREE_MONTHS_BEFORE = CURRENT_DAY - timedelta(days=90)
SIX_MONTHS_BEFORE = CURRENT_DAY - timedelta(days=180)
YEAR_BEFORE = CURRENT_DAY - timedelta(days=365)

# Timestamps
CURRENT_DAY_TS = datetime.timestamp(CURRENT_DAY)
THREE_MONTHS_BEFORE_TS = datetime.timestamp(THREE_MONTHS_BEFORE)
SIX_MONTHS_BEFORE_TS = datetime.timestamp(SIX_MONTHS_BEFORE)
YEAR_BEFORE_TS = datetime.timestamp(YEAR_BEFORE)


# related to date and time
def date_suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + date_suffix(t.day))


def is_time_between(begin_time, end_time, check_time=None):
    begin_time = time(begin_time[0], begin_time[1])
    end_time = time(end_time[0], end_time[1])
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return False


def get_start_end_date():
    final_start_date = ''
    start_date_human_readble = ''
    final_end_date = ''
    end_date_human_readble = ''

    try:
        today = datetime.today()
        five_days_ago = today - timedelta(days=5)

        start_date = input(
            "Start Date (YYYY-MM-DD): ").strip() or five_days_ago.strftime('%Y-%m-%d')

        end_date = input(
            "End Date (YYYY-MM-DD): ").strip() or today.strftime('%Y-%m-%d')

        if start_date != '':
            start_date = start_date.replace('/', '-')
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            final_start_date = start_date.strftime('%Y-%m-%d')
            start_date_human_readble = custom_strftime(
                '{S} %A %B, %Y', start_date)

        if end_date != '':
            end_date = end_date.replace('/', '-')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            final_end_date = end_date.strftime('%Y-%m-%d')
            end_date_human_readble = custom_strftime(
                '{S} %A %B, %Y', end_date)

    except Exception as e:
        print(e)
        final_start_date = five_days_ago.strftime('%Y-%m-%d')
        start_date_human_readble = custom_strftime(
            '{S} %A %B, %Y', five_days_ago)

        final_end_date = today.strftime('%Y-%m-%d')
        end_date_human_readble = custom_strftime(
            '{S} %A %B, %Y', today)

    start_end_date = {
        'start_date': [final_start_date, start_date_human_readble],
        'end_date': [final_end_date, end_date_human_readble]
    }

    return start_end_date


def clear_screen():
    command = "cls" if platform.system().lower() == "windows" else "clear"
    return subprocess.call(command, shell=True)


def print_char_under_string(msg, char='', newline='\n\n'):
    if char != '':
        msg += "\n" + (char * len(msg))
    print(msg, end=newline)


def create_related_dirs(project_dirs):
    # create 2 separate directories to save html and the scraped data
    for dirname, dirpath in project_dirs.items():
        # check weather the dir exists, if not create new one
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            print("{}: '{}' directory is created.".format(dirname, dirpath))


def get_nse_listed_companies():
    listings = pd.read_csv("data/listedcompanies/listedcompanies.csv")
    listings.set_index('SYMBOL')
    return listings.set_index('SYMBOL').T.to_dict('list')
