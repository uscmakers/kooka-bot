from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import numpy as np
import math

class visualizer:
    def __init__(self, robot, graph):
        self.robot = robot
        self.pose = self.obtainPose()
        self.graph = graph
        self.new_pos = gl.GLLinePlotItem(pos = self.pose, width = 1, color=(1, 0, 0, 1), antialias = True) 
        self.current_pos = gl.GLLinePlotItem(pos = self.pose, width = 1, color=(1, 1, 0, 1), antialias = True) 
        self.graph.addItem(self.new_pos)
        self.graph.addItem(self.current_pos)
        self.traj = None

    # return xyz coordinates of the robot's joints
    def obtainPose(self):
        pos_zero = (self.robot.x[0], self.robot.y[0], self.robot.z[0])
        pos_one = (self.robot.x[1], self.robot.y[1], self.robot.z[1])
        pos_two = (self.robot.x[2], self.robot.y[2], self.robot.z[2])
        pos_three = (self.robot.x[3], self.robot.y[3], self.robot.z[3])

        positions = np.array([pos_zero, pos_one, pos_two, pos_three])

        return positions

    # visualize all of the joints' new current positions upon sending a command
    def updateCurrentPos(self):
        self.graph.items.remove(self.current_pos)
        self.current_pos = gl.GLLinePlotItem(pos = self.obtainPose(), width = 1, color=(1, 1, 0, 1), antialias = True)
        self.graph.addItem(self.current_pos)

    # update and visualize all of the joints' future positions upon using sliders
    def draw(self):
        self.robot.cmd(self.robot.joint_ang_new)
        self.graph.items.remove(self.new_pos)
        self.pose = self.obtainPose()
        self.new_pos = gl.GLLinePlotItem(pos = self.pose, width = 1,color=(1, 0, 0, 1), antialias = True) 
        self.graph.addItem(self.new_pos)

    # display angle values of the joints in the GUI's text boxes
    def showAngle(self, slots, angles):
        slots[0].setText(str(format(angles[0]*180.0/math.pi, ".1f")))
        slots[1].setText(str(format(angles[1]*180.0/math.pi, ".1f")))
        slots[2].setText(str(format(angles[2]*180.0/math.pi, ".1f")))
        slots[3].setText(str(format(angles[3]*180.0/math.pi, ".1f")))

    # display the planned trajectories
    def showTraejc(self, traje):
        if(self.traj !=None):
            self.graph.items.remove(self.traj)
        self.traj = gl.GLLinePlotItem(pos = traje, width = 1, color=(1, 0, 1, 1), antialias = True)
        self.graph.addItem(self.traj)
