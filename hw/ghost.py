class Ghost:
	def __init__(self, positionx, positiony, ghostNumber):
		self.positionx = positionx
		self.positiony = positiony
		self.previousx = positionx
		self.previousy = positiony
		self.ghostNumber = ghostNumber