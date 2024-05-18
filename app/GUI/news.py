import wx
import newsSTM

class NewsApp(wx.Panel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.news_data = newsSTM.get_sentiments("AAPL")

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.BLACK)

        self.ticker_text = wx.StaticText(self, label="Ticker: ")
        self.ticker_text.SetForegroundColour(wx.WHITE)
        self.ticker = wx.TextCtrl(self, value='AAPL', style=wx.TE_PROCESS_ENTER)
        self.ticker.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.button = wx.Button(self, label="Enter")
        self.button.Bind(wx.EVT_BUTTON, self.on_enter)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.ticker_text, 0, wx.EXPAND | wx.ALL   , 5)
        hbox.Add(self.ticker, 0, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.button, 0, wx.EXPAND | wx.ALL, 5)

        self.vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        self.scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll.SetScrollRate(0, 20)
        self.scroll.SetBackgroundColour(wx.BLACK)
        self.scroll_box = wx.BoxSizer(wx.VERTICAL)
        self.scroll.SetSizer(self.scroll_box)
        
        # Display the news feed
        for r in self.news_data:
            score = f'[{r[0]}] {r[1]}'
            headline_text = wx.StaticText(self.scroll, label=score)
            if r[0] < 0:
                headline_text.SetForegroundColour(wx.RED)
            elif r[0] > 0:
                headline_text.SetForegroundColour(wx.GREEN)
            headline_text.Wrap(450)  # Set the maximum width for the text
            self.scroll_box.Add(headline_text, 0, wx.ALL, 5)
        self.scroll.SetSizer(self.scroll_box)
        self.vbox.Add(self.scroll, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.vbox)

    def on_enter(self, event):
        self.news_data.clear()
        self.news_data = newsSTM.get_sentiments(self.ticker.GetValue())
        
        # Delete everything in scroll_box
        self.scroll_box.Clear(True)
        for r in self.news_data:
            score = f'[{r[0]}] {r[1]}'
            headline_text = wx.StaticText(self.scroll, label=score)
            if r[0] < 0:
                headline_text.SetForegroundColour(wx.RED)
            elif r[0] > 0:
                headline_text.SetForegroundColour(wx.GREEN)
            headline_text.Wrap(450)  # Set the maximum width for the text
            self.scroll_box.Add(headline_text, 0, wx.ALL, 5)
            # self.scroll_box.Add(wx.StaticLine(self.scroll), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        
        self.scroll.SetSizer(self.scroll_box)
        self.scroll_box.FitInside(self.scroll)
        self.Refresh()
        
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="News Feed", size=(700, 300))
    NewsApp(frame, "News Feed")
    frame.Show()
    app.MainLoop()