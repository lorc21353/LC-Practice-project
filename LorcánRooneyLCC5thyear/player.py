from tkinter import *
from math import *

class player:
    def __init__(self, playerX, playerY, playerSize, mouseX, mouseY, canvas, gameMode):
        self.gameMode = gameMode
        self.Canvas = canvas
        self.pX = playerX
        self.pY = playerY
        self.pS = playerSize
        self.mX = mouseX
        self.mY = mouseY
        
        
    
    def draw(self, playerSize):
        self.pS = playerSize
        # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
        poly = self.Canvas.create_polygon([self.pX-self.pS, self.pY-self.pS, self.pX+self.pS, self.pY-self.pS, self.pX+self.pS, self.pY+self.pS, self.pX-self.pS, self.pY+self.pS], outline="grey", fill="grey", width=1)

    
    
    
    def calculateMovement(self, mouseX, mouseY, outputs):
        if self.gameMode == 0 or self.gameMode == 1:
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
                    if self.gameMode == 0:
                        newCenterOffsetX = cos(angle)*0.4
                        newCenterOffsetY = sin(angle)*0.4
                    elif self.gameMode == 1:
                        newCenterOffsetX = cos(angle)*0.8
                        newCenterOffsetY = sin(angle)*0.8
                elif x2 < 0 and y2 >= 0:
                    #second quadrant
                    if self.gameMode == 0:
                        newCenterOffsetX = cos(angle)*0.4
                        newCenterOffsetY = sin(angle)*0.4
                    elif self.gameMode == 1:
                        newCenterOffsetX = cos(angle)*0.8
                        newCenterOffsetY = sin(angle)*0.8
                elif x2 < 0 and y2 < 0:
                    #third quadrant
                    if self.gameMode == 0:
                        newCenterOffsetX = -cos(angle)*0.4
                        newCenterOffsetY = -sin(angle)*0.4
                    elif self.gameMode == 1:
                        newCenterOffsetX = -cos(angle)*0.8
                        newCenterOffsetY = -sin(angle)*0.8
                elif x2 >= 0 and y2 < 0:
                    #fourth quadrant
                    if self.gameMode == 0:
                        newCenterOffsetX = cos(angle)*0.4
                        newCenterOffsetY = sin(angle)*0.4
                    elif self.gameMode == 1:
                        newCenterOffsetX = cos(angle)*0.8
                        newCenterOffsetY = sin(angle)*0.8
            else:
                newCenterOffsetX = 0
                newCenterOffsetY = 0
                
            self.pX += newCenterOffsetX
            self.pY += newCenterOffsetY
                
        elif self.gameMode == 2:
            self.posX = outputs[0]
            self.posY = outputs[1]
            self.negX = outputs[2]
            self.negY = outputs[3]
            # four output nodes are required: positive X, negative X, positive Y, negative Y. by changing these around you can create movement in all directions--
            # --or even stand still by activating pos and neg at the same time, this allows the AI to have full control of its body while maintaining as few output nodes as i can
                
            if self.posX == 1 and self.pX < 1000:
                self.pX += 0.5
            if self.posY == 1 and self.pY < 600:
                self.pY += 0.5
            if self.negX == 1 and self.pX > 0:
                self.pX -= 0.5
            if self.negY == 1 and self.pY > 0:
                self.pY -= 0.5


    def getPos(self):
        return [self.pX, self.pY]
