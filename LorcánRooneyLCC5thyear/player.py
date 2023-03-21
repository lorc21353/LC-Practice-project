from tkinter import *
from math import *

class player:
    def __init__(self, playerX, playerY, playerSize, mouseX, mouseY, canvas):
        self.Canvas = canvas
        self.pX = playerX
        self.pY = playerY
        self.pS = playerSize
        self.mX = mouseX
        self.mY = mouseY
        
        
    
    def draw(self, playerX, playerY, playerSize):
        self.pX = playerX
        self.pY = playerY
        self.pS = playerSize
        # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
        poly = self.Canvas.create_polygon([self.pX-self.pS, self.pY-self.pS, self.pX+self.pS, self.pY-self.pS, self.pX+self.pS, self.pY+self.pS, self.pX-self.pS, self.pY+self.pS], outline="grey", fill="grey", width=1)

    
    
    
    def calculateMovement(self, mouseX, mouseY):
        x1 = self.pX
        y1 = self.pY
        self.mX = mouseX
        self.mY = mouseY
        x2 = self.mX
        y2 = self.mY
        
        x2 = x2-x1
        y2 = y2-y1
        if sqrt(x2*x2+y2*y2) < 350:
            if x2 != 0:
                angle = atan(y2/x2)*(180/pi)
            else:
                angle = 90
            
            if x2 >= 0 and y2 >= 0:
                #first quadrant
                newCenterOffsetX = cos(angle)*0.2
                newCenterOffsetY = sin(angle)*0.2
            elif x2 < 0 and y2 >= 0:
                #second quadrant
                newCenterOffsetX = cos(angle)*0.2
                newCenterOffsetY = sin(angle)*0.2
            elif x2 < 0 and y2 < 0:
                #third quadrant
                newCenterOffsetX = -cos(angle)*0.2
                newCenterOffsetY = -sin(angle)*0.2
            elif x2 >= 0 and y2 < 0:
                #fourth quadrant
                newCenterOffsetX = cos(angle)*0.2
                newCenterOffsetY = sin(angle)*0.2
        else:
            newCenterOffsetX = 0
            newCenterOffsetY = 0
            
