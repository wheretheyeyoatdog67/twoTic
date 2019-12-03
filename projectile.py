import pygame

clockSpeed = 100

class Projectile:
	def __init__(self, x, y,direction):
		self.direction = direction #True up False Down
		self.x = x + 25
		if(self.direction == True):
			self.y = y-25
		if(self.direction == False):
			self.y = y+75
		self.speed = 10
		self.time = 4
		self.active = True
		
	def displayShot(self,goMode,screen,count):
		ticksPerMove = clockSpeed/50
		if(goMode == True):
			if(count%ticksPerMove == 0 and self.direction == True):
				self.y-=self.time
			if(count%ticksPerMove == 0 and self.direction == False):
				self.y+=self.time
		pygame.draw.circle(screen,(255,0,0),(self.x,self.y),10)
		
	def update(self,goMode,screen,count):
		self.isActive()
		if self.active == True:self.displayShot(goMode,screen,count)

	def isActive(self):
		if (self.y < 80 or self.y >700):self.active = False
		else:self.active = True

	#collide(board.blocks,projs)
	def tragectory(self):
		pass



	