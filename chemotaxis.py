import numpy as np

# import matplotlib.pyplot as plt


class Chemotaxis:
    def __init__(self, D):
        self.conc = 0
        self.theta = np.random.rand() * 2 * np.pi
        # self.dt = 0
        self.D = D
        self.phi = np.random.rand() * np.pi

    def update(
        self, new_conc, relative_position
    ):  # maybe change to using NED for this or we are gonna get ourselves confused
        if new_conc > self.conc:
            new_North = (
                relative_position[0] + np.cos(self.theta) * np.sin(self.phi) * self.D
            )
            new_East = (
                relative_position[1] + np.sin(self.theta) * np.sin(self.phi) * self.D
            )
            new_Down = relative_position[2] + np.cos(self.phi) * self.D
        else:
            self.theta = np.random.rand() * 2 * np.pi
            self.phi = np.random.rand() * np.pi
            new_North = (
                relative_position[0] + np.cos(self.theta) * np.sin(self.phi) * self.D
            )
            new_East = (
                relative_position[1] + np.sin(self.theta) * np.sin(self.phi) * self.D
            )
            new_Down = relative_position[2] + np.cos(self.phi) * self.D
        self.conc = new_conc

        return new_North, new_East, new_Down
