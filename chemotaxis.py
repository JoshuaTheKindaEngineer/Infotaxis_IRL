import numpy as np
import matplotlib.pyplot as plt


class Chemotaxis:
    def __init__(self, D):
        self.conc = 0
        self.theta = np.random.rand() * 2 * np.pi
        # self.dt = 0
        self.D = D

    def update(
        self, new_conc, current_x, current_y
    ):  # maybe change to using NED for this or we are gonna get ourselves confused
        if new_conc > self.conc:
            new_x = current_x + np.cos(self.theta) * self.D
            new_y = current_y + np.sin(self.theta) * self.D
        else:
            self.theta = np.random.rand() * 2 * np.pi
            new_x = current_x + np.cos(self.theta)
            new_y = current_y + np.sin(self.theta)

        self.conc = new_conc

        return new_x, new_y
