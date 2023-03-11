import pygame
from pygame.locals import *
import random

import Box2D
from Box2D import *

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
PLAYER_SPEED = 5
PLAYER_BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5
PLAYER_LIVES = 3
FPS = 60
ENEMY_POINTS = 10

class Galaga:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 30)
        pygame.display.set_caption("Galaga")
        
        self.load_assets()

        self.world = b2World(gravity=(0, -10))
        
        self.ground_body = self.world.CreateStaticBody(
            position=(0, -10),
            shapes=b2PolygonShape(box=(50, 10)),
        )
        
        self.player_body = self.world.CreateDynamicBody(
            position=(0, 0),
            shapes=b2PolygonShape(box=(1, 1)),
            fixedRotation=True,
        )
        
        self.player_lives = PLAYER_LIVES
        self.player_score = 0
        self.enemies = self.spawn_enemies()
        # self.enemies = []
        # Call spawn enemey call
        self.enemy_bullets = []
        self.player_bullets = []

        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        #Player move left
                        pass
                    elif event.key == K_RIGHT:
                        #player move right
                        pass
                    elif event.key == K_SPACE:
                        self.fire_player_bullet()
                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_RIGHT):
                        #player stop move
                        pass
            
            time_step = 1.0 / 60.0
            velocity_iterations = 6
            position_iterations = 2
            self.world.Step(time_step, velocity_iterations, position_iterations)
            
            self.update_enemies()
            self.update_player_bullets()
            self.update_enemy_bullets()
            self.check_collisions()
            self.draw_scene()
            
            self.clock.tick(FPS)
        
        pygame.quit()

    def spawn_enemies(self):
        #Method call that spawns three rows of 8 enemies and returns the list of those enemies
        pass
    
    def fire_player_bullet(self):
        #self.shoot_sound.play()
        pass

    def fire_enemy_bullet(self, enemy_body):
        #select a random enemey and fire a bullet every x seconds
        #probably use a random int the lenght of the row and check if that enemy is still alive, if not add row length and check again

        #self.shoot_sound.play()
        pass

    def update_enemies(self):
        pass

    def update_bullets(self):
        #update player bullets that go up
        #update enemy bullest that go down
        pass

    def check_collisions(self):
        pass

    def draw_scene(self):
        self.screen.fill((0, 0, 0))
        
        for life in range(self.player_lives):
            self.screen.blit(self.player_image, (20 + life * 30, 20))
        
        score_text = self.font.render(f"Score: {self.player_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
        
        self.world.DrawDebugData()
        pygame.display.flip()

    def load_assets(self):
        self.player_image = pygame.image.load('player.png').convert_alpha()
        self.enemy_image = pygame.image.load('enemy.png').convert_alpha()
        self.player_bullet_image = pygame.image.load('player_bullet.png').convert_alpha()
        self.enemy_bullet_image = pygame.image.load('enemy_bullet.png').convert_alpha()
        self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        self.explosion_sound = pygame.mixer.Sound('explosion.wav')
        
    def play_explosion_sound(self):
        self.explosion_sound.play()

if __name__ == '__main__':
    game = Galaga()
    game.run()      