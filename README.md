# StockView

This repository contains sample code for Project QuantumLeap, a platform for machine-learning driven stock pattern analysis and backtesting.

## Structure
- `backend/` – simple Python utilities and microservice skeleton
- `data/` – sample CSV data used in the examples

## Running the backtest example
```bash
python backend/cli.py --report
```
This will run a moving-average crossover backtest on the sample dataset and print basic performance statistics.

## Scanning for signals
```bash
python backend/scanner.py | head
```

## Running the lightweight server
```bash
python backend/server.py
```
Endpoints:
* `POST /backtest` – JSON body `{"data": "data/sample_stock.csv", "short": 5, "long": 20}`
* `GET  /scan` – query parameters `data`, `short`, `long`

## Training a candlestick pattern classifier
The `backend/ml.py` script now supports a small labeled dataset in `data/labeled_candles.csv` and offers two algorithms:

```bash
python backend/ml.py --algo logreg
```

Use `--algo knn` to try a k-nearest-neighbours model. The script splits the dataset into training and validation sets and prints accuracy, precision, recall and F1 score.

## Graphical User Interface
```bash
python backend/gui.py
```
A small Tkinter GUI lets you run the backtest or train the ML model with custom parameters.

## Quick start script
You can use `start.py` to launch various utilities:

```bash
# Start the HTTP server
python start.py --server

# Launch the GUI
python start.py --gui

# Run the CLI backtest
python start.py --backtest

# Train the ML model
python start.py --train
```
