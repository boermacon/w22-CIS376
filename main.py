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
        
        #Load assets
        self.player_image = pygame.image.load('player.png').convert_alpha()
        self.enemy_image = pygame.image.load('enemy.png').convert_alpha()
        self.player_bullet_image = pygame.image.load('missile.png').convert_alpha()
        self.player_bullet_image = pygame.transform.scale(self.player_bullet_image, (20, 30))
        self.enemy_bullet_image = pygame.image.load('missile.png').convert_alpha()
        self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        # self.explosion_sound = pygame.mixer.Sound('explosion.wav')

        self.world = b2World(gravity=(0, 0))
        
        #self.ground_body = self.world.CreateStaticBody(position=(0, -10),shapes=b2PolygonShape(box=(50, 10)),)
        #self.body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        
        #self.tempBody = self.world.CreateStaticBody(position=(100/PPM, 0))
        #self.tempBody.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(10/PPM, SCREEN_HEIGHT/PPM)),density=1,friction=0.3))

        # Create a dynamic body
        self.player_body = self.world.CreateDynamicBody(position=(SCREEN_WIDTH / 2 / PPM, int((SCREEN_HEIGHT / PPM) * 0.9)))
        self.player_body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        self.player_body.userData = {'type': 'player'}
        #fixedRotation=True
        
        self.player_lives = PLAYER_LIVES
        self.player_score = 0
        self.enemies = self.spawn_enemies()
        # self.enemies = []

        # List to hold bullet bodies
        self.enemy_bullets = []
        self.player_bullets = []

        self.keys = []

        self.running = True

        self.loop()

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_LEFT and K_RIGHT not in self.keys:
                        if K_LEFT not in self.keys:
                            self.keys.append(K_LEFT)

                        self.player_body.linearVelocity = (-PLAYER_SPEED, 0)
                    elif event.key == K_RIGHT and K_LEFT not in self.keys:
                        if K_RIGHT not in self.keys:
                            self.keys.append(K_RIGHT)

                        self.player_body.linearVelocity = (PLAYER_SPEED, 0)
                    elif event.key == K_SPACE:
                        self.fire_player_bullet()
                if event.type == KEYUP:
                    if event.key == K_RIGHT and K_RIGHT in self.keys:
                        self.keys.pop(self.keys.index(K_RIGHT))
                    if event.key == K_LEFT and K_LEFT in self.keys:
                        self.keys.pop(self.keys.index(K_LEFT))
                    print(self.keys)
                    if not self.keys:
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
        myEnemies = []

        #Loop this to create all enemies
        newEnemy = self.world.CreateKinematicBody(position=(1300 / PPM, int((SCREEN_HEIGHT / PPM) * 0.9)))
        newEnemy.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        newEnemy.userData = {'type': 'enemy'}
        myEnemies.append(newEnemy)
        
        return myEnemies
    
    def fire_player_bullet(self):
        #MAKE SURE THIS CODE IS ADDED
        #self.shoot_sound.play()
        #enemyBulletBody.userData = {'type': 'player_bullet'}
        pygame.mixer.Sound.stop(self.shoot_sound) # Stopping any previous shooting sound

        # Creating offest to align bullet to player
        offset_x = 0.75
        offset_y = 2.5

        # Creating bullet body
        bullet = self.world.CreateKinematicBody(position=(self.player_body.position[0] + offset_x, ((self.player_body.position[1] + offset_y) * 0.9)))
        bullet.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        bullet.userData = {'type': 'player_bullet'}
        self.player_bullets.append(bullet)
        
        bullet.linearVelocity = (0, -70) # Setting bullets Y-velocity

        pygame.mixer.Sound.play(self.shoot_sound) # Initiating shooting sound

    def fire_enemy_bullet(self, enemy_body):
        #select a random enemey and fire a bullet every x seconds
        #probably use a random int the lenght of the row and check if that enemy is still alive, if not add row length and check again

        #MAKE SURE THIS CODE IS ADDED
        #self.shoot_sound.play()
        #enemyBulletBody.userData = {'type': 'enemy_bullet'}
        pass

    def update_enemies(self):
        pass

    def update_bullets(self):
        #update player bullets that go up
        #update enemy bullest that go down

        pass

    def check_collisions(self):
        #self.explosion_sound.play()
        for contact in self.world.contacts:
    
            if contact.touching:
                fixture_a, fixture_b = contact.fixtureA, contact.fixtureB
                body_a, body_b = fixture_a.body, fixture_b.body
                
                if body_a.userData['type'] == 'player' and (body_b.userData['type'] == 'enemy' or body_b.userData['type'] == 'enemy_bullet'):
                    self.world.DestroyBody(body_b)
                    self.enemies.remove(body_b)
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.running = False
                        return
                elif (body_a.userData['type'] == 'enemy' or body_a.userData['type'] == 'enemy_bullet') and body_b.userData['type'] == 'player':
                    self.world.DestroyBody(body_a)
                    self.enemies.remove(body_a)
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.running = False
                        return
                elif body_a.userData['type'] == 'player_bullet' and body_b.userData['type'] == 'enemy':
                    self.world.DestroyBody(body_a)
                    self.player_bullets.remove(body_a)
                    self.world.DestroyBody(body_b)
                    self.enemies.remove(body_b)
                    self.player_score += ENEMY_POINTS
                elif body_a.userData['type'] == 'enemy' and body_b.userData['type'] == 'player_bullet':
                    self.world.DestroyBody(body_a)
                    self.enemies.remove(body_a)
                    self.world.DestroyBody(body_b)
                    self.player_bullets.remove(body_b)
                    self.player_score += ENEMY_POINTS

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
        
        for enemy in self.enemies:
            vertices = [(enemy.transform * vertex) * PPM for vertex in enemy.fixtures[0].shape.vertices]
            #pygame.draw.polygon(self.screen, (0, 0, 255), vertices)
            self.screen.blit(self.enemy_image, vertices[0])

        # Drawing player bullets
        for bullet in self.player_bullets:
            vertices = [(bullet.transform * vertex) * PPM for vertex in bullet.fixtures[0].shape.vertices]
            self.screen.blit(self.player_bullet_image, vertices[0])

        #vertices = [(self.tempBody.transform * vertex) * PPM for vertex in self.tempBody.fixtures[0].shape.vertices]
        #pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

        self.world.DrawDebugData()
        pygame.display.flip()
        

if __name__ == '__main__':
    game = Galaga()
    game.run()      
