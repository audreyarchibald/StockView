#!/usr/bin/env python3
import argparse
from backtest import backtest

parser = argparse.ArgumentParser(description='Run simple moving average backtest.')
parser.add_argument('--data', default='data/sample_stock.csv', help='Path to CSV file')
parser.add_argument('--short', type=int, default=5, help='Short moving average window')
parser.add_argument('--long', type=int, default=20, help='Long moving average window')
parser.add_argument('--report', action='store_true', help='Print performance metrics')
args = parser.parse_args()

result = backtest(args.data, args.short, args.long)
print('Final equity:', result['equity'])
print('Number of trades:', result['num_trades'])
for t in result['trades']:
    print(f"{t[0]} {t[1]} {t[2]:.2f}")
if args.report:
    print('CAGR: {:.2%}'.format(result['cagr']))
    print('Sharpe Ratio: {:.2f}'.format(result['sharpe']))
    print('Max Drawdown: {:.2%}'.format(result['max_drawdown']))
    print('Sortino Ratio: {:.2f}'.format(result['sortino']))
