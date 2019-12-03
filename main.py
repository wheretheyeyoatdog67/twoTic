import pygame
import random
import os
import math
import json
import entity

#INIT
pygame.init()
pygame.font.init() 
 # init font
screen_WIDTH = 800
screen_HEIGHT = 700
# screen_WIDTH = 800
# screen_HEIGHT = 700
sideBar = 100
clockSpeed = 100
blockWidth = int((screen_WIDTH-sideBar)/14) #blockWidth x blockWidth blocks

blockHeight = screen_HEIGHT/14

halfBlockWidth = blockWidth/2

#SCREEN AND CLOCK
screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))
pygame.display.set_caption("2Tic")

#Image Initiation
bg = pygame.image.load("assets/bg3.png")
bgRotate2 = pygame.transform.rotate(bg, 270)
bgRotate = pygame.transform.rotate(bg, 90)

intro_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets","intro","sun" + str(x) + ".png")),(800,700)) for x in range(0,7)]
bomb =[pygame.transform.scale(pygame.image.load(os.path.join("assets","bomb","bomb" + str(x) + ".png")),(30,30)) for x in range(1,8)]
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
		pygame.draw.circle(screen,(255,0,0),(self.x,self.y),10)
		
	def update(self):
		self.isActive()
		if self.active == True:self.displayShot()

	def isActive(self):
		if (self.y < 80 or self.y >700):self.active = False
		else:self.active = True

	#collide(board.blocks,projs)
	def tragectory(self):
		pass



	

				



class Board:
	def __init__(self):
		self.blocks = []

	def drawBoard(self):
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

	def drawBlocks(self):
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




def clock():
	current_time = pygame.time.get_ticks()
	return current_time


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
	player1.update(frame,screen,testSprite)
	player2.update(frame,screen,testSprite)
	player1.nextObj(board.blocks)
	player2.nextObj(board.blocks)
	player1.collide(player2.projectiles)
	player2.collide(player1.projectiles)
	player1.removeDeactiveProj()
	player2.removeDeactiveProj()
	# player1.actions()
	board.blockCol(player1.projectiles)
	board.blockCol(player2.projectiles)
	updateProjectiles()
	pygame.display.update()
	

def intro():
	nextFrame = clock()
	frame = 0
	intro = True
	if music == True:
		playMusic(1)
	count = 0
	while intro:

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				intro = False
			if event.type == pygame.QUIT:
				return 0
		if clock() > nextFrame:                         
				frame = (frame+1)%8                         
				nextFrame += 80
				count+=1
		
		screen.blit(intro_image[frame-1],(0,0))
		screen.blit((testSprite.images[1*8+frame]),(270,250))
		pygame.draw.circle(screen,(255,255,0),(270+3*count,250+3*count),count)

		

		pygame.display.update()
		
makeMusic("hotline.ogg")
pygame.mixer.music.set_volume(0.5)
testSprite  = makeSprite("assets/links.gif", 32) 

gameRule = True
music = True



if __name__ == "__main__":
	intro()
	while gameRule:
		
		pygame.mixer.music.stop()
		board = Board()
		player1 = entity.Entity(200,650,3)
		player2 = entity.Entity(200,100,1)
		game = True
		count = 0
		maps = []
		nextFrame = clock()
		frame = 0
		currentItem = 0
		while game:
			
			#print(pygame.time.get_ticks())
			if clock() > nextFrame:                         
				frame = (frame+1)%8                         
				nextFrame += 80
				#player1.still = True
				#player2.still = True
			#Inputs and Exit
			gameTick = frame
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
							board.blocks.append([row,col,currentItem])
						# player1.x,player1.y = pygame.mouse.get_pos()
						# print("Coordinates(x,y): %s , %s" % (str(player1.x), str(player1.y)))
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_0:
							game= False
						if True:
							if event.key == pygame.K_a and player1.x != 0 and player1.blockLeft == False:
								player1.x -= blockWidth;
								player1.dir = 2
								player1.still = False
							elif event.key == pygame.K_d and player1.x != screen_WIDTH-150 and player1.blockRight == False:
								player1.x += blockWidth;
								player1.dir = 0
								player1.still = False
							elif event.key == pygame.K_w and player1.y != 100 and player1.blockAbove == False:
								player1.y -= blockWidth;
								player1.dir = 3
								player1.still = False
							elif event.key == pygame.K_s and player1.y != screen_HEIGHT-50 and player1.blockBelow == False:
								player1.y += blockWidth;
								player1.dir = 1
								player1.still = False
							else:player1.still = True

							if event.key == pygame.K_LEFT and player2.x != 0 and player2.blockLeft == False:
								player2.x -= blockWidth;
								player2.dir = 2
								player2.still = False

							elif event.key == pygame.K_RIGHT and player2.x != screen_WIDTH-150 and player2.blockRight == False:
								player2.x += blockWidth;
								player2.dir = 0
								player2.still = False
							elif event.key == pygame.K_UP and player2.y != 100 and player2.blockAbove == False:
								player2.y -= blockWidth;
								player2.dir = 3
								player2.still = False
							elif event.key == pygame.K_DOWN and player2.y != screen_HEIGHT-50 and player2.blockBelow == False:
								player2.y += blockWidth;
								player2.dir = 1
								player2.still = False
							else:
								player2.still = True

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

						if (event.key == pygame.K_i):
							if currentItem == 0:
								currentItem = 1
							else: currentItem = 0 


						if (event.key == pygame.K_m):
							fileName = input ("Save Map as maps/filename.txt: ")
							with open(fileName,'w') as filehandle:
								json.dump(board.blocks,filehandle)
							with open("maps/maps.txt","r+") as filehandle:
								maps = json.load(filehandle)
								maps.append([fileName])
								print(maps)
							with open("maps/maps.txt","w") as filehandle:
								json.dump(maps,filehandle)

							
						if (event.key == pygame.K_n):
							fileName = input ("Open Map as maps/filename.txt: ")
							if (fileName == 'list'):
								with open("maps/maps.txt", 'r') as filehandle:
									print(json.load(filehandle))	
								fileName = input ("Open Map as maps/filename.txt: ")
								with open(fileName, 'r') as filehandle:
									board.blocks = json.load(filehandle)
							else:
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




