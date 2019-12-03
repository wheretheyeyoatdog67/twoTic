import pygame

import random
import os
import math
import json
import entity




screen_WIDTH = 800
screen_HEIGHT = 700
sideBar = 100
clockSpeed = 100
blockWidth = int((screen_WIDTH-sideBar)/14) #blockWidth x blockWidth blocks
blockHeight = screen_HEIGHT/14
halfBlockWidth = blockWidth/2



player1_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets","imgs","bird" + str(x) + ".png")),(50,40)) for x in range(1,4)]


class Entity:
	IMGS = player1_images
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

	def drawEntity(self,frame,screen,testSprite):
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

	def update(self,frame,screen,testSprite):
		if self.alive == True:
			self.blockX = int(self.x/blockWidth + 1)
			self.blockY = int(self.y/blockWidth + 1)
			self.drawEntity(frame,screen,testSprite)

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





def makeSprite(filename, frames=1):
	thisSprite = newSprite(filename, frames)
	return thisSprite

def loadImage(fileName, useColorKey=False):
	if os.path.isfile(fileName):
		image = pygame.image.load(fileName)
		image = image.convert_alpha()
		# Return the image
		return image
	else:
		raise Exception("Error loading image: " + fileName + " - Check filename and path?")



class newSprite(pygame.sprite.Sprite):
	def __init__(self, filename, frames=1):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		img = loadImage(filename)
		self.originalWidth = img.get_width() // frames
		self.originalHeight = img.get_height()
		frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
		x = 0
		for frameNo in range(frames):
			frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
			frameSurf.blit(img, (x, 0))
			self.images.append(frameSurf.copy())
			x -= self.originalWidth
		self.image = pygame.Surface.copy(self.images[0])

		self.currentImage = 0
		self.rect = self.image.get_rect()
		self.rect.topleft = (0, 0)
		self.mask = pygame.mask.from_surface(self.image)
		self.angle = 0
		self.scale = 1

	def addImage(self, filename):
		self.images.append(loadImage(filename))

	def move(self, xpos, ypos, centre=False):
		if centre:
			self.rect.center = [xpos, ypos]
		else:
			self.rect.topleft = [xpos, ypos]

	def changeImage(self, index):
		self.currentImage = index
		if self.angle == 0 and self.scale == 1:
			self.image = self.images[index]
		else:
			self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
		oldcenter = self.rect.center
		self.rect = self.image.get_rect()
		originalRect = self.images[self.currentImage].get_rect()
		self.originalWidth = originalRect.width
		self.originalHeight = originalRect.height
		self.rect.center = oldcenter
		self.mask = pygame.mask.from_surface(self.image)
		if screenRefresh:
			updateDisplay()