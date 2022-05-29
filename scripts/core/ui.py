from PyQt5 import QtCore, QtGui, QtWidgets
from console import Console
import numpy as np
import pyqtgraph.opengl as gl
from vis import visualizer
from kooka import kookabot
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
        self.angleSlots = [self.joint_1_box, self.joint_2_box,
                           self.joint_3_box, self.joint_4_box, ]
        self.diffSlots = [self.delta_1,
                          self.delta_2, self.delta_3, self.delta_4]
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
        self.cartesian.clicked.connect(self.send_cmd_cartesien)
        self.vis.showAngle(self.diffSlots, self.kooka.diff())
        self.vis.draw()
        self.stir.clicked.connect(self.stirring)
        self.calibrate.clicked.connect(self.calibr)
        self.i = 0
        self.servoAngle = self.servoAngle = -int(self.kooka.joint_ang_new[3]*180/math.pi)+90
        self.newgoalcenter = None
        self.tra = np.empty([self.kooka.points, 3])
        self.planner.clicked.connect(self.trajplan)
        self.newplanning = None
        self.plannedangles = None
        self.angles = []
        self.deltastosend = []
        self.deltastosendOpposite = []
        self.xgoa, self.ygoa, self.zgoa = None, None, None
        print(self.servoAngle)
        self.every.clicked.connect(self.everything)
  

    def connecting(self):
        if(self.fullyConencted == False):
            self.USB1.connection(self.usb_1_slot.text())
            self.USB2.connection(self.usb_2_slot.text())
            self.USB3.connection(self.usb_3_slot.text())
            #self.USB4.connection(self.usb_4_slot.text(), self.terminal)
            self.USB3.send(180, 'y')

            if(self.USB1.connected == False or self.USB2.connected == False or self.USB3.connected == False):
                self.terminal.append('Connection failed.')
                self.terminal.append('')

            elif(self.USB1.connected == True and self.USB2.connected == True and self.USB3.connected == True):
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

    def maxAng(self, angs):
        vel = self.dt_slot.text()
        maxangl = max(abs(angs))
        n = 50*maxangl/float(vel)

        return n

    def send_cmd(self):
        self.kooka.currenAngUpdate()
        self.vis.updateCurrentPos()
        self.vis.draw()
        self.servoAngle = -int(self.kooka.joint_ang_new[3]*180/math.pi)+90
        print(self.servoAngle)
        
        if(self.fullyConencted == True):
            vel = self.dt_slot.text()
            self.kooka.deltaThetas = 180/math.pi*self.kooka.deltaThetas
            maxAngle = max(abs(self.kooka.deltaThetas))
            n = 50*maxAngle/float(vel)
            deltaThetaInterval = self.kooka.deltaThetas/n
            deltaThetaInterval[0] = -3*deltaThetaInterval[0]
            deltaThetaInterval[1] = -deltaThetaInterval[1]
            start = time.time()

# acceleration version
            n_a = 10
            n = n - n_a

            # accelerating loop
            for i in range(n_a):
                self.USB1.send(deltaThetaInterval[0]*i/n_a, 'x')
                self.USB2.send(deltaThetaInterval[1]*i/n_a, 'x')
                self.USB3.send(deltaThetaInterval[2]*i/n_a, 'x')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            # const speed loop
            for i in range(int(n)):
                self.USB1.send(deltaThetaInterval[0], 'x')
                self.USB2.send(deltaThetaInterval[1], 'x')
                self.USB3.send(deltaThetaInterval[2], 'x')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            for i in range(n_a):
                self.USB1.send(deltaThetaInterval[0]*(1-(i+1)/n_a), 'x')
                self.USB2.send(deltaThetaInterval[1]*(1-i/n_a), 'x')
                self.USB3.send(deltaThetaInterval[2]*(1-i/n_a), 'x')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            self.USB3.send(self.servoAngle, 'y')
            #self.USB1.send(self.servoAngle,'y')

#######
        self.kooka.deltaThetas = self.kooka.diff()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)


    def send_cmd_cartesien(self):
        '''
        cv_results = mainn() # ((x,y), displacement)

        pixel_to_meter = .28 / cv_results[1]
        x_meter = cv_results[0][0] * pixel_to_meter
        y_meter = cv_results[0][1] * pixel_to_meter
        x_meter += 0.12#.381
        y_meter -= 0.228#.254
        print(x_meter)
        print(y_meter)
        #print(self.kooka.current_joint_ang)
        self.kooka.currenAngUpdate()
        self.xgoa,self.ygoa,self.zgoa = x_meter, y_meter, 0.63
        '''
        self.kooka.currenAngUpdate()
        goal = [float(self.xslot.text()), float(self.yslot.text()), float(self.zslot.text())]
        
        print(goal)
        anglesss = self.kooka.ik(goal)
        print(anglesss)
        self.kooka.joint_ang_new = np.array([anglesss[0], anglesss[1], anglesss[2], anglesss[3]])
        #print(self.kooka.joint_ang_new*180/math.pi)
        #print(self.kooka.joint_ang_new)
        '''
        self.vis.showAngle(self.angleSlots, self.kooka.joint_ang_new)
        self.kooka.deltaThetas = self.kooka.diff()
        #print(self.kooka.deltaThetas*180/math.pi)
        self.vis.draw()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)
        self.kooka.currenAngUpdate()
        self.vis.updateCurrentPos()
        self.vis.draw()
        '''
        self.servoAngle = -int(self.kooka.joint_ang_new[3]*180/math.pi)+90
        #print(self.servoAngle)
        #print(self.servoAngle)
        #print(self.kooka.deltaThetas*180/math.pi)
        
        
        if(self.fullyConencted == True):
            vel = self.dt_slot.text()
            self.kooka.deltaThetas = 180/math.pi*self.kooka.diff()
            maxAngle = max(abs(self.kooka.deltaThetas))
            n = 50*maxAngle/float(vel)
            deltaThetaInterval = self.kooka.deltaThetas/n
            deltaThetaInterval[0] = -3*deltaThetaInterval[0]
            deltaThetaInterval[1] = -deltaThetaInterval[1]
            start = time.time()
            print(deltaThetaInterval)
            print(n)

# acceleration version
            n_a = 10
            n = n - n_a
            # accelerating loop
            for i in range(n_a):
                self.USB1.send(deltaThetaInterval[0]*i/n_a, 'x')
                self.USB2.send(deltaThetaInterval[1]*i/n_a, 'x')
                self.USB3.send(deltaThetaInterval[2]*i/n_a, 'x')
                #self.USB1.send(self.servoAngle,'y')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            # const speed loop
            for i in range(int(n)):
                self.USB1.send(deltaThetaInterval[0], 'x')
                self.USB2.send(deltaThetaInterval[1], 'x')
                self.USB3.send(deltaThetaInterval[2], 'x')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            for i in range(n_a):
                self.USB1.send(deltaThetaInterval[0]*(1-(i+1)/n_a), 'x')
                self.USB2.send(deltaThetaInterval[1]*(1-i/n_a), 'x')
                self.USB3.send(deltaThetaInterval[2]*(1-i/n_a), 'x')
                #self.USB4.send(deltaThetaInterval[3]*180/math.pi, 'x')
                time.sleep(0.02)
            self.USB3.send(self.servoAngle, 'y')

#######
        self.kooka.deltaThetas = self.kooka.diff()
        self.vis.showAngle(self.diffSlots, self.kooka.deltaThetas)

    def trajplan(self):
        # update the radius and the number of trajectory points
        self.kooka.setRadius(float(self.radius_slot.text()))
        self.kooka.setPoints(int(self.points_slot.text()))
        self.tra = np.empty([self.kooka.points, 3])
        '''
        self.kooka.points = int(self.points_slot.text())
        self.kooka.stir_radius = float(self.radius_slot.text())
        self.kooka.x_stir = np.zeros(self.kooka.points)
        self.kooka.y_stir = np.zeros(self.kooka.points)
        self.kooka.z_stir = np.zeros(self.kooka.points)
        '''

        # xyz coordinates where the kooka starts stirring
        #self.newgoalcenter = [float(self.xslot.text()), float(self.yslot.text()), float(self.zslot.text())]
        #center_x = self.newgoalcenter[0]-float(self.kooka.stir_radius)
        #center_y = self.newgoalcenter[1]
        #center_z = self.newgoalcenter[2]

        self.newgoalcenter = [float(self.xslot.text()), float(self.yslot.text()), float(self.zslot.text())]
        center_x = self.newgoalcenter[0]-float(self.kooka.stir_radius)
        center_y = self.newgoalcenter[1]
        center_z = self.newgoalcenter[2]

        # xyz coordinates of the kooka's stirring trajectory based on where the kooka starts stirring  
        for i in range(self.kooka.points):
            self.kooka.x_stir[i] = center_x + self.kooka.stir_radius*math.cos(2*math.pi*i/self.kooka.points)
            self.kooka.y_stir[i] = center_y + self.kooka.stir_radius*math.sin(2*math.pi*i/self.kooka.points)
            self.kooka.z_stir[i] = center_z

        # visualize the trajectory in the GUI
        for i in range(self.kooka.points):
            xx = np.array([self.kooka.x_stir[i], self.kooka.y_stir[i], self.kooka.z_stir[i]])
            self.tra[i] = xx
        self.vis.showTraejc(self.tra)
        self.newplanning = True
        self.angles.clear()
        current = [self.kooka.current_joint_ang[0]*180.0/(math.pi), self.kooka.current_joint_ang[1]*180.0/(math.pi), self.kooka.current_joint_ang[2]*180.0/(math.pi)]
        self.kooka.servoAngles.clear()
        # calculate angles required at each points
        for i in range(self.kooka.points):
            #angles.append(self.kooka.ik())

            # compute ik
            angless = self.kooka.ik(self.tra[i])

            # calculate required yaw, shoulder, and elbow joint angles
            yaww = float(angless[0])*180.0/(math.pi)
            shoulde = float(angless[1])*180.0/(math.pi)
            elb = float(angless[2])*180.0/(math.pi)

            self.angles.append([yaww, shoulde, elb])

            servoAngleee = -int(angless[3]*180/math.pi)+90

            self.kooka.servoAngles.append(servoAngleee)
            print(self.kooka.servoAngles[i])


        # clear the array of required joint angle commands
        self.deltastosend.clear()

        # fist required joint command
        #self.beginning = [self.angles[0][0]-current[0], self.angles[0][1]-current[1], self.angles[0][2]-current[2]]

        # calculate required joint angle commands moving from i th to i+1 points
        for i in range(self.kooka.points-1):
            # i th point
            anglesetone = self.angles[i]

            # i + 1 th point
            anglesettwo = self.angles[i+1]

            # (i + 1 th point angles) - (i th point angles)
            self.deltastosend.append([anglesettwo[0]-anglesetone[0], anglesettwo[1]-anglesetone[1], anglesettwo[2]-anglesetone[2]])
        
        # calculate the required angle commands moving the arm from the last to the first points within the trajectory
        anglesettwo = self.angles[0]
        anglesetone = self.angles[self.kooka.points-1]
        self.deltastosend.append([anglesettwo[0]-anglesetone[0], anglesettwo[1]-anglesetone[1], anglesettwo[2]-anglesetone[2]])
        self.deltastosendOpposite.append([anglesetone[0]-anglesettwo[0], anglesetone[1]-anglesettwo[1], anglesetone[2]-anglesettwo[2]])

        for i in range(self.kooka.points-1,0,-1):
            # i th point
            anglesetone = self.angles[i]

            # i - 1 th point
            anglesettwo = self.angles[i-1]

            self.deltastosendOpposite.append([anglesettwo[0]-anglesetone[0], anglesettwo[1]-anglesetone[1], anglesettwo[2]-anglesetone[2]])

        # multiply coefficients in the required deltathetas
        for i in range(self.kooka.points):
            #print(self.kooka.servoAngles[i])
            #self.deltastosend[i][0] = self.deltastosend[i][0]
            #self.deltastosend[i][1] = self.deltastosend[i][1]
            self.deltastosend[i][0] = -3*self.deltastosend[i][0]
            self.deltastosend[i][1] = -1*self.deltastosend[i][1]

            self.deltastosendOpposite[i][0] = -3*self.deltastosendOpposite[i][0]
            self.deltastosendOpposite[i][1] = -1*self.deltastosendOpposite[i][1]
            #print(self.deltastosend[i])


    def calibr(self):
        message = "c"
        self.USB1.ser.write(message.encode())
        retVal = self.USB1.ser.read()
        if(retVal == "d"):
            self.terminal.append("Joint 1 is calibrated.")
        else:
            self.terminal.append("Joint 1 calibration failed.")

        # self.USB2.ser.write(message.encode())
        #retVal = self.USB2.ser.read()
        # if(retVal == "d"):
        #    self.terminal.append("Joint 2 is calibrated.")
        # else:
        #    self.terminal.append("Joint 2 calibration failed.")
        # self.USB3.ser.write(message.encode())
        #retVal = self.USB3.ser.read()
        # if(retVal == "d"):
        #    self.terminal.append("Joint 3 is calibrated.")
        # else:
        #    self.terminal.append("Joint 3 calibration failed.")
        # return True

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

    def stirring(self):

        '''
        ## this is for debugging (line 329 - 347)
        if(self.newplanning == True):
            self.i = 1
            self.newplanning = False

        self.goal = self.tra[self.i]
        self.i+=1
        if(self.i == self.kooka.points):
            self.i = 0

        ## visualize the robot's position changes in the GUI
        angles = self.kooka.ik(self.goal)
        self.kooka.joint_ang_new = np.array([angles[0], angles[1], angles[2], angles[3]])
        self.kooka.deltaThetas = 180/math.pi*self.kooka.diff()
        print(self.kooka.deltaThetas)
        # display angle values of the new joints in the GUI's text boxes
        self.vis.showAngle(self.angleSlots, self.kooka.joint_ang_new)
        
        #self.kooka.deltaThetas = 180/math.pi*self.kooka.diff()
        #print(self.kooka.deltaThetas)

        self.kooka.currenAngUpdate()
        self.vis.updateCurrentPos()
        self.vis.draw()
        '''

        revolutions = int(self.rev_slot.text())

####### acceleration version
        if(self.fullyConencted == True):
            n_a = 10
            n = self.kooka.points - n_a
            xxx = 1
            for j in range(revolutions):

                if(j%2 == 0):

                    #accelerating loop
                    for i in range(n_a):
                        self.USB1.send(xxx*self.deltastosend[0][0]*i/n_a, 'x')
                        ## shouldn't it be self.deltastosend[0][0] ???
                        self.USB2.send(xxx*self.deltastosend[0][1]*i/n_a, 'x')
                        self.USB3.send(xxx*self.deltastosend[0][2]*i/n_a, 'x')
                        self.USB3.send(self.kooka.servoAngles[0], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)
                    #const speed loop
                    for i in range(int(n-1)):
                        self.USB1.send(xxx*self.deltastosend[i+1][0], 'x')
                        self.USB2.send(xxx*self.deltastosend[i+1][1], 'x')
                        self.USB3.send(xxx*self.deltastosend[i+1][2], 'x')
                        self.USB3.send(self.kooka.servoAngles[i+1], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)
                    for i in range(n_a):
                        self.USB1.send(xxx*self.deltastosend[self.kooka.points-1][0]*(1-(i+1)/n_a), 'x')
                        self.USB2.send(xxx*self.deltastosend[self.kooka.points-1][1]*(1-i/n_a), 'x')
                        self.USB3.send(xxx*self.deltastosend[self.kooka.points-1][2]*(1-i/n_a), 'x')
                        self.USB3.send(self.kooka.servoAngles[self.kooka.points-1], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)

                else:

                    #accelerating loop
                    for i in range(n_a):
                        self.USB1.send(xxx*self.deltastosendOpposite[0][0]*i/n_a, 'x')
                        ## shouldn't it be self.deltastosend[0][0] ???
                        self.USB2.send(xxx*self.deltastosendOpposite[0][1]*i/n_a, 'x')
                        self.USB3.send(xxx*self.deltastosendOpposite[0][2]*i/n_a, 'x')
                        self.USB3.send(self.kooka.servoAngles[0], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)
                    #const speed loop
                    for i in range(int(n-1)):
                        self.USB1.send(xxx*self.deltastosendOpposite[i+1][0], 'x')
                        self.USB2.send(xxx*self.deltastosendOpposite[i+1][1], 'x')
                        self.USB3.send(xxx*self.deltastosendOpposite[i+1][2], 'x')
                        self.USB3.send(self.kooka.servoAngles[i+1], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)
                    for i in range(n_a):
                        self.USB1.send(xxx*self.deltastosendOpposite[self.kooka.points-1][0]*(1-(i+1)/n_a), 'x')
                        self.USB2.send(xxx*self.deltastosendOpposite[self.kooka.points-1][1]*(1-i/n_a), 'x')
                        self.USB3.send(xxx*self.deltastosendOpposite[self.kooka.points-1][2]*(1-i/n_a), 'x')
                        self.USB3.send(self.kooka.servoAngles[self.kooka.points-1], 'y')
                        #print(self.deltastosend[0][0]*i/n_a+" "+self.deltastosend[0][1]*i/n_a+" "+self.deltastosend[0][2]*i/n_a)
                        #self.USB4.send(self.deltastosend[3]*180/math.pi, 'x')
                        time.sleep(0.02)



    def everything(self):
        self.send_cmd_cartesien()
        time.sleep(0.5)
        self.trajplan()
        time.sleep(0.5)
        self.stirring()