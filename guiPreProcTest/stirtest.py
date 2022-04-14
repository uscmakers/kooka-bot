from PyQt5 import QtCore, QtGui, QtWidgets
from consoletest import Console
import numpy as np
import pyqtgraph.opengl as gl
from vis import visualizer
from kookatest import kookabot
import math
from comm import comm
import serial
import time

class UI(QtWidgets.QMainWindow, Console):
    def __init__(self):
        super().__init__()
        self.setup(self)
        # self.command.clicked.connect(self.send_cmd)
        # self.calibrate.clicked.connect(self.connect())
        self.points_list = []
        self.angleSlots = [self.joint_1_box, self.joint_2_box, self.joint_3_box, self.joint_4_box,]
        self.diffSlots = [self.delta_1, self.delta_2, self.delta_3, self.delta_4]
        self.kooka = kookabot()
        self.vis = visualizer(self.kooka, self.view)
        self.joint_1_slider.setValue(180*self.kooka.joint_ang_new[0]/math.pi)
        self.joint_2_slider.setValue(180*self.kooka.joint_ang_new[1]/math.pi)
        self.joint_3_slider.setValue(-180*self.kooka.joint_ang_new[2]/math.pi)
        self.joint_4_slider.setValue(-180*self.kooka.joint_ang_new[3]/math.pi)
        self.joint_1_slider.valueChanged.connect(self.slide)
        self.joint_2_slider.valueChanged.connect(self.slide)
        self.joint_3_slider.valueChanged.connect(self.slide)
        self.joint_4_slider.valueChanged.connect(self.slide)
        self.vis.showAngle(self.angleSlots, self.kooka.joint_ang_new)
        self.vis.showAngle(self.diffSlots, self.kooka.diff())
        self.vis.draw()
        self.stir.clicked.connect(self.stirring)
        self.goal = []


    def slide(self, value):
        widgetname = self.focusWidget().objectName()

        if(int(widgetname) == 2 or int(widgetname) == 3):
            self.kooka.joint_ang_new[int(widgetname)] = -value*math.pi/180
        else:
            self.kooka.joint_ang_new[int(widgetname)] = value*math.pi/180
        
        self.vis.draw()
        self.vis.showAngle(self.angleSlots, self.kooka.joint_ang_new)
        self.kooka.deltaThetas = self.kooka.diff()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)

    def points(self):
        t = int(self.dt_slot.text())
        n = 50*t

        return n

    def stirring(self):

        #points = self.points()
        #points = int(self.dt_slot.text())*50
        #self.kooka.points = self.kooka.init_points(points)
        print(self.kooka.points)

        deltaThetaInterval = np.empty([self.kooka.points,3])
        n = np.empty(self.kooka.points)
        tra = np.empty([self.kooka.points,3])

        self.goal = [0, 0, 0]
        self.kooka.cmd(self.kooka.joint_ang_new)
        self.kooka.stir()

        for i in range(self.kooka.points):
            xx = np.array([self.kooka.x_stir[i], self.kooka.y_stir[i], self.kooka.z_stir[i]])
            tra[i] = xx
        self.vis.showTraejc(tra)

        for i in range(self.kooka.points):
            self.goal = tra[i]

            angles = self.kooka.ik(self.goal)
            self.kooka.currenAngUpdate()
            self.kooka.joint_ang_new = np.array([angles[0], angles[1], angles[2], angles[3]])
            self.vis.updateCurrentPos()
            self.vis.draw()

            self.kooka.deltaThetas = 180/math.pi*self.kooka.diff()
####### acceleration version

        revolutions = int(self.rev_slot.text())
        n_a = 10

        for i in range(n_a):
            print(str(deltaThetaInterval[0][0]*i/n_a) + "\t" + str(deltaThetaInterval[0][1]*i/n_a) + "\t" + str(deltaThetaInterval[0][2]*i/n_a))
            time.sleep(0.02)

        for i in range(revolutions*self.kooka.points):
            j = i%revolutions
            #const speed loop
            print(str(deltaThetaInterval[j][0]) + "\t" + str(deltaThetaInterval[j][1]) + "\t" + str(deltaThetaInterval[j][2]))
            time.sleep(0.02)

        for i in range(n_a):
            k = revolutions*self.kooka.points-i
            print(str(deltaThetaInterval[249][0]*(1-(k+1)/n_a)) + "\t" + str(deltaThetaInterval[249][1]*(1-(k+1)/n_a)) + "\t" + str(deltaThetaInterval[249][2]*(1-(k+1)/n_a)))
            time.sleep(0.02)

        self.kooka.deltaThetas = self.kooka.diff()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)
        self.vis.draw()

