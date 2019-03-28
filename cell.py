#
# CS 224 Spring 2019
# Semester Project
#
# Holds cell values and methods for changing cell values, comprises all cells in the game_of_life.py
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

'''
SURVIVAL:
    Survival means a cell will stay alive (active) until the next generation if it satisfies the neighborhood conditions
    If the neighborhood conditions are not satisfied, the cell will die (deactivate)
    
    If a cell has exactly x neighbors, it will survive to the next generation, otherwise it dies


BIRTH:
    Birth means a cell that is dead (deactive) will be born (activate) in the next generation if it satisfies the neighborhood conditions
    A cell is considered a neighbor if it is within the specified neighborhood and in the alive (active) state
    
    A cell is born if it has exactly x neighbors


STATES:
    States refers to the number of states that a cell has
    A cell can theoretically have an infinite number of states, but a limit of 10 is most reasonable
    
    There are x states, alive, dead, and x-2 states of decay
    
    For example, if a cell has 4 states, it has the following behavior:
    0 - Dead    (Graphically, this cell is white)
    1 - Alive   (Graphically, this cell is black)
    2 - Dying   (Graphically, this cell is a color different from all previous colors)
    3 - Dying   (Graphically, this cell is a color different from all previous colors)
    
    After the final state of decay, the cell will die (deactivate) and return to a value of 0
    
    For the purposes of birth, the states of decay (dying) are not considered to be alive


NEIGHBORHOOD:
    The neighborhood of a cell is defined according to the type of neighborhood it is given
    There are two main neighborhoods:
        Moore Neighborhood (M): All 8 cells surrounding the central cell both diagonally and orthogonally
            Domain: {1,2,3,4,5,6,7,8}
        Von Neumann Neighborhood (VN): Only the 4 cells surrounding the central cell orthogonally
            Domain: {1,2,3,4}

NOTE:
    A domain of 0 is allowed for the Survival value, this means that a living cell will always die in the next generation
'''

# imports
import pygame

class cell():
    # global variables
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = "Survival / Birth / States / Neighborhood"
    NEIGHBORS = 0
    
    SCALE = 0
    
    # constructor
    def __init__(self, surface, x_pos, y_pos, cell_width, ATTRIBUTES):
        # import globals
        global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, SCALE
        
        SURVIVAL = ATTRIBUTES[0]
        BIRTH = ATTRIBUTES[1]
        STATES = ATTRIBUTES[2]
        NEIGHBORHOOD = ATTRIBUTES[3]
        RULESET = ATTRIBUTES[4]
        
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
        global SCALE
        
        # set RGB color for borders on grid
        self.image.fill( (0, 0, 0) )
        
        # second parameter: sets RGB color for background of grid
        # third parameter: (right_border_width, bottom_border_width, col_border_width, row_border_width)
        pygame.draw.rect(self.image, (255, 255, 255), (1, 1, SCALE, SCALE) )
        
        self.surface.blit(self.image, (self.x_pos*SCALE, self.y_pos*SCALE) )
    
    
    # updates the cell
    def update(self):
        # import globals
        global SCALE
        
        # set top left corner as reference
        self.rect.topleft = (self.x_pos*SCALE, self.y_pos*SCALE)
    
    
    # updates number of neighbors
    def update_neighbors(self):
        # import globals
        global NEIGHBORS
        
        NEIGHBORS += 1
    
    
    # advances the state of the cell
    def change_state(self):
        # import globals
        global STATES
    
    
    # births the cell
    def birth(self):
        # import globals
        global BIRTH
