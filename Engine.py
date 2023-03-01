import pygame
import os

class Engine:

    delta_time = 0

    events = None

    scene = None

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.running = False
        self.width = width
        self.height = height
        self.init_pygame()

        self.mode = 0

    def init_pygame(self):
        # Startup the pygame system
        pygame.init()

        # Create our window
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Window title
        pygame.display.set_caption(self.title)
        
        self.clock = pygame.time.Clock()
        self.last_checked_time = pygame.time.get_ticks()

    def run(self):

        self.running = True

        while self.running:
            
            # Gathering input
            Engine.events = pygame.event.get()

            # Updating based on user input
            for event in Engine.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            # Updating and drawing objects in scene
            Engine.scene.update(Engine.events)
            Engine.scene.draw(self.screen)

            Engine.delta_time = self.clock.tick(Engine.current_scene.fps) / 1000

            pygame.display.flip()
                    


 