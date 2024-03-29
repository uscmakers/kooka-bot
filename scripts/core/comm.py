import serial

class comm:
    def __init__(self, name, baud=115200):
        self.baud = baud
        self.usb = ''
        self.ser = ''
        self.connected = False
        self.name = name

    def send(self, command, key):
        cmd = str(command)+str(key)
        self.ser.write(cmd.encode())

    def connection(self, usbport):
        self.ser = serial.Serial(usbport, self.baud)
        self.usb = usbport
        self.connected = True