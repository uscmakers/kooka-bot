import serial

ser = serial.Serial('/dev/ttyACM0',9600)

while(True):
    val = input("Speed command:")
    yy=val+"c"
    ser.write(yy.encode())