import game
import player
import enemy
import neat
import time
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))

runs_per_net = 5
game_time = 10

def eval_genome(genome, config):
    global gameMode
    global runs_per_net
    global game_time
    startTime = time.time_ns()/1000000000
    
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # as there is more than one run per genome the fitness will need to reflect the average, thus it is placed in a list
    fitness = []
    
    # do the required number of runs for each net
    for run in range(runs_per_net):
        game = game.game(0,0,0,0, gameMode)
        fitness = 0
        
        while currTime-startTime <= game_time:
            currTime = time.time_ns()/1000000000     
            inputs = game.getInputs()
            outputs = net.activate(inputs)
        
        
        
        

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome()
        
# placeHolder code to check if the default game without AI is working
# mouseX = 0
# mouseY = 0
# game1 = game.game(0,0,0,0, gameMode)
# while True:
#     game1.draw(0,0,10,10)
#     print(game1.winOrLose())
    
    