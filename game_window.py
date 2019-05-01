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
from copy import *

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
        self.cols = 96
        
        # sets the number of rows, ensuring there are enough to reach the bottom of the screen
        self.rows = self.cols * self.height / self.width + 1
        
        # get cell_width
        self.cell_width = self.width / self.cols
        
        # create grid of cell objects
        self.grid = [ [cell(self.image, i, j, self.cell_width, ATTRIBUTES) for i in range(self.cols) ] for j in range(self.rows) ]
    
    
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
        self.cols = columns
        
        # sets the number of rows, ensuring there are enough to reach the bottom of the screen
        self.rows = self.cols * self.height / self.width + 1
        
        # get cell_width
        self.cell_width = self.width / self.cols

        # create grid of cell objects
        self.grid = [[cell(self.image, i, j, self.cell_width, RULES) for i in range(self.cols)] for j in range(self.rows)]
        
        # find the new neighbors
        self.neighbor_finder(RULES[3])
    
    # activates the current cell when it is left-clicked
    def activate_cell(self, mouse_position):
        # stores x, y position of mouse pointer
        grid_position = [mouse_position[0], mouse_position[1]]
        
        # determines column in grid
        grid_position[0] = grid_position[0] / self.cell_width
        
        # determines row in grid
        grid_position[1] = ( grid_position[1] - self.y_offset ) / self.cell_width
        
        # changes cell to be alive
        if self.grid[grid_position[1]][grid_position[0]].contents == 0:
            self.grid[grid_position[1]][grid_position[0]].contents = 1
        # TODO: Fix clicking to advance states
        '''
        # advances state of cell
        else:
            # if the cell has reached the last state, the cell dies
            if self.grid[grid_position[1]][grid_position[0]].contents.contents == RULES[2][-1]:
                self.grid[grid_position[1]][grid_position[0]].contents.contents = 0
            # otherwise, the cell continues to the next state
            else:
                self.grid[grid_position[1]][grid_position[0]].contents.change_state()
        '''


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
    
    # holds cell logic, evaluates all cells to determine which cells will be alive or dead in the next generation
    def evaluate(self):
        # import globals
        global RULES
        
        # create new grid as copy of old grid
        new_grid = copy(self.grid)
        
        # constitutes cell logic, determines which cells will be alive or dead in the next generation
        for y_idx, row in enumerate(self.grid):
            for x_idx, cells in enumerate(row):
                # tracks whether the cell died this generation
                recently_dead = False
                
                # tracks whether the cell changed state this generation
                state_changed = False
                
                # if the cell is alive and set to always die, the cell dies
                if RULES[0] == [0] and cells.contents == 1:
                    if len(RULES[2]) != 2:
                        new_grid[y_idx][x_idx].change_state()
                    else:
                        new_grid[y_idx][x_idx].contents = 0
                    recently_dead = True
                    state_changed = True
                
                # if the cell is alive but does not have sufficient neighbors, or too many neighbors, the cell dies
                if cells.alive_neighbors not in RULES[0] and cells.contents == 1 and recently_dead == False:
                    if len(RULES[2]) != 2:
                        new_grid[y_idx][x_idx].change_state()
                    else:
                        new_grid[y_idx][x_idx].contents = 0
                    recently_dead = True
                    state_changed = True
                
                # if the cell is alive and has sufficient neighbors, the cell stays alive
                if cells.alive_neighbors in RULES[0] and cells.contents == 1:
                    new_grid[y_idx][x_idx].contents = 1
                
                # if the cell is dead and has sufficient neighbors, the cell comes alive
                if cells.alive_neighbors in RULES[1] and cells.contents == 0 and recently_dead == False:
                    new_grid[y_idx][x_idx].contents = 1
                
                # if the cell is in the dying phase, advance the state of the cell
                if cells.contents != 0 and cells.contents != 1 and state_changed == False:
                    # if the cell has reached the last state, the cell dies
                    if cells.contents == RULES[2][-1]:
                        new_grid[y_idx][x_idx].contents = 0
                    # otherwise, the cell continues to the next state
                    else:
                        new_grid[y_idx][x_idx].change_state()
        
        # set old grid to the new grid
        self.grid = new_grid
