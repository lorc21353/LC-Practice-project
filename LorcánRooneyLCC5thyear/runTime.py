import game
import player
import enemy
import neat
import time
import os
gameMode = int(input("select gamemode (0 = singleplayer, 1 = multiplayer, 2 = simualtion): "))

runs_per_net = 5
game_time = 10

def eval_genome(genome, config):
    global gameMode
    global runs_per_net
    global game_time
    startTime = time.time_ns()/1000000000
    
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # as there is more than one run per genome the fitness will need to reflect the normal performance, thus it is placed in a list
    fitnesses = []
    
    # do the required number of runs for each net
    for run in range(runs_per_net):
        game = game.game(0,0,0,0, gameMode)
        fitness = 0
        
        while currTime-startTime <= game_time:
            currTime = time.time_ns()/1000000000     
            inputs = game.getInputs()
            outputs = net.activate(inputs)
            game.Enemy.movement(outputs)
            game.draw(0,0,0,0)
            if game.winOrLose() == -1:
                fitness = 1000
            elif game.winOrLose() == -2:
                fitness = 0
            else:
                fitness = -970+game.winOrLose()
                
        fitnesses.append(fitness)
        
    # genomes fitness is its worst across all of its runs
    return min(fitnesses)

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

def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(1, eval_genome)
    winner = pop.run(pe.evaluate)
    print(winner)
    
    
if __name__ == '__main__':
    run()    