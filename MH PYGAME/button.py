import pygame

class Button():
    def __init__(self, x, y, w, h, dest, isRedirectingScreen = True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.destinationScreen = dest
        self.isRedirectingScreen = isRedirectingScreen
    def pointCollided(self, mouseX, mouseY):
        return mouseX > self.x and mouseX < self.x+self.w and mouseY > self.y and mouseY < self.y+self.h
    def transitionScreen(self):
        return self.destinationScreen
    def drawSelf(self, pygameSurface):
        pygame.draw.rect(pygameSurface, (0, 0, 255), (self.x, self.y, self.w, self.h), 5)