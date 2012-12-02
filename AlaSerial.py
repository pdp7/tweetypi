#!/usr/bin/python

from time import sleep
from serial import Serial

def checkSerial():
    ser = Serial('/dev/ttyS0', baudrate=9600, timeout=1)
    out = True
#    msg = "1234567890"
    msg = "Repository for Python scripts to display tweets on a character LCD connected to a Raspberry Pi."
    n = len(msg)

    ser.write(msg);
    sleep(1);
    data = ser.read(n)
    print 'checkSerial() data:', data
    if len(data) != n:
        out = False
    else:
        out = data == msg
    return out;

checkSerial()
