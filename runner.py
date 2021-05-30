from pathlib import Path
from commonfunctions import *
from technicalanalysis import *


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
        try:
            coff_day = int(input("Enter No. of Days to calculate SD: ") or 7)
            if coff_day <= 0:
                coff_day = 7
        except ValueError as e:
            coff_day = 7

        stock_dates = get_start_end_date()

        day_or_hour = input(
            "Press (D)ay or (H)our analysis?").upper() or 'D'

        csv_file_name = 'data/yfinance/csv/{}-day.csv'.format(company_name)
        json_file_name = 'data/yfinance/json/{}-1h.json'.format(company_name)
        company_full_name = listed_companies[company_name][1]

        if Path(csv_file_name).is_file() and Path(json_file_name).is_file():

            if day_or_hour == 'H':
                technical_analysis(company_name, company_full_name,
                                   csv_file_name, json_file_name, coff_day)
            else:
                technical_analysis_day(company_name, company_full_name,
                                       csv_file_name, stock_dates)
        else:
            print("Company data not found")
    else:
        print("Company Not found.")

    input("Press any key to continue....")
