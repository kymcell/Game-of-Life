#
# CS 224 Spring 2019
# Semester Project: The Game of Life
#
# Holds cell values and methods for changing cell values,
# comprises all cells within the game of life.
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

# imports
import pygame
from neighborhood import *

class cell():
    # class variables
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = "Survival / Birth / States / Neighborhood"
    
    SCALE = 0
    
    def __init__(self, surface, x_pos, y_pos, cell_width, ATTRIBUTES):
        # import globals
        global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, SCALE
        
        SURVIVAL = ATTRIBUTES[0]
        BIRTH = ATTRIBUTES[1]
        STATES = ATTRIBUTES[2]
        NEIGHBORHOOD = ATTRIBUTES[3]
        RULESET = ATTRIBUTES[4]
        self.contents = 0
        self.neighbors = []
        self.alive_neighbors = 0
        
        self.neighbor_positions = []
        
        # initialize surface
        self.surface = surface
        
        # set x and y positions of cell in the grid
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        # set scaling variable
        SCALE = cell_width
        
        # sets scaling of grid
        self.image = pygame.Surface( (SCALE, SCALE) )
        self.rect = self.image.get_rect()
    
    
    # displays the cell
    def display(self):
        # import globals
        global STATES, SCALE
        
        # if the cell is alive, fill the cell: Black
        if self.contents == 1:
            self.image.fill( (0, 0, 0) )
        
        # if the cell is dying, fill the cell with a unique color: Blue
        elif self.contents == 2:
            self.image.fill( (0, 0, 255) )
        
        # if the cell is dying, fill the cell with a unique color: Light Blue
        elif self.contents == 3:
            self.image.fill( (0, 128, 255) )
        
        # if the cell is dying, fill the cell with a unique color: Teal
        elif self.contents == 4:
            self.image.fill( (0, 255, 255) )
        
        # if the cell is dying, fill the cell with a unique color: Sea Green
        elif self.contents == 5:
            self.image.fill( (0, 255, 128) )
        
        # if the cell is dying, fill the cell with a unique color: Green
        elif self.contents == 6:
            self.image.fill( (0, 255, 0) )
        
        # if the cell is dying, fill the cell with a unique color: Lime Green
        elif self.contents == 7:
            self.image.fill( (128, 255, 0) )
        
        # if the cell is dying, fill the cell with a unique color: Yellow
        elif self.contents == 8:
            self.image.fill( (255, 255, 0) )
        
        # if the cell is dying, fill the cell with a unique color: Orange
        elif self.contents == 9:
            self.image.fill( (255, 128, 0) )
        
        # if the cell is dying, fill the cell with a unique color: Red
        elif self.contents == 10:
            self.image.fill((255, 0, 0))
        
        # if the cell is dying, fill the cell with a unique color: Pink
        elif self.contents == 11:
            self.image.fill((255, 0, 128))
        
        # if the cell is dying, fill the cell with a unique color: Purple
        elif self.contents == 12:
            self.image.fill((255, 0, 255))
        
        # if the cell is dying, fill the cell with a unique color: Blurple
        elif self.contents == 13:
            self.image.fill((128, 0, 255))
        
        # if the cell is not alive, draw border around cell
        else:
            # set RGB color for borders on grid
            self.image.fill( (0, 0, 0) )
            
            # second parameter: sets RGB color for background of grid
            # third parameter: (right_border_width, bottom_border_width, col_border_width, row_border_width)
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, SCALE, SCALE) )
        
        self.surface.blit(self.image, (self.x_pos*SCALE, self.y_pos*SCALE) )
    
    
    # updates the cell
    def update(self, ATTRIBUTES, grid):
        # import globals
        global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, SCALE
        
        # set top left corner as reference
        self.rect.topleft = (self.x_pos*SCALE, self.y_pos*SCALE)
        
        # set new attributes
        SURVIVAL = ATTRIBUTES[0]
        BIRTH = ATTRIBUTES[1]
        STATES = ATTRIBUTES[2]
        NEIGHBORHOOD = ATTRIBUTES[3]
        RULESET = ATTRIBUTES[4]
        
        # reset number of alive neighbors
        self.alive_neighbors = 0
        
        # add neighbors to neighbor list
        for neighbor in self.neighbor_positions:
            try:
                if grid[neighbor[1]][neighbor[0]].contents == 1:
                    self.alive_neighbors += 1
            except:
                pass
    
    
    # determines the number of neighbors
    def find_neighbors(self, NEIGHBORINO, columns, rows):
        # create empty list
        self.neighbor_positions = []
        
        # set user choice
        user_neighborhood_choice = NEIGHBORINO
        
        # sets neighbor_positions to the Moore Neighborhood
        if user_neighborhood_choice == "M":
            self.neighbor_positions = moore()
        
        # sets neighbor_positions to the Von Neumann Neighborhood
        if user_neighborhood_choice == "VN":
            self.neighbor_positions = neumann()

        # sets neighbor_positions to the Engholdt Neighborhood
        if user_neighborhood_choice == "E":
            self.neighbor_positions = engholdt()
        
        # determine positions of neighbors
        for neighbor in self.neighbor_positions:
            neighbor[0] += self.x_pos
            neighbor[1] += self.y_pos
        
        # fixes cells from bleeding over from the edges of the screen
        for neighbor in self.neighbor_positions:
            if neighbor[0] < 0:
                neighbor[0] += columns
            if neighbor[0] > columns - 1:
                neighbor[0] -= columns
            if neighbor[1] > rows - 1:
                neighbor[1] -= rows
    
    
    # advances the state of the cell
    def change_state(self):
        # increment the state of the cell
        self.contents += 1
