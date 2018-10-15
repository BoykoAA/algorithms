import numpy as np

class SGDRegressor(BaseEstimator):
    def __init__(self, eta=10**-3, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter
        self.mse_ = []
        self.weights_ = []

    def fit(self, X, y):
        X = np.hstack([np.ones((len(X), 1)), X])
        w = np.zeros(X.shape[1])

        for i in range(self.n_iter):
            w = w + self.eta * (y[i] - np.dot(X[i], w)) * X[i]

            self.mse_.append(mean_squared_error(y, np.dot(X, w)))
            self.weights_.append(w)

        self.w_ = sorted(list(zip(self.mse_, self.weights_)))[0][1]

        return self

    def predict(self, X):
        X = np.hstack([np.ones((len(X), 1)), X])
        return np.dot(X, self.w_)
