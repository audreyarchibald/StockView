import argparse

from backtest import load_prices, sma
from models import (
    train_logistic_regression,
    predict_logistic,
    RandomForestClassifier,
    AdaBoostClassifier,
    accuracy_score,
    f1_score,
)


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


def train(path='data/sample_stock.csv', short_window=5, long_window=20):
    """Backwards compatible training function (logistic regression)."""
    X, y = _prepare_dataset(path, short_window, long_window)
    weights, bias = train_logistic_regression(X, y)
    preds = predict_logistic(X, weights, bias)
    accuracy = accuracy_score(y, preds)
    return {
        'weights': weights,
        'bias': bias,
        'accuracy': accuracy,
    }


def evaluate_models(path, short_window, long_window, model_names):
    X, y = _prepare_dataset(path, short_window, long_window)
    split = int(0.8 * len(X))
    X_train, y_train = X[:split], y[:split]
    X_val, y_val = X[split:], y[split:]
    results = {}
    for name in model_names:
        if name == 'logistic':
            weights, bias = train_logistic_regression(X_train, y_train)
            preds = predict_logistic(X_val, weights, bias)
        elif name == 'forest':
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            preds = model.predict(X_val)
        elif name == 'boost':
            model = AdaBoostClassifier()
            model.fit(X_train, y_train)
            preds = model.predict(X_val)
        else:
            raise ValueError(f'Unknown model: {name}')
        acc = accuracy_score(y_val, preds)
        f1 = f1_score(y_val, preds)
        results[name] = {'accuracy': acc, 'f1': f1}
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train and evaluate ML models.')
    parser.add_argument('--data', default='data/sample_stock.csv', help='Path to CSV file')
    parser.add_argument('--short', type=int, default=5, help='Short moving average window')
    parser.add_argument('--long', type=int, default=20, help='Long moving average window')
    parser.add_argument('--model', choices=['logistic', 'forest', 'boost', 'all'], default='logistic', help='Model to train')
    args = parser.parse_args()

    models = ['logistic', 'forest', 'boost'] if args.model == 'all' else [args.model]
    results = evaluate_models(args.data, args.short, args.long, models)
    for name in models:
        res = results[name]
        print(f"{name.capitalize()} - Accuracy: {res['accuracy']:.2%} F1: {res['f1']:.2f}")
