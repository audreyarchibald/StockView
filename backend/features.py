import csv


def extract_candlestick_features(row):
    """Return candlestick features for a single row."""
    open_p = float(row['Open'])
    high = float(row['High'])
    low = float(row['Low'])
    close = float(row['Close'])

    body = close - open_p
    body_pct = body / open_p if open_p != 0 else 0
    upper_shadow = high - max(open_p, close)
    upper_shadow_pct = upper_shadow / open_p if open_p != 0 else 0
    lower_shadow = min(open_p, close) - low
    lower_shadow_pct = lower_shadow / open_p if open_p != 0 else 0
    range_pct = (high - low) / open_p if open_p != 0 else 0
    return [body_pct, upper_shadow_pct, lower_shadow_pct, range_pct]


def load_labeled_dataset(path):
    """Load labeled candlestick data and return X, y."""
    X = []
    y = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append(extract_candlestick_features(row))
            y.append(row.get('Pattern', ''))
    return X, y
