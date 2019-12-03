import pygame
import random
import os
import math
import json
import entity
import projectile
import boardClass
import intro
import inputs


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

colors = [(0,100,0),(255,0,0)]

#Timer Rule
goMode = True
game = True


def clock():
	current_time = pygame.time.get_ticks()
	return current_time

def gameTimer():
	global goMode
	if (count%clockSpeed == 0):
		if (goMode == False):
			goMode = True
			player1.shotOnTurn = False
			player2.shotOnTurn = False
		else: goMode = False

def updateProjectiles(goMode,screen,count):
	for x in player1.projectiles:
		x.update(goMode,screen,count)
	for x in player2.projectiles:
		x.update(goMode,screen,count)


def runGame():
	gameTimer()
	board.drawBoard(screen,goMode)
	board.drawBlocks(screen,frame)
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
	updateProjectiles(goMode,screen,count)
	pygame.display.update()
	


		









if __name__ == "__main__":
	testSprite  = entity.makeSprite("assets/links.gif", 32) 
	gameRule = True

	intro.intro(screen,testSprite)



	while gameRule:
		print("reset")
		pygame.mixer.music.stop()
		board = boardClass.Board()
		player1 = entity.Entity(200,650,3)
		player2 = entity.Entity(200,100,1)
		game = True
		count = 0
		maps = []
		nextFrame = clock()
		frame = 0
		currentItem = 0

		while game:
			if clock() > nextFrame:                         
				frame = (frame+1)%8                         
				nextFrame += 80


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRule = False
					game = False
				if(inputs.keyInput(screen,event,player1,player2,board,goMode) == False):
					game = False
				inputs.mouseInput(screen,event,board,currentItem)
			runGame()

			count+=1			



####################################################
#Controls
#           m : saves map
#			n : loads saved map
#			b: prints blocks array
#			0: restart game
#




