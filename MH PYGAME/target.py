import pygame

class Target():
    def __init__(self, x, y, isDragged = True):
        self.x = x
        self.y = y
        self.w = 20
        self.h = 40
        self.isDragged = isDragged
        self.thickness = 0
        self.isDeterminingThickness = True
    def drawSelf(self, pygameSurface):
        pygame.draw.rect(pygameSurface, (0, 0, 255), (self.x, self.y, self.w, self.h))