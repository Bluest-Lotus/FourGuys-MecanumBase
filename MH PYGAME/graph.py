import pygame
import queue
import math

class Graph():
    def __init__(self, pixelBorder, nodeBorder, framePixelWidth, framePixelHeight, xOffset, yOffset, nodeRad=10):
        self.pixelBorderBuffer = pixelBorder
        self.pixelNodeBuffer = nodeBorder
        self.framePixelWidth = framePixelWidth
        self.framePixelHeight = framePixelHeight
        self.localWidth = self.convertToLocalCoords(self.framePixelWidth-self.pixelBorderBuffer)
        self.localHeight = self.convertToLocalCoords(self.framePixelHeight-self.pixelBorderBuffer)
        self.nodeRadius = nodeRad
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.foundPath = False
        self.carRadius = 50
        self.targetNodeDist = 4
        self.isSearching = False
        self.xVectors = [1, 0, -1, 0, -1, 1, 1, -1]
        self.yVectors = [0, 1, 0, -1, -1, 1, -1, 1]
        self.globalStartingPos = []
        self.globalEndingPos = []
        self.computedPath = []
        self.targetCoords = []
        self.fullPath = []
    def drawGraph(self, pygameSurface):
        for y in range(self.pixelBorderBuffer+self.yOffset, self.framePixelHeight-self.pixelBorderBuffer+self.yOffset, self.pixelNodeBuffer):
            for x in range(self.pixelBorderBuffer+self.xOffset, self.framePixelWidth-self.pixelBorderBuffer+self.xOffset, self.pixelNodeBuffer):
                color = (0, 255, 0)
                if [x-self.xOffset, y-self.yOffset] == self.globalStartingPos or [x-self.xOffset, y-self.yOffset] == self.globalEndingPos:
                    color = (255, 0, 0)
                pygame.draw.circle(pygameSurface, color, (x, y), self.nodeRadius)
        if (self.foundPath):
            self.drawShortestPath(pygameSurface)
    def getLocalMouseCoords(self, mouseX, mouseY, obstacles, targets):
        for y in range(self.pixelBorderBuffer, self.framePixelHeight-self.pixelBorderBuffer, self.pixelNodeBuffer):
            for x in range(self.pixelBorderBuffer, self.framePixelWidth-self.pixelBorderBuffer, self.pixelNodeBuffer):
                if math.hypot(x-mouseX, y-mouseY) <= self.nodeRadius:
                    if self.globalStartingPos == []:
                        self.globalStartingPos = [x, y]
                    elif self.globalEndingPos == []:
                        self.globalEndingPos = [x, y]
                        self.foundPath = False
                        self.pathToTake = [[self.convertToLocalCoords(self.globalStartingPos[0]), self.convertToLocalCoords(self.globalStartingPos[1])]] + self.targetCoords + [[self.convertToLocalCoords(self.globalEndingPos[0]), self.convertToLocalCoords(self.globalEndingPos[1])]]
                        self.findShortestPath(obstacles, targets, self.pathToTake)
                        self.isSearching = True
                    else:
                        self.globalStartingPos = [x, y]
                        self.globalEndingPos = []
    def getLocalTargetCoords(self, mouseX, mouseY):
        for y in range(self.yOffset+self.pixelBorderBuffer, self.framePixelHeight-self.pixelBorderBuffer+self.yOffset, self.pixelNodeBuffer):
            for x in range(self.pixelBorderBuffer+self.xOffset, self.framePixelWidth-self.pixelBorderBuffer+self.xOffset, self.pixelNodeBuffer):
                if math.hypot(x-mouseX, y-mouseY) <= self.pixelNodeBuffer:
                    self.targetCoords.append([self.convertToLocalCoords(x-self.xOffset), self.convertToLocalCoords(y-self.yOffset)-1])
                    return [x, y]
        print("omg omg this didn't return anything")
    def convertToLocalCoords(self, val):
        return (val-self.pixelBorderBuffer)//self.pixelNodeBuffer+1
    def convertToGlobalCoords(self, val):
        return (val-1)*(self.pixelNodeBuffer) + self.pixelBorderBuffer
    def findShortestPath(self, obstacles, targets, pathToTake):
        print(pathToTake)
        for k in range(len(pathToTake)-1):
            #create graph and store starting and ending verticies as local coordinates
            myGraph = [[False for i in range(self.localWidth+1)] for j in range(self.localHeight+1)]
            startingPos = pathToTake[k]
            endingPos = pathToTake[k+1]
            #set the first node to be visited
            myGraph[startingPos[1]][startingPos[0]] = True

            #create our queue
            myQueue = queue.Queue()

            #add first node to queue and start BFS
            myQueue.put([startingPos, [startingPos]])

            #set ending coordinates
            endX, endY = endingPos

            self.computedPath = []

            while not myQueue.empty():
                curPos, prevPath = myQueue.get()
                curX, curY = curPos
                nodeIsInvalid = False
                for i in range(len(obstacles)):
                    if math.hypot((self.convertToGlobalCoords(curX)+self.xOffset)-obstacles[i].x, (self.convertToGlobalCoords(curY)+self.yOffset)-obstacles[i].y) <= (50+obstacles[i].rad):
                        nodeIsInvalid = True
                if nodeIsInvalid:
                    continue
                #MODIFY THIS, TWO CASES FOR TARGET OR END
                if k == len(pathToTake)-2:
                    if curX == endX and curY == endY:
                        self.computedPath += prevPath
                        if (k == len(pathToTake)-2):
                            self.foundPath = True
                        break
                else:
                    if curX == endX and curY-endY > 0 and curY-endY <= self.targetNodeDist:
                        self.computedPath += prevPath
                        print("MY GUY")
                        break
                #loop through adjacent nodes
                for i in range(len(self.xVectors)):
                    adjX = curX+self.xVectors[i]
                    adjY = curY+self.yVectors[i]
                    #check if we visited this node already
                    if 0 < adjX <= self.localWidth and 0 < adjY <= self.localHeight and not myGraph[adjY][adjX]:
                        myGraph[adjY][adjX] = True
                        newPrevPath = prevPath[:] + [[adjX, adjY]]
                        myQueue.put([[adjX, adjY], newPrevPath])
            if (k == len(pathToTake)-2) and not self.foundPath:
                self.foundPath = False
                self.computedPath = []
            print(self.computedPath)
                
    def drawShortestPath(self, pygameSurface):
        for i in range(len(self.computedPath)-1):
            pos1 = [self.convertToGlobalCoords(self.computedPath[i][0])+self.xOffset, self.convertToGlobalCoords(self.computedPath[i][1])+self.yOffset]
            pos2 = [self.convertToGlobalCoords(self.computedPath[i+1][0])+self.xOffset, self.convertToGlobalCoords(self.computedPath[i+1][1])+self.yOffset]
            pygame.draw.line(pygameSurface, (255, 0, 0), pos1, pos2, 4)