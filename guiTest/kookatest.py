import math
import numpy as np
import matplotlib.pyplot as plt
import random
from DH import DH
from sympy import sin, cos, symbols, lambdify
import time

# lengths of joints in yaw, shoulder, elbow, wrist
LINK_LEN = [0.03, 0.15, 0.1, 0.1]
INIT_ANG = [0, math.pi/2, -math.pi/2]

class kookabot:
    # initialize parameters and joint angles + positions
    def __init__(self):
        self.links = LINK_LEN   # link length initialization
        self.yaw, self.shoulder, self.elbow, self.wrist = self.joint_pos() # joint angles initialization
        self.joint_ang_new = self.joint_init(INIT_ANG) # joint angles to send as a command
        self.current_joint_ang = self.joint_init(INIT_ANG) # current joint angles
        self.x, self.y, self.z = self.fk(self.joint_ang_new) # use forward kinematics to initialize the positions
        self.deltaThetas = self.diff()
        # coocking trajectories
        self.x_stir = np.zeros(120)
        self.y_stir = np.zeros(120)
        self.z_stir = np.zeros(120)

    # initialize the joint angles
    def joint_init(self, INIT_ANG):
        joint_4 = -(math.pi/2+INIT_ANG[1]+INIT_ANG[2])
        ang_array = np.array([INIT_ANG[0], INIT_ANG[1], INIT_ANG[2], -math.pi/6])

        return ang_array

    # fk equation initialization based on the link lengths
    def joint_pos(self):
        # DH parameters for 4 joints
        dh1 = DH(math.pi/2, self.links[0], 0, 1)
        dh2 = DH(0, 0, self.links[1], 2)
        dh3 = DH(0, 0, self.links[2], 3)
        dh4 = DH(0, 0, self.links[3], 4)

        # each joint's coordinate transformation WRT the robot's base
        T01 = dh1.dh
        T02 = dh1.dh @ dh2.dh
        T03 = dh1.dh @ dh2.dh @ dh3.dh
        T04 = dh1.dh @ dh2.dh @ dh3.dh @ dh4.dh

        # joint 1's xyz equations taking 1 angle input
        dh1x = lambdify(dh1.theta,T01[0,3])
        dh1y = lambdify(dh1.theta,T01[1,3])
        dh1z = lambdify(dh1.theta,T01[2,3])
        
        # joint 1's xyz equations taking 2 angle inputs
        dh2x = lambdify((dh1.theta, dh2.theta), T02[0,3])
        dh2y = lambdify((dh1.theta, dh2.theta), T02[1,3])
        dh2z = lambdify((dh1.theta, dh2.theta), T02[2,3])

        # joint 1's xyz equations taking 3 angle inputs
        dh3x = lambdify((dh1.theta, dh2.theta, dh3.theta), T03[0,3])
        dh3y = lambdify((dh1.theta, dh2.theta, dh3.theta), T03[1,3])
        dh3z = lambdify((dh1.theta, dh2.theta, dh3.theta), T03[2,3])

        # joint 1's xyz equations taking 4 angle inputs
        dh4x = lambdify((dh1.theta, dh2.theta, dh3.theta, dh4.theta), T04[0,3])
        dh4y = lambdify((dh1.theta, dh2.theta, dh3.theta, dh4.theta), T04[1,3])
        dh4z = lambdify((dh1.theta, dh2.theta, dh3.theta, dh4.theta), T04[2,3])

        # return the joints' xyz equations
        return [dh1x, dh1y, dh1z], [dh2x, dh2y, dh2z], [dh3x, dh3y, dh3z], [dh4x, dh4y, dh4z]

    # forward kinematics calculation: outputs each joint's x, y, z
    def fk(self, angs):
        # 4 joints' angles
        ang1 = angs[0]
        ang2 = angs[1]
        ang3 = angs[2]
        ang4 = angs[3]

        # all joints' xyz positions calculations
        x = [self.yaw[0](ang1), self.shoulder[0](ang1, ang2), self.elbow[0](ang1, ang2, ang3), self.wrist[0](ang1, ang2, ang3, ang4)]
        y = [self.yaw[1](ang1), self.shoulder[1](ang1, ang2), self.elbow[1](ang1, ang2, ang3), self.wrist[1](ang1, ang2, ang3, ang4)]
        z = [self.yaw[2](ang1), self.shoulder[2](ang1, ang2), self.elbow[2](ang1, ang2, ang3), self.wrist[2](ang1, ang2, ang3, ang4)]

        # return all joints' xyz positions
        return x, y, z

    # update the position status upon sending a command
    def cmd(self,angs):
        self.x, self.y, self.z = self.fk(angs)


    # inverse kinematics calculation for 3 joints: outputs desired joint angles for the goal x, y, z pos of the elbow's tip
    def ik(self, goal):
        diag = math.sqrt(goal[0]**2+goal[1]**2+(goal[2]-self.links[0])**2)
        theta1 = math.atan(goal[1])/goal[0]
        theta3 = math.acos((diag**2-self.links[1]**2-self.links[2]**2)/(2*self.links[1]*self.links[2]))
        theta2 = math.atan((goal[2]-self.links[0])/goal[0])+math.atan((self.links[2]*math.sin(theta3)/(self.links[1]+self.links[2]*math.cos(theta3))))
        # theta4 = self.joint_ang[3]
        theta4 = -(math.pi/2-theta3-theta2)

        return [theta1, theta2, -theta3, -theta4]

    # print out robot arm's joint angles and tip position
    def status(self):
        print("Yaw: "+str(format(self.joint_ang_new[0],".2f"))+" [rad], Shoulder: "+str(format(self.joint_ang_new[1],".2f"))+" [rad], Elbow: "+str(format(self.joint_ang_new[2], ".2f"))+" [rad]")
        print("Joint 1 - x: "+str(format(self.x[0],".2f"))+", y: "+str(format(self.y[0],".2f"))+", z: "+str(format(self.z[0],".2f")))
        print("Joint 2 - x: "+str(format(self.x[1],".2f"))+", y: "+str(format(self.y[1],".2f"))+", z: "+str(format(self.z[1],".2f")))
        print("Joint 3 - x: "+str(format(self.x[2],".2f"))+", y: "+str(format(self.y[2],".2f"))+", z: "+str(format(self.z[2],".2f")))
        print()

    # create stirring trajectories
    def stir(self):
        center_x = self.x[2]-0.02
        center_y = self.y[2]
        center_z = self.z[2]

        for i in range(120):
            self.x_stir[i] = center_x + 0.02*math.cos(2*math.pi*i/120)
            self.y_stir[i] = center_y + 0.02*math.sin(2*math.pi*i/120)
            self.z_stir[i] = center_z

    def diff(self):
        ang1 = self.joint_ang_new
        ang2 = self.current_joint_ang

        return ang1 - ang2

    def currenAngUpdate(self):
        ang1 = self.joint_ang_new[0]
        ang2 = self.joint_ang_new[1]
        ang3 = self.joint_ang_new[2]
        ang4 = self.joint_ang_new[3]

        self.current_joint_ang = np.array([ang1, ang2, ang3, ang4])
