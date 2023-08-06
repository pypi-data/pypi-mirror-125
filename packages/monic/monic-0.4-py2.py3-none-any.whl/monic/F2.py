import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


class monospline:
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)

        self.n = self.y.size

        self.dif = self.x[1:] - self.x[:-1]
        self.m = (self.y[1:] - self.y[:-1]) / self.dif
        self.a = self.y[:]
        self.b = self.compute_b()
        self.c = (3 * self.m - self.b[1:] - 2 * self.b[:-1]) / self.dif
        self.d = (self.b[1:] + self.b[:-1] - 2 * self.m) / (self.dif * self.dif)

    def compute_b(self):
        b = np.empty(self.n)
        for i in range(1, self.n - 1):
            is_mono = self.m[i - 1] * self.m[i] > 0
            if is_mono:
                b[i] = 3 * self.m[i - 1] * self.m[i] / (
                            max(self.m[i - 1], self.m[i]) + 2 * min(self.m[i - 1], self.m[i]))
            else:
                b[i] = 0
            if is_mono and self.m[i] > 0:
                b[i] = min(max(0, b[i]), 3 * min(self.m[i - 1], self.m[i]))
            elif is_mono and self.m[i] < 0:
                b[i] = max(min(0, b[i]), 3 * max(self.m[i - 1], self.m[i]))

        b[0] = ((2 * self.dif[0] + self.dif[1]) * self.m[0] - self.dif[0] * self.m[1]) / (self.dif[0] + self.dif[1])
        b[self.n - 1] = ((2 * self.dif[self.n - 2] + self.dif[self.n - 3]) * self.m[self.n - 2]
                         - self.dif[self.n - 2] * self.m[self.n - 3]) / (self.dif[self.n - 2] + self.dif[self.n - 3])
        return b

    def evaluate(self, t_intrp):
        ans = []
        for tau in t_intrp:

            i = np.where(tau >= self.x)[0]
            if i.size == 0:
                i = 0
            else:
                i = i[-1]
            i = min(i, self.n - 2)
            res = self.a[i] + self.b[i] * (tau - self.x[i]) + self.c[i] * ((tau - self.x[i]) ** 2) + self.d[i] * (
                        (tau - self.x[i]) ** 3)
            ans.append(res)
        return ans


x1 = np.linspace(0.0, 10.0, 11)
y1 = np.cos(x1)
plt.plot(x1, y1, 'o')

interp = monospline(x1, y1)
x = np.linspace(min(x1), max(x1), 5000)
y = interp.evaluate(x)
plt.plot(x, y)

interp = CubicSpline(x1, y1)
plt.plot(x, interp(x))
plt.show()
