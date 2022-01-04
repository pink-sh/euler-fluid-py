import pygame
from constants import SIZE, SCALE, PAGE_SIZE
from container import Container


def draw_rect(surface, color, rect):
	shape = pygame.Surface(rect.size, pygame.SRCALPHA)
	pygame.draw.rect(shape, color, shape.get_rect())
	surface.blit(shape, rect)


pygame.init()

size = W, H = 640,640

screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyEulerean Fluid Simulator')

running = True


mouseActive = False
mouseDragging = False

previousPosition=(0,0)

boundSize = int(PAGE_SIZE/SIZE)
container = Container( 0.2, 0, 0.0000001 )

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseActive = True
		if event.type == pygame.MOUSEBUTTONUP:
			mouseActive = False
		if event.type == pygame.MOUSEMOTION:
			if mouseActive:
				mouseDragging = True
			else:
				mouseDragging = False

	

	pos_x, pos_y = pygame.mouse.get_pos()

	rel_pos_x = pos_x / boundSize
	rel_pos_y = pos_y / boundSize



	if mouseActive:
		container.AddDensity(rel_pos_x, rel_pos_y, 200)

	if mouseDragging:
		pos_x, pos_y = pygame.mouse.get_pos()

		rel_pos_x = pos_x / boundSize
		rel_pos_y = pos_y / boundSize

		amountX = x - previousPosition[0]
		amountY = y - previousPosition[1]

		container.AddVelocity(rel_pos_y, rel_pos_x, amountY/100, amountX/100)

	container.Step()

	previousPosition = (rel_pos_x,rel_pos_y)

	screen.fill((0, 0, 0))

	for x in range(0,640,boundSize-1):
		for y in range(0,640,boundSize-1):
			alpha = 0
			if int(x/boundSize) < SIZE and int(y/boundSize) < SIZE:
				alpha = 255 if container.density[int(x/boundSize)][int(y/boundSize)] > 255 else container.density[int(x/boundSize)][int(y/boundSize)]
			color = (22,54,100,alpha)
			draw_rect(screen, color, pygame.Rect(x, y, boundSize, boundSize))

	pygame.display.flip()


pygame.quit()