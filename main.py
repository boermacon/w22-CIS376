import pygame
from pygame.locals import *
import random

import Box2D
from Box2D import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
PPM = 20
PLAYER_SPEED = 30
ENEMY_SPEED = 10
PLAYER_BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5
ENEMY_SHOOT_PERCENTAGE = 3
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
        self.enemy_bullet_image = pygame.image.load('missile.png').convert_alpha()
        self.enemy_bullet_image = pygame.transform.rotate(self.enemy_bullet_image, 180)
        self.enemy_shoot_sound = pygame.mixer.Sound('blaster-2.mp3')
        #self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        #self.explosion_sound = pygame.mixer.Sound('explosion.wav')

        self.world = b2World(gravity=(0, 0))
        
        #self.ground_body = self.world.CreateStaticBody(position=(0, -10),shapes=b2PolygonShape(box=(50, 10)),)
        #self.body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        
        #self.tempBody = self.world.CreateStaticBody(position=(100/PPM, 0))
        #self.tempBody.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(10/PPM, SCREEN_HEIGHT/PPM)),density=1,friction=0.3))

        # Create a dynamic body
        self.player_body = self.world.CreateDynamicBody(position=(SCREEN_WIDTH / 2 / PPM, int((SCREEN_HEIGHT / PPM) * 0.9)))
        self.player_body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3,isSensor=True))
        self.player_body.userData = {'type': 'player'}
        #fixedRotation=True
        
        self.player_lives = PLAYER_LIVES
        self.player_score = 0
        self.enemies = self.spawn_enemies()
        # self.enemies = []
        # Call spawn enemey call
        self.enemy_bullets = []
        self.player_bullets = []

        self.running = True
        pygame.mixer.music.load('8-bit-space-music.mp3')
        pygame.mixer.music.play(-1)
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
            if int(self.player_body.position.x) in range(-10, 4) and self.player_body.linearVelocity == (-PLAYER_SPEED, 0):
                self.player_body.linearVelocity = (0, 0)
            if int(self.player_body.position.x) in range(76, 100) and self.player_body.linearVelocity == (PLAYER_SPEED, 0):
                self.player_body.linearVelocity = (0, 0)
            
            time_step = 1.0 / 60.0
            velocity_iterations = 6
            position_iterations = 2
            self.world.Step(time_step, velocity_iterations, position_iterations)
            
            self.update_enemies()
            self.update_bullets()
            self.check_collisions()
            self.draw_scene()

            self.fire_enemy_bullet()
            
            self.clock.tick(FPS)
        
        pygame.quit()

    def spawn_enemies(self):
        myEnemies = []

        #Loop this to create all enemies
        for i in range(10):
            newEnemy = self.world.CreateKinematicBody(position=((200 + (i*133)) / PPM, int((SCREEN_HEIGHT / PPM) * 0.15)))
            newEnemy.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
            newEnemy.userData = {'type': 'enemy'}
            myEnemies.append(newEnemy)
        
        return myEnemies
    
    def fire_player_bullet(self):
        #MAKE SURE THIS CODE IS ADDED
        #self.shoot_sound.play()
        #enemyBulletBody.userData = {'type': 'player_bullet'}
        pass

    def fire_enemy_bullet(self):
        #select a random enemey and fire a bullet every x seconds
        #probably use a random int the lenght of the row and check if that enemy is still alive, if not add row length and check again
        randNum = random.randint(0, 9)
        chanceToShoot = random.randint(0, 100)
        if (self.enemies[randNum] and chanceToShoot <= ENEMY_SHOOT_PERCENTAGE):
            enemyBulletBody = self.world.CreateKinematicBody(position=(self.enemies[randNum].position.x + 0.25, self.enemies[randNum].position.y + 0.5))
            enemyBulletBody.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(2/PPM,5/PPM)),density=1,friction=0.3))
            enemyBulletBody.userData = {'type': 'enemy_bullet'}
            enemyBulletBody.linearVelocity = (0, ENEMY_BULLET_SPEED)
            self.enemy_shoot_sound.play()
            self.enemy_bullets.append(enemyBulletBody)
        pass

    def update_enemies(self):
        for x in self.enemies:
            if (x):
                if (x.linearVelocity == (0, 0)):
                    x.linearVelocity = (ENEMY_SPEED, 0)
                elif int(x.position.x) in range(77, 100):
                    x.linearVelocity = (-ENEMY_SPEED, 1)
                elif int(x.position.x) in range(-10, 3):
                    x.linearVelocity = (ENEMY_SPEED, 1)
                elif int(x.position.y) in range(35, 40):
                    x.linearVelocity = (x.linearVelocity.x, -5)
        pass

    def update_bullets(self):
        #update player bullets that go up
        #update enemy bullest that go down

        pass

    def check_collisions(self):
        #self.explosion_sound.play()
        for contact in self.world.contacts:
            print("Contact")
            if contact.touching:
                fixture_a, fixture_b = contact.fixtureA, contact.fixtureB
                body_a, body_b = fixture_a.body, fixture_b.body
                
                if body_a.userData['type'] == 'player' and body_b.userData['type'] == 'enemy':
                    self.world.DestroyBody(body_b)
                    self.enemies.remove(body_b)
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.running = False
                        return
                elif body_a.userData['type'] == 'enemy' and body_b.userData['type'] == 'player':
                    self.world.DestroyBody(body_a)
                    self.enemies.remove(body_a)
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.running = False
                        return
                elif body_a.userData['type'] == 'player' and body_b.userData['type'] == 'enemy_bullet':
                    self.world.DestroyBody(body_b)
                    self.enemy_bullets.remove(body_b)
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.running = False
                        return
                elif body_a.userData['type'] == 'enemy_bullet' and body_b.userData['type'] == 'player':
                    self.world.DestroyBody(body_a)
                    self.enemy_bullets.remove(body_a)
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

        for enemyBullet in self.enemy_bullets:
            vertices = [(enemyBullet.transform * vertex) * PPM for vertex in enemyBullet.fixtures[0].shape.vertices]
            #pygame.draw.polygon(self.screen, (0, 0, 255), vertices)
            self.screen.blit(self.enemy_bullet_image, vertices[0])

        #vertices = [(self.tempBody.transform * vertex) * PPM for vertex in self.tempBody.fixtures[0].shape.vertices]
        #pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

        self.world.DrawDebugData()
        pygame.display.flip()
        

if __name__ == '__main__':
    game = Galaga()
    game.run()      