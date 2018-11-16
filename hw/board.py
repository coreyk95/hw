from pacman import Pacman
from ghost import Ghost
from logger import Logger
import random
import collections
from contextlib import suppress


class Board:
	def __init__(self, solutionFilePath, logFilePath, height, width, pillDensity, wallDensity, fruitProbability, fruitScore, timeMultiplier):
		self.pacman1 = Pacman(0,height-1)
		self.ghost1 = Ghost(width-1,0,1)
		self.ghost2 = Ghost(width-1,0,2)
		self.ghost3 = Ghost(width-1,0,3)
		self.solutionFilePath = solutionFilePath
		self.logFilePath = logFilePath
		self.height = height
		self.width = width
		self.pillDensity = pillDensity
		self.wallDensity = wallDensity
		self.fruitProbability = fruitProbability
		self.fruitScore = fruitScore
		self.timeMultiplier = timeMultiplier
		self.time = timeMultiplier * width * height
		self.grid = [[]]
		self.hasFruit = False
		self.logger = Logger(self.solutionFilePath, self.logFilePath)
		self.numPills = 0 #pills pacman currently has
		self.totalPills = 0
		self.didSpawn = False
		self.fruitx = -1 #fruit position
		self.fruity = -1
		self.solution = []

	#shortest path algorithm. only used to initialize walls. start is pacmans
	#initial position, goal is a surround cell of wall
	def bfs(self, grid, start, goal):
	    queue = collections.deque([[start]])
	    seen = set([start])
	    while queue:
	        path = queue.popleft()
	        x, y = path[-1]
	        if x == goal[0] and y == goal[1]:
	            return path
	        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
	            if 0 <= x2 < self.width and 0 <= y2 < self.height and grid[x2][y2] != "w" and (x2, y2) not in seen:
	                queue.append(path + [(x2, y2)])
	                seen.add((x2, y2))

	#Checks to see if surrounding, non-wall cells are reachable
	def isReachable(self, grid, start, goal):
		path = ()
		x = goal[0]
		y = goal[1]
		with suppress(IndexError):
			#check cell above
			if grid[x][y-1] != "w" and y-1 >= 0:
				path = self.bfs(grid, start, (x, y-1))
				if path is None:
					return False
		with suppress(IndexError):
			#check cell below
			if grid[x][y+1] != "w":
				path = self.bfs(grid, start, (x, y+1))
				if path is None:
					return False
		with suppress(IndexError):
			#check cell left
			if grid[x-1][y] != "w" and x-1 >= 0:
				path = self.bfs(grid, start, (x-1, y))
				if path is None:
					return False
		with suppress(IndexError):
			#check cell right
			if grid[x+1][y] != "w":
				path = self.bfs(grid, start, (x+1, y))
				if path is None:
					return False	
		return True

	#places walls depending on wall density
	def placeWalls(self):
		tempGrid = [["*"] * self.height for i in range(self.width)]
		tempGrid[self.pacman1.positionx][self.pacman1.positiony] = "m"
		tempGrid[self.ghost1.positionx][self.ghost1.positiony] = "1"
		for x in range(len(tempGrid)):
			for y in range(len(tempGrid[0])):
				if random.randint(0,100) < self.wallDensity:
					if tempGrid[x][y] != "m" and tempGrid[x][y] != "1":
						tempGrid[x][y] = "w"
						#check if surrounding non-wall cells are reachable, if not, delete it
						if not(self.isReachable(tempGrid, (self.pacman1.positionx, self.pacman1.positiony), (x, y))):
							tempGrid[x][y] = "*"
		return tempGrid

	#place pills depending on pilldensity. won't place pill on initial pacman or walls
	def placePills(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				if random.randint(0,100) < self.pillDensity:
					if self.grid[x][y] != "m" and self.grid[x][y] != "1" and self.grid[x][y] != "w":
						self.grid[x][y] = "p"
						self.totalPills += 1

	#place a fruit depending on the fruitprobability. won't place if there's already fruit on board
	def placeFruit(self):
		if random.randint(0,100) < self.fruitProbability and self.hasFruit == False:
			while self.hasFruit == False:
				x = random.randint(0, len(self.grid) - 1)
				y = random.randint(0, len(self.grid[0]) - 1)
				if self.grid[x][y] != "w" and self.grid[x][y] != "p":
					self.hasFruit = True
					self.grid[x][y] = "f"
					self.fruitx = x
					self.fruity = y
					return True
		return False

	#set board up with initial walls and pills, then record that setup
	def initializeBoard(self):
		self.grid = self.placeWalls()
		self.placePills()
		self.logger.createFirstSnapShot(self)

	#Check where pacman is and run it against his possible choices to move. Corner cases are if he's in corners or against a wall
	def choosePacmanMove(self):
		#not against anything
		if self.pacman1.positionx > 0 and self.pacman1.positiony > 0 and self.pacman1.positionx < self.width-1 and self.pacman1.positiony < self.height-1:
			move = random.choice(["left", "right", "up", "down", "hold"])
		#against bottom wall
		elif self.pacman1.positionx > 0 and self.pacman1.positiony > 0 and self.pacman1.positionx < self.width-1:
			move = random.choice(["left", "right", "up", "hold"])
		#against right wall
		elif self.pacman1.positionx > 0 and self.pacman1.positiony > 0 and self.pacman1.positiony < self.height-1:
			move = random.choice(["left", "up", "down", "hold"])
		#against top wall
		elif self.pacman1.positionx > 0 and self.pacman1.positionx < self.width-1 and self.pacman1.positiony < self.height-1:
			move = random.choice(["left", "right", "down", "hold"])
		#against left wall
		elif self.pacman1.positiony > 0 and self.pacman1.positionx < self.width-1 and self.pacman1.positiony < self.height-1:
			move = random.choice(["right", "up", "down", "hold"])
		#in top left corner
		elif self.pacman1.positionx < self.width-1 and self.pacman1.positiony < self.height-1:
			move = random.choice(["right", "down", "hold"])
		#in bottom left corner
		elif self.pacman1.positiony > 0 and self.pacman1.positionx < self.width-1:
			move = random.choice(["right", "up", "hold"])
		#in top right corner
		elif self.pacman1.positionx > 0 and self.pacman1.positiony < self.height-1:
			move = random.choice(["left", "down", "hold"])
		#in bottom right corner
		elif self.pacman1.positionx > 0 and self.pacman1.positiony > 0:
			move = random.choice(["left", "up", "hold"])
		return move

	#Check where ghosts are and run it against his possible choices to move. Corner cases are if they're in corners or against a wall
	def chooseGhostMove(self, ghostNum):
		if ghostNum == 1:
			ghost = self.ghost1
		elif ghostNum == 2:
			ghost = self.ghost2
		elif ghostNum == 3:
			ghost = self.ghost3
		if ghost.positionx > 0 and ghost.positiony > 0 and ghost.positionx < self.width-1 and ghost.positiony < self.height-1:
			move = random.choice(["left", "right", "up", "down"])
		elif ghost.positionx > 0 and ghost.positiony > 0 and ghost.positionx < self.width-1:
			move = random.choice(["left", "right", "up"])
		elif ghost.positionx > 0 and ghost.positiony > 0 and ghost.positiony < self.height-1:
			move = random.choice(["left", "up", "down"])
		elif ghost.positionx > 0 and ghost.positionx < self.width-1 and ghost.positiony < self.height-1:
			move = random.choice(["left", "right", "down"])
		elif ghost.positiony > 0 and ghost.positionx < self.width-1 and ghost.positiony < self.height-1:
			move = random.choice(["right", "up", "down"])
		elif ghost.positionx < self.width-1 and ghost.positiony < self.height-1:
			move = random.choice(["right", "down"])
		elif ghost.positiony > 0 and ghost.positionx < self.width-1:
			move = random.choice(["right", "up"])
		elif ghost.positionx > 0 and ghost.positiony < self.height-1:
			move = random.choice(["left", "down"])
		elif ghost.positionx > 0 and ghost.positiony > 0:
			move = random.choice(["left", "up"])
		return move

	#choose a move from choosePacmanMove and checks if he can move there (i.e. no wall). Runs until he can move to selected spot and moves there
	def makePacmanMove(self):
		choseMove = False
		while(choseMove == False):
			move = self.choosePacmanMove()
			if move == "right" and self.grid[self.pacman1.positionx+1][self.pacman1.positiony] != "w":
				self.pacman1.previousx, self.pacman1.previousy = self.pacman1.positionx, self.pacman1.positiony
				self.pacman1.positionx, self.pacman1.positiony = self.pacman1.positionx+1, self.pacman1.positiony
				choseMove = True
			elif move == "left" and self.grid[self.pacman1.positionx-1][self.pacman1.positiony] != "w":
				self.pacman1.previousx, self.pacman1.previousy = self.pacman1.positionx, self.pacman1.positiony
				self.pacman1.positionx, self.pacman1.positiony = self.pacman1.positionx-1, self.pacman1.positiony
				choseMove = True
			elif move == "up" and self.grid[self.pacman1.positionx][self.pacman1.positiony-1] != "w":
				self.pacman1.previousx, self.pacman1.previousy = self.pacman1.positionx, self.pacman1.positiony
				self.pacman1.positionx, self.pacman1.positiony = self.pacman1.positionx, self.pacman1.positiony-1
				choseMove = True
			elif move == "down" and self.grid[self.pacman1.positionx][self.pacman1.positiony+1] != "w":
				self.pacman1.previousx, self.pacman1.previousy = self.pacman1.positionx, self.pacman1.positiony
				self.pacman1.positionx, self.pacman1.positiony = self.pacman1.positionx, self.pacman1.positiony+1
				choseMove = True
			elif move == "hold":
				self.pacman1.previousx, self.pacman1.previousy = self.pacman1.positionx, self.pacman1.positiony
				choseMove = True
			else:
				choseMove = False

	#choose a move from chooseGhostMove and checks if they can move there (i.e. no wall). Runs until they can move to selected spot and moves there
	def makeGhostMove(self, ghostNum):
		choseMove = False
		#choose ghost to move
		if ghostNum == 1:
			ghost = self.ghost1
		elif ghostNum == 2:
			ghost = self.ghost2
		elif ghostNum == 3:
			ghost = self.ghost3
		while(not(choseMove)):
			move = self.chooseGhostMove(ghostNum)
			if move == "right" and self.grid[ghost.positionx+1][ghost.positiony] != "w": #check for walls
				ghost.previousx, ghost.previousy = ghost.positionx, ghost.positiony
				ghost.positionx, ghost.positiony = ghost.positionx+1, ghost.positiony
				choseMove = True
			elif move == "left" and self.grid[ghost.positionx-1][ghost.positiony] != "w":
				ghost.previousx, ghost.previousy = ghost.positionx, ghost.positiony
				ghost.positionx, ghost.positiony = ghost.positionx-1, ghost.positiony
				choseMove = True
			elif move == "up" and self.grid[ghost.positionx][ghost.positiony-1] != "w":
				ghost.previousx, ghost.previousy = ghost.positionx, ghost.positiony
				ghost.positionx, ghost.positiony = ghost.positionx, ghost.positiony-1
				choseMove = True
			elif move == "down" and self.grid[ghost.positionx][ghost.positiony+1] != "w":
				ghost.previousx, ghost.previousy = ghost.positionx, ghost.positiony
				ghost.positionx, ghost.positiony = ghost.positionx, ghost.positiony+1
				choseMove = True
			else:
				choseMove = False

	#move all characters and places fruit according to probability
	def runTurn(self):
		self.makePacmanMove()
		self.makeGhostMove(1)
		self.makeGhostMove(2)
		self.makeGhostMove(3)
		self.didSpawn = self.placeFruit()
		self.time -= 1

	#moves characters until the games are over and records to solution
	def runGame(self):
		gameOver = False
		while(self.time > 0 and not(gameOver)):
			self.runTurn()
			#Check if pac and ghost are on same cell
			if (self.pacman1.positionx == self.ghost1.positionx and self.pacman1.positiony == self.ghost1.positiony) or \
			   (self.pacman1.positionx == self.ghost2.positionx and self.pacman1.positiony == self.ghost2.positiony) or \
			   (self.pacman1.positionx == self.ghost3.positionx and self.pacman1.positiony == self.ghost3.positiony):
				gameOver = True
			#Check if pac and ghost exchanged cells
			elif (self.pacman1.positionx == self.ghost1.previousx and self.pacman1.positiony == self.ghost1.previousy and self.pacman1.previousx == self.ghost1.positionx and self.pacman1.previousy == self.ghost1.positiony) or \
			   (self.pacman1.positionx == self.ghost2.previousx and self.pacman1.positiony == self.ghost2.previousy and self.pacman1.previousx == self.ghost2.positionx and self.pacman1.previousy == self.ghost2.positiony) or \
			   (self.pacman1.positionx == self.ghost3.previousx and self.pacman1.positiony == self.ghost3.previousy and self.pacman1.previousx == self.ghost3.positionx and self.pacman1.previousy == self.ghost3.positiony):		
			   	gameOver = True
			#check for consumed pill
			elif (self.grid[self.pacman1.positionx][self.pacman1.positiony] == "p"):
				self.numPills += 1
				self.pacman1.score = int((self.numPills/self.totalPills)*100)
				self.grid[self.pacman1.positionx][self.pacman1.positiony] = "*"
			#check for consumed fruit
			elif (self.grid[self.pacman1.positionx][self.pacman1.positiony] == "f"):
				self.pacman1.score += self.fruitScore
				self.hasFruit = False
				self.grid[self.pacman1.positionx][self.pacman1.positiony] = "*"
			#check if all pills gone
			if self.totalPills == self.numPills:
				self.pacman1.score += int((self.time/self.timeMultiplier * self.width * self.height)*100)
				gameOver = True
			#record to solutionlog
			self.logger.recordPacmanMove(self)
			self.logger.recordGhostMove(1, self)
			self.logger.recordGhostMove(2, self)
			self.logger.recordGhostMove(3, self)
			#check if fruit spawned this turn
			if self.didSpawn == True:
				self.logger.recordFruit(self)
			self.logger.recordTime(self)
		







