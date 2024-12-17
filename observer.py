from abc import ABC, abstractmethod
from datetime import datetime
import re

class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, snapshot_time, stocks):
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, snapshot_time, stocks):
        pass

class StockData:
    def __init__(self, company, ticker, current_price, change_dollar, change_percent, ytd_change, high_52, low_52, pe_ratio):
        self.company = company
        self.ticker = ticker
        self.current_price = float(current_price)
        self.change_dollar = float(change_dollar)
        self.change_percent = float(change_percent)
        self.ytd_change = float(ytd_change)
        self.high_52 = float(high_52)
        self.low_52 = float(low_52)
        self.pe_ratio = float(pe_ratio)

    @staticmethod
    def parse_line(line):
        regex = r"(.+?)\s+([A-Z]+)\s+([\d.]+)\s+([-+]?[\d.]+)\s+([-+]?[\d.]+)\s+([-+]?[\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"
        match = re.match(regex, line)
        if match:
            return StockData(*match.groups())
        return None

class LocalStocks(Subject):
    def __init__(self):
        self.observers = []
        self.file_position = 0

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, snapshot_time, stocks):
        for observer in self.observers:
            observer.update(snapshot_time, stocks)

    def read_snapshot(self, file_path):
        with open(file_path, 'r') as file:
            file.seek(self.file_position)

            snapshot_time = None
            current_snapshot = []

            while True:
                line = file.readline()
                if not line:
                    break
                line = line.strip()
                
                if line.startswith("Last updated"):
                    snapshot_time = datetime.strptime(line[13:], '%b %d, %Y %I:%M:%S %p ET')
                elif line == "":
                    if snapshot_time and current_snapshot:
                        self.notify_observers(snapshot_time, current_snapshot)
                        self.file_position = file.tell()
                        return
                else:
                    stock = StockData.parse_line(line)
                    if stock:
                        current_snapshot.append(stock)

class AverageObserver(Observer):
    def __init__(self, file_path):
        self.file_path = file_path
        
    def update(self, snapshot_time, stocks):
        average_price = sum(stock.current_price for stock in stocks) / len(stocks)
        with open(self.file_path, 'a') as file:
            file.write(f"{snapshot_time}, Average price: {average_price:.2f}\n")

class HighLowObserver(Observer):
    def __init__(self, file_path):
        self.file_path = file_path

    def update(self, snapshot_time, stocks):
        with open(self.file_path, 'a') as file:
            file.write(f"Last updated {snapshot_time} ET\n")
            for stock in stocks:
                if (stock.high_52 != 0 and abs(stock.current_price - stock.high_52) / stock.high_52 <= 0.01) or \
                   (stock.low_52 != 0 and abs(stock.current_price - stock.low_52) / stock.low_52 <= 0.01):
                    file.write(f"{stock.ticker}: {stock.current_price}, {stock.high_52}, {stock.low_52}\n")
            file.write("\n")

class SelectionObserver(Observer):
    def __init__(self, file_path, tickers):
        self.file_path = file_path
        self.tickers = tickers

    def update(self, snapshot_time, stocks):
        with open(self.file_path, 'a') as file:
            file.write(f"Last updated {snapshot_time} ET:\n")
            for stock in stocks:
                if stock.ticker in self.tickers:
                    file.write(f"{stock.company} {stock.ticker} {stock.current_price} {stock.change_dollar} {stock.change_percent} {stock.ytd_change} {stock.high_52} {stock.low_52} {stock.pe_ratio}\n")
            file.write("\n")

def main():
    local_stocks = LocalStocks()

    avg_observer = AverageObserver("Average.dat")
    high_low_observer = HighLowObserver("HighLow.dat")
    tickers = ["ALL", "BA", "BC", "GBEL", "KFT", "MCD", "TR", "WAG"]
    selection_observer = SelectionObserver("Selections.dat", tickers)
    print("Adding average observer")
    local_stocks.add_observer(avg_observer)
    print("Reading snapshot")
    local_stocks.read_snapshot("ticker.dat")
    print("Adding high low observer")
    local_stocks.add_observer(high_low_observer)
    print("Reading snapshot")   
    local_stocks.read_snapshot("ticker.dat")
    print("Adding selection observer")
    local_stocks.add_observer(selection_observer)
    print("Reading snapshot")
    local_stocks.read_snapshot("ticker.dat")
    print("Removing selection observer")
    local_stocks.remove_observer(selection_observer)
    print("Reading snapshot")
    local_stocks.read_snapshot("ticker.dat")
    print("Removing high low observer")
    local_stocks.remove_observer(high_low_observer)
    print("Reading snapshot")
    local_stocks.read_snapshot("ticker.dat")

if __name__ == "__main__":
    main()
