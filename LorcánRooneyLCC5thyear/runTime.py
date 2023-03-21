import game
import player
import enemy

#placeHolder
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))
mouseX = 0
mouseY = 0
game1 = game.game(0,0,0,0, gameMode)
while True:
    game1.draw(0,0,10,10)
    game1.winOrLose()