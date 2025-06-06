import csv
import math
from random import random

from backtest import load_prices, sma


def _prepare_dataset(path, short_window, long_window):
    """Return feature matrix X and target vector y for ML training."""
    dates, prices = load_prices(path)
    short_ma = sma(prices, short_window)
    long_ma = sma(prices, long_window)
    X, y = [], []
    for i in range(1, len(prices) - 1):
        if short_ma[i] is None or long_ma[i] is None:
            continue
        # Features: moving average diff and daily return
        ma_diff = short_ma[i] - long_ma[i]
        ret = prices[i] / prices[i - 1] - 1
        X.append([ma_diff, ret])
        future_ret = prices[i + 1] / prices[i] - 1
        y.append(1 if future_ret > 0 else 0)
    return X, y


def train_logistic_regression(X, y, lr=0.1, epochs=1000):
    """Train a simple logistic regression model using SGD."""
    if not X:
        raise ValueError("Empty dataset")
    n_features = len(X[0])
    weights = [random() * 0.01 for _ in range(n_features)]
    bias = 0.0
    for _ in range(epochs):
        for xi, yi in zip(X, y):
            z = bias + sum(w * x for w, x in zip(weights, xi))
            pred = 1 / (1 + math.exp(-z))
            error = yi - pred
            bias += lr * error
            for i in range(n_features):
                weights[i] += lr * error * xi[i]
    return weights, bias


def predict(X, weights, bias):
    preds = []
    for xi in X:
        z = bias + sum(w * x for w, x in zip(weights, xi))
        p = 1 / (1 + math.exp(-z))
        preds.append(1 if p >= 0.5 else 0)
    return preds


def train(path='data/sample_stock.csv', short_window=5, long_window=20):
    X, y = _prepare_dataset(path, short_window, long_window)
    weights, bias = train_logistic_regression(X, y)
    preds = predict(X, weights, bias)
    correct = sum(p == t for p, t in zip(preds, y))
    accuracy = correct / len(y) if y else 0
    return {
        'weights': weights,
        'bias': bias,
        'accuracy': accuracy,
    }


if __name__ == '__main__':
    result = train()
    print('Training accuracy: {:.2%}'.format(result['accuracy']))
