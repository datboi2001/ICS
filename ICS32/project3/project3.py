#Datthew Nguyen, 61886297
from datetime import datetime
import downloading_API as api
import signal_strategies as ss
import indicators as ind


class DailyPrice:
    """A class that contains the price information of a stock on a given day."""
    def __init__(self, open = 0.0, high = 0.0, low = 0.0, close = 0.0, volume = 0.0, indicator = '', date = '', buy = '', sell = ''):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.indicator = indicator
        self.date = date
        self.buy = buy
        self.sell = sell


def _input_from_users() -> (str, str, str, str, str):
    """Ask the user to input information. Return the all the input. """
    api_key_file = input()
    partial_url = input()
    symbol = input()
    start_date = input()
    end_date = input()
    strategy = input()
    return api_key_file, partial_url, symbol, start_date, end_date, strategy


def _read_api(api_file: str) -> str:
    """Open and get the first line of the API key file."""
    api_file = open(api_file)
    return api_file.readline()


def _convert_to_list(data: dict, start_date: str, end_date: str) -> list or str:
    """Given the data from Alpha Advantage, convert the data of a stock into a list full of class objects
     that lies within the given start date and end date.
     """
    time_series_daily = 'Time Series (Daily)'
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    price_list = []
    try:
        for date in data[time_series_daily]:
            date_object = datetime.strptime(date, '%Y-%m-%d').date()
            if start_date <= date_object <= end_date:
                x = DailyPrice()
                x.open = data[time_series_daily][date]['1. open']
                x.high = data[time_series_daily][date]['2. high']
                x.low = data[time_series_daily][date]['3. low']
                x.close = data[time_series_daily][date]['4. close']
                x.volume = data[time_series_daily][date]['5. volume']
                x.date = date
                price_list.append(x)
    except KeyError:
        return 'FORMAT'
    else:
        price_list = sorted(price_list, key=lambda x: x.date, reverse=False)
        return price_list


def _indicator_command(name: str, price_list: list) -> list:
    """This function will sort through the sixth line of the input
     and call out the neccessary classes to perform the analysis. It returns a new
     price list with the updated indicators and buy and sell signals.
     """
    parts = name.split()
    if name.startswith('TR'):
        new_price_list = ind.TrueRange(price_list).map_indicator()
        final_price_list = ss.TRSignals(new_price_list, parts).buy_or_sell()
    else:
        period = int(parts[1])
        if name.startswith('MP'):
            new_price_list = ind.PriceAverage(price_list, period).map_indicator()
            final_price_list = ss.MPSignals(new_price_list, period).buy_or_sell()
        elif name.startswith('MV'):
            new_price_list = ind.VolumeAverage(price_list, period).map_indicator()
            final_price_list = ss.MVSignals(new_price_list, period).buy_or_sell()
        elif name.startswith('DP'):
            new_price_list = ind.PriceDirection(price_list, period).map_indicator()
            final_price_list = ss.DPSignals(new_price_list, parts).buy_or_sell()
        elif name.startswith('DV'):
            new_price_list = ind.VolumeDirection(price_list, period).map_indicator()
            final_price_list = ss.DVSignals(new_price_list, parts).buy_or_sell()
    return final_price_list


def _print_data(data:list, symbol: str, strategy: str) -> None:
    """Organize the data in a table. Print out the table."""
    print(symbol)
    print(len(data))
    print(strategy)
    print('Date\tOpen\tHigh\tLow\tClose\tVolume\tIndicator\tBuy?\tSell?')
    if strategy.startswith('TR') or strategy.startswith('MP') or strategy.startswith('MV'):
        for x in data:
            if x.indicator == '':
                print(f'{x.date}\t{x.open}\t{x.high}\t{x.low}\t{x.close}\t{x.volume}\t{x.indicator}\t{x.buy}\t{x.sell}')
            else:
                print(f'{x.date}\t{x.open}\t{x.high}\t{x.low}\t{x.close}\t{x.volume}\t{x.indicator:.4f}\t{x.buy}\t{x.sell}')
    else:
        for x in data:
            if x.indicator > 0:
                print(f'{x.date}\t{x.open}\t{x.high}\t{x.low}\t{x.close}\t{x.volume}\t+{x.indicator}\t{x.buy}\t{x.sell}')
            elif x.indicator <= 0:
                print(f'{x.date}\t{x.open}\t{x.high}\t{x.low}\t{x.close}\t{x.volume}\t{x.indicator}\t{x.buy}\t{x.sell}')


def run_analysis() -> None:
    """Dashboard of the program."""
    api_key_file, partial_url, symbol, start_date, end_date, strategy = _input_from_users()
    api_key = _read_api(api_key_file)
    stock_info = api.data_retrieval(api.build_url_with_query(api_key, symbol, partial_url))
    if type(stock_info) != dict:
        print('FAILED')
        print(stock_info)
        if stock_info == 0:
            print('NETWORK')
        elif type(stock_info) == str:
            print('NOT 200')
        else:
            print('FORMAT')
        return
    stock_data = _convert_to_list(stock_info, start_date, end_date)
    if stock_data == 'FORMAT':
        print('FAILED')
        print(200)
        print('FORMAT')
        return
    stock_data = _indicator_command(strategy, stock_data)
    _print_data(stock_data, symbol, strategy)

if __name__ == '__main__':
    run_analysis()