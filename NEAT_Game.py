from tkinter import *
from math import *
root = Tk() 
playerCenterX = 100
playerCenterY = 100
playerOffsetX = 50
playerOffsetY = 50
mouseAngleToPlayer = 0 
mouseX = 0
mouseY = 0
newCenterOffsetX = 0
newCenterOffsetY = 0 

def motion(event):
    global mouseX
    global mouseY
    mouseX = event.x
    mouseY = event.y
    
def calcmovement(x1, y1, x2, y2):
    global newCenterOffsetX
    global newCenterOffsetY
    x2 = x2-x1
    y2 = y2-y1
    
    if x2 != 0:
        angle = atan(y2/x2)*(180/pi)
    else:
        angle = 90
    
    if x2 >= 0 and y2 >= 0:
        #first quadrant
        newCenterOffsetX = cos(angle)
        newCenterOffsetY = sin(angle)
    elif x2 < 0 and y2 >= 0:
        #second quadrant
        newCenterOffsetX = cos(angle)
        newCenterOffsetY = sin(angle)
    elif x2 < 0 and y2 < 0:
        #third quadrant
        newCenterOffsetX = -cos(angle)
        newCenterOffsetY = -sin(angle)
    elif x2 >= 0 and y2 < 0:
        #fourth quadrant
        newCenterOffsetX = cos(angle)
        newCenterOffsetY = sin(angle)
        

root.geometry("1000x800") 
root.title("NEAT Game")


canvas = Canvas(root, width = 1000, height = 800)
poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline='gray', fill='gray', width=1)
canvas.pack()
root.bind('<Motion>', motion)

while True:
    calcmovement(playerCenterX, playerCenterY, mouseX, mouseY)
    playerCenterX += newCenterOffsetX
    playerCenterY += newCenterOffsetY
    canvas.delete(poly)
    poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline='gray', fill='gray', width=1)
    canvas.update()
    
    
