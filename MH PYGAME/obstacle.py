class Obstacle():
    def __init__(self, x, y, isDragged = True, rad = 10):
        self.x = x
        self.y = y
        self.isDragged = isDragged
        self.thickness = 0
        self.rad = rad
        self.isDeterminingThickness = True
    def drawSelf(self, pygameSurface, mouseX, mouseY):
        if self.isDragged:
            pass
        else:
            pass
        