class Logger:
	def __init__(self, solutionFilePath, logFilePath):
		self.solutionFilePath = solutionFilePath
		self.logFilePath = logFilePath

	#logs snapshot of initial board, including pacman, ghosts, walls, pills, and fruit. 
	def createFirstSnapShot(self, board):
		#logFile = open(self.logFilePath, "a")
		board.solution.append([str(board.width) + "\n" + str(board.height) + "\n" + \
			"m " + str(board.pacman1.positionx) + " " + str(board.pacman1.positiony)])
		for x in range(1,4):
			board.solution.append(["\n" + str(x) + " " + str(board.ghost1.positionx) + " " + str(board.ghost1.positiony)])
		for x in range(len(board.grid)):
			for y in range(len(board.grid[0])):
				if board.grid[x][y] == "w":
					board.solution.append(["\nw" + " " + str(x) + " " + str(y)])
		for x in range(len(board.grid)):
			for y in range(len(board.grid[0])):
				if board.grid[x][y] == "p":
					board.solution.append(["\np" + " " + str(x) + " " + str(y)])
		board.solution.append("\nt " + str(board.time) + " " + str(board.pacman1.score))

	#log pacman's move for solution
	def recordPacmanMove(self, board):
		board.solution.append(["\nm " + str(board.pacman1.positionx) + " " + str(board.pacman1.positiony)])

	#log ghosts' moves
	def recordGhostMove(self, ghostNum, board):
		#logFile = open(self.logFilePath, "a")
		if ghostNum == 1:
			board.solution.append(["\n" + str(ghostNum) + " " + str(board.ghost1.positionx) + " " + str(board.ghost1.positiony)])
		elif ghostNum == 2:
			board.solution.append(["\n" + str(ghostNum) + " " + str(board.ghost2.positionx) + " " + str(board.ghost2.positiony)])
		elif ghostNum == 3:
			board.solution.append(["\n" + str(ghostNum) + " " + str(board.ghost3.positionx) + " " + str(board.ghost3.positiony)])

	#log time and score
	def recordTime(self, board):
		#logFile = open(self.logFilePath, "a")
		board.solution.append(["\nt " + str(board.time) + " " + str(board.pacman1.score)])

	#log if fruit has been placed
	def recordFruit(self, board):
		#logFile = open(self.logFilePath, "a")
		board.solution.append(["\nf " + str(board.fruitx) + " " + str(board.fruity)])

	#log increase in score for resultslog during evaluation phase
	def recordChangeInScore(self, eval, score):
		logFile = open(self.logFilePath, "a")
		logFile.write("\n" + str(eval) + "\t" + str(score))

	#log initial parameters from cfg file for resultslog
	def recordInitParams(self, seed, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier):
		logFile = open(self.logFilePath, "a")
		logFile.write("Result Log\nWidth: " + str(width) + "\nHeight: " + str(height) + "\nPill Density: " + str(pillDensity) + \
			"\nWall Density: " + str(wallDensity) + "\nFruit Probability: " + str(fruitProbability) + "\nFruit Score: " + str(fruitScore) + \
			"\nTime Multiplier: " + str(timeMultiplier) + "\nSeed: " + str(seed) + "\n")

	#log best solution for solutionLog
	def recordBestSolution(self, solution):
		logFile = open(self.solutionFilePath, "a")
		for elem in solution:
			logFile.write("".join(elem))

	#log current run for the search
	def recordNewRun(self, run, seed):
		logFile = open(self.logFilePath, "a")
		logFile.write("\n\nRun " + str(run) + "\nSeed: " + str(seed))



