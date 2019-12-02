import pygame
import random
import os
import math
import json



#INIT
pygame.font.init()  # init font
WIN_WIDTH = 800
WIN_HEIGHT = 700
# WIN_WIDTH = 800
# WIN_HEIGHT = 700
sideBar = 100
clockSpeed = 100
blockWidth = int((WIN_WIDTH-sideBar)/14) #blockWidth x blockWidth blocks

blockHeight = WIN_HEIGHT/14

halfBlockWidth = blockWidth/2

#SCREEN AND CLOCK
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("2Tic")

#Image Initiation
bg = pygame.image.load("assets/bg3.png")
bgRotate2 = pygame.transform.rotate(bg, 270)
bgRotate = pygame.transform.rotate(bg, 90)
player1_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets","imgs","bird" + str(x) + ".png")),(50,40)) for x in range(1,4)]
intro_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets","intro","sun" + str(x) + ".png")),(800,700)) for x in range(0,7)]
header = pygame.image.load("assets/twotick.png")
crate = pygame.transform.scale(pygame.image.load("assets/crate.png"),(50,50))
colors = [(0,100,0),(255,0,0)]

#Timer Rule
goMode = True


#Music
pygame.mixer.init()
musicPaused = False

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
		
	def displayShot(self):
		ticksPerMove = clockSpeed/50
		if(goMode == True):
			if(count%ticksPerMove == 0 and self.direction == True):
				self.y-=self.time
			if(count%ticksPerMove == 0 and self.direction == False):
				self.y+=self.time
		pygame.draw.circle(WIN,(255,0,0),(self.x,self.y),10)
		
	def update(self):
		self.isActive()
		if self.active == True:self.displayShot()

	def isActive(self):
		if (self.y < 80 or self.y >700):self.active = False
		else:self.active = True

	#collide(board.blocks,projs)
	def tragectory(self):
		pass



class Entity:
	IMGS = player1_images
	def __init__(self, x, y):
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

	def drawEntity(self):
		WIN.blit(self.img,(self.x,self.y+5))
	
	def setpos(self,x,y):
		self.x = x 
		self.y = y
		WIN.blit(self.img,(self.x,self.y))

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




# else: self.blockRight = False
# 			else: self.blockLeft = False
# 			else: self.blockBelow = False
# 			else: self.blockAbove = False
			# if(block[0]-self.blockX == -1):
			# 	self.blockLeft = True
			# else: self.blockLeft = False
			# print(self.blockX,block[0])
			# if(block[1]-self.blockY == 1 and block[0]==self.blockX):
			# 	print("Yep")
			# 	self.blockBelow = True
			# else: self.blockBelow = False
			# if(block[1]-self.blockY == -1):
			# 	self.blockAbove = True
			# else: self.blockAbove = False


class Board:
	def __init__(self):
		self.blocks = []

	def drawBoard(self):
		WIN.blit(bgRotate,(0,0))
		WIN.blit(bgRotate2,(460,0))
		for col in range(21):pygame.draw.line(WIN, (204, 145, 94), (blockWidth*col,0), (blockWidth*(col),WIN_HEIGHT), 3)
		for row in range(21):pygame.draw.line(WIN,(204, 145, 94), (0,blockHeight*row), (WIN_WIDTH, blockHeight*row), 3)
		rect = pygame.Rect(700,0,100,700)
		rect2 = pygame.Rect(410,10,80,blockWidth)
		if goMode == True:col = colors[0]
		else: col = colors[1]
		WIN.blit(header,(-blockWidth-50,-25))
		pygame.draw.rect(WIN,(67,93,73),rect)
		pygame.draw.circle(WIN,col,(750,50),30)
		pygame.draw.circle(WIN,(97,42,63),(750,50),40)
		pygame.draw.circle(WIN,col,(750,50),30)

	def drawBlocks(self):
		if(len(self.blocks)!=0):
			for block in self.blocks:
				posX =  block[0]*blockWidth-blockWidth
				posY =	block[1]*blockWidth-blockWidth
				WIN.blit(crate,(posX,posY))	




def makeMusic(filename):
    pygame.mixer.music.load(filename)


def playMusic(loops=0):
    global musicPaused
    if musicPaused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(loops)
    musicPaused = False






def gameTimer():
	global goMode
	if (count%clockSpeed == 0):
		if (goMode == False):
			goMode = True
			player1.shotOnTurn = False
			player2.shotOnTurn = False
		else: goMode = False

def updateProjectiles():
	for x in player1.projectiles:
		x.update()
	for x in player2.projectiles:
		x.update()


def runGame():
	gameTimer()
	board.drawBoard()
	board.drawBlocks()
	player1.update()
	player2.update()
	player1.nextObj(board.blocks)
	player2.nextObj(board.blocks)
	player1.collide(player2.projectiles)
	player2.collide(player1.projectiles)
	player1.removeDeactiveProj()
	player2.removeDeactiveProj()
	updateProjectiles()
	pygame.display.update()
	

def intro():
	intro = True
	playMusic(1)
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				intro = False
		for x in intro_image:
			WIN.blit(x,(0,0))
			pygame.display.update()



makeMusic("hotline.ogg")
gameRule = True

if __name__ == "__main__":
	while gameRule:
		intro()
		board = Board()
		player1 = Entity(200,150)
		player2 = Entity(200,100)
		game = True
		count = 0
		maps = []
		while game:
			#Inputs and Exit
			gameTick = pygame.time.get_ticks()
			if (gameTick%1 == 0):
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						gameRule = False
						game = False
					if event.type == pygame.MOUSEBUTTONDOWN:
						x,y = pygame.mouse.get_pos()
						if (x < 700 and y > 100):
							row = math.ceil(x/blockWidth)
							col = math.ceil(y/blockWidth)
							board.blocks.append([row,col])
						# player1.x,player1.y = pygame.mouse.get_pos()
						# print("Coordinates(x,y): %s , %s" % (str(player1.x), str(player1.y)))
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_0:
							game= False
						# if goMode == True:
						if True:
							if event.key == pygame.K_a and player1.x != 0 and player1.blockLeft == False:player1.x -= blockWidth;
							if event.key == pygame.K_d and player1.x != WIN_WIDTH-150 and player1.blockRight == False:player1.x += blockWidth;
							if event.key == pygame.K_w and player1.y != 100 and player1.blockAbove == False:player1.y -= blockWidth;
							if event.key == pygame.K_s and player1.y != WIN_HEIGHT-50 and player1.blockBelow == False:player1.y += blockWidth;
							if event.key == pygame.K_LEFT and player2.x != 0 and player2.blockLeft == False:player2.x -= blockWidth;
							if event.key == pygame.K_RIGHT and player2.x != WIN_WIDTH-150 and player2.blockRight == False:player2.x += blockWidth;
							if event.key == pygame.K_UP and player2.y != 100 and player2.blockAbove == False:player2.y -= blockWidth;
							if event.key == pygame.K_DOWN and player2.y != WIN_HEIGHT-50 and player2.blockBelow == False:player2.y += blockWidth;
						if (event.key == pygame.K_1 and goMode == False):
							if (player1.projOnBlock(player1.x,player1.y) == False and player1.shotOnTurn == False):
								player1.projectiles.append(Projectile(player1.x,player1.y,True))
								player1.shotOnTurn = True
						if (event.key == pygame.K_2 and goMode == False):
							if (player1.projOnBlock(player1.x,player1.y) == False and player1.shotOnTurn == False):
								player1.projectiles.append(Projectile(player1.x,player1.y,False))
								player1.shotOnTurn = True
						if (event.key == pygame.K_8 and goMode == False):		
							print(player2.shotOnTurn)
							if (player2.projOnBlock(player2.x,player2.y) == False and player2.shotOnTurn == False):
								player2.projectiles.append(Projectile(player2.x,player2.y,True))
								player2.shotOnTurn = True
						if (event.key == pygame.K_9 and goMode == False):		
							print(player2.shotOnTurn)
							if (player2.projOnBlock(player2.x,player2.y) == False and player2.shotOnTurn == False):
								player2.projectiles.append(Projectile(player2.x,player2.y,False))
								player2.shotOnTurn = True


						if (event.key == pygame.K_m):
							fileName = input ("Save Map as FileName.txt: ")
							with open("maps.txt","a+") as filehandle:
								json.dump(fileName,filehandle)
							with open(fileName,'w') as filehandle:
								json.dump(board.blocks,filehandle)

						if (event.key == pygame.K_n):
							fileName = input ("Open Map as FileName.txt: ")
							if (fileName == 'list'):
								with open("maps.txt", 'r') as filehandle:
									print(json.load(filehandle))	

							fileName = input ("Open Map as FileName.txt: ")
							with open(fileName, 'r') as filehandle:
								board.blocks = json.load(filehandle)

						if (event.key == pygame.K_b):
							print(board.blocks)


					#if event.key == pygame.K_4:print(len(projs))
					#if event.key == pygame.K_1:print(pygame.time.get_ticks())
					#and goMode == False
				
			runGame()
			
	
			count+=1			



####################################################
#Controls
#           m : saves map
#			n : loads saved map
#			b: prints blocks array
#			0: restart game
#




