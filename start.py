import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Start StockView utilities')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--server', action='store_true', help='Start HTTP server')
    group.add_argument('--gui', action='store_true', help='Launch Tkinter GUI')
    group.add_argument('--backtest', action='store_true', help='Run CLI backtest')
    group.add_argument('--train', action='store_true', help='Run ML training')
    args = parser.parse_args()

    script = None
    if args.server:
        script = 'backend/server.py'
    elif args.gui:
        script = 'backend/gui.py'
    elif args.backtest:
        script = 'backend/cli.py'
    elif args.train:
        script = 'backend/ml.py'

    if script:
        subprocess.run([sys.executable, script])
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
