import numpy as np
from matplotlib import pyplot as plt


class DFT:
    def __init__(self, data_dimension, dft_rank):
        if type(data_dimension) == int:
            data_dimension = (data_dimension, 1)
        self.data_dimension = data_dimension
        self.dft_rank = dft_rank
        ran = np.arange(-np.pi, np.pi, 2 * np.pi / data_dimension[0])
        self.dft_cos = lambda k: np.cos(k * ran)
        self.dft_sin = lambda k: np.sin(k * ran)

    def cos_coefficients(self, data):
        n = self.dft_rank // 2
        out = np.ndarray(n)
        for k in range(n):
            out[k] = np.matmul(self.dft_cos(k), data) * (2 / len(data))
            if k == 0:
                out[k] /= 2
        return out

    def sin_coefficients(self, data):
        n = self.dft_rank // 2
        out = np.ndarray(n)
        for k in range(n):
            out[k] = np.matmul(self.dft_sin(k), data) * (2 / len(data))
            if k == 0:
                out[k] /= 2
        return out

    def modes_scalars_dynamics(self, data):
        m = np.zeros((self.data_dimension[0], self.dft_rank))
        s = np.zeros(self.dft_rank)
        d = np.zeros((self.data_dimension[1], self.dft_rank))
        for k in range(self.dft_rank):
            if not self.data_dimension == np.shape(data):
                data = np.reshape(data, self.data_dimension)
            if k % 2 == 0:
                m[:, k] += self.dft_cos(k // 2) / np.pi
                for l, col in enumerate(data.T):
                    d[l, k] += np.matmul(self.dft_cos(k // 2), col) * (2 * np.pi / len(data))
                s[k] = np.matmul(d[:, k], d[:, k].T)
            elif k % 2 == 1:
                m[:, k] += self.dft_sin(k // 2) / np.pi
                for l, col in enumerate(data.T):
                    d[l, k] += np.matmul(self.dft_sin(k // 2), col) * (2 * np.pi / len(data))
                s[k] = np.matmul(d[:, k], d[:, k].T)
        return m, s, d

    def fit(self, data):
        m, s, d = self.modes_scalars_dynamics(data)
        out = np.matmul(m, d.T)
        return out

    def cos_matrix(self):
        out = np.ndarray((self.data_dimension, self.data_dimension))
        for k in range(self.data_dimension):
            out[k] = self.dft_cos(k)
        return out

    def sin_matrix(self):
        out = np.ndarray((self.data_dimension, self.data_dimension))
        for k in range(self.data_dimension):
            out[k] = self.dft_sin(k)
        return out
