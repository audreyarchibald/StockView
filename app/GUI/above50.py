import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from StockAPI import StockAPI
import threading

class Above50SMAData():
    def __init__(self):
        self.number_in_days = 0
        self.numbers = 0

class Above50SMA(wx.Panel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.stock = StockAPI()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.data = Above50SMAData()

        self.data.number_in_days, self.total = self.stock.stocks_above_50sma()
        self.data.numbers = list(range(1,len(self.data.number_in_days)+1))
        # Create a matplotlib figure
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        
        # Create some sample data
        self.axes.plot(self.data.numbers, self.data.number_in_days[::-1])
        
        # Create a FigureCanvas to display the figure
        self.canvas = FigureCanvas(self, 0, self.figure)
        self.canvas.SetMinSize((400, 200))  # Set the minimum size of the canvas
        self.canvas.SetMaxSize((500, 500))  # Set the maximum size of the canvas

        self.sizer.Add(self.canvas, 1, wx.ALL, 5)
        self.SetSizer(self.sizer)

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="num50", size=(400, 300))
    Above50SMA(frame, "num50")
    frame.Show()
    app.MainLoop()