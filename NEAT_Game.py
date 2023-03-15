from tkinter import *
from math import *
import time
import neat
root = Tk()
canvasSizeX = 1000
canvasSizeY = 600
# this is a list because there will be more than one enemy at some point
enemyCenterX = []
enemyCenterX.append(canvasSizeX-100)
enemyCenterX.append(canvasSizeX-200)
enemyCenterY = []
enemyCenterY.append(canvasSizeY/2)
enemyCenterY.append(canvasSizeY/2)
playerCenterX = 100
playerCenterY = 100
playerOffsetX = 20
playerOffsetY = 20
playerState = "grey"
playerWin = False
mouseAngleToPlayer = 0 
mouseX = 0
mouseY = 0
newCenterOffsetX = 0
newCenterOffsetY = 0
# get program start time in ms
startTime = time.time_ns()/1000000


def eval_genomes(genomes, config):
    global playerCenterX
    global playerCenterY
    for genome_id, genome in genomes:
        genome.fitness = sqrt(1000*1000+600*600)/2-sqrt((playerCenterX-enemyCenterX[i])*(playerCenterX-enemyCenterX[i])+(playerCenterY-enemyCenterY[i])*(playerCenterY-enemyCenterY[i])) < playerOffsetX*2
        
        

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
    if sqrt(x2*x2+y2*y2) < 350:
        if x2 != 0:
            angle = atan(y2/x2)*(180/pi)
        else:
            angle = 90
        
        if x2 >= 0 and y2 >= 0:
            #first quadrant
            newCenterOffsetX = cos(angle)*0.4
            newCenterOffsetY = sin(angle)*0.4
        elif x2 < 0 and y2 >= 0:
            #second quadrant
            newCenterOffsetX = cos(angle)*0.4
            newCenterOffsetY = sin(angle)*0.4
        elif x2 < 0 and y2 < 0:
            #third quadrant
            newCenterOffsetX = -cos(angle)*0.4
            newCenterOffsetY = -sin(angle)*0.4
        elif x2 >= 0 and y2 < 0:
            #fourth quadrant
            newCenterOffsetX = cos(angle)*0.4
            newCenterOffsetY = sin(angle)*0.4
    else:
        newCenterOffsetX = 0
        newCenterOffsetY = 0
        
    
# step physics, only run at 30 steps per second
def physicsFrames():
    global playerCenterX
    global playerCenterY
    global newCenterOffsetX
    global newCenterOffsetY

    calcmovement(playerCenterX, playerCenterY, mouseX, mouseY)
    playerCenterX += newCenterOffsetX
    playerCenterY += newCenterOffsetY



def renderPlayer():
    global playerCenterX
    global playerCenterY
    global playerOffsetX
    global playerOffsetY
    global poly
    global canvas
    global playerState
    # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
    poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline=playerState, fill=playerState, width=1)

def renderEnemy():
    global enemyCenterX
    global enemyCenterY
    global playerOffsetX
    global playerOffsetY
    global enemy
    global canvas
    for i in range(len(enemyCenterX)):
        # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
        enemy = canvas.create_polygon([enemyCenterX[i]-playerOffsetX, enemyCenterY[i]-playerOffsetY, enemyCenterX[i]+playerOffsetX, enemyCenterY[i]-playerOffsetY, enemyCenterX[i]+playerOffsetX, enemyCenterY[i]+playerOffsetY, enemyCenterX[i]-playerOffsetX, enemyCenterY[i]+playerOffsetY], outline='red', fill='red', width=1)

def loseCondition():
    global enemyCenterX
    global enemyCenterY
    global playerOffsetX
    global playerCenterX
    global playerCenterY
    global playerState
    for i in range(len(enemyCenterX)):
        if sqrt((playerCenterX-enemyCenterX[i])*(playerCenterX-enemyCenterX[i])+(playerCenterY-enemyCenterY[i])*(playerCenterY-enemyCenterY[i])) < playerOffsetX*2:
            playerState = "red"
        else:
            playerState = "grey"

def winCondition():
    global playerCenterX
    global playerCenterY
    global canvasSizeX
    global playerState
    #print(canvasSizeX - playerCenterX)
    if canvasSizeX - playerCenterX < 100:
        playerState = "green"


root.geometry(str(canvasSizeX)+"x"+str(canvasSizeY)) 
root.title("NEAT Game")


canvas = Canvas(root, width = canvasSizeX, height = canvasSizeY)
poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline=playerState, fill=playerState, width=1)
enemy = canvas.create_polygon([enemyCenterX[0]-playerOffsetX, enemyCenterY[0]-playerOffsetY, enemyCenterX[0]+playerOffsetX, enemyCenterY[0]-playerOffsetY, enemyCenterX[0]+playerOffsetX, enemyCenterY[0]+playerOffsetY, enemyCenterX[0]-playerOffsetX,enemyCenterY[0]+playerOffsetY], outline='red', fill='red', width=1)
canvas.pack()
root.bind('<Motion>', motion)


# main / draw loop 
while True:
    currTime = time.time_ns()/1000000 # get current time in milliseconds
    canvas.delete("all")
    renderPlayer()
    renderEnemy()
    canvas.update()
    if currTime-startTime % 2 and playerState == "grey":
        physicsFrames()
        loseCondition()
        winCondition()
    elif playerState != "grey":
        time.sleep(0.4)
        playerState = "grey"
        playerCenterX = 100
        playerCenterY = 100
    
