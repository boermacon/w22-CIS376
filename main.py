import pygame
import random

import pygame
pygame.init()
pygame.display.list_modes()

class GridSpace:
    def __init__(self, r, s):
        self.rect = r
        self.state = s
    
    def returnRect(self):
        return self.rect
    
    def invertState(self):
        if self.state:
            self.state = False
        else:
            self.state = True
        

class Engine:
    displayWidth = 720
    displayHeight = 720
    numGrid = 20
    def __init__(self):
        pygame.init()
        self._running = False
        self._screen = pygame.display.set_mode((Engine.displayWidth, Engine.displayHeight))
        self.gridSize = (int)(Engine.displayWidth/Engine.numGrid)
        self.grid = Engine.newGrid(self)

    def loop(self):
        self._running = True
        rect = pygame.Rect(pygame.Rect(320, 240, 32, 32))
        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        print(pygame.mouse.get_pos()[0]//self.gridSize)
                        print(pygame.mouse.get_pos()[1]//self.gridSize)
                        self.grid[((pygame.mouse.get_pos()[0]//self.gridSize) * Engine.numGrid) + pygame.mouse.get_pos()[1]//self.gridSize].invertState()
            self._screen.fill((0,101,165))#(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            

            for space in self.grid:
                if space.state:
                    pygame.draw.rect(self._screen, (255,255,255), space.returnRect())
                else:
                    pygame.draw.rect(self._screen, (0,0,0), space.returnRect())
                
            
            ##3pygame.draw.rect(self._screen, (255,255,255), rect)
            pygame.display.flip()
            rect.x = rect.x + 1
            if(rect.x > 1024):
                rect.x = 0
    
    def newGrid(self):
        temp = []
        for i in range(Engine.numGrid):
            for k in range(Engine.numGrid):
                temp.append(GridSpace(pygame.Rect(pygame.Rect(i*self.gridSize, k*self.gridSize, self.gridSize, self.gridSize)), True))
        return temp



if __name__ == '__main__':
    e = Engine()
    e.loop()