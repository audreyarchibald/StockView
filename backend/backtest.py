import csv
import math
from statistics import mean, stdev

# Simple moving average crossover backtest using built-in libraries

def load_prices(path):
    """Return dates and closing prices from a CSV file."""
    dates, closes = [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(row['Date'])
            closes.append(float(row['Close']))
    return dates, closes

def sma(values, window):
    """Simple moving average."""
    res = []
    for i in range(len(values)):
        if i + 1 < window:
            res.append(None)
        else:
            res.append(mean(values[i + 1 - window : i + 1]))
    return res

def _metrics(prices):
    """Return daily returns and performance statistics."""
    if len(prices) < 2:
        return {
            'cagr': 0.0,
            'sharpe': 0.0,
            'max_drawdown': 0.0,
            'sortino': 0.0,
        }

    rets = []
    for i in range(1, len(prices)):
        rets.append(prices[i] / prices[i - 1] - 1)

    avg_ret = mean(rets)
    std_ret = stdev(rets) if len(rets) > 1 else 0
    downside = [r for r in rets if r < 0]
    if downside:
        sortino = avg_ret / math.sqrt(mean([d * d for d in downside])) * math.sqrt(252)
    else:
        sortino = 0.0

    equity = prices[-1] / prices[0]
    years = len(prices) / 252
    cagr = equity ** (1 / years) - 1 if years > 0 else 0
    sharpe = avg_ret / std_ret * math.sqrt(252) if std_ret != 0 else 0

    # Max drawdown
    peak = prices[0]
    drawdowns = []
    for p in prices:
        if p > peak:
            peak = p
        dd = (peak - p) / peak
        drawdowns.append(dd)
    max_drawdown = max(drawdowns) if drawdowns else 0

    return {
        'cagr': cagr,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'sortino': sortino,
    }


def backtest(path, short_window=5, long_window=20):
    dates, prices = load_prices(path)
    short_ma = sma(prices, short_window)
    long_ma = sma(prices, long_window)

    position = 0  # 1 for long, 0 for flat
    entry_price = 0
    trades = []
    equity = 1.0

    for i in range(len(prices)):
        if short_ma[i] is None or long_ma[i] is None:
            continue
        if position == 0 and short_ma[i] > long_ma[i]:
            position = 1
            entry_price = prices[i]
            trades.append((dates[i], 'BUY', entry_price))
        elif position == 1 and short_ma[i] < long_ma[i]:
            exit_price = prices[i]
            trades.append((dates[i], 'SELL', exit_price))
            equity *= exit_price / entry_price
            position = 0

    if position == 1:
        # close at last price
        exit_price = prices[-1]
        trades.append((dates[-1], 'SELL', exit_price))
        equity *= exit_price / entry_price

    metrics = _metrics(prices)
    result = {
        'equity': equity,
        'trades': trades,
        'num_trades': len(trades) // 2,
    }
    result.update(metrics)
    return result

if __name__ == '__main__':
    result = backtest('data/sample_stock.csv')
    print('Final equity:', result['equity'])
    print('Number of trades:', result['num_trades'])
    for t in result['trades']:
        print(t)
    print('CAGR: {:.2%}'.format(result['cagr']))
    print('Sharpe Ratio: {:.2f}'.format(result['sharpe']))
    print('Max Drawdown: {:.2%}'.format(result['max_drawdown']))
    print('Sortino Ratio: {:.2f}'.format(result['sortino']))
