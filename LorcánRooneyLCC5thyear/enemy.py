
# this could be made into a subclass of the player class but that looks way less clean and is far harder to read and edit if needs be
class enemy:
    def __init__(self, enemyX, enemyY, enemySize, canvas, gameMode):
        self.eX = enemyX
        self.eY = enemyY
        self.eS = enemySize
        self.Canvas = canvas
        self.gameMode = gameMode
        
    def draw(self, enemySize):
        self.pS = enemySize
        # this causes a slight squishing effect of the player in direction of movement, im pretty sure it's caused by it not rendering in the correct order but it looks cool so im leaving it in
        poly = self.Canvas.create_polygon([self.eX-self.eS, self.eY-self.eS, self.eX+self.eS, self.eY-self.eS, self.eX+self.eS, self.eY+self.eS, self.eX-self.eS, self.eY+self.eS], outline="red", fill="red", width=1)

    def movement(posX, posY, negX, negY):
        self.posX = posX
        self.posY = posY
        self.negX = negX
        self.negY = negY
        # four output nodes are required: positive X, negative X, positive Y, negative Y. by changing these around you can create movement in all directions--
        # --or even stand still by activating pos and neg at the same time, this allows the AI to have full control of its body while maintaining as few output nodes as i can
        if self.gameMode == 0:
            
            if self.posX == 1:
                self.eX += 0.5
            if self.posY == 1:
                self.eY += 0.5
            if self.negX == 1:
                self.eX -= 0.5
            if self.negY == 1:
                self.eY -= 0.5
                
                
        # placeholder multiplayer and simulation    
        elif self.gameMode == 1:
            print("multiplayer")
        elif self.gameMode == 2:
            print("simulation")
            
