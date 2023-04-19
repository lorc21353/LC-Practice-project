# imports
from tkinter import *
from math import *
import time
import player
import enemy


class game:
    def __init__(self, root, canvas, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY, gameMode):
        # delcare every vaiable used to control the game, a few of these are never actually used but still remain due to wanting to maintain modularity
        self.mex = moveEnemyX # the variables which can be used to move the enemy and the player from a higher level of abstraction, ie not needing to directly call Game.game.enemy
        self.mey = moveEnemyY # these movement variables are not used for much but were added when initially making the game class incase they were needed and were never removed
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.gameMode = gameMode
        self.root = root # root is the name used for the root window from tkinter
        self.root.geometry(str(1000)+"x"+str(600)) # set the size of the root
        self.root.title("NEAT Game") # set the title of the root
        self.canvas = canvas # set the canvas
        self.canvas.pack() # process and display the canvas
        self.Player = player.player(10,10,10,0,0,self.canvas, self.gameMode) # create an instance of the player class
        self.Enemy = enemy.enemy(800, 300, 10, self.canvas, self.gameMode) # create and instance of the enemy class
        self.startTime = time.time_ns()/1000000 # get the program start time, this is used to time events in the game such as when each round should end
        
    
    # draw function, it draws the window, enemy, and player
    def draw(self, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY):
        self.mex = moveEnemyX
        self.mey = moveEnemyY
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.mX = self.canvas.winfo_pointerx() - self.root.winfo_rootx()
        self.mY = self.canvas.winfo_pointery() - self.root.winfo_rooty()
        
        # ensure that the nothing goes outside the canvas, there is still a bug which allows the player to temporarily clip out of bounds but it fixes its self in a few seconds so i am not going to patch it
        # the bug can be replicated by putting the mouse close to the player near the edge of the screen and the quickly moving it out and up this will cause the player to skip the OOB check and clip outside the canvas bounds
        # the player will return back to the map in a few seconds, the net cannot perform this bug as it only works with mouse movement so i do not think its important enough to patch
        if self.mX > 1000:
            self.mX = 1000
        if self.mX < 0:
            self.mX = 0
        if self.mY > 600:
            self.mY = 600
        if self.mY < 0:
            self.mY = 0
        self.canvas.delete("all") # clear the canvas
        # i forgot to put == 0 after the mod operator so this if statement does literally nothing, there is already a check to make it 30fps in runTime anyway so there is no reason to fix this
        if (time.time_ns()/1000000 - self.startTime) % 2:
            if self.gameMode == 0 or self.gameMode == 1: # if gamemode is 0 or 1 then call the player calculate movement function
                self.Player.calculateMovement(self.mX,self.mY,None)
        
        # call the draw functions of the enemy and player and then update the canvas to display the new positions
        self.Enemy.draw(10)
        self.Player.draw(10)
        self.canvas.update()
        
    # this is used to check whether or not the player has beat the AI, i.e whether the player has made it to the other side or if they died
    # this is not only important to have a game end state but also this will be fed almost directly into the reward function
    def winOrLose(self):
        tempEnemyX = self.Enemy.getPos()[0]
        tempEnemyY = self.Enemy.getPos()[1]
        tempPlayerX = self.Player.getPos()[0]
        tempPlayerY = self.Player.getPos()[1]
        # return -1 if player dies, -2 if player wins, return the distance of enemy and player if neither of these are true
        if abs(tempEnemyX - tempPlayerX) < 20 and abs(tempEnemyY - tempPlayerY) < 20:
            return -1
        elif abs(1000-tempPlayerX) < 100:
            return -2
        else:
            return sqrt(pow(tempEnemyX-tempPlayerX, 2) + pow(tempEnemyY-tempPlayerY, 2))
        
        
# distance function, returns the distance from enemy to player
    def dist(self):
        # assigns the local position variables the return values of the get position function is each the enemy and player
        # 0 is the x coord 
        tempEnemyX = int(self.Enemy.getPos()[0])
        tempEnemyY = int(self.Enemy.getPos()[1])
        tempPlayerX = int(self.Player.getPos()[0])
        tempPlayerY = int(self.Player.getPos()[1])
        
        # this is an extemely poor way to do this and is no longer used, what this did was check if the player and enemy are in the exact same position
        #if tempEnemyY == 0 or tempPlayerY == 0 or tempEnemyY - tempPlayerY == 0:
        #    tempEnemyY = 1
        #    tempPlayerY = 1
        #if tempEnemyX == 0 or tempPlayerX == 0 or tempEnemyX - tempPlayerX == 0:
        #    tempEnemyX = 1
        #    tempPlayerX = 1
            
        return sqrt(pow(tempEnemyX-tempPlayerX, 2) + pow(tempEnemyY-tempPlayerY, 2)) # a real-world application of the pythagorean theorem
        
    def getInputs(self):
        return [self.Enemy.getPos()[0], self.Enemy.getPos()[1], self.Player.getPos()[0], self.Player.getPos()[1]] # returns the positions of the player and enemy in x and y it is called get inputs cause it is used as the inputs for the neural net