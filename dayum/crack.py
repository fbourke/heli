# hmmm.py

# crack.py

import pygame
from pygame.locals import *
import sys
import math
from math import*

SCREEN_SIZE = (1200, 600) #resolution of the game
global HORIZ_MOV_INCR
HORIZ_MOV_INCR = 10 #speed of movement
global FPS
global clock
global time_spent

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    '''Class for center screen on the player'''
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    def update(self):
      if self.player.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.player.centerx - 25
      if self.player.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.player.centerx + 25
      if self.player.centery > self.rect.centery + 25:
          self.rect.centery = self.player.centery - 25
      if self.player.centery < self.rect.centery - 25:
          self.rect.centery = self.player.centery + 25
      self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


class Obstacle(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tile.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class Cat(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cat5.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class Crashman(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contact = False
        self.jump = False
        self.image = pygame.image.load('actions/idle_right.png').convert()
        self.rect = self.image.get_rect()
        self.run_left = ["actions/run_left000.png","actions/run_left001.png",
                         "actions/run_left002.png", "actions/run_left003.png",
                         "actions/run_left004.png", "actions/run_left005.png",
                         "actions/run_left006.png", "actions/run_left007.png"]
        self.run_right = ["actions/run_right000.png","actions/run_right001.png",
                         "actions/run_right002.png", "actions/run_right003.png",
                         "actions/run_right004.png", "actions/run_right005.png",
                         "actions/run_right006.png", "actions/run_right007.png"]

        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0

    def update(self, up, down, left, right):
        if up:
            if self.contact:
                self.jump = True
                self.movy -= 20
        if down:
            if self.contact and self.direction == "right":
                self.image = pygame.image.load('actions/down_right.png').convert_alpha()
            if self.contact and self.direction == "left":
                self.image = pygame.image.load('actions/down_left.png').convert_alpha()

        if not down and self.direction == "right":
                self.image = pygame.image.load('actions/idle_right.png').convert_alpha()

        if not down and self.direction == "left":
            self.image = pygame.image.load('actions/idle_left.png').convert_alpha()

        if left:
            self.direction = "left"
            self.movx = -HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_left[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("actions/jump_left.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_right[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("actions/jump_right.png").convert_alpha()

        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)


        if not self.contact:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.jump:
            self.movy += 2
            self.rect.top += self.movy
            if self.contact == True:
                self.jump = False

        self.contact = False
        self.collide(0, self.movy, world)


    def collide(self, movx, movy, world):
        self.contact = False
        for o in world:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0

cat = pygame.image.load('cat5.jpg')

class Shot(pygame.sprite.Sprite):
    #speed = -11
    images = []
    def __init__(self, pos, mpos, angle):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        # self.image = self.images[0]
        self.image = pygame.image.load('dot.png').convert()
        s = 10
        self.rect = self.image.get_rect(midbottom=pos)
        # if mpos[0] > crashman.rect.x-camera.rect.x-25:
        self.xspeed = s*cos(angle)
        self.yspeed = s*sin(angle)
        if mposx < gx:
            self.xspeed=self.xspeed*-1
        self.rect.topleft = [self.x+self.xspeed,self.y+self.yspeed]

    def update(self):
        self.rect = self.rect.move(self.xspeed,self.yspeed)
        print('sup')
        if self.rect.top <= 0:
            self.kill()

class Level(object):
    '''Read a map and create a level'''
    def __init__(self, open_level):
        self.level1 = []
        self.world = []
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                if col == "X":
                    obstacle = Obstacle(x, y)
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col == "P":
                    self.crashman = Crashman(x,y)
                    self.all_sprite.add(self.crashman)
                if col == "o":
                    cat = Cat(x, y)
                    self.world.append(cat)
                    self.all_sprite.add(self.world)
                x += 25
            y += 25
            x = 0

    def get_size(self):
        lines = self.level1
        #line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)



def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
screen_rect = screen.get_rect()
background = pygame.image.load("bg2.png").convert_alpha()
background_rect = background.get_rect()
level = Level("level/level1")
level.create_level(0,0)
world = level.world
crashman = level.crashman
mposx=0
mpoxy=0
cat = pygame.image.load('cat5.jpg')
mask = pygame.surface.Surface(SCREEN_SIZE).convert_alpha()
mask.fill((0,0,0,255))
# pygame.mouse.set_visible(0)



# Shot.images = pygame.image.load('cat5.jpg').convert()


camera = Camera(screen, crashman.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite

FPS = 30
clock = pygame.time.Clock()
mask = pygame.image.load('mask4.png')
up = down = left = right = False
x, y = 0, 0
gx=0
gy=0
shots = pygame.sprite.Group()
while True:
    firing=False

    # Shot stuff
    all = pygame.sprite.RenderUpdates()
    all.update()

    asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
    bg = pygame.Surface(asize)

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mposx,mposy = event.pos
            mpos = (mposx, mposy)
            gx = crashman.rect.x-camera.rect.x+25
            gy = crashman.rect.y-camera.rect.y+30
            # print(crashman.rect.x-camera.rect.x)
            # angle = ((gy-mposy)/float(sqrt(((mposx-gx)**2)+((gy-mposy)**2))))
            angle = ((mposy-gy)/float(sqrt(((mposx-gx)**2)+((mposy-gy)**2))))
            angle = math.asin(angle)
            # if mposx < gx:
            #     angle = angle*-1

            # print(yangle)
            firing = True
        if firing:
            # print('FIRE!')
            shots.add(Shot((gx,gy),mpos,angle))
            # print('Gun X: %s' %gx)
            # print('Gun Y: %s' %gy)
            # print(mposx,mposy)


        if event.type == KEYDOWN and event.key == K_SPACE:
            up = True
        if event.type == KEYDOWN and event.key == K_s:
            down = True
        if event.type == KEYDOWN and event.key == K_a:
            left = True
        if event.type == KEYDOWN and event.key == K_d:
            right = True

        if event.type == KEYUP and event.key == K_SPACE:
            up = False
        if event.type == KEYUP and event.key == K_s:
            down = False
        if event.type == KEYUP and event.key == K_a:
            left = False
        if event.type == KEYUP and event.key == K_d:
            right = False
        dirty = all.draw(screen)
        pygame.display.update(dirty)

    for x in range(0, asize[0], background_rect.w):
        for y in range(0, asize[1], background_rect.h):
            screen.blit(background, (x, y))

    shots.update()
    shots.draw(screen)
    # pygame.display.update()

    time_spent = tps(clock, FPS)
    camera.draw_sprites(screen, all_sprite)
    
    screen.blit(mask,(crashman.rect.x-camera.rect.x-1375, crashman.rect.y-camera.rect.y-965))
    ## Cover the screen with the partly-translucent mask
    # screen.blit(mask,(0,0))

    crashman.update(up, down, left, right)
    camera.update()
    pygame.display.flip()