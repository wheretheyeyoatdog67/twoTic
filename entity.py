class Entity:
	#IMGS = player1_images
	def __init__(self, x, y,dir):
		self.x = x
		self.y = y
		self.tilt = 0  # degrees to tilt
		self.tick_count = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]
		self.shotOnTurn = False
		self.projectiles = []
		self.alive = True
		self.blockX = int(self.x/blockWidth + 1)
		self.blockY = int(self.y/blockWidth + 1)
		self.blockRight = False
		self.blockLeft = False
		self.blockAbove = False
		self.blockBelow = False
		self.dir = dir
		self.still = True

	def drawEntity(self):
		global frame
		if self.still == True:
			screen.blit((testSprite.images[self.dir*8+5]),(self.x-5,self.y-45))
		else:
			screen.blit((testSprite.images[self.dir*8+frame]),(self.x-5,self.y-45))

	def setpos(self,x,y):
		self.x = x 
		self.y = y
		screen.blit(self.img,(self.x,self.y))

	def rotate(self):
		global img
		self.img = pygame.transform.rotate(self.img, 90)

	def update(self):
		if self.alive == True:
			self.blockX = int(self.x/blockWidth + 1)
			self.blockY = int(self.y/blockWidth + 1)
			self.drawEntity()

	def removeDeactiveProj(self):
		#print((self.projectiles))
		for i in range(len(self.projectiles)):
			if self.projectiles[i-1].active == False:
				del self.projectiles[i-1]
				break

	def projOnBlock(self,entX,entY):
		if self.alive == False:
			return True
		if len(self.projectiles) ==0: 
			return False
		for i in range(len(self.projectiles)):
			if(entX == self.projectiles[i].x and entY == self.projectiles[i].y+blockWidth):return True
		else: return False

	def collide(self,projectiles):
		for proj in projectiles:
			bNumPx = math.floor(proj.x/blockWidth + 1)
			bNumPy = math.floor(proj.y/blockWidth + 1)
			if (self.blockX == bNumPx and self.blockY == bNumPy):
				self.alive = False

	def nextObj(self,blockArr):
		self.blockRight = False
		self.blockLeft = False
		self.blockBelow = False
		self.blockAbove = False
		for block in blockArr:
			if (block[0]-self.blockX == 1 and block[1] == self.blockY):self.blockRight = True
			if (block[0]-self.blockX == -1 and block[1] == self.blockY):self.blockLeft = True
			if (block[1]-self.blockY == 1 and block[0] == self.blockX):self.blockBelow = True
			if (block[1]-self.blockY == -1 and block[0] == self.blockX):self.blockAbove = True