import csv
import math
from random import random, shuffle

from backtest import load_prices, sma
from features import load_labeled_dataset


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


def train_multiclass_logistic_regression(X, y, lr=0.1, epochs=1000):
    """Train softmax regression for multi-class classification."""
    if not X:
        raise ValueError("Empty dataset")
    classes = sorted(set(y))
    class_to_idx = {c: i for i, c in enumerate(classes)}
    n_classes = len(classes)
    n_features = len(X[0])
    weights = [[random() * 0.01 for _ in range(n_features)] for _ in range(n_classes)]
    biases = [0.0 for _ in range(n_classes)]

    for _ in range(epochs):
        for xi, yi in zip(X, y):
            idx = class_to_idx[yi]
            scores = [biases[j] + sum(w * x for w, x in zip(weights[j], xi)) for j in range(n_classes)]
            max_s = max(scores)
            exp_scores = [math.exp(s - max_s) for s in scores]
            sum_exp = sum(exp_scores)
            probs = [e / sum_exp for e in exp_scores]
            for j in range(n_classes):
                error = (1 if j == idx else 0) - probs[j]
                biases[j] += lr * error
                for k in range(n_features):
                    weights[j][k] += lr * error * xi[k]
    return weights, biases, class_to_idx


def predict(X, weights, bias):
    preds = []
    for xi in X:
        z = bias + sum(w * x for w, x in zip(weights, xi))
        p = 1 / (1 + math.exp(-z))
        preds.append(1 if p >= 0.5 else 0)
    return preds


def predict_multiclass(X, weights, biases, class_to_idx):
    idx_to_class = {i: c for c, i in class_to_idx.items()}
    preds = []
    n_classes = len(weights)
    for xi in X:
        scores = [biases[j] + sum(w * x for w, x in zip(weights[j], xi)) for j in range(n_classes)]
        max_s = max(scores)
        exp_scores = [math.exp(s - max_s) for s in scores]
        sum_exp = sum(exp_scores)
        probs = [e / sum_exp for e in exp_scores]
        idx = probs.index(max(probs))
        preds.append(idx_to_class[idx])
    return preds


def train_knn(X, y, k=3):
    return {
        'X': X,
        'y': y,
        'k': k,
    }


def predict_knn(model, X):
    X_train = model['X']
    y_train = model['y']
    k = model['k']
    preds = []
    for xi in X:
        distances = [sum((a - b) ** 2 for a, b in zip(xi, xt)) for xt in X_train]
        nearest = sorted(range(len(distances)), key=lambda i: distances[i])[:k]
        votes = [y_train[i] for i in nearest]
        label = max(set(votes), key=votes.count)
        preds.append(label)
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


def _split_dataset(X, y, ratio=0.8):
    combined = list(zip(X, y))
    shuffle(combined)
    split = int(len(combined) * ratio)
    train = combined[:split]
    val = combined[split:]
    if train:
        X_train, y_train = zip(*train)
    else:
        X_train, y_train = [], []
    if val:
        X_val, y_val = zip(*val)
    else:
        X_val, y_val = [], []
    return list(X_train), list(y_train), list(X_val), list(y_val)


def _precision_recall_f1(y_true, preds):
    classes = set(y_true)
    tp = fp = fn = 0
    for cls in classes:
        for p, t in zip(preds, y_true):
            if p == cls and t == cls:
                tp += 1
            elif p == cls and t != cls:
                fp += 1
            elif p != cls and t == cls:
                fn += 1
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return precision, recall, f1


def train_pattern_classifier(path='data/labeled_candles.csv', algorithm='logreg', split_ratio=0.8):
    X, y = load_labeled_dataset(path)
    X_train, y_train, X_val, y_val = _split_dataset(X, y, ratio=split_ratio)

    if algorithm == 'knn':
        model = train_knn(X_train, y_train, k=3)
        preds = predict_knn(model, X_val)
    else:
        weights, biases, class_to_idx = train_multiclass_logistic_regression(X_train, y_train)
        preds = predict_multiclass(X_val, weights, biases, class_to_idx)

    accuracy = sum(p == t for p, t in zip(preds, y_val)) / len(y_val) if y_val else 0
    precision, recall, f1 = _precision_recall_f1(y_val, preds)
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Train ML models for candlestick patterns')
    parser.add_argument('--data', default='data/labeled_candles.csv', help='Path to labeled CSV file')
    parser.add_argument('--algo', choices=['logreg', 'knn'], default='logreg', help='Algorithm to use')
    parser.add_argument('--split', type=float, default=0.8, help='Training split ratio')
    args = parser.parse_args()

    result = train_pattern_classifier(path=args.data, algorithm=args.algo, split_ratio=args.split)
    print('Validation accuracy: {:.2%}'.format(result['accuracy']))
    print('Precision: {:.2%}'.format(result['precision']))
    print('Recall: {:.2%}'.format(result['recall']))
    print('F1 Score: {:.2%}'.format(result['f1']))
