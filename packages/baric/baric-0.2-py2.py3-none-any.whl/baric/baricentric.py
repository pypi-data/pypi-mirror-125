import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

class BarycentricInterpolator(_Interpolator1D):

    def __init__(self, xi, yi=None, axis=0):
        _Interpolator1D.__init__(self, xi, yi, axis)

        self.xi = np.asfarray(xi)
        self.set_yi(yi)
        self.n = len(self.xi)

        self.wi = np.zeros(self.n)
        self.wi[0] = 1
        for j in range(1, self.n):
            self.wi[:j] *= (self.xi[j]-self.xi[:j])
            self.wi[j] = np.multiply.reduce(self.xi[:j]-self.xi[j])
        self.wi **= -1

    def set_yi(self, yi, axis=None):

        if yi is None:
            self.yi = None
            return
        self._set_yi(yi, xi=self.xi, axis=axis)
        self.yi = self._reshape_yi(yi)
        self.n, self.r = self.yi.shape

    def add_xi(self, xi, yi=None):

        if yi is not None:
            if self.yi is None:
                raise ValueError("No previous yi value to update!")
            yi = self._reshape_yi(yi, check=True)
            self.yi = np.vstack((self.yi,yi))
        else:
            if self.yi is not None:
                raise ValueError("No update to yi provided!")
        old_n = self.n
        self.xi = np.concatenate((self.xi,xi))
        self.n = len(self.xi)
        self.wi **= -1
        old_wi = self.wi
        self.wi = np.zeros(self.n)
        self.wi[:old_n] = old_wi
        for j in range(old_n, self.n):
            self.wi[:j] *= (self.xi[j]-self.xi[:j])
            self.wi[j] = np.multiply.reduce(self.xi[:j]-self.xi[j])
        self.wi **= -1

    def __call__(self, x):
        return _Interpolator1D.__call__(self, x)

    def _evaluate(self, x):
        if x.size == 0:
            p = np.zeros((0, self.r), dtype=self.dtype)
        else:
            c = x[...,np.newaxis]-self.xi
            z = c == 0
            c[z] = 1
            c = self.wi/c
            p = np.dot(c,self.yi)/np.sum(c,axis=-1)[...,np.newaxis]
            # Now fix where x==some xi
            r = np.nonzero(z)
            if len(r) == 1:  # evaluation at a scalar
                if len(r[0]) > 0:  # equals one of the points
                    p = self.yi[r[0][0]]
            else:
                p[r[:-1]] = self.yi[r[-1]]
        return p


x1=np.linspace(0.0,10.0,11)
y1=np.sin(x1)
plt.plot(x1, y1, 'o')

intrp = BarycentricInterpolator(x1, y1)
x = np.linspace(min(x1), max(x1), 5000)
y = intrp.evaluate(x)
plt.plot(x, y)


intrp = CubicSpline(x1, y1)
plt.plot(x, intrp(x))
plt.show()
