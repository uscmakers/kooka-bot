from tkinter import *
import ikpy.chain
import time
import numpy as np
import serial


def sendCmd(joint_angles):
    try:
        message=joint_angles[0] + 'x' + joint_angles[0] + 'y' + joint_angles[0] + 'z'
        ser.write(message.encode())
    except Exception as e:
        print("Error writing to serial:")
        print(e)

def runIk(chain):
    target_position = [x_loc.get(), y_loc.get(), z_loc.get()]
    joint_angles=chain.inverse_kinematics(target_position)
    sendCmd(joint_angles)

try:
    ser = serial.Serial('/dev/cu.usbmodem14401',9600)
except Exception as e:
    print("There was an error connecting to the serial port:")
    print(e)

try:
    chain = ikpy.chain.Chain.from_urdf_file("path_to_urdf")
except Exception as e:
    print("Error accessing URDF")
    print(e)

root = Tk()
root.geometry("300x250")

r_wheel_cmm = Label(root, text ='Right Wheel Velocity Command [rad/s]') 
r_wheel_cmm.place(relx=10, rely=5,anchor = 'center')
l_wheel_cmm = Label(root, text ='Left Wheel Velocity Command [rad/s]') 
l_wheel_cmm.place(relx=20, rely=10,anchor = 'center')

x_loc = Entry(root, width=10)
x_loc.pack(side=TOP, padx=0, pady=5)

y_loc = Entry(root, width=10)
y_loc.pack(side=TOP, padx=0, pady=10)

z_loc = Entry(root, width=10)
z_loc.pack(side=TOP, padx=0, pady=13)


cmd = Button(root, text="Command", command = runIk(chain)).pack(side=TOP, padx=0, pady=10)

root.mainloop()


