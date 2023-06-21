import numpy as np
#import matplotlib.pyplot as plt


class Chemotaxis:
    def __init__(self, D):
        self.conc = 0
        self.theta = np.random.rand() * 2 * np.pi
        # self.dt = 0
        self.D = D
        self.phi = np.random.rand() * np.pi
    def update(
        self, new_conc, current_North, current_East, current_Down
    ):  # maybe change to using NED for this or we are gonna get ourselves confused
        if new_conc > self.conc:
            new_North = current_North + np.cos(self.theta) * np.sin(self.phi) * self.D
            new_East = current_East + np.sin(self.theta) * np.sin(self.phi) * self.D
            new_Down = current_Down + np.cos(self.phi) * self.D
        else:
            self.theta = np.random.rand() * 2 * np.pi
            self.phi = np.random.rand() * np.pi
            new_North = current_North + np.cos(self.theta) * np.sin(self.phi) * self.D
            new_East = current_East + np.sin(self.theta) * np.sin(self.phi) * self.D
            new_Down = current_Down + np.cos(self.phi) * self.D
        self.conc = new_conc

        return new_North, new_East, new_Down
