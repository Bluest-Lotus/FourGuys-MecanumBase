import math
import bluetooth
from bluetooth import Protocols
import time
import pygame

class Car():
    def __init__(self):
        self.messageBytes = b''
        self.currentNode = 0
        self.isMoving = False
        self.minDist = 50
        self.curSpeed = 0.6
        self.origSpeed = 0.6
        self.axes = [0 for i in range(6)]
        self.axesAdj = [0,0.004,0,0,0,0]
        self.buttons = [0 for i in range(10)]
        self.sp32 = 'SwerveBotDevKit'
        self.address = ''
        self.frame = 0
        print("at least this runs")
        devices = bluetooth.discover_devices()

        for addr in devices:
            print(addr)
            if self.sp32 == bluetooth.lookup_name(addr):
                self.address = addr
                print("found it")
                break
        port = 1
        self.sock = bluetooth.BluetoothSocket(Protocols.RFCOMM)
        self.sock.connect((self.address, port))
    def sendMotorInstructions(self, theta, power, turn):
        #compute 4 motor percents and send them with either socket or bluetooth

        #math.sin() returns in radians
        #convert this result to degrees w/ math.degrees()
        theta = math.radians(theta)
        # power = power * 255
        # turn = 0
        sin = math.sin(theta - math.pi/4);
        cos = math.cos(theta - math.pi/4);
        maximum = max(abs(sin), abs(cos));

        leftFront  = power * cos/maximum + turn;
        rightFront = power * sin/maximum - turn;
        leftRear   = power * sin/maximum + turn;
        rightRear  = power * cos/maximum - turn;

        if((power + abs(turn)) > 1):
            leftFront  /= power + abs(turn);
            rightFront /= power + abs(turn);
            leftRear   /= power + abs(turn);
            rightRear  /= power + abs(turn);
        #print([int(leftFront*255), int(rightFront*255), int(leftRear*255), int(rightRear*255)])
        return [int(leftFront*255), int(rightFront*255), int(leftRear*255), int(rightRear*255)]
    def setUpBTConnection(self):
        esp32 = 'SwerveBotDevKit'
        address = ''
        print("at least this runs")
        devices = bluetooth.discover_devices()

        for addr in devices:
            print(addr)
            if esp32 == bluetooth.lookup_name(addr):
                address = addr
                print("found it")
                break
        port = 1
        #self.sock = bluetooth.BluetoothSocket(Protocols.RFCOMM)
        #self.sock.connect((address, port))
    def callOutMotorInstructions(self, angle, power, turn):
        percentages = self.sendMotorInstructions(angle, power, turn)
        for i in range(4):
            self.messageBytes += str(percentages[i]).encode() + b' '
    def runCar(self, pathToTake, tip, tail):
        carCenter = self.getCenter(tip, tail)
        nextNode = pathToTake[self.currentNode]
        neededDegrees = self.getAngle(carCenter, nextNode)
        if math.hypot(carCenter[0]-pathToTake[self.currentNode][0], carCenter[1]-pathToTake[self.currentNode][1]) <= self.minDist:
            self.currentNode+=1
            if self.currentNode == len(pathToTake):
                self.isMoving = False
                self.messageBytes = b'0 0 0 0 0 0'
                #self.sock.send(self.messageBytes)
                self.curSpeed = self.origSpeed
                return
        self.callOutMotorInstructions(neededDegrees, self.curSpeed, 0)
        #self.sock.send(self.messageBytes)
        #time.sleep(0.09)
        self.curSpeed *= 0.92
        self.sendData()
    def getAngle(self, tail, tip):
        tipX, tipY = tip
        tailX, tailY = tail
        netXComponent = tip[0]-tail[0]
        netYComponent = -tip[1]+tail[1]
        deg = math.degrees(math.atan2(netYComponent, netXComponent))
        if deg < 0:
            deg = 360+deg
        return deg
    def getCenter(self, tail, tip):
        x1, y1 = tip
        x2, y2 = tail
        return [(x1+x2)//2, (y1+y2)//2]
    def runTele(self, joystick):
        self.frame+=1
        if self.frame % 6 == 0:
            self.messageBytes = b''
            for axis in range(6):
                self.axes[axis] = joystick.get_axis(axis)+self.axesAdj[axis]
            for axis in range(10):
                self.buttons[axis] = joystick.get_button(axis)
            angle = math.degrees(math.atan2(-self.axes[1], self.axes[0]))
            power = math.hypot(self.axes[0], self.axes[1]) % 360
            turn  = self.axes[2]
            percentages = self.sendMotorInstructions(angle, power, turn)
            for i in range(4):
                self.messageBytes += str(percentages[i]).encode() + b' '
            self.messageBytes += str(self.buttons[0]).encode() + b' '
            self.messageBytes += str(self.buttons[4]).encode() + b' '
            self.sendData()
    def sendData(self):
        self.sock.send(self.messageBytes)
        self.messageBytes = b''
        