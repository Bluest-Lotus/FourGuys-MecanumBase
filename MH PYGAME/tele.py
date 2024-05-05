import MecanumCarClass
import time

myCar = MecanumCarClass.Car()

#myCar.initTele()
time.sleep(1)

while True:
    myCar.runTele()
    myCar.sendData()
    time.sleep(0.09)