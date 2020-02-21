import pygame
import time
import random

from pygame.locals import*
from time import sleep

class Sprite(object):
	def __init__(self, x_pos, y_pos, width, height):
		self.x = x_pos
		self.y = y_pos
		self.w = width
		self.h = height
		self.collidedWithMario = False
		self.scrollPos = 0
		self.needCoin = False

	def Update(self):
		pass

	def Draw(self, view):
		pass

	def isMario(self):
		pass

	def isCoin():
		pass

class Mario(Sprite):
	def __init__(self,m):
		super(Mario, self).__init__(0, 401, 63, 99)
		self.prev_x = self.x
		self.prev_y = self.y
		self.m = m
		self.framesInAir = 0
		self.picture = 0
		self.vert_vel = 0

	def doesCollide(self, b):
		b.collidedWithMario = False
		
		if(b.isMario()):
			return False
		
		#lengths of all sides of the brick
		brickRight = b.x+b.w;
		brickLeft = b.x;
		brickTop = b.y;
		brickBottom = b.y+b.h;
		
		#lengths of all sides of the mario image
		marioRight =self.x+self.w;
		marioLeft = self.x;
		marioTop = self.y;
		marioBottom = self.y+self.h;
		
		#place to store the previous position if there is a collision (this is how to correct it)
		prevRight = self.prev_x + self.w;
		prevLeft = self.prev_x;
		prevTop = self.prev_y;
		prevBottom = self.prev_y + self.h;
				
		if(marioRight <= brickLeft):
			return False
		if(marioLeft >= brickRight):
			return False
		if(marioBottom <= brickTop): # assumes bigger is downward
			return False
		if(marioTop >= brickBottom): # assumes bigger is downward
			return False
		
		#hit right side of brick
		if(prevLeft >= brickRight and marioLeft < brickRight):
			self.x = brickRight
		
		#hit left side of brick
		if(prevRight <= brickLeft and marioRight > brickLeft):
			self.x = brickLeft - self.w;

		#hit top of brick or on ground
		if(prevBottom <= brickTop and marioBottom > brickTop):
			self.vert_vel = 0
			self.y = brickTop-self.h
			self.framesInAir = 0

		#hit bottom of brick
		if(prevTop >= brickBottom and marioTop < brickBottom):
			self.vert_vel = 7
			self.y = brickBottom
			b.collidedWithMario = True
		
		return True

	#Override 
	def Update(self):
		self.framesInAir+= 1
		self.vert_vel += 3.1
		self.y += self.vert_vel
		for i in self.m.sprites:			
			self.doesCollide(i)
		self.prev_x = self.x;
		self.prev_y = self.y;

	#Override
	def Draw(self, view):
		mario_image1 = pygame.image.load("mario1.png")
		mario_image2 = pygame.image.load("mario2.png")
		mario_image3 = pygame.image.load("mario3.png")
		mario_image4 = pygame.image.load("mario4.png")
		mario_image5 = pygame.image.load("mario5.png")
		mario_image = [mario_image1, mario_image2, mario_image3, mario_image4, mario_image5]
		view.model.rect = mario_image[self.picture].get_rect()
		view.screen.blit(mario_image[self.picture], [0, self.y])

	#Override
	def isMario(self):
		return True

	#Override
	def isCoin(self):
		return False

class Brick(Sprite):
	def __init__(self, x_pos, y_pos, width, height, groundBrick):
		super(Brick, self).__init__(x_pos, y_pos, width, height)
		self.groundBrick = groundBrick

	#Override
	def Update(self):
		return

	#Override
	def Draw(self, view):
		if(self.groundBrick == True):
			ground_image = pygame.image.load("ground_image.png")
			view.model.rect = ground_image.get_rect()
			view.screen.blit(ground_image, [self.x,self.y])
		else:
			brick_image = pygame.image.load("brick_image.jpg")
			view.model.rect = brick_image.get_rect()
			view.screen.blit(brick_image, [self.x - self.scrollPos, self.y])

	#Override
	def isMario(self):
		return False

	#Override
	def isCoin(self): 
		return False

class CoinBlock(Sprite):
	def __init__(self, x_pos, y_pos, width, height):
		super(CoinBlock, self).__init__(x_pos, y_pos, width, height)
		self.coinCount = 5
	
	#Override
	def Update(self):
		if(self.collidedWithMario):
			self.coinCount-=1
			if(self.coinCount < 0):
				self.needCoin = False
			if(self.coinCount >= 0):
				self.needCoin = True;

	#Override
	def Draw(self, view):
		if(self.coinCount <= 0):
	 		coinBlockDead_image = pygame.image.load("coinBlockDead_image.png")
			view.model.rect = coinBlockDead_image.get_rect()
			view.screen.blit(coinBlockDead_image, [self.x - self.scrollPos, self.y])
		else:
			coinBlock_image = pygame.image.load("coinBlock_image.png")
			view.model.rect = coinBlock_image.get_rect()
			view.screen.blit(coinBlock_image, [self.x - self.scrollPos, self.y])

	#Override
	def isMario(self): 
		return False
	#Override
	def isCoin(self):
		return False

class Coin(Sprite):
	def __init__(self, x_pos, y_pos, width, height):
		super(Coin, self).__init__(x_pos, y_pos, width, height)
		self.verticalVelocity = -5
		self.horizontalVelocity = (random.randint(0,20) - 10)

	#Override
	def Update(self):
		self.verticalVelocity += 2;
		self.y += self.verticalVelocity;
		self.x += self.horizontalVelocity;

	#Override
	def Draw(self, view): 
		coin_image = pygame.image.load("coin_image.png")
		view.model.rect = coin_image.get_rect()
		view.screen.blit(coin_image, [self.x - self.scrollPos, self.y])

	#Override
	def isMario(self):
		return False;
	
	#Override
	def isCoin(self):
		return True

class Model():
	def __init__(self):
		self.mario = Mario(self);
		self.sprites = []
		self.sprites.append(self.mario)
		#add ground
		self.addBrick(0, 500, 200000, 10, True);
		#add bricks
		for i in range(100):
			if(i%2 == 0):
				self.addBrick(100+200*i, 428, 108, 72, False);
			else:
				self.addBrick(100+600*i, 200, 108, 72, False);
		#add coin blocks
		for i in range(50):
			self.addCoinBlock(300+800*i, 250, 75, 75);

	def update(self):
		for i in self.sprites:
			i.scrollPos = self.mario.x;
			i.Update();
			if(i.needCoin):
				self.addCoin(i.x, i.y, i.w, i.h)
				i.needCoin = False
		#removes coins from the sprites list 
		for i in self.sprites:
			if(i.y > 600 and i.isCoin()):
				self.sprites.remove(i)
	def addBrick(self, x, y, w, h, groundBrick):
		b = Brick(x, y, w, h, groundBrick)
		self.sprites.append(b)
	def addCoinBlock(self, x, y, w, h):
		c = CoinBlock(x, y, w, h)
		self.sprites.append(c)
	def addCoin(self, x, y, w, h):
		c = Coin(x, y, w, h)
		self.sprites.append(c)

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.background_image = pygame.image.load("Background.png")
		self.model = model
		self.model.rect = self.background_image.get_rect()

	def update(self):    
		self.screen.blit(self.background_image, [(0 - self.model.mario.x * .1),0])
		for i in self.model.sprites:
			i.Draw(self) 			
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -=10
			self.model.mario.picture-=1
			if(self.model.mario.picture < 0):
				self.model.mario.picture = 4
			if(self.model.mario.x < 0):
				self.model.mario.x = 0
		if keys[K_RIGHT]:
			self.model.mario.x +=10;
			self.model.mario.picture+=1
			if(self.model.mario.picture >= 5):
				self.model.mario.picture = 0
		if keys[K_SPACE]:
			if(self.model.mario.framesInAir < 5):
				self.model.mario.vert_vel -= 8.4

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")