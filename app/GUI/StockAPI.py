import yfinance as yf
import threading
import pandas as pd
import datetime
import ta
import requests
import matplotlib.pyplot as plt

class Indicators:
    def __init__(self) -> None:
        self.rsi = 0
        self.macd = 0
        self.sma = 0
        self.stocha = 0
        self.mfi = 0
        self.bollinger = 0
        self.adx = 0
        self.atr = 0
        self.ema = 0
        self.overall = 0

class StockAPI:
    def __init__(self):
        self.tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', \
                        'PYPL', 'INTC', 'FB', 'JPM', 'V', 'JNJ', 'WMT', 'BAC', 'PG', 'XOM', \
                            'UNH', 'DIS', 'VZ', 'HD', 'PFE', 'CMCSA', 'KO', 'ADBE', 'T', 'MRK',\
                                  'PEP', 'CSCO']
        try:
            with open('/Users/Hanson/wx_stock/app/GUI/watchlist.txt', 'r') as f:
                self.tickers = f.read().strip().split('\n')
        except FileNotFoundError:
            with open('/Users/Hanson/wx_stock/app/GUI/watchlist.txt', 'w') as f:
                f.write('\n'.join(self.tickers))

    def download_data_1(self):
        f = open('/Users/Hanson/wx_stock/app/s&p500.txt', 'r')
        stocks = f.read().strip().split(' ')
        data = yf.download(stocks, start="2020-01-01", end="2023-12-31")
        return data

    def save_to_xl(self, data, ticker):
        df = pd.DataFrame(data)
        df.to_excel('/Users/Hanson/wx_stock/app/tickers/' + ticker + '.xlsx')

    def get_spx_tickers(self):
        # Fetching the constituents of S&P 500 index from Wikipedia
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        spx_tickers = pd.read_html(url)[0]['Symbol'].tolist()
        return spx_tickers

    def get_nasdaq_tickers(self):
        # Fetching the constituents of NASDAQ-100 index from Wikipedia
        url = "https://en.wikipedia.org/wiki/NASDAQ-100"
        nasdaq_tickers = pd.read_html(url)[2]['Ticker']
        return nasdaq_tickers

    def stocks_above_50sma(self):
        spx_tickers = self.get_spx_tickers()
        # Download historical data for all S&P 500 tickers
        data = yf.download(spx_tickers, period="150d")

        # Calculate the 50-day SMA for each stock
        sma_50 = data['Close'].rolling(window=50).mean()

        # Get the latest closing price for each stock
        latest_close = data['Close'].iloc[-1]

        # Count the number of stocks above their 50-day SMA
        number_in_days = []
        for i in range(1, 50):
            above_sma_count = (data['Close'].iloc[-i]> sma_50.iloc[-i]).sum()
            number_in_days.append(above_sma_count)
        # above_sma_count = (latest_close > sma_50.iloc[-1]).sum()

        # Total number of stocks in the S&P 500 index
        total_count = len(spx_tickers)

        return number_in_days, total_count

    def plot_sma(self, data):
        days = list(data.keys())
        num = list(data.values())[::-1]
        plt.plot(days, num)
        plt.xlabel('Days')
        plt.ylabel('Count')
        plt.title('Number of Tickers Above SMA')
        plt.show()

    def fetch_historical_data(self, ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    def calculate_moving_averages(self, data, window):
        data['SMA_' + str(window)] = data['Close'].rolling(window=window).mean()
        data['EMA_' + str(window)] = data['Close'].ewm(span=window, adjust=False).mean()

    def calculate_macd(self, data):
        data['MACD'] = ta.trend.MACD(data['Close']).macd()

    def calculate_rsi(self, data):
        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

    def calculate_bollinger_bands(self, data):
        bollinger = ta.volatility.BollingerBands(data['Close'])
        data['Bollinger_High'] = bollinger.bollinger_hband()
        data['Bollinger_Low'] = bollinger.bollinger_lband()

    def calculate_vwap(self, data):
        data['Cumulative_Volume_Price'] = (data['Close'] * data['Volume']).cumsum()
        data['Cumulative_Volume'] = data['Volume'].cumsum()
        data['VWAP'] = data['Cumulative_Volume_Price'] / data['Cumulative_Volume']

    def calculate_stochastic_oscillator(self, data):
        stoch = ta.momentum.StochasticOscillator(high=data['High'], low=data['Low'], close=data['Close'])
        data['Stoch_Osc'] = stoch.stoch()

    def calculate_obv(self, data):
        data['OBV'] = ta.volume.OnBalanceVolumeIndicator(data['Close'], data['Volume']).on_balance_volume()

    def calculate_atr(self, data):
        data['ATR'] = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close']).average_true_range()

    def fetch_additional_data(self, ticker):
        stock_info = yf.Ticker(ticker).info
        dividend_yield = stock_info.get('dividendYield')
        pe_ratio = stock_info.get('trailingPE')
        return dividend_yield, pe_ratio
    
    def get_watchlist_data(self):
        profolio = []
        for ticker in self.tickers:
            data = yf.download(ticker, period='2d')
            close = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            percentage_change = ((close - previous_close) / previous_close) * 100
            volume = data['Volume'].iloc[-1]
            profolio.append((ticker, close, percentage_change, volume))
        return profolio
    
    def get_indicators(ticker):
        data = Indicators()
        info = yf.download(ticker, period='1y')
        data.rsi = round(ta.momentum.RSIIndicator(info['Close']).rsi().iloc[-1], 1)
        data.macd = round(ta.trend.MACD(info['Close']).macd().iloc[-1], 1)
        data.sma = round(info['Close'].rolling(window=50).mean().iloc[-1], 1)
        data.stocha = round(ta.momentum.StochasticOscillator(high=info['High'], low=info['Low'], close=info['Close']).stoch().iloc[-1], 1)
        data.mfi = round(ta.volume.MFIIndicator(high=info['High'], low=info['Low'], close=info['Close'], volume=info['Volume']).money_flow_index().iloc[-1], 1)
        data.bollinger = round(ta.volatility.BollingerBands(info['Close']).bollinger_hband().iloc[-1], 1)
        data.adx = round(ta.trend.ADXIndicator(info['High'], info['Low'], info['Close']).adx().iloc[-1], 1)
        data.atr = round(ta.volatility.AverageTrueRange(info['High'], info['Low'], info['Close']).average_true_range().iloc[-1], 1)
        data.ema = round(info['Close'].ewm(span=50, adjust=False).mean().iloc[-1], 1)
        data.overall = round((data.rsi + data.macd + data.sma + data.stocha + data.mfi + data.bollinger + data.adx + data.atr + data.ema) / 9, 1)
        return data


if __name__ == '__main__':
    stock_api = StockAPI()