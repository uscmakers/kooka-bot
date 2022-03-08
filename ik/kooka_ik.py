import math
import numpy as np
import random


class kooka_ik:

    # initialize parameters and joint angles + positions
    def __init__(self, link1_len = 0.3, link2_len = 0.3):
        # parameters
        self.link = 3                     # kukabot's three joints: yaw, shoulder, elbow
        self.joints = np.zeros(3)    
        self.pos_x = np.zeros(3)          # x, y, z coordinates for each joint
        self.pos_y = np.zeros(3)
        self.pos_z = np.zeros(3)
        self.link1_len = link1_len        # each link's length
        self.link2_len = link2_len

        # joint angles and positions
        self.joint_init()
        self.fk()
        self.stir_center = np.zeros(3)

    # kukabot's joint angles random initialization
    def joint_init(self):            
        yaw = 0
        shoulder = 0.7 
        elbow = 1.2 

        self.joints[0] = yaw
        self.joints[1] = shoulder
        self.joints[2] = elbow
        return self.joints

    # inverse kinematics calculation: outputs desired joint angles for the goal x, y, z of the arm's tip
    def ik(self, goal):              
        diag = math.sqrt(goal[0]**2+goal[1]**2+goal[2]**2)
        theta1 = math.atan(goal[1]/goal[0])
        theta3 = math.acos((diag**2-self.link1_len**2-self.link2_len**2)/(2*self.link1_len*self.link2_len))
        theta2 = math.atan(goal[2]/goal[0])+math.atan(self.link2_len*math.sin(theta3)/(self.link1_len+self.link2_len*math.cos(theta3)))

        self.joints[0] = theta1
        self.joints[1] = theta2
        self.joints[2] = theta3
        return self.joints

    # forward kinematics calculation: outputs each joint's x, y, z
    def fk(self):                    
        x1 = 0
        y1 = 0
        z1 = 0
        x2 = self.link1_len*math.cos(self.joints[1])*math.cos(self.joints[0])
        y2 = self.link1_len*math.cos(self.joints[1])*math.sin(self.joints[0])
        z2 = self.link1_len*math.sin(self.joints[1])
        x3 = x2+self.link2_len*math.cos(self.joints[1]-self.joints[2])*math.cos(self.joints[0])
        y3 = y2+self.link2_len*math.cos(self.joints[1]-self.joints[2])*math.sin(self.joints[0])
        z3 = z2+self.link2_len*math.sin(self.joints[1]-self.joints[2])

        self.pos_x[0] = x1
        self.pos_y[0] = y1
        self.pos_z[0] = z1 
        self.pos_x[1] = x2
        self.pos_y[1] = y2
        self.pos_z[1] = z2 
        self.pos_x[2] = x3
        self.pos_y[2] = y3
        self.pos_z[2] = z3 

    # print out robot arm's joint angles and tip position
    def print_status(self):          
        print("Yaw: "+str(format(self.joints[0],".2f"))+" [rad], Shoulder: "+str(format(self.joints[1],".2f"))+" [rad], Elbow: "+str(format(self.joints[2], ".2f"))+" [rad]")
        print("Joint 1 - x: "+str(format(self.pos_x[0],".2f"))+", y: "+str(format(self.pos_y[0],".2f"))+", z: "+str(format(self.pos_z[0],".2f")))
        print("Joint 2 - x: "+str(format(self.pos_x[1],".2f"))+", y: "+str(format(self.pos_y[1],".2f"))+", z: "+str(format(self.pos_z[1],".2f")))
        print("Joint 3 - x: "+str(format(self.pos_x[2],".2f"))+", y: "+str(format(self.pos_y[2],".2f"))+", z: "+str(format(self.pos_z[2],".2f")))
        print()

    # create stirring trajectories
    def stir(self, radius=0.15, n_points=30, n_stirs=1):                
        center_x = self.pos_x[2]-radius
        center_y = self.pos_y[2]
        center_z = self.pos_z[2]
        self.stir_center[0] = center_x
        self.stir_center[1] = center_y
        self.stir_center[2] = center_z

        output = []
        for i in range(n_stirs):
            for i in range(n_points + 1):
                coord = [0]*3
                coord[0] = center_x + radius*math.cos(2*math.pi*i/n_points)
                coord[1] = center_y + radius*math.sin(2*math.pi*i/n_points)
                coord[2] = center_z
                output.append(coord)
        return output
                                                                                                                                                                       


if __name__ == '__main__':
    try:
        main()
    except:
        print("Sorry, please try again.")