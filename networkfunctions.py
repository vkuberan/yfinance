import random
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from nseapiendpoints import *

# seconds
DEFAULT_TIMEOUT = 5
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],  # http://httpstat.us/
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
USER_AGENT += 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'


# To set default timeout parameter for our scrapper
# Refer: https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#request-hooks
class VeluWebHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)


# NSE Data is a special case that's why we are using separate function to get nse data
# refer this page for help
# https://stackoverflow.com/questions/65072787/python-selenium-data-does-not-load-website-security
def fetch_nse_data(link_source):
    data = {}
    try:
        adapter = VeluWebHTTPAdapter(
            max_retries=retry_strategy, timeout=5)
        http = requests.Session()
        headers = {'user-agent': USER_AGENT}
        http.headers.update(headers)
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        response = http.get(link_source[0])
        response.raise_for_status()
        response = http.get(link_source[1])
        response.raise_for_status()
        data['headers'] = response.headers
        data['body'] = response.text
    except Exception as e:
        print("Error: {}".format(e))
    return data


def fetch_nse_data_from_endpoints(nse_endpoints=''):
    if nse_endpoints == '':
        for nifty, endpoints in nse_api_endpoints.items():
            print("Fetching {}....".format(nifty.upper().replace('-', ' ')))
            data = fetch_nse_data(endpoints)
            if data['headers']:
                file_name = data['headers']['Content-disposition'].split('=')[
                    1]
                download_path = 'data/unclean/' + file_name
                with open(download_path, 'w') as writer:
                    writer.write(data['body'])

            # Its a better practice to delay the requests because too much
            # request will lead to a ban for this ip from NSEIndia
            secure_random = random.SystemRandom()
            wait_for = round(secure_random.uniform(.1, 2.5), 2)
            print("Wait for {} seconds.".format(wait_for))
            time.sleep(wait_for)
    else:
        if len(nse_endpoints) == 2:
            data = fetch_nse_data(nse_endpoints)
            if data['headers']:
                file_name = data['headers']['Content-disposition'].split('=')[
                    1]
                download_path = 'data/unclean/' + file_name
                with open(download_path, 'w') as writer:
                    writer.write(data['body'])
        else:
            print(
                "Something goes wrong. Try to supply proper NSE Endpoints. \
                    Refer: nseapiendpoints.py")


# Other than NSEINDIA use this one.
def fetch_data_from_url(link_source):
    data = ''
    try:
        adapter = VeluWebHTTPAdapter(
            max_retries=retry_strategy, timeout=5)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        response = http.get(link_source)
        # print(response.headers)

        data = response.text
    except Exception as e:
        print(e)

    return data


def generate_yfinance_url(symbol, start_date, end_date, chart='NO'):
    yfinance_url = ''
    if chart == 'NO':
        base_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}'.format(
            symbol)
        qry_string_1 = "?period1={}&period2={}".format(start_date, end_date)
        qry_string_2 = "&interval=1d&events=history&includeAdjustedClose=true"
        yfinance_url = '{}{}{}'.format(base_url, qry_string_1, qry_string_2)
    elif chart == '1h' or chart == '15m' or chart == '30m':
        base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/?symbol={}'.format(
            symbol)
        qry_string_1 = "&period1={}&period2={}".format(start_date, end_date)
        qry_string_2 = "&useYfid=true&interval={}".format(chart)
        yfinance_url = '{}{}{}'.format(base_url, qry_string_1, qry_string_2)
    return yfinance_url
