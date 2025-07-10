import csv
from collections import deque

class TradingBot:
    """Simple moving average crossover trading bot."""

    def __init__(self, prices):
        self.prices = prices
        self.balance = 1000.0
        self.position = 0.0
        self.ma5_window = deque(maxlen=5)
        self.ma10_window = deque(maxlen=10)
        self.last_signal = 0  # 0 = no position, 1 = long

    def moving_average(self, window):
        return sum(window) / len(window)

    def update(self, price):
        self.ma5_window.append(price)
        self.ma10_window.append(price)
        if len(self.ma5_window) < 5 or len(self.ma10_window) < 10:
            return None
        ma5 = self.moving_average(self.ma5_window)
        ma10 = self.moving_average(self.ma10_window)
        signal = 1 if ma5 > ma10 else 0
        if signal != self.last_signal:
            self.trade(signal, price)
            self.last_signal = signal
        return signal

    def trade(self, signal, price):
        if signal == 1 and self.balance > 0:
            # buy with all balance
            self.position = self.balance / price
            self.balance = 0
        elif signal == 0 and self.position > 0:
            # sell all
            self.balance = self.position * price
            self.position = 0

    def run(self):
        for price in self.prices:
            self.update(price)
        # final portfolio value
        return self.balance + self.position * self.prices[-1]


def load_prices(path):
    prices = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prices.append(float(row['Close']))
    return prices


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simple moving average trading bot")
    parser.add_argument('csvfile', help='CSV file with Date and Close columns')
    args = parser.parse_args()
    prices = load_prices(args.csvfile)
    bot = TradingBot(prices)
    final_value = bot.run()
    print(f"Final portfolio value: {final_value:.2f}")


if __name__ == '__main__':
    main()
