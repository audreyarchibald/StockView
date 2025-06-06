import argparse
from backtest import load_prices, sma


def scan(path, short_window=5, long_window=20):
    dates, prices = load_prices(path)
    short_ma = sma(prices, short_window)
    long_ma = sma(prices, long_window)
    signals = []
    for i in range(len(prices)):
        if i == 0 or short_ma[i] is None or long_ma[i] is None:
            continue
        if short_ma[i-1] is None or long_ma[i-1] is None:
            continue
        if short_ma[i] > long_ma[i] and short_ma[i-1] <= long_ma[i-1]:
            signals.append((dates[i], 'BULLISH'))
        elif short_ma[i] < long_ma[i] and short_ma[i-1] >= long_ma[i-1]:
            signals.append((dates[i], 'BEARISH'))
    return signals


def main():
    parser = argparse.ArgumentParser(description='Scan for moving average crossovers.')
    parser.add_argument('--data', default='data/sample_stock.csv')
    parser.add_argument('--short', type=int, default=5)
    parser.add_argument('--long', type=int, default=20)
    args = parser.parse_args()

    for date, sig in scan(args.data, args.short, args.long):
        print(date, sig)


if __name__ == '__main__':
    main()
