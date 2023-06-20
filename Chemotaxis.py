import numpy as np
#import matplotlib.pyplot as plt
class Chemotaxis:
    def __init__(self, x, y,D):
        self.x = x
        self.y = y
        self.conc = 0
        self.theta = np.random.rand()*2*np.pi
        self.dt = 0
        self.D = D

    def update(self,old_conc,new_conc):
        if new_conc>old_conc:
            x = x + np.cos(self.theta)*self.D
            y = y + np.sin(self.theta)*self.D
        else:
            self.theta = np.random.rand()*2*np.pi
            x = x + np.cos(self.theta)
            y = y + np.sin(self.theta)
        return x,y
 
