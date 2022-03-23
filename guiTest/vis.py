from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import numpy as np
import math

class visualizer:
    def __init__(self, robot, graph):
        self.robot = robot
        self.pose = self.assign_pos()
        self.graph = graph
        self.new_pos = gl.GLLinePlotItem(pos = self.pose, width = 1, color=(1, 0, 0, 1), antialias = True)
        self.current_pos = gl.GLLinePlotItem(pos = self.pose, width = 1, color=(1, 1, 0, 1), antialias = True)
        self.graph.addItem(self.new_pos)
        self.graph.addItem(self.current_pos)

    def assign_pos(self):
        pos_zero = (self.robot.x[0], self.robot.y[0], self.robot.z[0])
        pos_one = (self.robot.x[1], self.robot.y[1], self.robot.z[1])
        pos_two = (self.robot.x[2], self.robot.y[2], self.robot.z[2])
        pos_three = (self.robot.x[3], self.robot.y[3], self.robot.z[3])

        positions = np.array([pos_zero, pos_one, pos_two, pos_three])

        return positions

    def updateCurrentPos(self):
        self.graph.items.remove(self.current_pos)
        self.current_pos = gl.GLLinePlotItem(pos = self.assign_pos(), width = 1, color=(1, 1, 0, 1), antialias = True)
        self.graph.addItem(self.current_pos)

    def draw(self):
        self.robot.cmd(self.robot.joint_ang_new)
        self.graph.items.remove(self.new_pos)
        self.pose = self.assign_pos()
        self.new_pos = gl.GLLinePlotItem(pos = self.pose, width = 1,color=(1, 0, 0, 1), antialias = True)
        self.graph.addItem(self.new_pos)

    def showAngle(self, slots, angles):
        slots[0].setText(str(format(angles[0]*180.0/math.pi, ".1f")))
        slots[1].setText(str(format(angles[1]*180.0/math.pi, ".1f")))
        slots[2].setText(str(format(angles[2]*180.0/math.pi, ".1f")))
        slots[3].setText(str(format(angles[3]*180.0/math.pi, ".1f")))

    def showTraejc(self, traje):
        trajectories = gl.GLLinePlotItem(pos = traje, width = 1, color=(1, 0, 1, 1), antialias = True)
        self.graph.addItem(trajectories)
