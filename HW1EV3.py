#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.iodevices import UARTDevice
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import ubinascii, ujson, urequests, utime
import socket

# Create your objects here.
ev3 = EV3Brick()
LeftMotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
RightMotor = Motor(Port.D, Direction.COUNTERCLOCKWISE)

IP = "192.168.0.102"
PORT = 1234

# Define Functions to communicate with Pi:
def SetupSocket(IP, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    print("Setup Socket")
    return s

def UnpackSocket(s):
    msg = s.recv(256)
    print(msg)
    msg = msg.decode('utf-8')
    msg = msg.split('/n')[0]
    Gyro = ujson.loads(msg)
    XGyro = Gyro['X'][0]
    YGyro = Gyro['Y'][0]
    ZGyro = Gyro['Z'][0]
    return XGyro, YGyro, ZGyro

# Code starts here
ev3.speaker.beep()
s = SetupSocket(IP, PORT)

while True:
    XGyro, YGyro, ZGyro = UnpackSocket(s)
    AbsX = abs(XGyro)
    AbsY = abs(YGyro)
    AbsZ = abs(ZGyro)
    OutstandingAngle = max(AbsX, AbsY, AbsZ)

    # This enables the robot to turn while it moves backwards
    multiplicationTerm = 1
    if XGyro > 30:
        multiplicationTerm = 1
    elif XGyro < -30:
        multiplicationTerm = -1

    # This tells the motors how to move.
    if OutstandingAngle == AbsX:
        if XGyro > 0:
            print("Move Backward")
            LeftMotor.run(-800)
            RightMotor.run(-800)
        else:
            print("Move Forward")
            LeftMotor.run(800)
            RightMotor.run(800)
    elif OutstandingAngle == AbsY: 
        if YGyro > 0:
            print("Turn Right")
            LeftMotor.run(multiplicationTerm*800)
            RightMotor.run(multiplicationTerm*100)
        else: 
            print("Turn Left")
            LeftMotor.run(multiplicationTerm*100)
            RightMotor.run(multiplicationTerm*800)
    elif  OutstandingAngle == AbsZ:
        if ZGyro > 0:
            print("Turn Left")
            LeftMotor.run(multiplicationTerm*100)
            RightMotor.run(multiplicationTerm*800)
        else: 
            print("Turn Right")
            LeftMotor.run(multiplicationTerm*800)
            RightMotor.run(multiplicationTerm*100)



