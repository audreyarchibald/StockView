import wx
from StockAPI import StockAPI as sa

class WatchList(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.stockapi = sa()
        self.portfolio_data = self.stockapi.get_watchlist_data()
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Display portfolio overview
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, "Stock")
        self.list_ctrl.InsertColumn(1, "Current Price")
        self.list_ctrl.InsertColumn(2, "Change (%)")
        self.list_ctrl.InsertColumn(3, "Volume")  # Add volume column
        
        for i, data in enumerate(self.portfolio_data):
            index = self.list_ctrl.InsertItem(i, data[0])
            self.list_ctrl.SetItem(index, 1, str(round(data[1], 2)))
            self.list_ctrl.SetItem(index, 2, str(round(data[2], 2)))
            self.list_ctrl.SetItem(index, 3, str(data[3]))  # Set volume value
            
            if data[2] < 0:
                self.list_ctrl.SetItemTextColour(index, wx.RED)
            elif data[2] > 0:
                self.list_ctrl.SetItemTextColour(index, wx.GREEN)
        
        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbox)

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Indicators", size=(400, 300))
    WatchList(frame)
    frame.Show()
    app.MainLoop()
