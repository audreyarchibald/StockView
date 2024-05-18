import wx
import wx.adv
import backtester as bt
import subprocess

class Backtester(wx.Panel):
    def __init__(self, parent, title):
        super().__init__(parent)
        gridsizer = wx.GridSizer(7, 4, 5, 5)
        # self.SetBackgroundColour(wx.BLACK)

        #Define labels and text
        self.ticker_label = wx.StaticText(self, label="Ticker:")
        self.start_date_label = wx.StaticText(self, label="Start date:")
        self.end_date_label = wx.StaticText(self, label="End date:")
        self.interval_label = wx.StaticText(self, label="Interval:")
        # self.sma_label = wx.StaticText(self, label="SMA days:")
        self.equity_label = wx.StaticText(self, label="Equity:")
        self.balance_label = wx.StaticText(self, label="Balance:")
        self.gain_label = wx.StaticText(self, label="Gain:")
        self.co1_label = wx.StaticText(self, label="param1:")
        self.co2_label = wx.StaticText(self, label="param2:")
        self.cu1_label = wx.StaticText(self, label="param3:")
        self.cu2_label = wx.StaticText(self, label="param4:")

        self.ticker_text = wx.TextCtrl(self, value='')
        self.start_date_text = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DEFAULT)
        self.end_date_text = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DEFAULT)
        self.interval_text = wx.TextCtrl(self, value='1d')
        # self.sma_text = wx.TextCtrl(self, value='50')
        self.equity_text = wx.TextCtrl(self, value='100000')
        self.balance_text = wx.TextCtrl(self, value='')
        self.gain_text = wx.TextCtrl(self, value='')
        self.co1_text = wx.TextCtrl(self, value='Close')
        self.co2_text = wx.TextCtrl(self, value='SMA_50')
        self.cu1_text = wx.TextCtrl(self, value='Close')
        self.cu2_text = wx.TextCtrl(self, value='SMA_50')
        
        self.enter_button = wx.Button(self, label="Enter")
        self.enter_button.Bind(wx.EVT_BUTTON, self.on_enter)

        # Add the indicators to the sizer
        gridsizer.Add(self.ticker_label, 0, wx.EXPAND)
        gridsizer.Add(self.ticker_text, 0, wx.EXPAND)
        gridsizer.Add(self.start_date_label, 0, wx.EXPAND)
        gridsizer.Add(self.start_date_text, 0, wx.EXPAND)
        gridsizer.Add(self.end_date_label, 0, wx.EXPAND)
        gridsizer.Add(self.end_date_text, 0, wx.EXPAND)
        gridsizer.Add(self.interval_label, 0, wx.EXPAND)
        gridsizer.Add(self.interval_text, 0, wx.EXPAND)
        gridsizer.Add(self.equity_label, 0, wx.EXPAND)
        gridsizer.Add(self.equity_text, 0, wx.EXPAND)
        # gridsizer.Add(self.sma_label, 0, wx.EXPAND)
        # gridsizer.Add(self.sma_text, 0, wx.EXPAND)
        gridsizer.Add(self.co1_label, 0, wx.EXPAND)
        gridsizer.Add(self.co1_text, 0, wx.EXPAND)
        gridsizer.Add(self.co2_label, 0, wx.EXPAND)
        gridsizer.Add(self.co2_text, 0, wx.EXPAND)
        gridsizer.Add(self.cu1_label, 0, wx.EXPAND)
        gridsizer.Add(self.cu1_text, 0, wx.EXPAND)
        gridsizer.Add(self.cu2_label, 0, wx.EXPAND)
        gridsizer.Add(self.cu2_text, 0, wx.EXPAND)
        gridsizer.Add(self.balance_label, 0, wx.EXPAND)
        gridsizer.Add(self.balance_text, 0, wx.EXPAND)
        gridsizer.Add(self.gain_label, 0, wx.EXPAND)
        gridsizer.Add(self.gain_text, 0, wx.EXPAND)
        gridsizer.Add(self.enter_button, 0, wx.EXPAND)
        
        self.box_label = title
        self.box = wx.StaticBox(self, label=self.box_label)
        # self.box.SetForegroundColour(wx.WHITE)
        box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        box_sizer.Add(gridsizer, 0, wx.EXPAND)


        self.SetSizer(box_sizer)

    def on_enter(self, event):
        ticker = self.ticker_text.GetValue()
        start_date = self.start_date_text.GetValue().FormatISODate()
        end_date = self.end_date_text.GetValue().FormatISODate()
        interval = self.interval_text.GetValue()
        # sma_days = int(self.sma_text.GetValue())
        equity = float(self.equity_text.GetValue())
        co1 = self.co1_text.GetValue()
        co2 = self.co2_text.GetValue()
        cu1 = self.cu1_text.GetValue()
        cu2 = self.cu2_text.GetValue()
        conditions = [co1, co2, cu1, cu2]

        strategy = bt.Strategy(100, ticker, equity, start_date, end_date, interval)
        strategy.run(conditions)
        
        balance = int(strategy.cash)
        gain = round(((strategy.cash - strategy.equity)/strategy.equity), 3)
        self.balance_text.SetValue(str(balance))
        self.gain_text.SetValue(str(gain))
        self.Refresh()

        # Open the log file in a text editor
        log_file_path = f'app/GUI/logs/{ticker}_log.txt'  
        try:
            subprocess.Popen(["open", "-t", log_file_path])
        except Exception as e:
            print(f"Failed to open log file: {e}")

        strategy.stock.make_plot()
        
        
        
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Backtester", size=(800, 300))
    Backtester(frame, "Backtester")
    frame.Show()
    app.MainLoop()