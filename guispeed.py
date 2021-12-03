from tkinter import *
import time
import numpy as np
import serial

try:
    ser = serial.Serial('/dev/ttyACM0',9600)
except:
    print("The serial port doesn't exist.")

root = Tk()
root.geometry("300x250")

def sendCmd():
    try:
        yy=stepper_1.get()+"w"+stepper_2.get()+"x"+stepper_3.get()+"y"+stepper_4.get()+"z"
        ser.write(yy.encode())
    except:
        print("No microcontroller is connected.")

r_wheel_cmm = Label(root, text ='Right Wheel Velocity Command [rad/s]') 
r_wheel_cmm.place(relx=10, rely=5,anchor = 'center')
l_wheel_cmm = Label(root, text ='Left Wheel Velocity Command [rad/s]') 
l_wheel_cmm.place(relx=20, rely=10,anchor = 'center')

stepper_1 = Entry(root, width=10)
stepper_1.pack(side=TOP, padx=0, pady=5)

stepper_2 = Entry(root, width=10)
stepper_2.pack(side=TOP, padx=0, pady=10)

stepper_3 = Entry(root, width=10)
stepper_3.pack(side=TOP, padx=0, pady=13)

stepper_4 = Entry(root, width=10)
stepper_4.pack(side=TOP, padx=0, pady=14)

cmd = Button(root, text="Command", command = sendCmd).pack(side=TOP, padx=0, pady=10)

root.mainloop()