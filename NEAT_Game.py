from tkinter import *
root = Tk() 
playerCenterX = 100
playerCenterY = 100
playerOffsetX = 50
playerOffsetY = 50


root.geometry("500x300") 
root.title("NEAT Game")


canvas = Canvas(root, width = 500, height = 300)
poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline='gray', fill='gray', width=1)
canvas.pack()

while True:
    canvas.delete(poly)
    playerCenterX += 1
    playerCenterY += 1
    print(playerOffsetX)
    poly = canvas.create_polygon([playerCenterX-playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY-playerOffsetY, playerCenterX+playerOffsetX, playerCenterY+playerOffsetY, playerCenterX-playerOffsetX, playerCenterY+playerOffsetY], outline='gray', fill='gray', width=1)
    canvas.update()
    