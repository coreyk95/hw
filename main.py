from board import Board
import helpers
import random
from pprint import pprint
from logger import Logger
from datetime import datetime
import time



def main():
	#grab params
	solutionFilePath, logFilePath, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier, randomSeed, runs, evals = helpers.loadConfig()
	bestSolution = []
	bestScore = 0
	logger = Logger(solutionFilePath, logFilePath)
	logger.recordInitParams(randomSeed, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier)

	if randomSeed == "-1":
		seed = datetime.now()
	else:
		seed = datetime.strptime(randomSeed, '%Y-%m-%d %H:%M:%S.%f')

	seedInt = int(time.mktime(seed.timetuple()))

	for i in range(1, runs + 1):
		logger.recordNewRun(i, seed) #record current run
		tempSolution = []
		tempScore = 0
		for k in range(1, evals + 1):	
			print(k)	
			seedInt += 1
			seed = datetime.fromtimestamp(seedInt)
			random.seed(seed) #set new seed for a new board
			board = Board(solutionFilePath, logFilePath, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier)
			board.initializeBoard()
			board.runGame()
			if board.pacman1.score > tempScore: #keep track of best score/solution for current run
				tempScore = board.pacman1.score
				tempSolution = board.solution
				logger.recordChangeInScore(k, tempScore)
		if tempScore > bestScore: #keep track of best score/solution across all runs
			bestScore = tempScore
			bestSolution = tempSolution
	print(bestScore)
	logger.recordBestSolution(bestSolution)


if __name__ == "__main__":
	main()