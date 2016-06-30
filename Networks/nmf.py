import numpy as np
from sys import stderr

class NMF:
    
    """
    Fit a matrix factorization model for a matrix X with missing values.

    Typically used as a recommendation system.

    such that
        X = W H.T + E 
    where
        X is of shape (m, n)    - data matrix
        W is of shape (m, rank) - approximated row space
        H is of shape (n, rank) - approximated column space
        E is of shape (m, n)    - residual (error) matrix
    """

    ALG_GD = "gd"
    ALG_PGD = "pgd"
    ALG_MU  = "mu"

    def __init__(self, rank=10, max_iter=100, eta=0.01, algorithm="gd",
                 compute_error=True, verbose=True):
        """
        :param rank: Rank of the matrices of the model.
        :param max_iter: Maximum nuber of SGD iterations.
        :param eta: SGD learning rate.
        :param projected: Use projected gradient descent.
        """
        self.rank = rank
        self.max_iter = max_iter
        self.eta = eta
        self.algorithm = algorithm
        self.compute_error = compute_error
        self.verbose = verbose
        assert self.algorithm in {self.ALG_GD, self.ALG_PGD, self.ALG_MU}
    
    
    def fit(self, X):
        """
        Fit model parameters W, H.
        Imporant: changed to nan variables.

        :param X: 
            Non-negative data matrix of shape (m, n)
            Unknown values are assumed to take the value of zero (0).
        """
        I = 1.0 * (X != 0)

        W = np.random.rand(X.shape[0], self.rank)
        H = np.random.rand(X.shape[1], self.rank)

        # Errors
        self.error = np.zeros((self.max_iter,))

        for t in range(self.max_iter):

            # Gradient-descent based
            if self.algorithm in [self.ALG_GD, self.ALG_PGD]:
                dW =  ((X - W.dot(H.T)) * I).dot(H)
                W  =  W + self.eta * dW
                if self.algorithm == self.ALG_PGD:
                    W[np.where(W < 0)] = 0

                dH =  ((X - W.dot(H.T)) * I).T.dot(W)
                H  = H + self.eta * dH

                if self.algorithm == self.ALG_PGD:
                    H[np.where(H < 0)] = 0

            # Multiplicative-update based
            if self.algorithm == self.ALG_MU:
                XI = X

                XIH    = XI.dot(H)
                WHTIH  = (W.dot(H.T) * I).dot(H)
                W      = W * np.nan_to_num(XIH / WHTIH)

                WTXI   = W.T.dot(XI)
                WTWHTI = W.T.dot(W.dot(H.T) * I)
                H      = H * np.nan_to_num(WTXI / WTWHTI).T


            if self.compute_error:
                self.error[t] = np.linalg.norm((X-W.dot(H.T))*I, ord="fro")**2
                num_zeros = sum(W.ravel() == 0) + sum(H.ravel() == 0)
                print(t, self.error[t], num_zeros)

            if self.verbose:
                stderr.write("%d/%d\r" % (t, self.max_iter))
                stderr.flush()

        stderr.write("\n")

        self.W = W
        self.H = H
    
    
    def predict(self, i, j):
        """
        Predict score for row i and column j
        :param i: Row index.
        :param j: Column index.
        """
        return self.W[i, :].dot(self.H[j, :])
    

    def predict_all(self):
        """
        Return approximated matrix for all
        columns and rows.
        """
        return self.W.dot(self.H.T)


    def recommend(self, X, i, k=5):
        """
        Recommend items for row i and data X.
        :param i: Row index.
        :param X: Data matrix.
        :param k: Number of items to recommend.
        """
        x = self.W[i, :].dot(self.H.T)
        z = np.nonzero(X[i] == 0)[0]
        return sorted(z, key=lambda i: x[i], reverse=True)[:k]
