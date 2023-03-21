from tkinter import *
from math import *
import time
import player
import enemy


class game:
    def __init__(self, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY):
        self.mex = moveEnemyX
        self.mey = moveEnemyY
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.root = Tk()
        #self.root.bind('<Motion>', motion)
        self.root.geometry(str(1000)+"x"+str(600)) 
        self.root.title("NEAT Game")
        self.canvas = Canvas(self.root, width = 1000, height = 600)
        self.canvas.pack()
        self.Player = player.player(10,10,10,0,0,self.canvas)
        
    
    
    def draw(self, moveEnemyX, moveEnemyY, movePlayerX, movePlayerY, mouseX, mouseY):
        self.mex = moveEnemyX
        self.mey = moveEnemyY
        self.mpx = movePlayerX
        self.mpy = movePlayerY
        self.mX = mouseX
        self.mY = mouseY
        
        self.Player.draw(10,10,10)
        
        self.canvas.update()
        
        
        
        
        