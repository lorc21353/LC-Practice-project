import game
import neat
import time
import os
import statistics
from tkinter import *
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))
root = Tk()
canvas = Canvas(root, width = 1000, height = 600)
runs_per_net = 1
game_time = 25
generations = 1
#var to check which net is doing its fitness calc during simulation play
enemyNet = True
global Game

# fitness function for the network
def eval_genome(genome, config):
    global Game
    # declare the local variables
    currTime = 0.0
    startTime = time.time_ns()/1000000000
    if gameMode == 0:
        # declare a local var called net that is the current genome's net
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        # as there is may be more than one run per genome the fitness will need to reflect the normal performance, thus it is placed in a list
        fitnesses = []
        
        # do the required number of runs for each net
        for runs in range(runs_per_net):
            averageDists = [] 
            # declare a new instance of the game class and parse the required data 
            Game = game.game(root, canvas, 0,0,0,0, gameMode)
            fitness = 0
            
            while currTime-startTime <= game_time:
                # optimisation to make the game run at a higher framerate by only taking distance measurements once every 200ms
                if currTime % 0.2 == 0:
                    averageDists.append(Game.dist())
                currTime = time.time_ns()/1000000000     
                inputs = Game.getInputs()
                outputs = net.activate(inputs)
                Game.Enemy.movement(outputs)
                Game.draw(0,0,0,0)
                if Game.winOrLose() == -1:
                    fitness = 100000
                    break
                elif Game.winOrLose() == -2:
                    fitness = 500-statistics.mean(averageDists)
                    break
                else:
                    fitness = 1000-statistics.mean(averageDists)
                    
            fitnesses.append(fitness)
        # genomes fitness is its worst across all of its runs
        return min(fitnesses)
    elif gameMode == 2:
        if enemyNet:
            # declare a local var called net that is the current genome's net
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            # as there is may be more than one run per genome the fitness will need to reflect the normal performance, thus it is placed in a list
            fitnesses = []
            
            averageDists = [] 
            fitness = 0
                
                # optimisation to make the game run at a higher framerate by only taking distance measurements once every 200ms
            if currTime % 0.2 == 0:
              averageDists.append(Game.dist())
              currTime = time.time_ns()/1000000000     
            inputs = Game.getInputs()
            outputs = net.activate(inputs)
            Game.Player.calculateMovement(0,0,outputs)
            if Game.winOrLose() == -1:
                fitness = 100000
            elif Game.winOrLose() == -2:
                fitness = 500-statistics.mean(averageDists)
            else:
                fitness = 1000-statistics.mean(averageDists)
                        
            fitnesses.append(fitness)
             
            # genomes fitness is its worst across all of its runs
            return min(fitnesses)
        
        # playerNet fitness function
        elif True != enemyNet:
            if Game.winOrLose() == -1:
                fitness = 0
            elif Game.winOrLose == -2:
                fitness = 1000-Game.dist()/100
            return fitness
    
        

def eval_genomes(genomes, config):
    if gameMode == 0:
        for genome_id, genome in genomes:
            genome.fitness = eval_genome(genome, config)
            
    if gameMode == 2:
        genome.fitness = eval_genome(genome, config)
        

def run():
    # boilder place code to load the config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    # boiler plate code to create and record the populations
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    
    if gameMode == 2:
        pop2 = neat.Population(config)
        stats2 = neat.StatisticsReporter()
        pop2.add_reporter(stats2)
        pop2.add_reporter(neat.StdOutReporter(True))

    # run the AI for a number of generations using eval_genomes as the fitness fuction
    if gameMode == 0:
        winner = pop.run(eval_genomes, generations)
        print(winner)
    elif gameMode == 1:
        print("multiplayer")
    elif gameMode == 2:
        global Game
        # declare a game for simulation play
        Game = game.game(root, canvas, 0,0,0,0, gameMode)
        while True:
            enemyNet = True
            pop.run(eval_genomes, generations)
            enemyNet = False
            pop2.run(eval_genomes, generations)
            Game.draw(0,0,0,0)
    
    #check if you are in the main file and if you are run the program (this is a library requirement)
if __name__ == '__main__':
    run()    