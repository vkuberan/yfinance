import pandas as pd


# To find Standard Deviations and Means of a stock
def find_std_and_mean(data):
    msg = ''
    open_std = round(data['OPEN'].std(axis=0, skipna=True), 2)
    high_std = round(data['HIGH'].std(axis=0, skipna=True), 2)
    low_std = round(data['LOW'].std(axis=0, skipna=True), 2)
    close_std = round(data['CLOSE'].std(axis=0, skipna=True), 2)

    open_mean = round(data['OPEN'].mean(), 2)
    high_mean = round(data['HIGH'].mean(), 2)
    low_mean = round(data['LOW'].mean(), 2)
    close_mean = round(data['CLOSE'].mean(), 2)

    open_max = round(data['OPEN'].max(), 2)
    high_max = round(data['HIGH'].max(), 2)
    low_max = round(data['LOW'].max(), 2)
    close_max = round(data['CLOSE'].max(), 2)

    open_min = round(data['OPEN'].min(), 2)
    high_min = round(data['HIGH'].min(), 2)
    low_min = round(data['LOW'].min(), 2)
    close_min = round(data['CLOSE'].min(), 2)

    open_data = "{} [{} - {}]".format(open_mean, open_min, open_max)
    close_data = "{} [{} - {}]".format(close_mean, close_min, close_max)
    high_data = "{} [{} - {}]".format(high_mean, high_min, high_max)
    low_data = "{} [{} - {}]".format(low_mean, low_min, low_max)

    msg = ("{:<20} \nOpen: {}, \nHigh: {}, \nLow: {}, \nClose: {}\n".format(
        "Average:", open_data, high_data, low_data, close_data
    ))
    msg += ("{:<20} Open: {}, High: {}, Low: {}, Close: {}\n".format(
        "\nStandard Deviation:", open_std, high_std, low_std, close_std
    ))

    open_between = 'Open Range: [{} - {}]'.format(
        round((open_mean - open_std), 2), round((open_mean + open_std), 2))
    high_between = 'High Range: [{} - {}]'.format(
        round((high_mean - high_std), 2), round((high_mean + high_std), 2))
    low_between = 'Low Range: [{} - {}]'.format(
        round((low_mean - low_std), 2), round((low_mean + low_std), 2))
    close_between = 'Close Range: [{} - {}]'.format(
        round((close_mean - close_std), 2), round((close_mean + close_std), 2))

    msg += '\nRange:\n'
    msg += '{}, {}\n'.format(open_between, close_between)
    msg += '{}, {}\n\n'.format(high_between, low_between)

    msg += "High Max: {}, Low min: {}\n\n".format(high_max, low_min)
    # Fib golden ratio retracement
    diff = high_max - low_min
    fib_retrace_1 = high_max - (0.236 * diff)
    fib_retrace_2 = high_max - (0.382 * diff)
    # non fib is added in some calculations
    fib_retrace_3 = high_max - (0.50 * diff)
    fib_retrace_4 = high_max - (0.618 * diff)

    fib_retrace_1 = round(fib_retrace_1, 2)
    fib_retrace_2 = round(fib_retrace_2, 2)
    fib_retrace_3 = round(fib_retrace_3, 2)
    fib_retrace_4 = round(fib_retrace_4, 2)

    msg += "Fibonacci Retracement Level\n"
    msg += "Level 1 at 0.236: {}\n".format(fib_retrace_1)
    msg += "Level 2 at 0.382: {}\n".format(fib_retrace_2)
    msg += "Level 3 at 0.50: {}\n".format(fib_retrace_3)
    msg += "Level 4 at 0.618: {}\n\n".format(fib_retrace_4)

    fib_ext_1 = high_max + (0.236 * diff)
    fib_ext_2 = high_max + (0.382 * diff)
    # non fib is added in some calculations
    fib_ext_3 = high_max + (0.50 * diff)
    fib_ext_4 = high_max + (0.618 * diff)

    fib_ext_1 = round(fib_ext_1, 2)
    fib_ext_2 = round(fib_ext_2, 2)
    fib_ext_3 = round(fib_ext_3, 2)
    fib_ext_4 = round(fib_ext_4, 2)

    msg += "Fibonacci Extensions Level\n"
    msg += "Level 1 at 0.236: {}\n".format(fib_ext_1)
    msg += "Level 2 at 0.382: {}\n".format(fib_ext_2)
    msg += "Level 3 at 0.50: {}\n".format(fib_ext_3)
    msg += "Level 4 at 0.618: {}\n\n".format(fib_ext_4)

    day_open = data.head(1).iloc[0]['OPEN']
    day_close = data.tail(1).iloc[0]['CLOSE']
    cash_gain = round(day_close - day_open, 2)
    percent_gained = round(((day_close - day_open) / day_close) * 100, 2)

    msg += ("\nOPEN: {}, CLOSE: {}, GAIN IN (₹): {}, GAIN in (%): {}\n".format(
        day_open, day_close, cash_gain, percent_gained))

    return msg
