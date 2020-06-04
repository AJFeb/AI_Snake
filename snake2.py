import pygame
from random import randint

pygame.init()

display = pygame.display.set_mode((400,300))

stop = False
while stop == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    pygame.draw.rect(display, (255,255,255), [200,150,10,10])
    pygame.display.update()
pygame.quit()
quit()

class Game:
	def quit(self, event):
		if self.event.type == pygame.QUIT:
			pygame.quit()

	def function():
		pass

class Movements:
	#
	x = 10
	y = 10
	speed = 1

	def up(self):
		self.y += self.speed
	def down(self):
		self.y -= self.speed
	def right(self):
		self.x += self.speed
	def left(self):
		self.x -= self.speed

class App:
	pass
	

#App().run()