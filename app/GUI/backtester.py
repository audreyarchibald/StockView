import yfinance as yf
import matplotlib.pyplot as plt

class Stock():
    def __init__(self, symbol, start_date, end_date, interval):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = self.get_data()
        self.get_bollinger_bands(20)
        self.get_smav()
        self.get_emav()
        self.get_macd()
        self.get_rsi()
        self.get_stochastic()
        self.output_csv()

    def output_csv(self):
        self.data.to_csv(f"app/GUI/tickers/{self.symbol}.csv")

    def get_data(self):
        data = yf.download(self.symbol, start=self.start_date, end=self.end_date, 
                           interval=self.interval)
        return data
    
    def get_rsi(self):
        delta = self.data['Adj Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.data['RSI'] = rsi  # Add RSI column to the data DataFrame
        return True

    def get_stochastic(self):
        low_14, high_14 = self.data['Low'].rolling(window=14).min(), \
                            self.data['High'].rolling(window=14).max()
        k = 100 * ((self.data['Adj Close'] - low_14) / (high_14 - low_14))
        d = k.rolling(window=3).mean()
        self.data['%K'] = k
        self.data['%D'] = d
        return True
    
    def get_macd(self):
        exp12 = self.data['Adj Close'].ewm(span=12, adjust=False).mean()
        exp26 = self.data['Adj Close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        self.data['MACD'] = macd
        self.data['Signal'] = signal
        return True
    
    def get_smav(self):
        sma_days = [25,50, 80, 100, 125, 150, 200]
        for s in sma_days:
            smav = self.data['Adj Close'].rolling(window=s).mean()
            self.data[f'SMA_{s}'] = smav
        return True
    
    def get_emav(self):
        ema_days = [25,50, 80, 100, 125, 150, 200]
        for e in ema_days:
            emav = self.data['Adj Close'].ewm(span=e, adjust=False).mean()
            self.data[f'EMA_{e}'] = emav
        return True
    
    def get_bollinger_bands(self, window):
        sma = self.data['Adj Close'].rolling(window=window).mean()
        std = self.data['Adj Close'].rolling(window=window).std()
        upper = sma + 2 * std
        lower = sma - 2 * std
        self.data[f'BB_U'] = upper
        self.data[f'BB_L'] = lower
        return True
    
    def crossover(self, input1, input2):
        crossover_date = []
        for i in range(1, len(self.data)):
            if self.data[input1].iloc[i] > self.data[input2].iloc[i] \
                and self.data[input1].iloc[i-1] <= self.data[input2].iloc[i-1]:
                crossover_date.append(self.data.index[i]) 
        return crossover_date
    
    def crossunder(self, input1, input2):
        crossunder_date = []
        for i in range(1, len(self.data)):
            if self.data[input1].iloc[i] < self.data[input2].iloc[i] \
                and self.data[input1].iloc[i-1] >= self.data[input2].iloc[i-1]:
                crossunder_date.append(self.data.index[i])
        return crossunder_date
    
    def make_plot(self):
        x = self.data.index
        y = self.data['Close']
        plt.plot(x, y)
        plt.plot(x, self.data['SMA_25'], label='SMA 25')
        plt.plot(x, self.data['SMA_50'], label='SMA 50')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title('Plot')
        actions = self.data.loc[self.data['action'].isin(['Buy', 'Sell'])]
        for index, row in actions.iterrows():
            if row['action'] == 'Buy':
                plt.annotate('Buy', (index, row['Close']), xytext=(-10, 10), 
                 textcoords='offset points', arrowprops=dict(arrowstyle='->', 
                 connectionstyle='arc3,rad=0'), color='green')
            elif row['action'] == 'Sell':
                plt.annotate('Sell', (index, row['Close']), xytext=(-10, -10), 
                 textcoords='offset points', arrowprops=dict(arrowstyle='->', 
                 connectionstyle='arc3,rad=0'), color='red')
        plt.legend()
        plt.show()
    
    
class Strategy():
    def __init__(self, qty, ticker, equity, start_date, end_date, interval):
        self.qty = qty
        self.stock = Stock(ticker, start_date=start_date, end_date=end_date, interval=interval)
        self.equity = equity
        self.cash = 0.00
        self.cash = self.equity
        self.profolio = []
        self.capital = 0.00
        self.log_file = open(f'app/GUI/logs/{ticker}_log.txt', "w")

    def conditions(self, co1, co2, cu1, cu2):
        self.crossover_date = self.stock.crossover(co1, co2)
        self.crossunder_date = self.stock.crossunder(cu1, cu2)
        
    def entry(self, qty, index):
        price = self.stock.data['Close'].iloc[index]
        self.capital = price * qty
        self.cash -= self.capital
    
    def exit(self, qty, index):
        price = self.stock.data['Close'].iloc[index]
        self.capital = price * qty
        self.cash += self.capital

    def show_balance(self):
        print(f"Equity: {self.equity}")
        print(f"Cash: {self.cash:.2f}")
        print(f'Gain/Loss: {(self.cash - self.equity)/self.equity:.2f}')

    def log_entry_exit(self, entry_exit):
        self.log_file.write(entry_exit + "\n")

    def log_action(self, action , qty, id, price):
        action_data = f'{action}: Qty={qty}, ID={id}, amount={self.capital:.2f}, \
                            price = {price:.2f}, balance = {self.cash:.2f}'
        self.log_entry_exit(action_data)

    def run(self, conditions):

        # Define the conditions for the strategy
        self.conditions(conditions[0], conditions[1], conditions[2], conditions[3])

        # mark the actions on the data
        self.stock.data['action'] = ''
        self.stock.data.loc[self.crossover_date, 'action'] = 'Buy'
        self.stock.data.loc[self.crossunder_date, 'action'] = 'Sell'

        # Check the column for the first non-empty cell
        # main condition: buy-sell pairs
        first_non_empty_cell = self.stock.data['action'].notnull().idxmax()
        if self.stock.data.loc[first_non_empty_cell, 'action'] == 'Sell':
            self.stock.data.loc[first_non_empty_cell, 'action'] = ''
        
        # Ensure the actions start with 'Sell' and alternate between 'Buy' and 'Sell'
        action = 'Buy'
        for i in range(len(self.stock.data)):
            if self.stock.data['action'].iloc[i] != None:
                this = self.stock.data['action'].iloc[i]
                if this == action: #if not duplicated
                    action = 'Sell' if action == 'Buy' else 'Buy'
                else:
                    self.stock.data['action'].iloc[i] = ''
            
        self.stock.output_csv()

        #cauculate the trades according to the actions column
        for i in range(len(self.stock.data)):
            if self.stock.data['action'].iloc[i] == 'Buy':
                self.entry(self.qty, i)
                self.log_action('BUY', self.qty, i, price=self.stock.data['Close'].iloc[i])
            elif self.stock.data['action'].iloc[i] == 'Sell':
                self.exit(self.qty, i)
                self.log_action('SELL', self.qty, i, price = self.stock.data['Close'].iloc[i])
        
        self.show_balance()



if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2024-04-23'
    interval = '1D'
    ticker = 'TQQQ'
    conditions = ['Close','SMA_25', 'Close', 'SMA_25']
    strategy = Strategy(100, ticker, 100000, start_date, end_date, interval)
    # strategy.stock.make_plot(strategy.stock.data.index, strategy.stock.data['Close'])
    strategy.run(conditions)
    strategy.stock.make_plot()