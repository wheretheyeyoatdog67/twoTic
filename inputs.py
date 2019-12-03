import pygame
import math
import json
import projectile

screen_WIDTH = 800
screen_HEIGHT = 700
# screen_WIDTH = 800
# screen_HEIGHT = 700
sideBar = 100
clockSpeed = 100
blockWidth = int((screen_WIDTH-sideBar)/14) #blockWidth x blockWidth blocks
blockHeight = screen_HEIGHT/14
halfBlockWidth = blockWidth/2



def mouseInput(screen,event,board,currentItem):
	if event.type == pygame.MOUSEBUTTONDOWN:
						x,y = pygame.mouse.get_pos()
						if (x < 700 and y > 100):
							row = math.ceil(x/blockWidth)
							col = math.ceil(y/blockWidth)
							board.blocks.append([row,col,currentItem])
						# player1.x,player1.y = pygame.mouse.get_pos()
						# print("Coordinates(x,y): %s , %s" % (str(player1.x), str(player1.y)))
					


def keyInput(screen,event,player1,player2,board,goMode):
	if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_0:
							return False
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
								player1.projectiles.append(projectile.Projectile(player1.x,player1.y,True))
								player1.shotOnTurn = True
						if (event.key == pygame.K_2 and goMode == False):
							if (player1.projOnBlock(player1.x,player1.y) == False and player1.shotOnTurn == False):
								player1.projectiles.append(projectile.Projectile(player1.x,player1.y,False))
								player1.shotOnTurn = True
						if (event.key == pygame.K_8 and goMode == False):		
							if (player2.projOnBlock(player2.x,player2.y) == False and player2.shotOnTurn == False):
								player2.projectiles.append(projectile.Projectile(player2.x,player2.y,True))
								player2.shotOnTurn = True
						if (event.key == pygame.K_9 and goMode == False):		
							if (player2.projOnBlock(player2.x,player2.y) == False and player2.shotOnTurn == False):
								player2.projectiles.append(projectile.Projectile(player2.x,player2.y,False))
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