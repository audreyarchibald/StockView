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

## Training a simple ML model
```bash
python backend/ml.py
```
This trains a logistic regression classifier (implemented with only the Python standard library) on the sample dataset and prints the training accuracy.

## Graphical User Interface
```bash
python backend/gui.py
```
A small Tkinter GUI lets you run the backtest or train the ML model with custom parameters.
