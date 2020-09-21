import FaBo9Axis_MPU9250
import time
import sys
import socket
import json

# Define Functions:

def createSocket(IP, Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    s.listen(5)
    clientsocket, address = s.accept()
    print("Socket Created")
    return clientsocket

def sendSocket(Xgyro, Ygyro, Zgyro, clientsocket):
    m = {}
    m['X'] = [Xgyro]
    m['Y'] = [Ygyro]
    m['Z'] = [Zgyro]
    msg = json.dumps(m)
    msg = msg + '\n'
    clientsocket.send(bytes(msg))
    print('sent dictionary')
    
def readIMU():
    gyro = mpu9250.readGyro()
    Xgyro = gyro['x']
    Ygyro = gyro['y']
    Zgyro = gyro['z']
    print(Xgyro, Ygyro, Zgyro)
    return Xgyro, Ygyro, Zgyro

# Global Variables and Objects:
mpu9250= FaBo9Axis_MPU9250.MPU9250()
IP = "192.168.0.102"
PORT = 1234

# Program Starts Here:

clientsocket = createSocket(IP, PORT)

while True:
    Xgyro, Ygyro, Zgyro = readIMU()
    sendSocket(Xgyro, Ygyro, Zgyro, clientsocket)
    time.sleep(0.1)
