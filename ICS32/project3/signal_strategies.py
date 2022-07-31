#Datthew Nguyen, 61886297
class TRSignals:
    def __init__(self, price_list, threshold):
        self._price_list = price_list
        self._buy_threshhold = threshold[1]
        self._sell_threshhold = threshold[2]


    def buy_or_sell(self) -> list:
        """Generate buy or sell signals after analyzing the buying and selling threshold."""
        buy_point = float(self._buy_threshhold[1:])
        buy_symbol = self._buy_threshhold[0]
        sell_point = float(self._sell_threshhold[1:])
        sell_symbol = self._sell_threshhold[0]
        for x in range(1, len(self._price_list)):
            price_data = self._price_list[x]
            true_range = price_data.indicator
            if buy_symbol == '<':
                if true_range < buy_point:
                    price_data.buy = 'BUY'
            if sell_symbol == '>':
                if true_range > sell_point:
                    price_data.sell = 'SELL'
            if buy_symbol == '>':
                if true_range > buy_point:
                    price_data.buy = 'BUY'
            if sell_symbol == '<':
                if true_range < sell_point:
                    price_data.sell = 'SELL'
        return self._price_list


class MPSignals:
    def __init__(self, price_list, period):
        self._price_list = price_list
        self._period = period

    def buy_or_sell(self) -> list:
        """Generate a buy signals if the closing price is
        above the average and the previous closing price is not
        above the previous average. Vice versa."""
        for x in range(self._period, len(self._price_list)):
            average = self._price_list[x].indicator
            close = float(self._price_list[x].close)
            p_average = self._price_list[x-1].indicator
            p_close = float(self._price_list[x-1].close)
            if close > average and p_close <=  p_average:
                self._price_list[x].buy = 'BUY'
            elif close < average and p_close >= p_average:
                self._price_list[x].sell = 'SELL'
        return self._price_list


class MVSignals:
    def __init__(self, price_list, period):
        self._price_list = price_list
        self._period = period

    def buy_or_sell(self) -> list:
        """This function works just like the MovingAveragePriceSignals buy_or_sell method.
        However, this function only works with the volume of each data point."""
        for x in range(self._period, len(self._price_list)):
            average = self._price_list[x].indicator
            volume = float(self._price_list[x].volume)
            p_average = self._price_list[x-1].indicator
            p_volume = float(self._price_list[x-1].volume)
            if volume > average and p_volume <= p_average:
                self._price_list[x].buy = 'BUY'
            elif volume < average and p_volume >= p_average:
                self._price_list[x].sell = 'SELL'
        return self._price_list


class DirectionSignals:
    def __init__(self, price_list, threshhold):
        self._price_list = price_list
        self._buy_threshold = int(threshhold[2])
        self._sell_threshold = int(threshhold[3])


    def buy_or_sell(self)-> list:
        """Generate buy or sell signals from the given buy and
        sell threshold."""
        for x in range(1, len(self._price_list)):
            if self._price_list[x].indicator > self._buy_threshold and self._price_list[x-1].indicator <= self._buy_threshold:
                self._price_list[x].buy = 'BUY'
            elif self._price_list[x].indicator < self._sell_threshold and self._price_list[x-1].indicator >= self._sell_threshold:
                self._price_list[x].sell = 'SELL'
        return self._price_list


class DPSignals(DirectionSignals):
    pass

class DVSignals(DirectionSignals):
    pass

# Generating the buy and sell signals of the Price Direction Indicator is identical to that of
# the Volume Direction Indicator. Therefore, I created a parent class that generates the buy and sell
# signals of both indicators and create two children classes that inherit the parent class to satisfy
# the requirement of the project write up.