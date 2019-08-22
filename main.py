# Birdy! - platform game

import pygame, random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init() # sounds and music
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(FONT_NAME)

        self.running = True
        self.playing = False

        self.score = None
        self.all_sprites = None
        self.platforms = None
        self.player = None
        self.base = None

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.base = BasePlatform(WIDTH/2, HEIGHT)
        self.all_sprites.add(self.player, self.base)
        self.platforms.add(self.base)

        for plat_args in PLATFORM_LIST:
            plat = Platform(*plat_args)
            self.platforms.add(plat)
            self.all_sprites.add(plat)

        for plat_args in MOVING_PLATFORM_LIST:
            plat = MovingPlatform(*plat_args)
            self.platforms.add(plat)
            self.all_sprites.add(plat)

        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop - update
        self.all_sprites.update()
        # check if player hits platform - only if falling
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False,
                                           pygame.sprite.collide_rect_ratio(1.1)) # collide_rect_ratio fixes vibration
        if hits and self.player.vel.y > 0:
            # print(hits) # to delete
            self.player.pos.y = hits[0].rect.top
            #self.player.acc.y = 0
            self.player.vel.y = 0
            self.player.can_jump = True
            if isinstance(hits[0], MovingPlatform):
                self.player.pos.x += hits[0].x_speed
        else:
            self.player.can_jump = False



        # scroll screen if player is too high up
        if self.player.rect.top <= HEIGHT / 5:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.pos.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill() # removes sprite from all groups
                    self.score += 10 # add to score if plat is pushed down

        # player dies
        if self.player.rect.top >= HEIGHT:
            for sprite in self.all_sprites:
                sprite.pos.y -= self.player.vel.y # scroll up
                if sprite.rect.bottom < 0: # hits top of screen
                    sprite.kill()

        if len(self.platforms) == 0: # end game when all platforms killed
            self.playing = False

        # spawn new platforms
        while len(self.platforms) < 6:
            y = random.randint(-75, -PLATFORM_HEIGHT)
            dice = random.randint(1,4)

            if dice == 1:
                plat = MovingPlatform(y, PLATFORM_HEIGHT)
            else:
                plat = Platform(y, PLATFORM_HEIGHT)

            self.platforms.add(plat)
            self.all_sprites.add(plat)


    def events(self):
        # game loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


    def draw(self):
        # game loop - draw
        self.screen.fill(PEACH)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, NAVY, 20, 20)
        # *after* drawing everything, flip the display
        # same as pygame.display.update() with no args
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game start screen
        self.screen.fill(PEACH)
        self.draw_text("b i r d y", 48, WHITE, WIDTH/2, 60)
        self.draw_text("use the arrow keys to move;", 20, NAVY, WIDTH/2, 220)
        self.draw_text("press the up key to jump;", 20, NAVY, WIDTH/2, 260)
        self.draw_text("press any key to begin.", 20, WHITE, WIDTH/2, 350)
        pygame.display.flip()
        self.wait_for_key()

    def show_gameover_screen(self):
        # game over/continue screen
        pass


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_gameover_screen()

pygame.quit()