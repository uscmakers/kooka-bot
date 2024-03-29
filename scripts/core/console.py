import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph.opengl as gl
import serial

class Console(object):
    def setup(self, widget):
        super(Console, self).__init__()
        self.setGeometry(250, 330, 900, 350)
        self.setFixedSize(900, 350)
        self.setWindowTitle("Kooka")

        # joint 1
        self.joint_1_label = QtWidgets.QLabel('Yaw :' , self)
        self.joint_1_label.move(7, 20)

        self.joint_1_box = QtWidgets.QTextBrowser(self)
        self.joint_1_box.move(80, 20)
        self.joint_1_box.setFixedWidth(55)
        self.joint_1_slider = QtWidgets.QSlider(self)
        self.joint_1_slider.setOrientation(QtCore.Qt.Horizontal)
        self.joint_1_slider.setGeometry(QtCore.QRect(145, 30, 160, 16))
        self.joint_1_slider.setMinimum(-90)
        self.joint_1_slider.setMaximum(90)
        self.joint_1_slider.setObjectName('0')

        self.delta_1_label = QtWidgets.QLabel('Δθ :' , self)
        self.delta_1_label.move(310, 20)

        self.delta_1 = QtWidgets.QTextBrowser(self)
        self.delta_1.move(340, 20)
        self.delta_1.setFixedWidth(55)

        # joint 2
        self.joint_2_label = QtWidgets.QLabel('Shoulder :' , self)
        self.joint_2_label.move(7, 70)

        self.joint_2_box = QtWidgets.QTextBrowser(self)
        self.joint_2_box.move(80, 70)
        self.joint_2_box.setFixedWidth(55)

        self.joint_2_slider = QtWidgets.QSlider(self)
        self.joint_2_slider.setOrientation(QtCore.Qt.Horizontal)
        self.joint_2_slider.setGeometry(QtCore.QRect(145, 30+50, 160, 16))
        self.joint_2_slider.setMinimum(45)
        self.joint_2_slider.setMaximum(135)
        self.joint_2_slider.setObjectName('1')

        self.delta_2_label = QtWidgets.QLabel('Δθ :' , self)
        self.delta_2_label.move(310, 70)

        self.delta_2 = QtWidgets.QTextBrowser(self)
        self.delta_2.move(340, 70)
        self.delta_2.setFixedWidth(55)

        # joint 3
        self.joint_3_label = QtWidgets.QLabel('Elbow :' , self)
        self.joint_3_label.move(7, 120)

        self.joint_3_box = QtWidgets.QTextBrowser(self)
        self.joint_3_box.move(80, 120)
        self.joint_3_box.setFixedWidth(55)

        self.joint_3_slider = QtWidgets.QSlider(self)
        self.joint_3_slider.setOrientation(QtCore.Qt.Horizontal)
        self.joint_3_slider.setGeometry(QtCore.QRect(145, 30+100, 160, 16))
        self.joint_3_slider.setMinimum(0)
        self.joint_3_slider.setMaximum(180)
        self.joint_3_slider.setObjectName('2')

        self.delta_3_label = QtWidgets.QLabel('Δθ :' , self)
        self.delta_3_label.move(310, 120)

        self.delta_3 = QtWidgets.QTextBrowser(self)
        self.delta_3.move(340, 120)
        self.delta_3.setFixedWidth(55)

        # joint 4
        self.joint_4_label = QtWidgets.QLabel('Wrist :' , self)
        self.joint_4_label.move(7, 170)

        self.joint_4_box = QtWidgets.QTextBrowser(self)
        self.joint_4_box.move(80, 170)
        self.joint_4_box.setFixedWidth(55)

        self.joint_4_slider = QtWidgets.QSlider(self)
        self.joint_4_slider.setOrientation(QtCore.Qt.Horizontal)
        self.joint_4_slider.setGeometry(QtCore.QRect(145, 30+150, 160, 16))
        self.joint_4_slider.setMinimum(0)
        self.joint_4_slider.setMaximum(90)
        self.joint_4_slider.setObjectName('3')

        self.delta_4_label = QtWidgets.QLabel('Δθ :' , self)
        self.delta_4_label.move(310, 170)

        self.delta_4 = QtWidgets.QTextBrowser(self)
        self.delta_4.move(340, 170)
        self.delta_4.setFixedWidth(55)

        # message box
        self.terminal_label = QtWidgets.QLabel('Terminal', self)
        self.terminal_label.move(20, 200)
        self.terminal = QtWidgets.QTextBrowser(self)
        self.terminal.move(20,150+80)
        self.terminal.setFixedWidth(200)
        self.terminal.setFixedHeight(150)

        # buttons
        self.connec = QtWidgets.QPushButton('Connect', self)
        self.connec.move(260, 230)

        self.calibrate = QtWidgets.QPushButton('Calibrate', self)
        self.calibrate.move(260, 270)

        self.command = QtWidgets.QPushButton('Command', self)
        self.command.move(260, 310)

        self.cartesian = QtWidgets.QPushButton('Command [xyz]', self)
        self.cartesian.move(390, 390)
        self.cartesian.setFixedWidth(110)

        # self.command.clicked.connect(self.send_cmd)

        self.stir = QtWidgets.QPushButton('Stir', self)
        self.stir.move(260, 350)


        self.planner = QtWidgets.QPushButton('Plan', self)
        self.planner.move(260, 390)

        # 3D visualization
        self.view=gl.GLViewWidget(self)
        self.view.move(550,10)
        self.view.setFixedWidth(460)
        self.view.setFixedHeight(430)
        self.gx = gl.GLGridItem()
        self.gx.rotate(0, 0, 0, 0)
        self.gx.translate(0, 0, 0)
        self.gx.scale(0.05, 0.05, 0)
        self.view.addItem(self.gx)

        # USB slots
        # USB 1
        self.usb_1 = QtWidgets.QLabel('USB 1 :' , self)
        self.usb_1.move(400, 20)
        self.usb_1_slot = QtWidgets.QLineEdit(self)
        self.usb_1_slot.move(448,20)

        # USB 2
        self.usb_2 = QtWidgets.QLabel('USB 2 :' , self)
        self.usb_2.move(400, 70)
        self.usb_2_slot = QtWidgets.QLineEdit(self)
        self.usb_2_slot.move(448,70)

        # USB 3
        self.usb_3 = QtWidgets.QLabel('USB 3 :' , self)
        self.usb_3.move(400, 120)
        self.usb_3_slot = QtWidgets.QLineEdit(self)
        self.usb_3_slot.move(448,120)

        # time intervial
        self.dt = QtWidgets.QLabel('Vel (deg/sec) :' , self)
        self.dt.move(410,450)
        self.dt_slot = QtWidgets.QLineEdit(self)
        self.dt_slot.move(510,450)
        self.dt_slot.setFixedWidth(55)

        self.rev = QtWidgets.QLabel('Revolutions: ',self)
        self.rev.move(610,450)
        self.rev_slot = QtWidgets.QLineEdit(self)
        self.rev_slot.move(710,450)
        self.rev_slot.setFixedWidth(55)

        self.points = QtWidgets.QLabel('Points: ',self)
        self.points.move(810,450)
        self.points_slot = QtWidgets.QLineEdit(self)
        self.points_slot.move(870,450)
        self.points_slot.setFixedWidth(55)

        self.radius = QtWidgets.QLabel('Radius: ',self)
        self.radius.move(280,450)
        self.radius_slot = QtWidgets.QLineEdit(self)
        self.radius_slot.move(335,450)
        self.radius_slot.setFixedWidth(55)
        
        # Goals
        self.goalpose = QtWidgets.QLabel('Goal', self)
        self.goalpose.move(400, 230)

        # x goal
        self.xgoal = QtWidgets.QLabel('X [m]:', self)
        self.xgoal.move(390, 270)
        self.xslot = QtWidgets.QLineEdit(self)
        self.xslot.move(440, 270)
        self.xslot.setFixedWidth(55)

        # y goal
        self.ygoal = QtWidgets.QLabel('Y [m]:', self)
        self.ygoal.move(390, 310)
        self.yslot = QtWidgets.QLineEdit(self)
        self.yslot.move(440, 310)
        self.yslot.setFixedWidth(55)

        # z goal
        self.zgoal = QtWidgets.QLabel('Z [m]:', self)
        self.zgoal.move(390, 350)
        self.zslot = QtWidgets.QLineEdit(self)
        self.zslot.move(440, 350)
        self.zslot.setFixedWidth(55)

        self.every = QtWidgets.QPushButton('Everything', self)
        self.every.move(80, 420)