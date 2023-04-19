
# this could be made into a subclass of the player class but that looks way less clean and is far harder to read and edit if needs be
class enemy:
    def __init__(self, enemyX, enemyY, enemySize, canvas, gameMode):
        # add the required variables to self
        self.eX = enemyX
        self.eY = enemyY
        self.eS = enemySize
        self.Canvas = canvas
        self.gameMode = gameMode
        
    def draw(self, enemySize):
        self.pS = enemySize
        # calculate the corners of the rectangle by taking the size of it away from the center and then draw a rectangle with those corners
        poly = self.Canvas.create_polygon([self.eX-self.eS, self.eY-self.eS, self.eX+self.eS, self.eY-self.eS, self.eX+self.eS, self.eY+self.eS, self.eX-self.eS, self.eY+self.eS], outline="red", fill="red", width=1)

    def movement(self, outputs):
        # convert the four outputs passed to this function inside and array into movement directions
        self.posX = outputs[0] # move right
        self.posY = outputs[1] # move down
        self.negX = outputs[2] # move left
        self.negY = outputs[3] # move up
        # four output nodes are required: positive X, negative X, positive Y, negative Y. by changing these around you can create movement in all directions--
        # --or even stand still by activating pos and neg at the same time, this allows the AI to have full control of its body while maintaining as few output nodes as i can
        if self.gameMode == 0 or 1 or 2:
            
            if self.posX == 1 and self.eX < 1000:
                self.eX += 0.5
            if self.posY == 1 and self.eY < 600:
                self.eY += 0.5
            if self.negX == 1 and self.eX > 0:
                self.eX -= 0.5
            if self.negY == 1 and self.eY > 0:
                self.eY -= 0.5
            
            
    # return enemys current x and y coords
    def getPos(self):
        return [self.eX, self.eY]
