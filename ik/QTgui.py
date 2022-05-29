import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph.opengl as gl
import pyqtgraph as pg

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(250, 330, 900, 350)
    win.setWindowTitle("Kooka Control GUI")

    # send = QtWidgets.QPushButton(win)
    # send.move(240, 50) 

    # joint 1 (yaw)
    joint_1_label = QtWidgets.QLabel('Joint 1 : ', win)
    joint_1_label.move(20, 20)

    joint_1 = QtWidgets.QLineEdit(win)
    joint_1.move(80,20)
    joint_1.setFixedWidth(40)

    joint_1_x = QtWidgets.QLabel('x : ', win)
    joint_1_x.move(130, 20)

    joint_1_x_box = QtWidgets.QTextBrowser(win)
    joint_1_x_box.move(150, 20)
    joint_1_x_box.setFixedWidth(50)

    joint_1_y = QtWidgets.QLabel('y : ', win)
    joint_1_y.move(210, 20)

    joint_1_y_box = QtWidgets.QTextBrowser(win)
    joint_1_y_box.move(230, 20)
    joint_1_y_box.setFixedWidth(50)

    joint_1_z = QtWidgets.QLabel('z : ', win)
    joint_1_z.move(290, 20)

    joint_1_z_box = QtWidgets.QTextBrowser(win)
    joint_1_z_box.move(310, 20)
    joint_1_z_box.setFixedWidth(50)

    # joint 2 (shoulder)
    joint_2_label = QtWidgets.QLabel('Joint 2 : ', win)
    joint_2_label.move(20, 70)

    joint_2 = QtWidgets.QLineEdit(win)
    joint_2.move(80,70)
    joint_2.setFixedWidth(40)

    joint_2_x = QtWidgets.QLabel('x : ', win)
    joint_2_x.move(130, 70)

    joint_2_x_box = QtWidgets.QTextBrowser(win)
    joint_2_x_box.move(150, 70)
    joint_2_x_box.setFixedWidth(50)

    joint_2_y = QtWidgets.QLabel('y : ', win)
    joint_2_y.move(210, 70)

    joint_2_y_box = QtWidgets.QTextBrowser(win)
    joint_2_y_box.move(230, 70)
    joint_2_y_box.setFixedWidth(50)

    joint_2_z = QtWidgets.QLabel('z : ', win)
    joint_2_z.move(290, 70)

    joint_2_z_box = QtWidgets.QTextBrowser(win)
    joint_2_z_box.move(310, 70)
    joint_2_z_box.setFixedWidth(50)

    # joint 3 (elbow)
    joint_3_label = QtWidgets.QLabel('Joint 3 : ', win)
    joint_3_label.move(20, 120)

    joint_3 = QtWidgets.QLineEdit(win)
    joint_3.move(80,120)
    joint_3.setFixedWidth(40)

    joint_3_x = QtWidgets.QLabel('x : ', win)
    joint_3_x.move(130, 120)

    joint_3_x_box = QtWidgets.QTextBrowser(win)
    joint_3_x_box.move(150, 120)
    joint_3_x_box.setFixedWidth(50)

    joint_2_y = QtWidgets.QLabel('y : ', win)
    joint_2_y.move(210, 120)

    joint_2_y_box = QtWidgets.QTextBrowser(win)
    joint_2_y_box.move(230, 120)
    joint_2_y_box.setFixedWidth(50)

    joint_2_z = QtWidgets.QLabel('z : ', win)
    joint_2_z.move(290, 120)

    joint_2_z_box = QtWidgets.QTextBrowser(win)
    joint_2_z_box.move(310, 120)
    joint_2_z_box.setFixedWidth(50)

    # message box
    terminal_label = QtWidgets.QLabel('Terminal', win)
    terminal_label.move(20, 150)

    terminal = QtWidgets.QTextBrowser(win)
    terminal.move(20,180)
    terminal.setFixedWidth(200)
    terminal.setFixedHeight(150)
    terminal.append("asd")

    # buttons
    connect = QtWidgets.QPushButton('Connect', win)
    connect.move(260, 180)

    connect = QtWidgets.QPushButton('Calibrate', win)
    connect.move(260, 220)

    connect = QtWidgets.QPushButton('Command', win)
    connect.move(260, 260)

    connect = QtWidgets.QPushButton('Stir', win)
    connect.move(260, 300)

    view=gl.GLViewWidget(win)
    view.move(400,10)
    view.setFixedWidth(460)
    view.setFixedHeight(330)
    gx = gl.GLGridItem()
    gx.rotate(90, 0, 1, 0)
    gx.translate(-10, 0, 0)
    view.addItem(gx)
    gy = gl.GLGridItem()
    gy.rotate(90, 1, 0, 0)
    
    gy.translate(0, -10, 0)
    view.addItem(gy)
    gz = gl.GLGridItem()
    gz.translate(0, 0, -10)
    view.addItem(gz)

    win.show()
    sys.exit(app.exec_())

window()