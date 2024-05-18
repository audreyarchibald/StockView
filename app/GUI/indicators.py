import wx
from StockAPI import StockAPI as sa

class IndicatorsData:
    def __init__(self):
        self.rsi = 70
        self.macd = 0.002
        self.sma = 50
        self.stochastic = 80
        self.mfi = 60
        self.bollinger_bands = 0.002
        self.adx = 30
        self.atr = 0.002
        self.ema = 50
        self.overall = 0.4

class Indicators(wx.Panel):
    def __init__(self, parent, ticker):
        super().__init__(parent)
        gridsizer = wx.GridSizer(6, 4, 1, 1)
        self.SetBackgroundColour(wx.BLACK)
        self.ticker = ticker

        #Define indicators
        self.rsi_label = wx.StaticText(self, label="RSI:", style=wx.ALIGN_CENTER)
        self.macd_label = wx.StaticText(self, label="MACD:", style=wx.ALIGN_CENTER)
        self.sma_label = wx.StaticText(self, label="SMA:", style=wx.ALIGN_CENTER)
        self.stocha_label = wx.StaticText(self, label="Stochastic:", style=wx.ALIGN_CENTER)
        self.mfi_label = wx.StaticText(self, label="MFI:", style=wx.ALIGN_CENTER)
        self.bollinger_label = wx.StaticText(self, label="Bollinger Bands:", style=wx.ALIGN_CENTER)
        self.adx_label = wx.StaticText(self, label="ADX:", style=wx.ALIGN_CENTER)
        self.atr_label = wx.StaticText(self, label="ATR:", style=wx.ALIGN_CENTER)
        self.ema_label = wx.StaticText(self, label="EMA:", style=wx.ALIGN_CENTER)
        self.overall_label = wx.StaticText(self, label="Overall:", style=wx.ALIGN_CENTER)

        self.rsi_text = wx.StaticText(self, label="")
        self.macd_text = wx.StaticText(self, label="")
        self.sma_text = wx.StaticText(self, label="")
        self.stocha_text = wx.StaticText(self, label="")
        self.mfi_text = wx.StaticText(self, label="")
        self.bollinger_text = wx.StaticText(self, label="")
        self.adx_text = wx.StaticText(self, label="")
        self.atr_text = wx.StaticText(self, label="")
        self.ema_text = wx.StaticText(self, label="")
        self.overall_text = wx.StaticText(self, label="")

        # Add the indicators to the sizer
        gridsizer.Add(self.rsi_label, 0, wx.EXPAND)
        gridsizer.Add(self.rsi_text, 0, wx.EXPAND)
        gridsizer.Add(self.macd_label, 0, wx.EXPAND)
        gridsizer.Add(self.macd_text, 0, wx.EXPAND)
        gridsizer.Add(self.sma_label, 0, wx.EXPAND)
        gridsizer.Add(self.sma_text, 0, wx.EXPAND)
        gridsizer.Add(self.stocha_label, 0, wx.EXPAND)
        gridsizer.Add(self.stocha_text, 0, wx.EXPAND)
        gridsizer.Add(self.mfi_label, 0, wx.EXPAND)
        gridsizer.Add(self.mfi_text, 0, wx.EXPAND)
        gridsizer.Add(self.bollinger_label, 0, wx.EXPAND)
        gridsizer.Add(self.bollinger_text, 0, wx.EXPAND)
        gridsizer.Add(self.adx_label, 0, wx.EXPAND)
        gridsizer.Add(self.adx_text, 0, wx.EXPAND)
        gridsizer.Add(self.atr_label, 0, wx.EXPAND)
        gridsizer.Add(self.atr_text, 0, wx.EXPAND)
        gridsizer.Add(self.ema_label, 0, wx.EXPAND)
        gridsizer.Add(self.ema_text, 0, wx.EXPAND)
        gridsizer.Add(self.overall_label, 0, wx.EXPAND)
        gridsizer.Add(self.overall_text, 0, wx.EXPAND)

        self.update()

        self.SetSizer(gridsizer)

    def update(self):
        data = sa.get_indicators(self.ticker)
        self.rsi_text.SetLabel(str(data.rsi))
        self.macd_text.SetLabel(str(data.macd))
        self.sma_text.SetLabel(str(data.sma))
        self.stocha_text.SetLabel(str(data.stocha))
        self.mfi_text.SetLabel(str(data.mfi))
        self.bollinger_text.SetLabel(str(data.bollinger))
        self.adx_text.SetLabel(str(data.adx))
        self.atr_text.SetLabel(str(data.atr))
        self.ema_text.SetLabel(str(data.ema))
        
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Indicators", size=(400, 300))
    Indicators(frame, 'AAPL')
    frame.Show()
    app.MainLoop()