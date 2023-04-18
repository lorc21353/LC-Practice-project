# import the libraries and classes required
import game
import keyboard
import neat
import time
import os
import statistics
import matplotlib.pyplot as plt 
from neat.six_util import iteritems
from tkinter import *
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): ")) # ask the user what gamemode they want to play
root = Tk() # declare the root of the window using tk
canvas = Canvas(root, width = 1000, height = 600) # create the canvas that everything will be drawn on 
runs_per_net = 1 # how many runs each net gets
game_time = 25 # how long a singleplayer game is
sim_game_time = 5 # unused 
generations = 6 # how many generations should the single player mode run for
# declare the most important global variables
global Game
global pop2
global currGame
global plotFitnessOfEnemy
global plotGenerationNumberEnemy
plotGenerationNumberEnemy = []
plotFitnessOfEnemy = []
global plotFitnessOfPlayer
global plotGenerationNumberPlayer
plotGenerationNumberPlayer = []
plotFitnessOfPlayer = []

# fitness function for the network
def eval_genome(genome, config):
    # get the globals
    global Game
    global plotFitnessOfEnemy
    global plotGenerationNumberEnemy
    # declare the local variables
    currTime = 0.0
    startTime = time.time_ns()/1000000000

    if gameMode == 0: # if in single player
        # declare a local var called net that is the current genome's net
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        # as there is may be more than one run per genome the fitness will need to reflect the normal performance, thus it is placed in a list
        fitnesses = []
        
        # do the required number of runs for each net
        for runs in range(runs_per_net):
            averageDists = []
            # declare a new instance of the game class and parse the required data 
            Game = game.game(root, canvas, 0,0,0,0, gameMode)
            averageDists.append(Game.dist())
            fitness = 0
            
            while currTime-startTime <= game_time:
                currTime = time.time_ns()/1000000000 # set the current time to the current real life time 
                # optimisation to make the game run at a higher framerate by only taking distance measurements once every 200ms
                #print(round(currTime % 0.2, 2))
                if round(currTime % 0.2, 2) == 0:
                    averageDists.append(Game.dist())
                    
                if currTime % 0.02: # 30 times a second 
                    inputs = Game.getInputs() # get current game state
                    outputs = net.activate(inputs) # pass game state to neural net
                    Game.Enemy.movement(outputs) # pass outputs from net to the enemy class inside the game class
                    Game.draw(0,0,0,0) # call the game draw function
                if Game.winOrLose() == -1: # if the enemy catches the player then set the fitness to an absurdly high amount
                    fitness = 100000
                    break # exit the game loop 
                elif Game.winOrLose() == -2: # if the player wins set the fitness to a low value minus the average distance from the player
                    fitness = 500-statistics.mean(averageDists)
                    break # exit the game loop
                else: # if neither the player or enemy win then set fitness to a high value minus the average distance from the
                    fitness = 1000-statistics.mean(averageDists)
                    
            fitnesses.append(fitness) # add the fitness to the fitnesses list
        # genomes fitness is its worst across all of its runs
        plotFitnessOfEnemy.append(min(fitnesses))
        plotGenerationNumberEnemy.append(pop.generation)
        return min(fitnesses)
    
# declare the global vars used for sim mode
global stagnation
global reporters
global species
# declare the pop var, used in single player and sim modes
global pop
def eval_genomes(genomes, config):
    # get the global variables used in simulation mode
    global pop
    global pop2
    global stagnation
    global reporters
    global species

    if gameMode == 2: # if gamemode is equal to 2 then declare the reproduction local variable 
        reproduction = config.reproduction_type(config.reproduction_config, reporters, stagnation)


    if gameMode == 0: # if in single player then call the eval genome function of the single player enemy
        for genome_id, genome in genomes: # for every genome id and genome inside of genomes
            genome.fitness = eval_genome(genome, config) # set fitness to the return value of eval genome
            
    elif gameMode == 2: # if in simulation mode
        j = 0 # declare local counter variable j
        pop2.reporters.start_generation(pop2.generation) # call the reporter classes function to print the start generation text
        for genome_id, genome in genomes: # for every tuple in genomes
            j+=1 # add one to counter variable
            if j >= len(list(iteritems(pop2.population))): # if for some reason j is larger or the same size as the size of the player populations size (the reason is almost always due to a stagnation extinction) reset counter to 0
                j = 0
                print("something has gone very wrong here") # print that there was an error and what went wrong
                print("there are only", len(list(iteritems(pop2.population))), "there should be", len(list(iteritems(pop.population))))
            genome.fitness = eval_enemy(genome, config, j) # call the evaluate enemy function passing all the required variables, set the fitness value of the genome to the return value
        try: # this is inside a try except because ocassionally it will throw an error, while i cannot say exactly what causes the error i think it is to do with the removal of a genome from the population, if there are too many removed it will cause a null error. as this is to do with how the library handles this i decided it made more sense to just catch the error instead of trying to rewrite the entire library just for this one error
            pop2.population = pop2.reproduction.reproduce(config, pop2.species, config.pop_size, pop2.generation)
        except:
            print("reproduction error for pop2")
        pop2.species.speciate(config, pop2.population, pop2.generation) # separate the population into species 
        pop2.reporters.end_generation(config, pop2.population, pop2.species) # call the end generation funtion to tell the reporters that this generation is ended
        pop2.generation+=1 # add one to the generation counter
        
 # playerNet fitness function for sim mode
def eval_player(genome, config, currentGame):
    global plotGenerationNumberPlayer
    global plotFitnessOfPlayer
    genome = genome[1] # set the genome to the actual genome and ignore the id value at position 0
    fitness = 0 # local var fitness
    net = neat.nn.FeedForwardNetwork.create(genome, config) # create the net using the library function and pass the genome for the player and the config file
    inputs = currentGame.getInputs() # get the current game state
    outputs = net.activate(inputs) # pass the game state to the net that was just created
    currentGame.Player.calculateMovement(0,0,outputs) # pass the outputs of the net to the calculate movement function inside of the player class inside of the current game object
    if currentGame.winOrLose() == -1: # if the player dies fitness is zero
            fitness = 0
    elif currentGame.winOrLose() == -2: # if the player wins fitness is set to a large value plus the current distance from the enemy
        fitness = 1000+currentGame.dist()/100
    else: # if nobody wins the player fitness is a middle value plus the distance to the enemy
        fitness = 500+currentGame.dist()/10
    plotFitnessOfPlayer.append(fitness)
    plotGenerationNumberPlayer.append(pop2.generation)
    return fitness # return the fitness value calculated

def returnExistingFitnessValues(genomes, config):
    for gneomeid, genome in genomes: # this code does pretty much nothing and just sets the fitness value to itself, the only point of this function is so i can use it to pass the current fitness values assigned during the eval player function back to the net when creating the next generation
        genome.fitness = genome.fitness
        print(genome.fitness, genome)

def eval_enemy(genome, config, j):
    # get the globals and delare the locals needed
        global plotFitnessOfPlayer
        global plotFitnessOfEnemy
        global plotGenerationNumberEnemy
        global currGame
        currGame = []
        global pop2
        currGame = game.game(root, canvas, 0,0,0,0,2) # create new instance of game class
        population2 = list(iteritems(pop2.population)) # create a list containing the population of genomes inside of the pop class
        iters = 0 # create a local var called iters to be used to count what frame this instance of game is on, this could be used with i in range() in a for loop but i just felt like using a while loop when i wrote this function
        # declare a local var called net that is the current genome's net
        net = neat.nn.FeedForwardNetwork.create(genome, config) # create the actual net from the genome settings and the conig file settings 
        while iters < 2500:
            iters += 1
            inputs = currGame.getInputs() # get the current game state variables to be passed to the neural net (the vars are the x and y of the player and the enemy)
            outputs = net.activate(inputs) # pass the vars to the neural net and take the outputs of the net and save them to the local var outputs
            currGame.Enemy.movement(outputs) # pass the outputs from the net to the enemy class
            genome = population2[j-1] # the genome for the player character is the current iteration of the enemy fitness value minus one 
            eval_player(genome, config, currGame) # pass the genome config and current game class to the player fitness function
            #print(pop2.population[j].fitness)
            currGame.Player.draw(20) # call the draw function inside of the player class from the current game object
            
            fitness = 0 # local var for fitness value of enemy
            
            if currGame.winOrLose() == -1: # if enemy wins fitness is equal to a large value minus how many frames it took to win
                fitness = 100000-iters
                break # exit the loop
            elif currGame.winOrLose() == -2: # if the player wins then fitness is equal to a small value minus the distance to the player that the enemy was
                fitness = 500-currGame.dist()
                break
            else: # if nobody wins then fitness is equal to a middle value minus the distance to the player
                fitness = 1000-currGame.dist()
                
            currGame.draw(0,0,0,0) # call the game class draw function
        population2[j-1][1].fitness = eval_player(genome, config, currGame) # set the fitness value of the current player genome to the output of the player fitness function
        print(population2[j-1][1].fitness, "player fitness value") # print the player fitness and the enemy fitness
        print(fitness, "enemy fitness value")
        plotFitnessOfEnemy.append(fitness)
        plotGenerationNumberEnemy.append(pop.generation)
        return fitness # return the enemy fitness value
    

def run():
    # get the two vars the populations are going to be stored in
    global pop
    global pop2
    # boiler plate code to load the config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    # boiler plate code to create and record the population
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    
    # when gamemode is 2 (simulation mode) create a new population called pop2 
    # add the reporter objects from the neat library in order to be able to call functions from the reporter object later on in the fitness function
    if gameMode == 2:
        pop2 = neat.Population(config)
        stats2 = neat.StatisticsReporter()
        pop2.add_reporter(stats2)
        pop2.add_reporter(neat.StdOutReporter(True))
        # retrieve and set global variables typically contained in the population class, however i found it to simply be easier for this project to just make them global instead as i need to access them a lot from outside of the population class
        global stagnation
        stagnation = config.stagnation_type(config.stagnation_config, pop2.reporters)
        global reporters
        reporters = pop2.reporters
        global species
        species = config.species_set_type(config.species_set_config, reporters)
        
    global Game # get the game global variable 
    # run the AI for a number of generations using eval_genomes as the fitness fuction
    if gameMode == 0: # when gamemode is on single player call the population.run function from the neat library on it, parse the fitness function and the number of generations to run
        winner = pop.run(eval_genomes, generations)
        print(winner) # print the weights of the best genome
    elif gameMode == 1: # if in multiplayer mode
        Game = game.game(root, canvas, 0,0,0,0, gameMode) # create an instance of the game class inside of the global Game variable
        gameWon = False # set gameWon to false 
        while True: # forever loop through checking if the user has inputted a value
            outputs = [None, None, None, None] # these outputs are the inputs for the enemy class, they are parsed the same way as inside the neat function, created as a list and passed directly to the enemy class for decoding
            # if the player presses one of the move keys set the corresponding output value to one otherwise set it to 0
            if keyboard.is_pressed('w'):
                outputs[3] = 1
            else:
                outputs[3] = 0
            if keyboard.is_pressed('a'):
                outputs[2] = 1
            else:
                outputs[2] = 0
            if keyboard.is_pressed('s'):
                outputs[1] = 1
            else:
                outputs[1] = 0
            if keyboard.is_pressed('d'):
                outputs[0] = 1
            else:
                outputs[0] = 0
            Game.Enemy.movement(outputs) # pass the outputs list directly to the enemy class for decoding and executing
            if Game.winOrLose() == -1: # if enemy touches the player set gameWon to true to end the game 
                print("Player 2 wins")
                gameWon = True
            elif Game.winOrLose() == -2:
                print("Player 1 wins")
                gameWon = True
            Game.draw(0,0,0,0)
            
            while gameWon:
                Game.canvas.update() # update the game canvas, if i do not call this the window will simply crash. the reason for this as far as i can tell is that the code is in an infinite loop without updating the window so windows assumes the window has become unresponsive
                if keyboard.is_pressed(' '): # when space key is pressed create a fresh instance of the game class
                    Game = game.game(root, canvas, 0,0,0,0, gameMode)
                    gameWon = False # set gamewon back to default to exit the game over loop 
    elif gameMode == 2: # when simulation mode is on create a new game instance and call the run function on pop
        # declare a game for simulation play
        Game = game.game(root, canvas, 0,0,0,0, gameMode)
        
        pop.run(eval_genomes, 10)

    
#check if you are in the main file and if you are run the program (this is a library requirement)
if __name__ == '__main__':
    run()

import sumfitnesses

plotMeanFitnessEnemy = sumfitnesses.sumfitnesses()
#print(plotFitnessOfEnemy)
#print(plotGenerationNumberEnemy)
print(plotMeanFitnessEnemy.sumfitnesses(plotFitnessOfEnemy, plotGenerationNumberEnemy))
plt.plot(plotMeanFitnessEnemy.sumfitnesses(plotFitnessOfEnemy, plotGenerationNumberEnemy))
plt.show()