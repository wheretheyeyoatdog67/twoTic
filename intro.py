import pygame
import os
#Music
pygame.mixer.init()

intro_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets","intro","sun" + str(x) + ".png")),(800,700)) for x in range(0,7)]

pygame.mixer.music.set_volume(0.5)
musicPaused = False
music = True



def makeMusic(filename):
	pygame.mixer.music.load(filename)


def playMusic(loops=0):
	global musicPaused
	if musicPaused:
		pygame.mixer.music.unpause()
	else:
		pygame.mixer.music.play(loops)
	musicPaused = False

makeMusic("music/hotline.ogg")


def intro(screen,testSprite):
	nextFrame = pygame.time.get_ticks()
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
		if pygame.time.get_ticks() > nextFrame:                         
				frame = (frame+1)%8                         
				nextFrame += 80
				count+=1
		
		screen.blit(intro_image[frame-1],(0,0))
		screen.blit((testSprite.images[1*8+frame]),(270,250))
		pygame.draw.circle(screen,(255,255,0),(270+3*count,250+3*count),count)
		pygame.display.update()