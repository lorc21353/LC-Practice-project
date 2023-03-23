import game
import player
import enemy
import neat
import time
import os
from tkinter import *
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))
root = Tk()
canvas = Canvas(root, width = 1000, height = 600)
runs_per_net = 1
game_time = 25


def eval_genome(genome, config):
    global gameMode
    global runs_per_net
    global game_time
    currTime = 0
    startTime = time.time_ns()/1000000000
    
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # as there is more than one run per genome the fitness will need to reflect the normal performance, thus it is placed in a list
    fitnesses = []
    
    # do the required number of runs for each net
    for run in range(runs_per_net):
        mostestClosest = 10000000
        Game = game.game(root, canvas, 0,0,0,0, gameMode)
        #global Game
        fitness = 0
        
        while currTime-startTime <= game_time:
            if Game.dist() < mostestClosest:
                mostestClosest = Game.dist()
            currTime = time.time_ns()/1000000000     
            inputs = Game.getInputs()
            outputs = net.activate(inputs)
            Game.Enemy.movement(outputs)
            Game.draw(0,0,0,0)
            if Game.winOrLose() == -1:
                fitness = 100000
                break
            elif Game.winOrLose() == -2:
                fitness = 500-mostestClosest
                break
            elif mostestClosest - Game.dist() > 1500:
                fitness = 1000-mostestClosest
            else:
                fitness = 1000-mostestClosest
                
        fitnesses.append(fitness)
    # genomes fitness is its worst across all of its runs
    return min(fitnesses)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
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

    # run the AI
    pop.run(eval_genomes, 6)
    
    
if __name__ == '__main__':
    run()    