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
ENEMY_POINTS, MISSILE_POINTS = 10, 1
NUM_ENEMIES = 10

class Galaga:
    """Class for a Galaga Game recreation."""
    def __init__(self):
        """Constructor for Galaga class."""
        # Initizalize pygame, clock, and mixer
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        # Set Display dimensions, font size, and window caption
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
        self.shoot_sound = pygame.mixer.Sound('blaster-2.mp3')
        #self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        #self.explosion_sound = pygame.mixer.Sound('explosion.wav')

        # Create a world
        self.world = b2World(gravity=(0, 0))

        # Create a dynamic body
        self.player_body = self.world.CreateDynamicBody(position=(SCREEN_WIDTH / 2 / PPM, int((SCREEN_HEIGHT / PPM) * 0.9)))
        self.player_body.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3,isSensor=True))
        self.player_body.userData = {'type': 'player'}
        
        # Set player lives, score, enemies, bullet holder lists, game state, andrunning state
        self.player_lives = PLAYER_LIVES
        self.player_score = 0
        self.enemies = self.spawn_enemies()
        self.enemy_bullets = []
        self.player_bullets = []
        self.gameState = 0
        self.running = True
        
        # List to hold pressed keys
        self.keys = []

        # Play music
        pygame.mixer.music.load('8-bit-space-music.mp3')
        pygame.mixer.music.play(-1)

        # Run the loop method
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
                    #print(self.keys)
                    if not self.keys:
                        self.player_body.linearVelocity = (0, 0)
                        
            if int(self.player_body.position.x) in range(-10, 4) and self.player_body.linearVelocity == (-PLAYER_SPEED, 0):
                self.player_body.linearVelocity = (0, 0)
            if int(self.player_body.position.x) in range(76, 100) and self.player_body.linearVelocity == (PLAYER_SPEED, 0):
                self.player_body.linearVelocity = (0, 0)
            
            time_step = 1.0 / 60.0
            velocity_iterations = 6
            position_iterations = 2
            self.world.Step(time_step, velocity_iterations, position_iterations)
            
            self.fire_enemy_bullet()
            self.update_enemies()
            self.check_collisions()
            self.gameState = self.check_game_state()
            self.draw_scene()

            self.clock.tick(FPS)
        
        self.endGame()

    def spawn_enemies(self):
        """Method that handles enemy generation. Takes self as input. Outputs a list of (kinematic) bodies."""
        # Create an empty list for enemies
        myEnemies = []

        # Iterate through a loop NUMENEMY. Create kinematic bodies with fixtures and user data appending those bodies to the my enemies list
        for i in range(NUM_ENEMIES):
            newEnemy = self.world.CreateKinematicBody(position=((200 + (i*133)) / PPM, int((SCREEN_HEIGHT / PPM) * 0.15)))
            newEnemy.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
            newEnemy.userData = {'type': 'enemy'}
            myEnemies.append(newEnemy)
        
        # Return the created enemies list
        return myEnemies
    
    def fire_player_bullet(self):
        pygame.mixer.Sound.stop(self.shoot_sound) # Stopping any previous shooting sound

        # Creating offest to align bullet to player
        offset_x = 0.75
        offset_y = 2.5

        # Creating bullet body
        bullet = self.world.CreateDynamicBody(position=(self.player_body.position[0] + offset_x, ((self.player_body.position[1] + offset_y) * 0.9)))
        bullet.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(25/PPM,25/PPM)),density=1,friction=0.3))
        bullet.userData = {'type': 'player_bullet'}
        self.player_bullets.append(bullet)
        
        bullet.linearVelocity = (0, -70) # Setting bullets Y-velocity

        pygame.mixer.Sound.play(self.shoot_sound) # Initiating shooting sound
        
    def fire_enemy_bullet(self):
        """Method that handles enemy bullet firing. Takes self as input"""
        # Shutdown game if error occurs where we try to fire an enemey bullet with no enemies present
        if len(self.enemies) <= 0:
            exit(-1)

        #Select a random enemy and fire a bullet based on a percentage.
        randNum = random.randint(0, (len(self.enemies)-1))
        chanceToShoot = random.randint(0, 100)
        if (self.enemies[randNum] and chanceToShoot <= ENEMY_SHOOT_PERCENTAGE):
            enemyBulletBody = self.world.CreateKinematicBody(position=(self.enemies[randNum].position.x + 0.25, self.enemies[randNum].position.y + 0.5))
            enemyBulletBody.CreateFixture(Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(2/PPM,5/PPM)),density=1,friction=0.3))
            enemyBulletBody.userData = {'type': 'enemy_bullet'}
            enemyBulletBody.linearVelocity = (0, ENEMY_BULLET_SPEED)
            self.enemy_shoot_sound.play()
            self.enemy_bullets.append(enemyBulletBody)

        #Destroys bullets that have gone off the bottom of the screen.
        for x in self.enemy_bullets:
            if x.position.y >= 70:
                self.world.DestroyBody(x)
                self.enemy_bullets.remove(x)

    def update_enemies(self):
        """Method that handles enemy movement."""
        #Loop that adjusts velocity for each enemy depending on their x,y position.
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

    def check_game_state(self):
        """Method to check and return the state of the game. Takes self as input. Outputs integer 0 for running, 1 for loss, and 2 for win."""
        # Check if lives and return loss if no lives
        if self.player_lives <= 0:
            self.running = False
            return 1
        # Check if there are enemies and return win if there are no enemies
        elif len(self.enemies) <= 0:
            self.running = False
            return 2
        # Return running as there is no win or loss
        else:
            return 0

    def check_collisions(self):
        """Method to check collisions in the game. Takes self as input."""
        # Loop for all current contacts
        for contact in self.world.contacts:
            # If contacts are currently touching get their fixtures and bodies
            if contact.touching:
                fixture_a, fixture_b = contact.fixtureA, contact.fixtureB
                body_a, body_b = fixture_a.body, fixture_b.body
                
                # Check if a player as collided with an enemy -> destroy enemy and remove a life
                if body_a.userData['type'] == 'player' and body_b.userData['type'] == 'enemy':
                    self.world.DestroyBody(body_b)
                    self.enemies.remove(body_b)
                    self.player_lives -= 1
                elif body_a.userData['type'] == 'enemy' and body_b.userData['type'] == 'player':
                    self.world.DestroyBody(body_a)
                    self.enemies.remove(body_a)
                    self.player_lives -= 1

                # Check if a player has collided with an enemy bullet -> destroy enemy bullet and remove a life
                elif body_a.userData['type'] == 'player' and body_b.userData['type'] == 'enemy_bullet':
                    self.world.DestroyBody(body_b)
                    self.enemy_bullets.remove(body_b)
                    self.player_lives -= 1
                elif body_a.userData['type'] == 'enemy_bullet' and body_b.userData['type'] == 'player':
                    self.world.DestroyBody(body_a)
                    self.enemy_bullets.remove(body_a)
                    self.player_lives -= 1
                
                # Check if an enemey has collided with a player bullet -> destroy both entities and increase points
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

                # Check if an enemey bullet has collided with a player bullet -> destroy both entities and increase points
                elif body_a.userData['type'] == 'player_bullet' and body_b.userData['type'] == 'enemy_bullet':
                    self.world.DestroyBody(body_a)
                    self.player_bullets.remove(body_a)
                    self.world.DestroyBody(body_b)
                    self.enemy_bullets.remove(body_b)
                    self.player_score += MISSILE_POINTS
                elif body_a.userData['type'] == 'enemy_bullet' and body_b.userData['type'] == 'player_bullet':
                    self.world.DestroyBody(body_a)
                    self.enemy_bullets.remove(body_a)
                    self.world.DestroyBody(body_b)
                    self.player_bullets.remove(body_b)
                    self.player_score += MISSILE_POINTS

    def draw_scene(self):
        """Method to draw screen during main game loop. Takes self as input."""
        # Clear screen as black
        self.screen.fill((0, 0, 0))
        
        # Display lives in top left corner
        for life in range(self.player_lives):
            self.screen.blit(self.player_image, (20 + life * 30, 20))
        
        # Display Score in top right corner
        score_text = self.font.render(f"Score: {self.player_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
        
        # Draw the player body
        # Get vertices from player body's fixture and display image at those vertices
        vertices = [(self.player_body.transform * vertex) * PPM for vertex in self.player_body.fixtures[0].shape.vertices]
        self.screen.blit(self.player_image, vertices[0])
        
        # Draw enemies using principles of player body rendering in a loop
        for enemy in self.enemies:
            vertices = [(enemy.transform * vertex) * PPM for vertex in enemy.fixtures[0].shape.vertices]
            self.screen.blit(self.enemy_image, vertices[0])

        # Draw enemy bullets using principles from player body rendering in a loop
        for enemyBullet in self.enemy_bullets:
            vertices = [(enemyBullet.transform * vertex) * PPM for vertex in enemyBullet.fixtures[0].shape.vertices]
            self.screen.blit(self.enemy_bullet_image, vertices[0])
            
        # Drawing player bullets
        for bullet in self.player_bullets:
            vertices = [(bullet.transform * vertex) * PPM for vertex in bullet.fixtures[0].shape.vertices]
            self.screen.blit(self.player_bullet_image, vertices[0])

        # Draw / update screen
        self.world.DrawDebugData()
        pygame.display.flip()
    
    def endGame(self):
        """Method to handle endscreen display. Takes self as input"""
        endRun = False
        # If we quit before we won/lost
        if self.gameState == 0:
            pygame.quit()
        else:
            endRun = True
        
        #Loop until exit
        while endRun:
            #Blank Screen and new font size
            fontSize = 50
            self.screen.fill((0, 0, 0))
            self.font = pygame.font.Font(None, fontSize)
            
            #If we lost
            if self.gameState == 1:
                # Render loss text
                text_surface = self.font.render("You Lost", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                self.screen.blit(text_surface, text_rect)

                # Render score 'fontSize' distance below above text
                text_surface = self.font.render("Score: " + str(self.player_score), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + fontSize))
                self.screen.blit(text_surface, text_rect)
            
            #If we won    
            elif self.gameState == 2:
                # Render win text
                text_surface = self.font.render("You Won", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                self.screen.blit(text_surface, text_rect)

                # Render score 'fontSize' distance below above text
                text_surface = self.font.render("Score: " + str(self.player_score), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + fontSize))
                self.screen.blit(text_surface, text_rect)

            # Flip the display
            pygame.display.flip()

            #Check for exit
            for event in pygame.event.get():
                if event.type == QUIT:
                    endRun = False
                    pygame.quit()

# Python start code
if __name__ == '__main__':
    game = Galaga()     