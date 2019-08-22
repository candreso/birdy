# sprite classes for platformer
import pygame, random
from settings import *
# import os

# game_folder = os.path.dirname(__file__)
# img_folder = os.path.join(game_folder, "img")
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,20)) # what the sprite looks like
                    # pygame.image.load(os.path.join(image_folder, "name")).convert()
        # self.image.set_colorkey(BLACK)
        self.image.fill(BURNT_ORANGE)
        self.rect = self.image.get_rect() # rectangle that encloses the sprite
        #self.rect = self.rect.inflate(0, 2)
        self.rect.midbottom = (WIDTH / 2, HEIGHT-BasePlatform.height-45)
        self.pos = vec(WIDTH / 2, HEIGHT-BasePlatform.height-45)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.can_jump = False

    def update(self):
        self.acc = vec(0, G)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            if self.can_jump:
                self.vel.y = JUMP_SPEED
        # elif keys[pygame.K_DOWN]:
        #     self.acc.y = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, bY, h, color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.width = random.randint(55, 150)
        x = random.randint(int(self.width / 2), int(WIDTH - self.width / 2))
        self.cX = x
        self.bY = bY
        self.image = pygame.Surface((self.width, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec(self.cX, self.bY)
        self.rect.midbottom = (self.cX, self.bY)

    def update(self):
        self.rect.midbottom = self.pos


class BasePlatform(pygame.sprite.Sprite):
    height = 30

    def __init__(self, cX, bY):
        pygame.sprite.Sprite.__init__(self)
        self.cX = cX
        self.bY = bY
        self.image = pygame.Surface((WIDTH, BasePlatform.height))
        self.image.fill(NAVY)
        self.rect = self.image.get_rect()
        self.pos = vec(self.cX, self.bY)
        self.rect.midbottom = (self.cX, self.bY)

    def update(self):
        self.rect.midbottom = self.pos


class MovingPlatform(Platform):
    def __init__(self, bY, h):
        super().__init__(bY, h, SEA_GREEN)
        self.vel = vec(0, 0)
        self.x_speed = 3

    def update(self):
        self.vel = vec(self.x_speed, 0)
        self.pos += self.vel
        self.rect.midbottom = self.pos

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.x_speed *= -1
