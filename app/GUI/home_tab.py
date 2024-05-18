import wx
import threading
from news import NewsApp as news
from watchlist import WatchList as wl
from indicators import Indicators as ind
from above50 import Above50SMA as above50
from backtester_box import Backtester

class HomeTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.lock = threading.Lock()
        self.gridsizer = wx.GridSizer(2, 3, 1, 1)
        
        # define the boxes
        self.news = news(self, "news")
        self.wl = wl(self)
        self.ind = ind(self, "AAPL")
        self.above50 = above50(self, "above 50 SMA")
        self.backtest = Backtester(self, "Backtester")

        # Add the boxes to the sizer
        self.gridsizer.Add(self.wl, 0, wx.EXPAND)
        self.gridsizer.Add(self.ind, 0, wx.EXPAND)
        self.gridsizer.Add(self.news, 0, wx.EXPAND)
        self.gridsizer.Add(self.above50, 0, wx.EXPAND)
        self.gridsizer.Add(self.backtest, 0, wx.EXPAND)

        self.ind.ticker = self.news.ticker.GetValue()
        self.news.button.Bind(wx.EVT_BUTTON, self.on_enter)
        self.news.ticker.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        
        self.ind.ticker = self.wl.list_ctrl.GetItemText(0)
        self.wl.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        self.SetSizer(self.gridsizer)

    def on_item_selected(self, event):
        selected_index = event.GetIndex()
        selected_data = self.wl.portfolio_data[selected_index]
        self.ind.ticker = selected_data[0]
        self.backtest.ticker_text.SetValue(selected_data[0])
        self.ind.update()
        # self.backtest.on_enter(event)
        self.news.ticker.SetValue(selected_data[0])
        self.news.on_enter(event) 

    def on_enter(self, event):
        self.ind.ticker = self.news.ticker.GetValue()
        self.backtest.ticker_text.SetValue(self.news.ticker.GetValue())
        self.ind.update()
        self.news.on_enter(event)
        
if __name__ == "__main__":
    # Create a wxPython app
    app = wx.App()
    # Create a frame and a notebook
    frame = wx.Frame(None, title="Stock 2.0")
    # frame.SetIcon(wx.Icon("icon.icn"))
    home_tab = HomeTab(frame)
    frame.Maximize()
    frame.Show()
    app.MainLoop()