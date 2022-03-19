from PyQt5 import QtCore, QtGui, QtWidgets
from consoletest import Console
import numpy as np
import pyqtgraph.opengl as gl
from vis import visualizer
from kookatest import kookabot
import math
from comm import comm
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
        self.fullyConencted = False
        self.USB1 = comm('USB 1')
        self.USB2 = comm('USB 2')
        self.USB3 = comm('USB 3')
        self.USB4 = comm('USB 4')
        self.connec.clicked.connect(self.connecting)
        self.vis.showAngle(self.angleSlots, self.kooka.joint_ang_new)
        self.command.clicked.connect(self.send_cmd)
        self.vis.showAngle(self.diffSlots, self.kooka.diff())
        self.vis.draw()
        self.stir.clicked.connect(self.stirring)
        self.calibrate.clicked.connect(self.calibr)

    def connecting(self):
        if(self.fullyConencted == False):
            self.USB1.connection(self.usb_1_slot.text(), self.terminal)
            self.USB2.connection(self.usb_2_slot.text(), self.terminal)
            self.USB3.connection(self.usb_3_slot.text(), self.terminal)
            self.USB4.connection(self.usb_4_slot.text(), self.terminal)

            if(self.USB1.connected == False or self.USB2.connected == False or self.USB3.connected == False or self.USB4.connected == False):
                self.terminal.append('Connection failed.')
                self.terminal.append('')

            elif(self.USB1.connected == True and self.USB2.connected == True and self.USB3.connected == True and self.USB4.connected == True):
                self.terminal.append('Connection succeed!')
                self.fullyConencted = True
                self.connec.setText("Disconnect")
                self.terminal.append("Hardware mode on.")
                self.terminal.append('')

        elif(self.fullyConencted == True):
            self.fullyConencted = False
            self.connec.setText("Connect")
            self.terminal.append('Simulation mode on.')
            self.terminal.append('')


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

    def send_cmd(self):
        self.kooka.currenAngUpdate()
        self.vis.updateCurrentPos()
        self.vis.draw()
        if(self.fullyConencted == True):
            vel = self.dt_slot.text()
            maxAngle = max(abs(self.kooka.deltaThetas))
            n = 50*maxAngle/vel
            deltaThetaInterval = self.kooka.deltaThetas/n
            for i in range(n):
                self.USB1.send(deltaThetaInterval[0]*180/math.pi, 'x')
                self.USB2.send(deltaThetaInterval[1]*180/math.pi, 'x')
                self.USB3.send(deltaThetaInterval[2]*180/math.pi, 'x')
                self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)

        self.kooka.deltaThetas = self.kooka.diff()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)

    def stirring(self):
        while(True):
            print("asd")

    def calibr(self):
        message = "c"
        self.USB1.ser.write(message.encode())
        retVal = self.USB1.ser.read()
        if(retVal == "d"):
            self.terminal.append("Joint 1 is calibrated.")
        else:
            self.terminal.append("Joint 1 calibration failed.")
        self.USB2.ser.write(message.encode())
        retVal = self.USB2.ser.read()
        if(retVal == "d"):
            self.terminal.append("Joint 2 is calibrated.")
        else:
            self.terminal.append("Joint 2 calibration failed.")
        self.USB3.ser.write(message.encode())
        retVal = self.USB3.ser.read()
        if(retVal == "d"):
            self.terminal.append("Joint 3 is calibrated.")
        else:
            self.terminal.append("Joint 3 calibration failed.")
        return True



    ''' An example of drawing a straight line
    def draw(self):
        
        point1 = (0, 0, 0)  #specify the (x, y, z) values of the first point in a tuple
        point2 = (5, 6, 8)  #specify the (x, y, z) values of the second point in a tuple

        self.points_list.append(point1) #add the point1 tuple to the points_list
        self.points_list.append(point2) #add the point2 tuple to the points_list
        points_array = np.array(self.points_list) #convert the list to an array
        drawing_variable = gl.GLLinePlotItem(pos = points_array, width = 1, antialias = True)   #make a variable to store drawing data(specify the points, set antialiasing)
        self.view.addItem(drawing_variable)
        '''
