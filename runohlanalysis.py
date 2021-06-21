from ohlanalysis import *
from commonfunctions import *
from datetime import datetime, time, timedelta

keepAlive = True
listed_companies = get_nse_listed_companies()


while keepAlive:
    clear_screen()
    prompt_msg = "Enter the Symbol of the Company (Ex: POWERGRID) or "
    prompt_msg += "Q to quit: "

    company_name = input(prompt_msg).upper().strip()

    if company_name == 'Q':
        keepAlive = False
        break
    elif company_name in listed_companies:
        company_full_name = listed_companies[company_name][1]
        stock_dates = get_start_end_date()

        start_date = stock_dates['start_date'][0]
        end_date = stock_dates['end_date'][0]

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        ohl_analysis(start_date, end_date, company_name, company_full_name)

    input("Press any key to continue...")
