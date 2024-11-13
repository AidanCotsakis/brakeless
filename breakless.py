
import pygame
import time
import os
import random
import math

# 100-199 reserved for walls
windowSize = [1920,1080]
surfaceSize = [48*8, 27*8]
gameOrginOffset = [11.5*8,1*8]
gameSwipeOffset = 0
gameScale = [25,25]
tileSize = 8
targetLevel = -1
currentLevel = 0
move = 0
moveq = 0
landed = True
start = [0,0]
finish = [0,0]
player = [0,0]
playerOffset = [0,0]
landDelay = -1
landDelayValue = 4
particles = []

pygame.init()
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode(windowSize, pygame.NOFRAME)
win = pygame.surface.Surface(surfaceSize)

# load levels from document
levels = []
levelsave = []
with open('levels.txt', 'r') as data:
	for line in data:
		if 'metadata' in line:
			levels.append(levelsave)
			levelsave = []

		else:
			levelrow = line.split()
			levelrow = [int(i) for i in levelrow]
			levelsave.append(levelrow)

	levels.append(levelsave)
	levelsave = []

# load wall sprites
wallSprites = []
wallSpriteHeight = 2
for i in range(1,17):
	wallSprites.append(pygame.image.load('images/wall{}.png'.format(i)))

startSprite = pygame.image.load('images/start.png')
finishSprite = pygame.image.load('images/finish.png')
playerSprite = pygame.image.load('images/player.png')


class particleObj(object):
	def __init__(self, x, y, angleRange, speedRange, sizeRange, lifeRange, colour, colourVarience, radius):
		self.x = x + random.randint(-radius, radius)
		self.y = y + random.randint(-radius, radius)
		self.angle = random.randint(angleRange[0], angleRange[1])*math.pi/180
		self.speed = random.randint(speedRange[0], speedRange[1])/100
		self.size = random.randint(sizeRange[0], sizeRange[1])
		self.life = random.randint(lifeRange[0], lifeRange[1])

		red = colour[0] + random.randint(-colourVarience, colourVarience)
		green = colour[1] + random.randint(-colourVarience, colourVarience)
		blue = colour[2] + random.randint(-colourVarience, colourVarience)
		if red < 0: red = 0
		elif red > 255: red = 255
		if green < 0: green = 0
		elif green > 255: green = 255
		if blue < 0: blue = 0
		elif blue > 255: blue = 255
		self.colour = (red, green, blue)

	def handle(self):
		self.y += self.speed*(-math.sin(self.angle))
		self.x += self.speed*(math.cos(self.angle))

		self.life -= 1
		if self.life < 30:
			self.size = 1

	def draw(self):
		pygame.draw.rect(win, self.colour, (self.x,self.y+gameSwipeOffset,self.size,self.size))


def loadLevel(levelNum):
	loadedLevel = levels[levelNum]

	_start = [0,0]
	_finish = [0,0]

	drawMap = []
	for y in enumerate(loadedLevel):
		drawRow = []
		for x in enumerate(y[1]):
			
			if loadedLevel[y[0]][x[0]] == 2:
				_start = [x[0],y[0]]
			elif loadedLevel[y[0]][x[0]] == 3:
				_finish = [x[0],y[0]]

			# write everything that isnt a wall
			if loadedLevel[y[0]][x[0]] != 1:
				drawRow.append(loadedLevel[y[0]][x[0]])
			
			# treat walls differently in draw map
			elif loadedLevel[y[0]][x[0]] == 1:

				#variable to remeber what is next to each wall CLOCKWISE [north east south west]
				directions = [False, False, False, False]
				# check if wall north
				if y[0] > 0:
					if loadedLevel[y[0]-1][x[0]] == 1:
						directions[0] = True
				# check if wall east
				if x[0] < len(y[1])-1:
					if loadedLevel[y[0]][x[0]+1] == 1:
						directions[1] = True
				# check if wall south
				if y[0] < len(loadedLevel)-1:
					if loadedLevel[y[0]+1][x[0]] == 1:
						directions[2] = True
				# check if wall west
				if x[0] > 0:
					if loadedLevel[y[0]][x[0]-1] == 1:
						directions[3] = True

				# Wall IDS:
				# 100 101 102   103
				# 104 105 106   107
				# 108 109 110   111

				# 112 113 114   115

				# append correct number based on map above (index + 100)
				if not directions[0] and directions[1] and directions[2] and not directions[3]: drawRow.append(100)
				elif not directions[0] and directions[1] and directions[2] and directions[3]: drawRow.append(101)
				elif not directions[0] and not directions[1] and directions[2] and directions[3]: drawRow.append(102)
				elif not directions[0] and not directions[1] and directions[2] and not directions[3]: drawRow.append(103)
				elif directions[0] and directions[1] and directions[2] and not directions[3]: drawRow.append(104)
				elif directions[0] and directions[1] and directions[2] and directions[3]: drawRow.append(105)
				elif directions[0] and not directions[1] and directions[2] and directions[3]: drawRow.append(106)
				elif directions[0] and not directions[1] and directions[2] and not directions[3]: drawRow.append(107)
				elif directions[0] and directions[1] and not directions[2] and not directions[3]: drawRow.append(108)
				elif directions[0] and directions[1] and not directions[2] and directions[3]: drawRow.append(109)
				elif directions[0] and not directions[1] and not directions[2] and directions[3]: drawRow.append(110)
				elif directions[0] and not directions[1] and not directions[2] and not directions[3]: drawRow.append(111)
				elif not directions[0] and directions[1] and not directions[2] and not directions[3]: drawRow.append(112)
				elif not directions[0] and directions[1] and not directions[2] and directions[3]: drawRow.append(113)
				elif not directions[0] and not directions[1] and not directions[2] and directions[3]: drawRow.append(114)
				elif not directions[0] and not directions[1] and not directions[2] and not directions[3]: drawRow.append(115)
		drawMap.append(drawRow)

	return (loadedLevel, drawMap, _start, _finish)


def draw():
	win.fill((255,255,255))

	for y in range(len(levelData)):
		for x in range(len(levelData[0])):
			if levelDrawMap[y][x] == 2:
				win.blit(startSprite, (x*tileSize+gameOrginOffset[0], y*tileSize+gameOrginOffset[1]+gameSwipeOffset))
			elif levelDrawMap[y][x] == 3:
				win.blit(finishSprite, (x*tileSize+gameOrginOffset[0], y*tileSize+gameOrginOffset[1]+gameSwipeOffset))

	# draw walls
	for y in range(len(levelData)):
		if player[1] == y:
			win.blit(playerSprite, (player[0]*tileSize+gameOrginOffset[0] + playerOffset[0], player[1]*tileSize+gameOrginOffset[1]+gameSwipeOffset+playerOffset[1]))
		for x in range(len(levelData[0])):
			if levelDrawMap[y][x] >= 100 and levelDrawMap[y][x] <= 999 + len(wallSprites):
				win.blit(wallSprites[levelDrawMap[y][x]-100], (x*tileSize+gameOrginOffset[0], y*tileSize+gameOrginOffset[1]-wallSpriteHeight+gameSwipeOffset))

	for particle in particles:
		particle.draw()

	window.blit(pygame.transform.scale(win, windowSize), (0,0))
	pygame.display.update()



levelData, levelDrawMap, start, finish = loadLevel(currentLevel)
player = start



tick = 0
while True:

	tick += 1
	clock.tick(60)
		
	for event in pygame.event.get():
		#exit
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w or event.key == pygame.K_UP: #listen for 'w'
				if move == 0:
					move = 1
				else: moveq = 1
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT: #listen for 'a'
				if move == 0:
					move = 2
				else: moveq = 2
			if event.key == pygame.K_s or event.key == pygame.K_DOWN: #listen for 's'
				if move == 0: 
					move = 3
				else: moveq = 3
			if event.key == pygame.K_a or event.key == pygame.K_LEFT: #listen for 's'
				if move == 0: 
					move = 4
				else: moveq = 4
			if event.key == pygame.K_SPACE:
				move = 0
				moveq = 0
				player = start
				playerOffset = [0,0]
				landed = True
				landDelay = -1

	# move player
	if move > 0 and targetLevel < 0:
		if move == 1 and player[1] > 0:
			if levelData[player[1]-1][player[0]] != 1:
				player = [player[0], player[1]-1]
				landed = False
			elif landDelay < 0:
				landed = True
				landDelay = 0
		elif move == 2 and player[0] < len(levelData[0])-1:
			if levelData[player[1]][player[0]+1] != 1:
				player = [player[0]+1, player[1]]
				landed = False
			elif landDelay < 0:
				landed = True
				landDelay = 0
		elif move == 3 and player[1] < len(levelData)-1:
			if levelData[player[1]+1][player[0]] != 1:
				player = [player[0], player[1]+1]
				landed = False
			elif landDelay < 0:
				landed = True
				landDelay = 0
		if move == 4 and player[0] > 0:
			if levelData[player[1]][player[0]-1] != 1:
				player = [player[0]-1, player[1]]
				landed = False
			elif landDelay < 0:
				landed = True
				landDelay = 0
	
		# animate player land
		if move > 0 and targetLevel < 0 and landed and playerOffset == [0,0]:
			if move == 1:
				playerOffset = [0,-1]
			elif move == 2:
				playerOffset = [1,0]
			elif move == 3:
				playerOffset = [0,1]
			elif move == 4:
				playerOffset = [-1,0]

		if targetLevel < 0 and landed and playerOffset != [0,0] and landDelay >= landDelayValue:
			playerOffset = [0,0]
			move = 0
			landDelay = -1

		if landDelay >= 0:
			landDelay += 1

	if landed and moveq > 0:
		move = moveq
		moveq = 0
		landDelay = -1
		playerOffset = [0,0]

	if player == finish and landed:
		targetLevel = currentLevel + 1
		finish = [-1,-1]
		landDelay = -1
		playerOffset = [0,0]
	
	# change level
	if targetLevel >= 0:
		# first time setup
		if gameSwipeOffset == 0:
			success = True
			if targetLevel >= len(levels)-1:
				targetLevel = 0
				
			levelVelocity = 0
			if targetLevel > currentLevel:
				levelAcceleration = -1
			elif targetLevel < currentLevel:
				levelAcceleration = 1
			else:
				success = False
				targetLevel = -1

		if success:
			# apply accelereation
			levelVelocity += levelAcceleration
			gameSwipeOffset += levelVelocity
			# load new level and position it when 
			if abs(gameSwipeOffset) >= surfaceSize[1]-tileSize*0:
				levelData, levelDrawMap, start, finish = loadLevel(targetLevel)

				player = start
				move = 0
				landed = True
				particles = []
				playerOffset = [0,0]
				landDelay = -1

				gameSwipeOffset *= -1
				levelVelocity += levelAcceleration
				levelAcceleration *= -1

			if gameSwipeOffset == 0:
				currentLevel = targetLevel
				targetLevel = -1

	# PARTICLES
	if tick % 2 == 0 and not landed:
		particles.append(particleObj(player[0]*tileSize+gameOrginOffset[0] + playerOffset[0]+tileSize/2, player[1]*tileSize+gameOrginOffset[1]+gameSwipeOffset+playerOffset[1]+tileSize/2-1, (0,360), (1,20), (1,2), (5,45), (2,119,189), 5, 0))
	if tick % 10 == 0 and targetLevel < 0:
		particles.append(particleObj(finish[0]*tileSize+gameOrginOffset[0] + tileSize/2, finish[1]*tileSize+gameOrginOffset[1]+gameSwipeOffset+tileSize/2-2, (60,120), (10,30), (1,2), (10,60), (53,185,53), 5, 2))
	if tick % 10 == 0 and targetLevel < 0:
		particles.append(particleObj(start[0]*tileSize+gameOrginOffset[0] + tileSize/2, start[1]*tileSize+gameOrginOffset[1]+gameSwipeOffset+tileSize/2-2, (60,120), (10,30), (1,2), (10,60), (231,35,39), 5, 2))
	for particle in particles:
		particle.handle()
	for particle in list(particles):
		if particle.life <= 0:
			particles.remove(particle)

	draw()
