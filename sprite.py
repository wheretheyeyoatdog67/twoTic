#sprite test
import pygame, math, sys, os

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
gameClock = pygame.time.Clock()
musicPaused = False
hiddenSprites = pygame.sprite.OrderedUpdates()
screenRefresh = True
background = None
WIN_WIDTH = 800
WIN_HEIGHT = 700


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


screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
testSprite  = makeSprite("assets/links.gif", 32) 

nextFrame = clock()
frame = 0
game = True
while game:
	screen.fill((255,255,255))
	if clock() > nextFrame:                         
		frame = (frame+1)%8                         
		nextFrame += 80
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				screen.blit((testSprite.images[0*8+frame]),(200,200))
			elif event.key == pygame.K_DOWN:
				screen.blit((testSprite.images[1*8+frame]),(200,200))
			elif event.key == pygame.K_LEFT:
				screen.blit((testSprite.images[2*8+frame]),(200,200))
			elif event.key == pygame.K_UP:
				screen.blit((testSprite.images[3*8+frame]),(200,200))
			else:
				screen.blit((testSprite.images[1*8+5]),(200,200))

			pygame.display.update()
