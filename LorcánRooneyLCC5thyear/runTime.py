import game
import neat
import time
import os
import statistics
from neat.six_util import iteritems, itervalues
from tkinter import *
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))
root = Tk()
canvas = Canvas(root, width = 1000, height = 600)
runs_per_net = 1
game_time = 25
sim_game_time = 5
generations = 150
#var to check which net is doing its fitness calc during simulation play
#no longer used
#enemyNet = True
global Game
global pop2
global currGame

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
                if currTime % 0.02:
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
    

global stagnation
global reporters
global species
global pop
def eval_genomes(genomes, config):
    global pop
    global pop2
    global stagnation
    global reporters
    global species
    if gameMode == 2:
        reproduction = config.reproduction_type(config.reproduction_config, reporters, stagnation)


    if gameMode == 0:
        for genome_id, genome in genomes:
            genome.fitness = eval_genome(genome, config)
            
    elif gameMode == 2:
        j = 0
        pop2.reporters.start_generation(pop2.generation)
        for genome_id, genome in genomes:
            j+=1
            if j >= len(list(iteritems(pop2.population))):
                j = 0
                print("something has gone very wrong here")
                print("there are only", len(list(iteritems(pop2.population))), "there should be", len(list(iteritems(pop.population))))
            genome.fitness = eval_enemy(genome, config, j)
        pop2.population = pop2.reproduction.reproduce(config, pop2.species, config.pop_size, pop2.generation)
        pop2.species.speciate(config, pop2.population, pop2.generation)
        pop2.reporters.end_generation(config, pop2.population, pop2.species)
        pop2.generation+=1
        
 # playerNet fitness function for sim mode
def eval_player(genome, config, currentGame):
    genome = genome[1]
    fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    inputs = currentGame.getInputs()
    outputs = net.activate(inputs)
    currentGame.Player.calculateMovement(0,0,outputs)
    if currentGame.winOrLose() == -1:
            fitness = 0
    elif currentGame.winOrLose() == -2:
        fitness = 1000+currentGame.dist()/100
    else:
        fitness = 500+currentGame.dist()/10
    return fitness

def returnExistingFitnessValues(genomes, config):
    for gneomeid, genome in genomes:
        genome.fitness = genome.fitness
        print(genome.fitness, genome)

def eval_enemy(genome, config, j):
        global currGame
        currGame = []
        global pop2
        currGame = game.game(root, canvas, 0,0,0,0,2)
        population2 = list(iteritems(pop2.population))
        iters = 0
        # declare a local var called net that is the current genome's net
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        while iters < 2500:
            iters += 1
            inputs = currGame.getInputs()
            outputs = net.activate(inputs)
            currGame.Enemy.movement(outputs)
            genome = population2[j-1]
            eval_player(genome, config, currGame)
            #print(pop2.population[j].fitness)
            currGame.Player.draw(20)
            
            fitness = 0
            
            if currGame.winOrLose() == -1:
                fitness = 100000-iters
                break
            elif currGame.winOrLose() == -2:
                fitness = 500-currGame.dist()
                break
            else:
                fitness = 1000-currGame.dist()
                
            currGame.draw(0,0,0,0)
        population2[j-1][1].fitness = eval_player(genome, config, currGame)
        print(population2[j-1][1].fitness, "player fitness value")
        print(fitness, "enemy fitness value")
        return fitness
    

def run():
    global pop
    global pop2
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
        global stagnation
        stagnation = config.stagnation_type(config.stagnation_config, pop2.reporters)
        global reporters
        reporters = pop2.reporters
        global species
        species = config.species_set_type(config.species_set_config, reporters)
        

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
            #enemyNet = True
        pop.run(eval_genomes, generations)
            #enemyNet = False
            #pop2.run(eval_genomes, generations)
            #Game.draw(0,0,0,0)
    
    #check if you are in the main file and if you are run the program (this is a library requirement)
if __name__ == '__main__':
    run()    