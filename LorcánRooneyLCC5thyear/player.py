# imports
from tkinter import *
from math import *

class player:
    def __init__(self, playerX, playerY, playerSize, mouseX, mouseY, canvas, gameMode):
        # get the vars needed and add them to self 
        self.gameMode = gameMode
        self.Canvas = canvas
        self.pX = playerX
        self.pY = playerY
        self.pS = playerSize
        self.mX = mouseX
        self.mY = mouseY
        
        
    
    def draw(self, playerSize):
        self.pS = playerSize
        # this might look complicated but its literally just drawing a centered square, all it does is take away and add the size of the enemy from the center to get the corners and then draws it
        # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
        poly = self.Canvas.create_polygon([self.pX-self.pS, self.pY-self.pS, self.pX+self.pS, self.pY-self.pS, self.pX+self.pS, self.pY+self.pS, self.pX-self.pS, self.pY+self.pS], outline="grey", fill="grey", width=1)

    
    
    # calculating the movement of the player
    def calculateMovement(self, mouseX, mouseY, outputs):
        if self.gameMode == 0 or self.gameMode == 1: # if in singleplayer or multiplayer
            # the reason for assigning the local variables from self instead of directly using self is that i wrote this function before i turned player into a class and it was easier to just keep the same local var names and just assign them from self instead of changing the function
            x1 = self.pX
            y1 = self.pY
            self.mX = mouseX
            self.mY = mouseY
            x2 = self.mX
            y2 = self.mY
            
            # change the variables to be relative to each other, this makes the math easier as i can now treat every case as the special case where one point is at 0,0
            x2 = x2-x1
            y2 = y2-y1
            # this section is a load of trig
            if sqrt(x2*x2+y2*y2) < 350:
                if x2 != 0:
                    # calculate the angle in degrees using the atan function
                    angle = atan(y2/x2)*(180/pi)
                else:
                    # this avoids a divide by zero error in y2/x2
                    angle = 90
                
                if x2 >= 0 and y2 >= 0:
                    #first quadrant
                    # this is basically the same for all of them so ill only explain once
                    # the new x offset is equal to the cosine of the atan angle multiplied by the constant 0.4 (or 0.8 if in multiplayer)
                    # same with the y offset except its the sine of the atan angle
                    # these new offset values are then added to the current coords thus moving the player
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
                # if there is no input dont move
                newCenterOffsetX = 0
                newCenterOffsetY = 0
                
            self.pX += newCenterOffsetX
            self.pY += newCenterOffsetY
                
        elif self.gameMode == 2:
            # simulation mode outputs
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

    # get position function just returns current position of player
    def getPos(self):
        return [self.pX, self.pY]
