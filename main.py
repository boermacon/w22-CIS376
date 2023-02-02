import pygame
import random

class GridSpace:
    """Object class to store information for grid spaces"""
    def __init__(self, gridRect, circlePoints, gridState, circleState, neighborList):
        """Initilization class which takes self, a grid rect, a circle point list, 2 state booleans, and a list as inputs."""
        self.gRect = gridRect
        self.cPoints = circlePoints
        self.gState = gridState
        self.cState = circleState
        self.neighbors = neighborList
    
    def returnGridRect(self):
        """Method to return a gridspace's rect variable. Takes self as input."""
        return self.gRect
    
    def invertGridState(self):
        """Method to invert the grid state of a grid space. Takes self as input."""
        if self.gState:
            self.gState = False
        else:
            self.gState = True
    
    def invertCircleState(self):
        """Method to invert the circle state of a grid space. Takes self as input."""
        if self.cState:
            self.cState = False
        else:
            self.cState = True

    def giveGridState(self):
        """Method to return the grid state of a gridspace. Takes self as input."""
        return self.gState
    
    def giveCircleState(self):
        """Method to return the cirlce state of a gridspace. Takes self as input."""
        return self.cState

    def giveNeighbors(self):
        """Method which returns the list of neighbors of a gridspace. Takes self as input."""
        return self.neighbors     
    
    def giveCirclePoints(self):
        """Method wich returns the list of circle points. Takes self as input."""
        return self.cPoints

class Engine:
    displayWidth = 720
    displayHeight = 720
    numGrid = 20
    FPS = 10
    def __init__(self):
        pygame.init()
        self._running = False
        self._screen = pygame.display.set_mode((Engine.displayWidth, Engine.displayHeight))
        self.gridSize = (int)(Engine.displayWidth/Engine.numGrid)
        self.grid = Engine.newGrid(self)
        self.myClock = pygame.time.Clock()

    def loop(self):
        self._running = True
        generator = False
        wallColor = (random.randint(0,240), random.randint(0,240), random.randint(0,240))
        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        if not generator: self.grid[((pygame.mouse.get_pos()[0]//self.gridSize) * Engine.numGrid) + pygame.mouse.get_pos()[1]//self.gridSize].invertGridState()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        generator = not generator
                        if not generator:
                            self.resetPlayer()

            self._screen.fill((255, 255, 255))
            if(generator):
                self.grid = self.updateGrid()
                self._screen.fill((random.randint(0,240), random.randint(0,240), random.randint(0,240)))
                

            for space in self.grid:
                if space.giveGridState():
                    pygame.draw.rect(self._screen, (0,0,0), space.returnGridRect())
                else:
                    pygame.draw.rect(self._screen, wallColor, space.returnGridRect())
                if space.giveCircleState():
                    pygame.draw.circle(self._screen, (255,127,0), space.giveCirclePoints()[0], space.giveCirclePoints()[1])
            pygame.display.update()
            self.myClock.tick(Engine.FPS)
    
    def newGrid(self):
        """ Method for genterating a new grid list. Takes only self as input. Ouputs a list of gridspace objects.
        """
        #Temporary List element
        temp = []

        #Iterate through the number of rows
        for i in range(Engine.numGrid):
            #Iterate through the number of columns
            for k in range(Engine.numGrid):
                #Create/clear a list of neighbors
                neighbors = []
                #Row is only valid in the downwards direction
                if i == 0:
                    #Column is only valid in the rightward direction
                    if k == 0:
                        neighbors.append(i*Engine.numGrid + (k+1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                        neighbors.append((i+1)*Engine.numGrid + (k+1))
                    #Column is only valid in the leftward diection
                    elif k == Engine.numGrid - 1:
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                    #Column is valid in both directions
                    else:
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                        neighbors.append((i+1)*Engine.numGrid + (k-1))
                        neighbors.append((i+1)*Engine.numGrid + k)
                        neighbors.append((i+1)*Engine.numGrid + (k+1))
                #Row is only valid in the upward direction
                elif i == Engine.numGrid - 1:
                    #Column is only valid in the rightward direction
                    if k == 0:
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append((i-1)*Engine.numGrid + (k+1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                    #Column is only valid in the leftward diection
                    elif k == Engine.numGrid - 1:
                        neighbors.append((i-1)*Engine.numGrid + (k-1))
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append(i*Engine.numGrid + (k-1))
                    #Column is valid in both directions
                    else:
                        neighbors.append((i-1)*Engine.numGrid + (k-1))
                        neighbors.append((i-1)*Engine.numGrid + k)
                        neighbors.append((i-1)*Engine.numGrid + (k+1))
                        neighbors.append(i*Engine.numGrid + (k-1))
                        neighbors.append(i*Engine.numGrid + (k+1))
                #Row is valid in both directions
                else:
                    #Column is only valid in the rightward direction
                    if k == 0:
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append(((i-1)*Engine.numGrid) + (k+1))
                        neighbors.append((i*Engine.numGrid) + (k+1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                        neighbors.append(((i+1)*Engine.numGrid) + (k+1))
                    #Column is only valid in the leftward diection
                    elif k == Engine.numGrid - 1:
                        neighbors.append(((i-1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append((i*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                    #Column is valid in both directions
                    else:
                        neighbors.append(((i-1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i-1)*Engine.numGrid) + k)
                        neighbors.append(((i-1)*Engine.numGrid) + (k+1))
                        neighbors.append((i*Engine.numGrid) + (k-1))
                        neighbors.append((i*Engine.numGrid) + (k+1))
                        neighbors.append(((i+1)*Engine.numGrid) + (k-1))
                        neighbors.append(((i+1)*Engine.numGrid) + k)
                        neighbors.append(((i+1)*Engine.numGrid) + (k+1))

                #Add a new gridspace object into the temporary grid list with its cordinates, state, and list of neighbors 
                temp.append(GridSpace(pygame.Rect(pygame.Rect(i*self.gridSize, k*self.gridSize, self.gridSize-1, self.gridSize-1)),
                    [((i*self.gridSize) + (self.gridSize//2), (k*self.gridSize) + (self.gridSize//2)), (self.gridSize//2)], False, False, neighbors))
        #Return the temporary grid list
        return temp

    def updateGrid(self):
        """Method to update an Engine object's grid. Takes itself as an input and outputs a list of gridspace objects.
        """
        #Temporary grid list is created
        temporaryGrid = []
        #Iterate through all of the grids in an instance of Engine's grid list
        for i in self.grid:
            #Set the number of neighbors to 0 and get a list of neighbors from the current gridspace
            numNeighbors = 0
            neighbors = i.giveNeighbors()
            
            #Iterate through the neighbors adding one for each neighbor that is active
            for k in neighbors:
                if self.grid[k].giveGridState():
                    numNeighbors += 1

            #Gridspace is now active if it has 3 active neighbors and wasn't active
            if numNeighbors == 3 and not i.giveGridState():
                temporaryGrid.append(GridSpace(i.returnGridRect(), i.giveCirclePoints(), True, i.giveCircleState(), i.giveNeighbors()))
            #Gridspace is now dead if it had only 1 or more than 4 neighbors
            elif numNeighbors <= 1 or numNeighbors > 4:
                temporaryGrid.append(GridSpace(i.returnGridRect(), i.giveCirclePoints(), False, i.giveCircleState(), i.giveNeighbors()))
            #Gridspace otherwise maintains its state
            else:
                temporaryGrid.append(GridSpace(i.returnGridRect(), i.giveCirclePoints(), i.giveGridState(), i.giveCircleState(), i.giveNeighbors()))
        
        #Returns the updated grid list
        return temporaryGrid
                
    def resetPlayer(self):
        for space in self.grid:
            if space.giveCircleState():
                space.invertCircleState()
        if not self.grid[0].giveGridState():
            self.grid[0].invertGridState()
        self.grid[0].invertCircleState()
        

if __name__ == '__main__':
    e = Engine()
    e.loop()