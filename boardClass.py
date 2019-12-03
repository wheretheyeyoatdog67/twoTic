import pygame
import os
import math 

screen_WIDTH = 800
screen_HEIGHT = 700
sideBar = 100
blockWidth = int((screen_WIDTH-sideBar)/14) #blockWidth x blockWidth blocks
blockHeight = screen_HEIGHT/14
halfBlockWidth = blockWidth/2
bg = pygame.image.load("assets/bg3.png")
bgRotate2 = pygame.transform.rotate(bg, 270)
bgRotate = pygame.transform.rotate(bg, 90)

colors = [(0,100,0),(255,0,0)]

header = pygame.image.load("assets/twotick.png")
crate = pygame.transform.scale(pygame.image.load("assets/crate.png"),(50,50))
bomb =[pygame.transform.scale(pygame.image.load(os.path.join("assets","bomb","bomb" + str(x) + ".png")),(30,30)) for x in range(1,8)]

class Board:
	def __init__(self):
		self.blocks = []

	def drawBoard(self,screen,goMode):
		screen.blit(bgRotate,(0,0))
		screen.blit(bgRotate2,(460,0))
		for col in range(21):pygame.draw.line(screen, (204, 145, 94), (blockWidth*col,0), (blockWidth*(col),screen_HEIGHT), 3)
		for row in range(21):pygame.draw.line(screen,(204, 145, 94), (0,blockHeight*row), (screen_WIDTH, blockHeight*row), 3)
		rect = pygame.Rect(700,0,100,700)
		rect2 = pygame.Rect(410,10,80,blockWidth)
		if goMode == True:col = colors[0]
		else: col = colors[1]
		screen.blit(header,(-blockWidth-50,-25))
		pygame.draw.rect(screen,(67,93,73),rect)
		pygame.draw.circle(screen,col,(750,50),30)
		pygame.draw.circle(screen,(97,42,63),(750,50),40)
		pygame.draw.circle(screen,col,(750,50),30)

	def drawBlocks(self,screen,frame):
		if(len(self.blocks)!=0):
			for block in self.blocks:

				posX =  block[0]*blockWidth-blockWidth
				posY =	block[1]*blockWidth-blockWidth
				if block[2] == 0:
					screen.blit(crate,(posX,posY))
				else:
					screen.blit(bomb[frame-1],(posX,posY))

	def blockCol(self,projectiles):
		projC = 0
		for proj in projectiles:
			blockC = 0
			for block in self.blocks:
				if(math.floor(proj.x/50)+1 == block[0] and math.floor(proj.y/50)+1 == block[1]):
					print("collision")
					del self.blocks[blockC]
					del projectiles[projC]
					break
				blockC +=1
			projC+=1