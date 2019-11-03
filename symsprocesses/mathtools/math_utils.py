import numpy as np

class Const:
    def __init__(self, value):
        self._value = value
    
    def __call__(x):
        return self._value

class TwoDimLinearMesh:
    def __init__(self, x0, x1, y0, y1, step_width_x, step_width_y, step_width_line_x, step_width_line_y):
        assert x0 < x1, "x0 must be smaller than x1!"
        self._x0 = x0
        self._x1 = x1 + .01
        assert y0 < y1, "y0 must be smaller than y1!"
        self._y0 = y0
        self._y1 = y1 + .01
        self._step_width_x = step_width_x
        self._step_width_y = step_width_y
        self._step_width_line_x = step_width_line_x
        self._step_width_line_y = step_width_line_y
        self._X = []
        self._Y = []

    def create(self):
        xs = np.arange(self._x0, self._x1, self._step_width_x)
        line_y = np.arange(self._y0, self._y1, self._step_width_line_y)

        for x in xs:
            x_in_y_dir = []
            for y_l in line_y:
                x_in_y_dir.append([x, y_l])
            self._X.append(x_in_y_dir)

        ys = np.arange(self._y0, self._y1, self._step_width_y)
        line_x = np.arange(self._x0, self._x1, self._step_width_line_x)

        for y in ys:
            y_in_x_dir = []
            for x_l in line_x:
                y_in_x_dir.append([y, x_l])
            self._Y.append(y_in_x_dir)

        return self._X, self._Y

    def map(self, diffeo):
        X = []
        Y = []

        for x in self._X:
            x_in_y_dir = []
            for x_y in x:
                x_ind_y_dir.append(diffeo(x_y[0], x_y[1]))
            X.append(x_in_y_dir)

        for y in self._Y:
            y_in_x_dir = []
            for y_x in y:
                y_ind_x_dir.append(diffeo(y_x[0], y_x[1]))
            Y.append(y_in_x_dir)

        return X, Y

    def plot(X, Y):
        return None

        


linear_mesh = TwoDimLinearMesh(- .5, + .5, .5, 1.5, .2, .2, .005, .005)
X, Y = linear_mesh.create()
plot(X, Y)