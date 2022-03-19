from PyQt5 import QtCore, QtGui, QtWidgets
from console import Console
class UI(QtWidgets.QMainWindow, Console):
    def __init__(self):
        super().__init__()
        self.setup(self)
        self.command.clicked.connect(self.send_cmd)
    def send_cmd(self):
        try:
            joint_1_delta = float(self.joint_1.text())-float(self.joint_1_ang)
        except:
            self.terminal.append("Joint 1 command value is invalid.")
        try:
            joint_2_delta = float(self.joint_2.text())-float(self.joint_2_ang)
        except:
            self.terminal.append("Joint 2 command value is invaild.")
        try:
            joint_3_delta = float(self.joint_2.text())-float(self.joint_2_ang)
        except:
            self.terminal.append("Joint 3 command value is invaild.")
        if(self.joint_1.text().replace("-","").isdigit() and self.joint_2.text().replace("-","").isdigit() and self.joint_3.text().replace("-","").isdigit()):
            try:
                cmd1 = str(self.joint_1.text())+"x"
                print(cmd1)
                self.ser1.write(cmd1.encode())
            except:
                self.terminal.append("Connection with the robot x doesn’t exist.")
            try:
                cmd2 = str(self.joint_2.text())+"x"
                self.ser2.write(cmd2.encode())
            except:
                self.terminal.append("Connection with the robot y doesn’t exist.")
            try:
                cmd3 = str(self.joint_3.text())+"x"
                self.ser3.write(cmd3.encode())
            except:
                self.terminal.append("Connection with the robot z doesn’t exist.")
    def calibrate(self):
        self.ser1.write("c")
        retVal = self.ser1.read()
        if(retVal == "d"):
            self.terminal.append("Joint 1 is calibrated.")
        else:
            self.terminal.append("Joint 1 calibration failed.")
        self.ser2.wrtie("c")
        retVal = self.ser2.read()
        if(retVal == "d"):
            self.terminal.append("Joint 2 is calibrated.")
        else:
            self.terminal.append("Joint 2 calibration failed.")
        self.ser3.write("c")
        retVal = self.ser3.read()
        if(retVal == "d"):
            self.terminal.append("Joint 3 is calibrated.")
        else:
            self.terminal.append("Joint 3 calibration failed.")
        return True