import numpy as np

class SGDClassifier(BaseEstimator):
    def __init__(self, C, eta=10**(-3), n_iter=10):
        self.eta = eta
        self.n_iter = n_iter
        self.C = C
        self.loss_ = []
        self.weight_ = []

    def fit(self, X, y):
        X = np.hstack([np.ones((len(X), 1)), X])
        w = np.zeros(X.shape[1])

        for i in tqdm.tqdm_notebook(range(self.n_iter)):
            w = w + self.eta * (self.C * y[i] * sigma(-y[i] * np.dot(X[i],  w)) * X[i] - kronker(w))

            self.weight_.append(w)
            self.loss_.append(log_loss(y, [sign(i) for i in np.dot(X, w)]))

        self.loss_weight_data = {'loss' : self.loss_, 'weight' : self.weight_}
        self.loss_weight = pd.DataFrame(self.loss_weight_data)
        self.loss_weight.sort_values(by='loss', inplace=True)
        self.w_ = self.loss_weight['weight'].values[0]

        return self

    def predict(self, X):
        X = np.hstack([np.ones((len(X), 1)), X])
        prediction = [sign(a) for a in np.dot(X , self.w_)]

        return prediction

    def predict_proba(self, X):
        X = np.hstack([np.ones((len(X), 1)), X])
        prediction = (np.dot(X, self.w_))
        prob = [sigma(i) for i in prediction]

        return prob
