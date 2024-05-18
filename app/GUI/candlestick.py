import mplfinance as mpf
import yfinance as yf
from datetime import date, timedelta
import matplotlib.pyplot as plt

class CandleStickGraph():

    def __init__(self, symbol:str, days:int) -> None:
        super().__init__()
        self.days = days
        self.symbol = symbol
        self.get_date(self.days)

    def get_date(self, days:int):
        self.today = date.today()
        self.before = self.today - timedelta(days=days)
        self.before = self.before.strftime("%Y-%m-%d")
        #return self.before, self.today

    def plot(self):
        df = yf.download(self.symbol, start=self.before, end=self.today)
        #fig, ax = plt.subplots(figsize=(8,6))
        mpf.plot(df, type='candle', mav=(25,50), volume=True)
        mpf.show()
        #plt.plot(fig)


a = CandleStickGraph('nvda', 200)
a.plot()