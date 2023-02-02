import pygame
import random

import pygame
pygame.init()
pygame.display.list_modes()

class GridSpace:
    def __init__(self, r, s, n):
        self.rect = r
        self.state = s
        self.neighbors = n
    
    def returnRect(self):
        return self.rect
    
    def invertState(self):
        if self.state:
            self.state = False
        else:
            self.state = True
    
    def giveState(self):
        return self.state

    def giveNeighbors(self):
        return self.neighbors
        

class Engine:
    displayWidth = 720
    displayHeight = 720
    numGrid = 20
    def __init__(self):
        pygame.init()
        self._running = False
        self._screen = pygame.display.set_mode((Engine.displayWidth, Engine.displayHeight))
        self.gridSize = (int)(Engine.displayWidth/Engine.numGrid)
        ##self.gridSize = (int)(720/Engine.numGrid)
        self.grid = Engine.newGrid(self)

    def loop(self):
        self._running = True
        generator = False
        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        if not generator: self.grid[((pygame.mouse.get_pos()[0]//self.gridSize) * Engine.numGrid) + pygame.mouse.get_pos()[1]//self.gridSize].invertState()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        generator = not generator
            self._screen.fill((0,101,165))#(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            

            if(generator):
                self.grid = self.updateGrid()

            for space in self.grid:
                if space.state:
                    pygame.draw.rect(self._screen, (255,255,255), space.returnRect())
                else:
                    pygame.draw.rect(self._screen, (0,0,0), space.returnRect())
            pygame.display.flip()
    
    def newGrid(self):
        temp = []

        for i in range(Engine.numGrid):
            for k in range(Engine.numGrid):
                neighbors = []
                if i == 0:
                    if k == 0:
                        neighbors.append(i*Engine.numGrid + (k+1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                        neighbors.append((i+1)*Engine.numGrid + (k+1))
                        ##'''
                    elif k == Engine.numGrid - 1:
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                    else:
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                        neighbors.append((i+1)*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                        neighbors.append((i+1)*Engine.numGrid + (k+1))
                elif i == Engine.numGrid - 1:
                    if k == 0:
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append((i-1)*Engine.numGrid + (k+1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                    elif k == Engine.numGrid - 1:
                        neighbors.append((i-1)*Engine.numGrid + (k-1))
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append(i*Engine.numGrid + (k-1))
                    else:
                        neighbors.append((i-1)*Engine.numGrid + (k-1))
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append((i-1)*Engine.numGrid + (k+1))
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                else:
                    if k == 0:
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append(((i-1)*Engine.numGrid) + (k+1))
                        neighbors.append((i*Engine.numGrid) + (k+1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                        neighbors.append(((i+1)*Engine.numGrid) + (k+1))
                    elif k == Engine.numGrid - 1:
                        neighbors.append(((i-1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append((i*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                    else:
                        neighbors.append(((i-1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append(((i-1)*Engine.numGrid) + (k+1))
                        neighbors.append((i*Engine.numGrid) + (k-1))
                        neighbors.append((i*Engine.numGrid) + (k+1))
                        neighbors.append(((i+1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                        neighbors.append(((i+1)*Engine.numGrid) + (k+1))
                
                    
                    ##'''
                #print(neighbors)
                temp.append(GridSpace(pygame.Rect(pygame.Rect(i*self.gridSize, k*self.gridSize, self.gridSize-1, self.gridSize-1)), False, neighbors))
        return temp

    def updateGrid(self):
        temporaryGrid = []
        for i in self.grid:
            numNeighbors = 0
            neighbors = i.giveNeighbors()
            
            for k in neighbors:
                if self.grid[k].giveState():
                    numNeighbors += 1

            if numNeighbors == 3 and not i.giveState():
                temporaryGrid.append(GridSpace(i.returnRect(), True, i.giveNeighbors()))
            elif numNeighbors <= 1 or numNeighbors > 4:
                temporaryGrid.append(GridSpace(i.returnRect(), False, i.giveNeighbors()))
            else:
                temporaryGrid.append(GridSpace(i.returnRect(), i.giveState(), i.giveNeighbors()))
        
        return temporaryGrid
                




if __name__ == '__main__':
    e = Engine()
    e.loop()