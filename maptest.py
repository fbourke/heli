import pygame
import sys
import pygame.camera
from pygame.locals import *

def tile_table(file, width, height):	#example function to load tiles from tileset file
	image = pygame.image.load(file).convert()
	image_width, image_height = image.get_size()
	tile_table = []
	for x in range(0, int(image_width/width)):
		line = []
		tile_table.append(line)
		for y in range(0, int(image_height/height)):
			rect = (x*width, y*height, width, height)
			line.append(image.subsurface(rect))
	return tile_table

import ConfigParser

class Level(object):	#loads the text file defining the map
	def load_file(self, filename):
		self.map = []
		self.key = {}
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
		self.tileset = parser.get("level", "tileset")
		self.map = parser.get("level", "map").split("\n")
		for section in parser.sections():
			if len(section) == 1:
				desc = dict(parser.items(section))
				self.key[section] = desc
		self.width = len(self.map[0])
		self.height = len(self.map)

	def get_tile(self, x, y):
		try:
			char = self.map[y][x]
		except IndexError:
			return {}
		try:
			return self.key[char]
		except KeyError:
			return {}

	def get_bool(self, x, y, name):
		value = self.get_tile(x,y).get(name)
		return value in (True, 1, "true", "yes", "True", "Yes", "1", "on", "On")

	def is_wall(self, x, y):	
		#Is there a wall there?
		return self.get_bool(x,y, "wall")

	def is_blocking(self, x, y):
		#Is this space blocking movement?
		if not 0 <= x < self.width or not 0 <= y < self.height:
			return True
		return (self.get_bool(x,y, "block"))

	def render(self):	#draws appropriate tiles for each space
		wall = self.is_wall
		tiles = MAP_CACHE[self.tileset]
		image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
		overlays = {}
		for map_y, line in enumerate(self.map):
			for map_x, c in enumerate(line):
				if wall(map_x, map_y):
                    # Draw different tiles depending on if it is corner, side, etc
					if not wall(map_x, map_y+1):
						if wall(map_x+1, map_y) and wall(map_x-1, map_y):
							tile = 1, 2
						elif wall(map_x+1, map_y):
							tile = 0, 2
						elif wall(map_x-1, map_y):
							tile = 2, 2
						else:
							tile = 3, 2
					else:
						if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
							tile = 1, 1
						elif wall(map_x+1, map_y+1):
							tile = 0, 1
						elif wall(map_x-1, map_y+1):
							tile = 2, 1
						else:
							tile = 3, 1
				else:
					try:
						tile = self.key[c]['tile'].split(',')
						tile = int(tile[0]), int(tile[1])
					except (ValueError, KeyError):
                        # Default to ground tile if not one of other types
						tile = 0, 3
				tile_image = tiles[tile[0]][tile[1]]
				image.blit(tile_image,(map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
		return image, overlays

level = Level()
level.load_file("level.map")	#specifies the text file to be used

window_width = 300
window_height = 300
MAP_TILE_WIDTH = 24		#defining tile width and height
MAP_TILE_HEIGHT = 16
map_width = MAP_TILE_WIDTH * level.width
map_height = MAP_TILE_HEIGHT * level.height

screen = pygame.display.set_mode((window_width, window_height))	#creates window
pygame.display.set_caption("Map Test")

MAP_CACHE = {"pygametileset.bmp": tile_table("pygametileset.bmp", MAP_TILE_WIDTH, MAP_TILE_HEIGHT)}	#specifies the image file to be used

clock = pygame.time.Clock()

background, overlay_dict = level.render()	#draws the level
overlays = pygame.sprite.RenderUpdates()

for (x,y), image in overlay_dict.iteritems():
	totaltiles += 1

	overlay = pygame.sprite.Sprite(overlays)
	overlay.image = image
	overlay.rect = image.get_rect().move(x*16, y*16 - 16)

background_x = 0
background_y = 0
x_change = -3

screen.blit(background,(background_x, background_y, window_width, window_height))
#overlays.draw(screen)
pygame.display.flip()	#updates the display surface

game_over = False
while not game_over:	#This is the main game loop
    # We will draw other objects here...

	clock.tick(30)			#updates screen 30 times per second
	for event in pygame.event.get():
		key_pressed = pygame.key.get_pressed()

	if event.type == pygame.locals.QUIT:
		game_over = True
	elif key_pressed[K_LEFT]:
		background_x -= x_change
	elif key_pressed[K_RIGHT]:
		background_x += x_change
	elif key_pressed[K_UP]:
		background_y -= x_change
	elif key_pressed[K_DOWN]:
		background_y += x_change
	elif key_pressed[K_ESCAPE]:
		quit()

	if background_x > 0:
		background_x = 0
	if background_x < -(map_width - window_width):
		background_x = -(map_width - window_width)
	if background_y > 0:
		background_y = 0
	if background_y < -(map_height - window_height):
		background_y = -(map_height - window_height)

	screen.blit(background,(background_x, background_y, window_width, window_height))
	pygame.display.flip()	
