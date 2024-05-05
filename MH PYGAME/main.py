import pygame
import cv2
import numpy
from pupil_apriltags import Detector
import threading
import sys
import MecanumCarClass
import graph
import button
import obstacle
import math
import target
import webbrowser
import time

menuScaleFactor = 0.9

WIDTH = 1920*menuScaleFactor
HEIGHT = 1080*menuScaleFactor

#initialize webcam code and what will be blitted to pygame

'''
BASIC PROCEDURE
-convert BGR format of image to RGB
-flip and rotate image 90 degrees with numpy
-display it
'''

tipTracker = cv2.TrackerCSRT()
tailTracker = cv2.TrackerCSRT()
tipTracked = False
tailTracked = False

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def getMidPoint(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return [(x1+x2)//2, (y1+y2)//2]

def camera_thread():
    global camera_pygame_frame
    global frameBGRGray
    global tip
    global tail
    while camera.isOpened():
        ret, frame = camera.read()
        frameBGRGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = aprilTagDetector.detect(frameBGRGray)
        # if not tipTracked and screenState == "auto-ob":
        #     hitbox = cv2.selectROI(frameBGRGray)
        #     tipTracker.init(frameBGRGray, hitbox)
        #     tipTracked = True
        # ok, box = tipTracker.update(frameBGRGray)
        # if ok:
        #     p1 = (int(box[0]), int(box[1]))
        #     p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
        #     cv2.rectangle(frameRGB, p1, p2, (255,0,0), 2)
        #draw detections
        if detections:
            for detection in detections:
                if (detection.tag_id == 2):
                    tip = detection.center.astype(int).tolist()
                elif (detection.tag_id == 0):
                    tail = detection.center.astype(int).tolist()
                corners = detection.corners.astype(int)
                cv2.polylines(frameRGB, [corners], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.circle(frameRGB, detection.center.astype(int), 5, (0, 255, 0), 2, cv2.LINE_AA)
        if tip != [] and tail != []:
            cv2.line(frameRGB, tip, tail, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.circle(frameRGB, getMidPoint(tip, tail), 50, (255, 0, 0), 5, cv2.LINE_AA)
        camera_pygame_frame = numpy.rot90(frameRGB)

aprilTagDetector = Detector(quad_sigma=0.1)
camera = cv2.VideoCapture(2, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(1280*0.80))
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(720*0.80))
pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
camera_pygame_frame = None
frameBGRGray = None
tip = []
tail = []
myClock = pygame.time.Clock()
running = True
camera_thr = threading.Thread(target=camera_thread, daemon=True)
camera_thr.start()
stopFlag = threading.Event()
myGraph = graph.Graph(100, 70, int(1024), int(576), 345, 280)
myCar = MecanumCarClass.Car()

screenState = "home"

buttonDict = {}
buttonDict["home"] = [button.Button(380, 590, 310, 90, "tele"), button.Button(1050, 590, 310, 90, "auto-choose"), button.Button(720, 590, 310, 90, "github", isRedirectingScreen=False)]
buttonDict["tele"] = [button.Button(100,50,255,80,"home")]
buttonDict["auto-ob"] = [button.Button(100,45,255,80,"home"), button.Button(585, 150, 255, 80, "obs", isRedirectingScreen=False), button.Button(890, 150, 255, 80, "target", isRedirectingScreen=False)]
buttonDict["auto-choose"] = [button.Button(540, 515, 310, 100, "auto-ob"), button.Button(875, 515, 310, 100, "to-mouse")]
buttonDict["to-mouse"] = [button.Button(100,50,255,80,"home")]

obstacles = []
targets = []

#LOAD IMAGES
home = pygame.image.load("img\\home.png").convert()
home = pygame.transform.scale(home, (home.get_width()*menuScaleFactor, home.get_height()*menuScaleFactor))
tele = pygame.image.load("img\\tele.png").convert()
tele = pygame.transform.scale(tele, (tele.get_width()*menuScaleFactor, tele.get_height()*menuScaleFactor))
auto_obstacle = pygame.image.load("img\\auto-obstacle.png").convert()
auto_obstacle = pygame.transform.scale(auto_obstacle, (auto_obstacle.get_width()*menuScaleFactor, auto_obstacle.get_height()*menuScaleFactor))
auto_choose = pygame.image.load("img\\auto-choose.png").convert()
auto_choose = pygame.transform.scale(auto_choose, (auto_choose.get_width()*menuScaleFactor, auto_choose.get_height()*menuScaleFactor))
to_mouse = pygame.image.load("img\\to-mouse.png").convert()
to_mouse = pygame.transform.scale(to_mouse, (to_mouse.get_width()*menuScaleFactor, to_mouse.get_height()*menuScaleFactor))

isDraggingObstacle = False
isDraggingTarget = False

while running:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            stopFlag.set()
            camera.release()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(obstacles)):
                if obstacles[i].isDeterminingThickness:
                    obstacles[i].isDeterminingThickness = False
            for i in range(len(targets)):
                if targets[i].isDeterminingThickness:
                    targets[i].isDeterminingThickness = False
            if isDraggingObstacle:
                curDraggedObstacle = []
                isDraggingObstacle = False
                obstacles.append(obstacle.Obstacle(mousePos[0], mousePos[1], isDragged=False))
            if isDraggingTarget:
                curDraggedTarget = []
                isDraggingTarget = False
                print("hello")
                localTargCoords = myGraph.getLocalTargetCoords(mousePos[0], mousePos[1])
                targets.append(target.Target(localTargCoords[0]-40, localTargCoords[1], isDragged=False))
                obstacles.append(obstacle.Obstacle(localTargCoords[0], localTargCoords[1], rad=targets[-1].w))
            for i in range(len(buttonDict[screenState])):
                if (buttonDict[screenState][i].pointCollided(mousePos[0], mousePos[1])):
                    if (buttonDict[screenState][i].isRedirectingScreen):
                        screenState = buttonDict[screenState][i].transitionScreen()
                        break
                    elif (buttonDict[screenState][i].transitionScreen() == "obs"):
                        if not isDraggingObstacle:
                            curDraggedObstacle = mousePos
                            isDraggingObstacle = True
                    elif buttonDict[screenState][i].transitionScreen() == "github":
                        webbrowser.open("https://bluest-lotus.github.io/FourGuys-MecanumBase/")
                    else:
                        if not isDraggingTarget:
                            curDraggedTarget = mousePos
                            isDraggingTarget = True
            myGraph.getLocalMouseCoords(mousePos[0]-myGraph.xOffset, mousePos[1]-myGraph.yOffset, obstacles, targets)
            if myGraph.globalEndingPos != []:
                myCar.isMoving = True
    if tip!=[] and tail!=[]:
        print(myCar.getAngle(tail, tip))
    if screenState == "home":
        obstacles = []
        screen.blit(home, (0,0))
        for i in range(len(buttonDict["home"])):
            buttonDict["home"][i].drawSelf(screen)
    elif camera_pygame_frame is not None and screenState == "tele":
        screen.blit(tele, (0,0))
        myImg = pygame.surfarray.make_surface(camera_pygame_frame)
        screen.blit(myImg, (345,190))
        for i in range(len(buttonDict["tele"])):
            buttonDict["tele"][i].drawSelf(screen)
        myCar.runTele(joystick)
    elif camera_pygame_frame is not None and screenState == "auto-ob":
        myImg = pygame.surfarray.make_surface(camera_pygame_frame)
        screen.blit(auto_obstacle, (0,0))
        screen.blit(myImg, (345,280))
        for i in range(len(buttonDict["auto-ob"])):
            buttonDict["auto-ob"][i].drawSelf(screen)
        myGraph.drawGraph(screen)
        if (isDraggingTarget):
            pygame.draw.rect(screen, (0, 0, 255), (mousePos[0], mousePos[1], 10, 20))
        for i in range(len(targets)):
            targets[i].drawSelf(screen)
        for i in range(len(targets)):
            if targets[i].isDeterminingThickness:
                targets[i].w = abs(targets[i].x-mousePos[0])
                targets[i].h = abs(targets[i].y-mousePos[1])
            targets[i].drawSelf(screen)
        ####################################################################################################
        if (isDraggingObstacle):
            pygame.draw.circle(screen, (0, 255, 0), curDraggedObstacle, 100, 3)
            curDraggedObstacle = mousePos
        for i in range(len(obstacles)):
            pygame.draw.circle(screen, (0, 255, 0), [obstacles[i].x, obstacles[i].y], obstacles[i].rad, 3)
        for i in range(len(obstacles)):
            if obstacles[i].isDeterminingThickness:
                obstacles[i].rad = math.hypot(mousePos[0]-obstacles[i].x, mousePos[1]-obstacles[i].y)
            pygame.draw.circle(screen, (0, 255, 0), [obstacles[i].x, obstacles[i].y], obstacles[i].rad, 3)
    elif screenState == "auto-choose":
        screen.blit(auto_choose, (0,0))
        for i in range(len(buttonDict["auto-choose"])):
            buttonDict["auto-choose"][i].drawSelf(screen)
    elif screenState == "to-mouse":
        screen.blit(to_mouse, (0,0))
        myImg = pygame.surfarray.make_surface(camera_pygame_frame)
        screen.blit(myImg, (345,280))
        for i in range(len(buttonDict["to-mouse"])):
            buttonDict["to-mouse"][i].drawSelf(screen)
    if myCar.isMoving:
        myCar.runCar(myGraph.computedPath, tip, tail)
    pygame.display.update()
    myClock.tick(60)
    pygame.display.set_caption(str(myClock.get_fps()))

pygame.quit()
sys.exit()