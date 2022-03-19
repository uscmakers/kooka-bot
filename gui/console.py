import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph.opengl as gl
import serial

class Console(object):
    def setup(self, widget):
        super(Console, self).__init__()
        self.setGeometry(250, 330, 900, 350)
        self.setWindowTitle("Kooka")
        self.usb1 = 'COM13'
        self.usb2 = 'COM20'
        self.usb3 = 'COM21'
        self.ser1 = ''
        self.ser2 = ''
        self.ser3 = ''
        self.baud = 9600
        try:
            self.ser1 = serial.Serial(self.usb1,self.baud)
            print("Connected")
            
        except:
            print("USB1 Not Connected")
        try:
            self.ser2 = serial.Serial(self.usb2,self.baud)
            print("Connected")
            
        except:
            print("USB2 Not Connected")
        try:
            self.ser3 = serial.Serial(self.usb3,self.baud)
            print("Connected")
            
        except:
            print("USB3 Not Connected")

        self.joint_1_ang = 0
        self.joint_2_ang = 0
        self.joint_3_ang = 0

        # joint 1
        self.joint_1_label = QtWidgets.QLabel('Joint 1 :' , self)
        self.joint_1_label.move(20, 20)

        self.joint_1 = QtWidgets.QLineEdit(self)
        self.joint_1.move(20+60,20)
        self.joint_1.setFixedWidth(40)

        self.joint_1_x = QtWidgets.QLabel('x : ', self)
        self.joint_1_x.move(20+110, 20)

        self.joint_1_x_box = QtWidgets.QTextBrowser(self)
        self.joint_1_x_box.move(20+130, 20)
        self.joint_1_x_box.setFixedWidth(50)

        self.joint_1_y = QtWidgets.QLabel('y : ', self)
        self.joint_1_y.move(20+190, 20)

        self.joint_1_y_box = QtWidgets.QTextBrowser(self)
        self.joint_1_y_box.move(20+210, 20)
        self.joint_1_y_box.setFixedWidth(50)

        self.joint_1_z = QtWidgets.QLabel('z : ', self)
        self.joint_1_z.move(20+270, 20)

        self.joint_1_z_box = QtWidgets.QTextBrowser(self)
        self.joint_1_z_box.move(20+290, 20)
        self.joint_1_z_box.setFixedWidth(50)

        # joint 2
        self.joint_2_label = QtWidgets.QLabel('Joint 2 :' , self)
        self.joint_2_label.move(20, 70)

        self.joint_2 = QtWidgets.QLineEdit(self)
        self.joint_2.move(20+60,70)
        self.joint_2.setFixedWidth(40)

        self.joint_2_x = QtWidgets.QLabel('x : ', self)
        self.joint_2_x.move(20+110, 70)

        self.joint_2_x_box = QtWidgets.QTextBrowser(self)
        self.joint_2_x_box.move(20+130, 70)
        self.joint_2_x_box.setFixedWidth(50)

        self.joint_2_y = QtWidgets.QLabel('y : ', self)
        self.joint_2_y.move(20+190, 70)

        self.joint_2_y_box = QtWidgets.QTextBrowser(self)
        self.joint_2_y_box.move(20+210, 70)
        self.joint_2_y_box.setFixedWidth(50)

        self.joint_2_z = QtWidgets.QLabel('z : ', self)
        self.joint_2_z.move(20+270, 70)

        self.joint_2_z_box = QtWidgets.QTextBrowser(self)
        self.joint_2_z_box.move(20+290, 70)
        self.joint_2_z_box.setFixedWidth(50)

        # joint 3
        self.joint_3_label = QtWidgets.QLabel('Joint 3 :' , self)
        self.joint_3_label.move(20, 120)

        self.joint_3 = QtWidgets.QLineEdit(self)
        self.joint_3.move(20+60,120)
        self.joint_3.setFixedWidth(40)

        self.joint_3_x = QtWidgets.QLabel('x : ', self)
        self.joint_3_x.move(20+110, 120)

        self.joint_3_x_box = QtWidgets.QTextBrowser(self)
        self.joint_3_x_box.move(20+130, 120)
        self.joint_3_x_box.setFixedWidth(50)

        self.joint_3_y = QtWidgets.QLabel('y : ', self)
        self.joint_3_y.move(20+190, 120)

        self.joint_3_y_box = QtWidgets.QTextBrowser(self)
        self.joint_3_y_box.move(20+210, 120)
        self.joint_3_y_box.setFixedWidth(50)

        self.joint_3_z = QtWidgets.QLabel('z : ', self)
        self.joint_3_z.move(20+270, 120)

        self.joint_3_z_box = QtWidgets.QTextBrowser(self)
        self.joint_3_z_box.move(20+290, 120)
        self.joint_3_z_box.setFixedWidth(50)

        # message box
        self.terminal_label = QtWidgets.QLabel('Terminal', self)
        self.terminal_label.move(20, 150)
        self.terminal = QtWidgets.QTextBrowser(self)
        self.terminal.move(20,150+30)
        self.terminal.setFixedWidth(200)
        self.terminal.setFixedHeight(150)

        # buttons
        self.connect = QtWidgets.QPushButton('Connect', self)
        self.connect.move(260, 180)

        self.calibrate = QtWidgets.QPushButton('Calibrate', self)
        self.calibrate.move(260, 220)

        self.command = QtWidgets.QPushButton('Command', self)
        self.command.move(260, 260)

        # self.command.clicked.connect(self.send_cmd)

        self.stir = QtWidgets.QPushButton('Stir', self)
        self.stir.move(260, 300)

        # 3D visualization
        self.view=gl.GLViewWidget(self)
        self.view.move(400,10)
        self.view.setFixedWidth(460)
        self.view.setFixedHeight(330)
        self.gx = gl.GLGridItem()
        self.gx.rotate(90, 0, 1, 0)
        self.gx.translate(-10, 0, 0)
        self.view.addItem(self.gx)
        self.gy = gl.GLGridItem()
        self.gy.rotate(90, 1, 0, 0)
        self.gy.translate(0, -10, 0)
        self.view.addItem(self.gy)
        self.gz = gl.GLGridItem()
        self.gz.translate(0, 0, -10)
        self.view.addItem(self.gz)