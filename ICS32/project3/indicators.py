#Datthew Nguyen, 61886297
class TrueRange:
    def __init__(self, price_list: list):
        self._price_list = price_list


    def map_indicator(self) -> list:
        """Compute the true range of a stock."""
        for i in range(len(self._price_list)-1):
            high = float(self._price_list[i+1].high)
            low = float(self._price_list[i+1].low)
            previous_close = float(self._price_list[i].close)
            if previous_close > high:
                true_range = previous_close - low
            elif previous_close < low:
                true_range = high - previous_close
            else:
                true_range = high - low
            true_range = true_range / previous_close * 100
            self._price_list[i + 1].indicator = true_range
        return self._price_list


class PriceAverage:
    def __init__(self, price_list: list, num_days: int):
        self._num_days = num_days
        self._price_list = price_list


    def map_indicator(self)-> list:
        """Calculate the moving average of the price from the given data and
        transfer that value to the indicator attribute of the price data."""
        trading_days = len(self._price_list)
        for x in range(0, trading_days - self._num_days + 1):
            total = 0
            for i in range(x, x + self._num_days):
                total += float(self._price_list[i].close)
            price_average = total / self._num_days
            self._price_list[x + self._num_days-1].indicator = price_average
        return self._price_list


class VolumeAverage:
    def __init__(self, price_list: list, num_days: int):
        self._num_days = num_days
        self._price_list = price_list


    def map_indicator(self) -> list:
        """Calculate the moving average of the volume from the given data and
        transfer that value to the indicator attribute of each DailyPrice object from
        the price list.
        """
        trading_days = len(self._price_list)
        for x in range(0, trading_days - self._num_days + 1):
            total = 0
            for i in range(x, x + self._num_days):
                total += float(self._price_list[i].volume)
            price_average = total / self._num_days
            self._price_list[x + self._num_days - 1].indicator = price_average
        return self._price_list


class PriceDirection:
    def __init__(self, price_list: list, num_days: int):
        self._num_days = num_days
        self._price_list = price_list

    def n_days_ago_direction(self, index) -> int:
        """Find the direction of closing price n days ago."""
        close = float(self._price_list[index].close)
        previous_close = float(self._price_list[index - 1].close)
        if close > previous_close:
            return 1
        else:
            return -1


    def map_indicator(self) -> list:
        """Find the directional indicator of each data point
        and transfer that value to the indicator attribute of each data point.
        """
        self._price_list[0].indicator = 0
        count = 0
        for x in range(1, len(self._price_list)):
            close = float(self._price_list[x].close)
            previous_close = float(self._price_list[x-1].close)
            if close > previous_close :
                count = count + 1
            elif close < previous_close:
                count = count - 1
            if x > self._num_days:
                count = count - (self.n_days_ago_direction(x - self._num_days))
            self._price_list[x].indicator = count
        return self._price_list


class VolumeDirection:
    def __init__(self, price_list: list, num_days: int):
        self._num_days = num_days
        self._price_list = price_list


    def n_days_ago_direction(self, index) -> int:
        """Find the directional indicator of the volume n days ago."""
        volume = float(self._price_list[index].volume)
        previous_volume = float(self._price_list[index - 1].volume)
        if volume > previous_volume:
            return 1
        else:
            return -1


    def map_indicator(self) -> list:
        """Calculate the directional indicator of the volume of each data point
        and transfer that value to the indicator attribute of each data point.
        """
        self._price_list[0].indicator = 0
        count = 0
        for x in range(1, len(self._price_list)):
            volume = float(self._price_list[x].volume)
            previous_volume = float(self._price_list[x-1].volume)
            if volume > previous_volume :
                count = count + 1
            elif volume < previous_volume:
                count = count - 1
            if x > self._num_days:
                count = count - (self.n_days_ago_direction(x - self._num_days))
            self._price_list[x].indicator = count
        return self._price_list