import math
import numpy as np
from sympy import sin, cos, symbols, lambdify

class DH:
    def __init__(self, twistAngle=0, offJoint=0, linklen=0, x=''):
        self.jointOff = offJoint
        self.angleTwist =twistAngle
        self.theta = symbols('theta'+str(x))
        self.lenlink = linklen
        self.dh = self.update()

    # dh parameter table used for transformation
    def update(self):
        dh = np.array([[cos(self.theta), -sin(self.theta)*math.cos(self.angleTwist), sin(self.theta)*sin(self.angleTwist) , self.lenlink*cos(self.theta)],
                       [sin(self.theta), cos(self.theta)*math.cos(self.angleTwist) , -cos(self.theta)*sin(self.angleTwist), self.lenlink*sin(self.theta)],
                       [0              , sin(self.angleTwist)                      , math.cos(self.angleTwist)            , self.jointOff               ],
                       [0              , 0                                         , 0                                    , 1                           ]])    

        return dh
