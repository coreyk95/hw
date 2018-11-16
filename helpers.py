import random
import configparser
import sys

#load in parameters from cfg file
def loadConfig():
	if len(sys.argv) == 2:
		cfgFile = sys.argv[1]
	else:
		cfgFile = 'default.cfg'

	config = configparser.ConfigParser()
	config.read(cfgFile)
	solutionFilePath = config['GPAC']['SolutionFilePath']
	logFilePath = config['GPAC']['LogFilePath']
	height = int(config['GPAC']['Height'])
	width = int(config['GPAC']['Width'])
	pillDensity = int(config['GPAC']['PillDensity'])
	wallDensity = int(config['GPAC']['WallDensity'])
	fruitProbability = int(config['GPAC']['FruitSpawnProbability'])
	fruitScore = int(config['GPAC']['FruitScore'])
	timeMultiplier = int(config['GPAC']['TimeMultiplier'])
	randomSeed = config['GPAC']['RandomSeed']
	runs = int(config['GPAC']['Runs'])
	evals = int(config['GPAC']['FitnessEvals'])
	return solutionFilePath, logFilePath, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier, randomSeed, runs, evals

#prints the pacman board
def print_grid(grid):
    for row in grid:
        print(row)