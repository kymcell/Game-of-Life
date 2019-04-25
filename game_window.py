#
# CS 224 Spring 2019
# Semester Project
#
# Creates the game window to be used by game_of_life.py
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

'''
WORLD:
    The game world consists of a theoretically infinite 2-Dimensional grid of orthogonal squares
    For our purposes the grid will have a finite limit, chosen from multiple options by the user
'''

# imports
from cell import *

class game_window():
    # class variables
    size = (0, 0)
    RULES = []
    
    def __init__(self, screen, x_offset, y_offset, ATTRIBUTES):
        # import globals
        global RULES
        
        # iniitialize screen
        self.screen = screen
        
        # initialize offsets
        self.x_offset = x_offset
        self.y_offset = y_offset
        
        # position game_window
        vector = pygame.math.Vector2
        self.pos = vector(self.x_offset, self.y_offset)
        
        # get screen resolution
        resolution = pygame.display.Info()
        
        # set width and height
        self.width = resolution.current_w
        self.height = resolution.current_h - self.y_offset
        
        # set surface where the grid will be placed and the game of life will be played
        self.image = pygame.Surface( (self.width, self.height) )
        self.rect = self.image.get_rect()
        
        # set the rules for the cells
        RULES = ATTRIBUTES
        
        # set columns, must be one of the following options for 1920x1080 resolution screen:
        # cols = 24, 48, 96, 120, 192, 240
        cols = 96
        
        # sets the number of rows, ensuring there are enough to reach the bottom of the screen
        rows = cols * self.height / self.width + 1
        
        # get cell_width
        self.cell_width = self.width / cols
        
        # create grid of cell objects
        self.grid = [ [cell(self.image, i, j, self.cell_width, ATTRIBUTES) for i in range(cols) ] for j in range(rows) ]
    
    
    # displays the window and cells
    def display(self):
        # set RGB color for background
        self.image.fill( (0, 0, 0) )
        
        # call cell display
        for row in self.grid:
            for cell in row:
                cell.display()
        
        # display game_window
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
    
    
    # updates the window and cells
    def update(self, new_params):
        # import globals
        global RULES
        
        # set top left corner as reference
        self.rect.topleft = self.pos
        
        # set new attributes
        RULES = new_params
        
        # call cell update
        for row in self.grid:
            for cell in row:
                cell.update(RULES, self.grid)
    
    # resizes the grid to the user's choice
    def resize(self, columns):
        # import globals
        global RULES
        
        # clear the grid of all cells
        self.reset()
        
        # set number of columns
        cols = columns
        
        # sets the number of rows, ensuring there are enough to reach the bottom of the screen
        rows = cols * self.height / self.width + 1
        
        # get cell_width
        self.cell_width = self.width / cols

        # create grid of cell objects
        self.grid = [[cell(self.image, i, j, self.cell_width, RULES) for i in range(cols)] for j in range(rows)]

        # find the new neighbors
        self.neighbor_finder()
    
    # activates the current cell when it is left-clicked
    def activate_cell(self, mouse_position):
        # stores x, y position of mouse pointer
        grid_position = [mouse_position[0], mouse_position[1]]
        
        # determines column in grid
        grid_position[0] = grid_position[0] / self.cell_width
        
        # determines row in grid
        grid_position[1] = ( grid_position[1] - self.y_offset ) / self.cell_width
        
        # changes cell to be alive
        self.grid[grid_position[1]][grid_position[0]].contents = 1


    # kills the current cell when it is right-clicked
    def kill_cell(self, mouse_position):
        # stores x, y position of mouse pointer
        grid_position = [mouse_position[0], mouse_position[1]]
    
        # determines column in grid
        grid_position[0] = grid_position[0] / self.cell_width
    
        # determines row in grid
        grid_position[1] = (grid_position[1] - self.y_offset) / self.cell_width
    
        # changes cell to be dead
        self.grid[grid_position[1]][grid_position[0]].contents = 0

    # kills all cells
    def reset(self):
        # pause propagation
        # TODO: pause propogation here
        
        # iterate through every cell and kill it
        for row in self.grid:
            for cell in row:
                cell.contents = 0

    # find the neighbors for each cell
    def neighbor_finder(self, NEIGHBORINO):
        # determine neighbors for all cells
        for row in self.grid:
            for cells in row:
                cells.find_neighbors(NEIGHBORINO)