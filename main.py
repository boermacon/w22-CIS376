import pygame
import random

"""Code was developed off of the base game loop code which was developed/showcased in class"""
"""Group members: Connor Boerma and Fabian Kirberg"""
"""Start of Connor's code"""
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
    #Class wide variables for general management of the game
    displayWidth = 720
    displayHeight = 720
    numGrid = 20
    FPS = 10
    def __init__(self):
        """Constructor method for Engine class."""
        #Initialize pygame
        pygame.init()
        #Set the game loop boolean to false
        self._running = False
        #Create a pygame display/surface
        self._screen = pygame.display.set_mode((Engine.displayWidth, Engine.displayHeight))
        #Create a gridsize var
        self.gridSize = (int)(Engine.displayWidth/Engine.numGrid)
        #Grid list
        self.grid = Engine.newGrid(self)
        #Game clock
        self.myClock = pygame.time.Clock()
        #Player location holder
        self.myPlayer = 0

    def loop(self):
        """Main game loop method. Takes self as input."""
        #Turn on the game loop and disable the cell generator
        self._running = True
        generator = False
        #Create a random wall color
        wallColor = (random.randint(0,240), random.randint(0,240), random.randint(0,240))
        #Game loop
        while self._running:
            #Create a new event queue
            events = pygame.event.get()
            #Parse through all of the events
            for event in events:
                #If quit event, then exit the game
                if event.type == pygame.QUIT:
                    self._running = False
                #If the mouse is pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Check button type
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        #Find and invert cells while generator is off
                        if not generator: self.grid[((pygame.mouse.get_pos()[0]//self.gridSize) * Engine.numGrid) + pygame.mouse.get_pos()[1]//self.gridSize].invertGridState()
                #If keys in general
                if event.type == pygame.KEYDOWN:
                    #Spacebar pressed
                    if event.key == pygame.K_SPACE:
                        #Invert generator
                        generator = not generator
                        #Call reset player method with the generators status passed through
                        self.resetPlayer(generator)

                    """End of Connor's code and start of Fabian's"""
                    """Character Movement"""
                    #Player movement, only allowed if generator is off
                    if generator == False:
                        #If up is pressed and the grid space above the player is open and within the bounds of the game
                        if event.key == pygame.K_UP and (self.myPlayer) % (Engine.numGrid) != 0 and self.grid[self.myPlayer-1].giveGridState() == True:
                            #Clear the player from the current position and move the player circle to the new space
                            self.grid[self.myPlayer].invertCircleState()
                            self.myPlayer = self.myPlayer-1
                            self.grid[self.myPlayer].invertCircleState()
                        #If down is pressed and the grid space below the player is open and within the bounds of the game
                        if event.key == pygame.K_DOWN and (self.myPlayer+1) % (Engine.numGrid) != 0 and self.grid[self.myPlayer+1].giveGridState() == True:
                            #Clear the player from the current position and move the player circle to the new space
                            self.grid[self.myPlayer].invertCircleState()
                            self.myPlayer = self.myPlayer+1
                            self.grid[self.myPlayer].invertCircleState()
                        #If right is pressed and the grid space to the right of the player is open and within the bounds of the game
                        if event.key == pygame.K_RIGHT and (self.myPlayer+Engine.numGrid) < (Engine.numGrid*Engine.numGrid) and self.grid[self.myPlayer+Engine.numGrid].giveGridState() == True:
                            #Clear the player from the current position and move the player circle to the new space
                            self.grid[self.myPlayer].invertCircleState()
                            self.myPlayer = self.myPlayer+Engine.numGrid
                            self.grid[self.myPlayer].invertCircleState()
                        #If left is pressed and the grid space to the left of the player is open and within the bounds of the game
                        if event.key == pygame.K_LEFT and 0 <= (self.myPlayer-Engine.numGrid) and self.grid[self.myPlayer-Engine.numGrid].giveGridState() == True:
                            #Clear the player from the current position and move the player circle to the new space
                            self.grid[self.myPlayer].invertCircleState()
                            self.myPlayer = self.myPlayer-Engine.numGrid
                            self.grid[self.myPlayer].invertCircleState()

                        """Check if the my player index value is the same as the final grid index after the player has moved"""
                        #If the player has reached the bottom right corner of the grid, reset the board and display the win message
                        if self.myPlayer == (Engine.numGrid*Engine.numGrid)-1:
                            #Array containing the win message
                            winMessage = [69,70,71,84,85,92,106,107,111,124,125,132,149,150,151,164,165,166,167,184,187,189,192,204,205,206,207,209,210,211,212,229,232,244,245,246,247,267,269,270,271,272,284,285,286,287,290,311,329,330,331,332,368,369,370,372]
                            self.grid[self.myPlayer].invertCircleState()
                            for space in self.grid:
                                if space.giveGridState():
                                    space.invertGridState()
                            for i in winMessage:
                                self.grid[i].invertGridState()

            """End of Fabian's Code and start of Connor's"""
            #Is generator active?
            if generator:
                #Update the grid
                self.grid = self.updateGrid()
                #Flash the border colors to indicate the updated status
                self._screen.fill((random.randint(0,240), random.randint(0,240), random.randint(0,240)))
            #Generator not active
            else:
                #Keep border color white
                self._screen.fill((255, 255, 255))
                
            #Iterate through the list of gridspaces
            for space in self.grid:
                #Check the grid states
                if space.giveGridState():
                    #Draw active/passable grids in black
                    pygame.draw.rect(self._screen, (0,0,0), space.returnGridRect())
                else:
                    #Draw inactive/wall grids in the defined wall color
                    pygame.draw.rect(self._screen, wallColor, space.returnGridRect())
                #Check if a grid holds the player and draw an orange circle if it does
                if space.giveCircleState():
                    pygame.draw.circle(self._screen, (255,127,0), space.giveCirclePoints()[0], space.giveCirclePoints()[1])
            
            #Update the pygame display
            pygame.display.update()
            #Have the pygame clock tick in order to meet the Engine class's defined FPS
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
                
    def resetPlayer(self, genStatus):
        """Method to reset the player "entity". Takes self and boolean as inputs."""
        #If the generator is on
        if genStatus:
            #Find and clear all player states from the board
            for space in self.grid:
                if space.giveCircleState():
                    space.invertCircleState()
        #Else the generator is off
        else:
            #Check and set the first gridspace as a valid space if it isn't
            if not self.grid[0].giveGridState():
                self.grid[0].invertGridState()
            #Reset necessary variables to indicate that the first grid space holds the player character
            self.grid[0].invertCircleState()
            self.myPlayer = 0
        
"""End of Connor's Code"""

if __name__ == '__main__':
    e = Engine()
    e.loop()
