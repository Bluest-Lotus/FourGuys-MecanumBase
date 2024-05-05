import bluetooth
from bluetooth import Protocols
import time
import pygame
import MecanumCarClass
import math
mech = MecanumCarClass.Car()

Stick = True
Blutooth = True

messageBytes = b''

if(Stick):
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

if(Blutooth):
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
    sock = bluetooth.BluetoothSocket(Protocols.RFCOMM)
    sock.connect((address, port))

axes = [0 for i in range(6)]
axesAdj = [0,0.004,0,0,0,0]
buttons = [0 for i in range(10)]

def printJoyInputs():
    messageString = ""
    for a in range(6):
        messageString += 'Ax%d:%3d | '% (a, axes[a]) + " "
    for b in range(10):
        messageString += 'Bt%d:%d | '% (b, buttons[b]) + " "
    print(messageString)

def sayHi():
    for x in range(5):
        sock.send((125).to_bytes(1, byteorder='big')+b'\x01'+b'\x00'+b'\xff')
        time.sleep(0.01)
    print("I already said hey")
    sock.close() 


def remoteControlMessageBytes():
    global messageBytes
    for axis in range(6):
        axes[axis] = int(100*(round(joystick.get_axis(axis)+axesAdj[axis],2)+1))
        messageBytes += axes[axis].to_bytes(1,byteorder='big')
    for button in range(10):
        buttons[button] = joystick.get_button(button)
        messageBytes += buttons[button].to_bytes(1,byteorder='big')

def thetaPowerControlMessageBytes():
    global messageBytes
    for axis in range(6):
        axes[axis] = joystick.get_axis(axis)+axesAdj[axis]
    angle = math.degrees(math.atan2(-axes[1], axes[0]))
    power = math.hypot(axes[0], axes[1]) % 360
    turn  = axes[2]
    percentages = mech.sendMotorInstructions(angle, power, turn)
    for i in range(4):
        messageBytes += str(percentages[i]).encode() + b' '
    # valueA = 0 # left front  -- actually controls left back
    # valueB = 0  # right front -- actually right back
    # valueC = 0 # left back   -- actually left front
    # valueD = -110    #right back   -- actually right front
    # messageBytes += str(valueA).encode() + b' '
    # messageBytes += str(valueB).encode() + b' '
    # messageBytes += str(valueC).encode() + b' '
    # messageBytes += str(valueD).encode() + b' '

while True:
    pygame.event.get()
    
    messageBytes = b''
    # remoteControlMessageBytes()
    thetaPowerControlMessageBytes()
    sock.send(messageBytes)
    
    time.sleep(0.09)

valueA = -100 
valueB = 255
valueC = -255
valueD = 0
for i in range(10):
    messageBytes = b''

    messageBytes += str(valueA).encode() + b' '
    messageBytes += str(valueB).encode() + b' '
    messageBytes += str(valueC).encode() + b' '
    messageBytes += str(valueD).encode() + b' '
    
    # messageBytes += b'-235 '
    # remoteControlMessageBytes()
    sock.send(messageBytes)
    time.sleep(0.1)

