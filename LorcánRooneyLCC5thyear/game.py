from tkinter import *
from math import *
import time
import player
import enemy


class game:
    def __init__(self, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY, gameMode):
        self.mex = moveEnemyX
        self.mey = moveEnemyY
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.gameMode = gameMode
        self.root = Tk()
        self.root.geometry(str(1000)+"x"+str(600)) 
        self.root.title("NEAT Game")
        self.canvas = Canvas(self.root, width = 1000, height = 600)
        self.canvas.pack()
        self.Player = player.player(10,10,10,0,0,self.canvas)
        self.Enemy = enemy.enemy(800, 300, 10, self.canvas, self.gameMode)
        self.startTime = time.time_ns()/1000000
        
    
    
    def draw(self, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY):
        self.mex = moveEnemyX
        self.mey = moveEnemyY
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.mX = self.canvas.winfo_pointerx() - self.root.winfo_rootx()
        self.mY = self.canvas.winfo_pointery() - self.root.winfo_rooty()
        
        if self.mX > 1000:
            self.mX = 1000
        if self.mX < 0:
            self.mX = 0
        if self.mY > 600:
            self.mY = 600
        if self.mY < 0:
            self.mY = 0
        self.canvas.delete("all")
        if (time.time_ns()/1000000 - self.startTime) % 2:
            if self.gameMode == 0:
                self.Player.calculateMovement(self.mX,self.mY)
                #print(self.mX, self.mY)
            elif self.gameMode == 1:
                print("multiplayer")
            elif self.gameMode == 2:
                print("simulation")
        self.Enemy.draw(10)
        self.Player.draw(10)
        self.canvas.update()
        
    # this is used to check whether or not the player has beat the AI, i.e whether the player has made it to the other side or if they died
    # this is not only important to have a game end state but also this will be fed almost directly into the reward function
    #def winOrLose:
        
        
        
        
        