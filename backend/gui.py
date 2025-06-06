import tkinter as tk
from tkinter import messagebox

from backtest import backtest
from ml import train


def run_backtest():
    data = data_var.get() or 'data/sample_stock.csv'
    short = int(short_var.get() or 5)
    long = int(long_var.get() or 20)
    result = backtest(data, short, long)
    output = (
        f"Equity: {result['equity']:.2f}\n"
        f"Trades: {result['num_trades']}\n"
        f"CAGR: {result['cagr']:.2%}\n"
        f"Sharpe: {result['sharpe']:.2f}\n"
        f"Max DD: {result['max_drawdown']:.2%}\n"
        f"Sortino: {result['sortino']:.2f}"
    )
    messagebox.showinfo('Backtest Result', output)


def run_training():
    data = data_var.get() or 'data/sample_stock.csv'
    short = int(short_var.get() or 5)
    long = int(long_var.get() or 20)
    result = train(data, short, long)
    output = f"Training accuracy: {result['accuracy']:.2%}"
    messagebox.showinfo('Training Result', output)


root = tk.Tk()
root.title('StockView')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Data path
tk.Label(frame, text='Data Path:').grid(row=0, column=0, sticky='e')
data_var = tk.StringVar(value='data/sample_stock.csv')
tk.Entry(frame, textvariable=data_var, width=30).grid(row=0, column=1)

# Short window
tk.Label(frame, text='Short MA:').grid(row=1, column=0, sticky='e')
short_var = tk.StringVar(value='5')
tk.Entry(frame, textvariable=short_var, width=10).grid(row=1, column=1, sticky='w')

# Long window
tk.Label(frame, text='Long MA:').grid(row=2, column=0, sticky='e')
long_var = tk.StringVar(value='20')
tk.Entry(frame, textvariable=long_var, width=10).grid(row=2, column=1, sticky='w')

# Buttons
tk.Button(frame, text='Run Backtest', command=run_backtest).grid(row=3, column=0, pady=5)
tk.Button(frame, text='Train Model', command=run_training).grid(row=3, column=1, pady=5)

root.mainloop()
