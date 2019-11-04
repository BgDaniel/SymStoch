import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from moebius_transfomation import reflection0

class Const:
    def __init__(self, value):
        self._value = value
    
    def __call__(x):
        return self._value

class TwoDimLinearMesh:
    def __init__(self, x, y, x0, x1, y0, y1, step_width_x, step_width_y, step_width_line_x, step_width_line_y,
        offset=0.25):
        assert x0 < x1, "x0 must be smaller than x1!"
        self._x0 = x0
        self._x1 = x1
        assert y0 < y1, "y0 must be smaller than y1!"
        self._y0 = y0
        self._y1 = y1
        self._step_width_x = step_width_x
        self._step_width_y = step_width_y
        self._step_width_line_x = step_width_line_x
        self._step_width_line_y = step_width_line_y
        self._X = []
        self._Y = []
        self._offset = offset
        self._x = x
        self._y = y

    def create(self):
        xs = np.arange(self._x0, self._x1 + self._step_width_x, self._step_width_x)
        line_y = np.arange(self._y0, self._y1 + self._step_width_line_y, self._step_width_line_y)

        for x in xs:
            x_in_y_dir = []
            for y_l in line_y:
                x_in_y_dir.append([x, y_l])
            self._X.append(x_in_y_dir)

        ys = np.arange(self._y0, self._y1 + self._step_width_line_y, self._step_width_y)
        line_x = np.arange(self._x0, self._x1 + self._step_width_line_x, self._step_width_line_x)

        for y in ys:
            y_in_x_dir = []
            for x_l in line_x:
                y_in_x_dir.append([x_l, y])
            self._Y.append(y_in_x_dir)

        return self._X, self._Y

    def map(self, diffeo):
        X = []
        Y = []

        for x in self._X:
            x_in_y_dir = []
            for x_y in x:
                x_in_y_dir.append(diffeo(x_y))
            X.append(x_in_y_dir)

        for y in self._Y:
            y_in_x_dir = []
            for y_x in y:
                y_in_x_dir.append(diffeo(y_x))
            Y.append(y_in_x_dir)

        return X, Y

    def plot(self):
        for x_in_y_dir in self._X:
            x, y = [p[0] for p in x_in_y_dir], [p[1] for p in x_in_y_dir]
            plt.plot(x, y, linewidth=.6, color='blue')
        for y_in_x_dir in self._Y:
            x, y = [p[0] for p in y_in_x_dir], [p[1] for p in y_in_x_dir]
            plt.plot(x, y, linewidth=.6, color='blue')
       
        plt.xlim(self._x0 - self._offset, self._x1 + self._offset)
        plt.ylim(self._y0 - self._offset, self._y1 + self._offset)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.plot(self._x0, self._y0)
        plt.show()
  

        


linear_mesh = TwoDimLinearMesh(.0, 1.0, - .5, + .5, .5, 1.5, .025, .025, .005, .005)
linear_mesh.create()
#linear_mesh.plot()
linear_mesh.map(reflection0(1.0))