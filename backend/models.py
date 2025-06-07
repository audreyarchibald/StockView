"""Simple ML models implemented without external dependencies."""

import math
import random

# Logistic Regression using SGD (same as in ml.py but packaged in a function)

def train_logistic_regression(X, y, lr=0.1, epochs=1000):
    if not X:
        raise ValueError("Empty dataset")
    n_features = len(X[0])
    weights = [random.random() * 0.01 for _ in range(n_features)]
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

def predict_logistic(X, weights, bias):
    preds = []
    for xi in X:
        z = bias + sum(w * x for w, x in zip(weights, xi))
        p = 1 / (1 + math.exp(-z))
        preds.append(1 if p >= 0.5 else 0)
    return preds


# Decision stump used for ensemble methods
class DecisionStump:
    def __init__(self):
        self.feature = 0
        self.threshold = 0.0
        self.invert = False

    def fit(self, X, y, sample_weight=None):
        n_samples = len(X)
        if sample_weight is None:
            sample_weight = [1.0 / n_samples] * n_samples
        n_features = len(X[0])
        best_err = float('inf')
        for j in range(n_features):
            values = sorted(set(x[j] for x in X))
            for thr in values:
                for inv in (False, True):
                    err = 0.0
                    for xi, yi, w in zip(X, y, sample_weight):
                        pred = 1 if (xi[j] >= thr) != inv else 0
                        if pred != yi:
                            err += w
                    if err < best_err:
                        best_err = err
                        self.feature = j
                        self.threshold = thr
                        self.invert = inv

    def predict_single(self, xi):
        pred = 1 if (xi[self.feature] >= self.threshold) != self.invert else 0
        return pred

    def predict(self, X):
        return [self.predict_single(xi) for xi in X]


class RandomForestClassifier:
    """Extremely small random forest using decision stumps."""

    def __init__(self, n_estimators=10):
        self.n_estimators = n_estimators
        self.trees = []

    def fit(self, X, y):
        n_samples = len(X)
        self.trees = []
        for _ in range(self.n_estimators):
            indices = [random.randrange(n_samples) for _ in range(n_samples)]
            X_boot = [X[i] for i in indices]
            y_boot = [y[i] for i in indices]
            stump = DecisionStump()
            stump.fit(X_boot, y_boot)
            self.trees.append(stump)

    def predict(self, X):
        preds = []
        for xi in X:
            votes = sum(tree.predict_single(xi) for tree in self.trees)
            preds.append(1 if votes >= len(self.trees) / 2 else 0)
        return preds


class AdaBoostClassifier:
    """Very small AdaBoost using decision stumps."""

    def __init__(self, n_estimators=10):
        self.n_estimators = n_estimators
        self.stumps = []
        self.stump_weights = []

    def fit(self, X, y):
        n_samples = len(X)
        weights = [1.0 / n_samples] * n_samples
        self.stumps = []
        self.stump_weights = []
        for _ in range(self.n_estimators):
            stump = DecisionStump()
            stump.fit(X, y, sample_weight=weights)
            preds = stump.predict(X)
            err = sum(w for p, yi, w in zip(preds, y, weights) if p != yi)
            err = max(err, 1e-10)
            alpha = 0.5 * math.log((1 - err) / err)
            # Update weights
            for i in range(n_samples):
                if preds[i] == y[i]:
                    weights[i] *= math.exp(-alpha)
                else:
                    weights[i] *= math.exp(alpha)
            # Normalize
            total = sum(weights)
            weights = [w / total for w in weights]
            self.stumps.append(stump)
            self.stump_weights.append(alpha)

    def predict(self, X):
        preds = []
        for xi in X:
            score = 0.0
            for stump, alpha in zip(self.stumps, self.stump_weights):
                pred = 1 if stump.predict_single(xi) == 1 else -1
                score += alpha * pred
            preds.append(1 if score >= 0 else 0)
        return preds


def accuracy_score(y_true, y_pred):
    correct = sum(1 for p, t in zip(y_pred, y_true) if p == t)
    return correct / len(y_true) if y_true else 0


def f1_score(y_true, y_pred):
    tp = sum(1 for p, t in zip(y_pred, y_true) if p == 1 and t == 1)
    fp = sum(1 for p, t in zip(y_pred, y_true) if p == 1 and t == 0)
    fn = sum(1 for p, t in zip(y_pred, y_true) if p == 0 and t == 1)
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn) if tp + fn else 0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0
