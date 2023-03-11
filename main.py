import pygame
from pygame.locals import *
import random

import Box2D
from Box2D import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
PPM = 20
PLAYER_SPEED = 30
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

        self.world = b2World(gravity=(0, 0))
        
        self.ground_body = self.world.CreateStaticBody(
            position=(0, -10),
            shapes=b2PolygonShape(box=(50, 10)),
        )
        
        # Create a dynamic body
        self.player_body = self.world.CreateDynamicBody(position=(SCREEN_WIDTH / 2 / PPM, int((SCREEN_HEIGHT / PPM) * 0.9)))
        self.player_body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        #fixedRotation=True
        
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
                        self.player_body.linearVelocity = (-PLAYER_SPEED, 0)
                    elif event.key == K_RIGHT:
                        self.player_body.linearVelocity = (PLAYER_SPEED, 0)
                    elif event.key == K_SPACE:
                        self.fire_player_bullet()
                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_RIGHT):
                        self.player_body.linearVelocity = (0, 0)
            
            time_step = 1.0 / 60.0
            velocity_iterations = 6
            position_iterations = 2
            self.world.Step(time_step, velocity_iterations, position_iterations)
            
            self.update_enemies()
            self.update_bullets()
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
        
        # Draw the player body
        vertices = [(self.player_body.transform * vertex) * PPM for vertex in self.player_body.fixtures[0].shape.vertices]
        #pygame.draw.polygon(self.screen, (0, 0, 255), vertices)
        self.screen.blit(self.player_image, vertices[0])
        
        self.world.DrawDebugData()
        pygame.display.flip()

    def load_assets(self):
        self.player_image = pygame.image.load('player.png').convert_alpha()
        self.enemy_image = pygame.image.load('enemy.png').convert_alpha()
        self.player_bullet_image = pygame.image.load('missile.png').convert_alpha()
        self.enemy_bullet_image = pygame.image.load('missile.png').convert_alpha()
        #self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        #self.explosion_sound = pygame.mixer.Sound('explosion.wav')
        
    def play_explosion_sound(self):
        self.explosion_sound.play()

if __name__ == '__main__':
    game = Galaga()
    game.run()      