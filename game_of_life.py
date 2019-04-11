#
# CS 224 Spring 2019
# Semester Project
#
# There are infinite possibilities within the realm of cellular automata.
# This program seeks to emulate many of those possibilities through completely customizable parameters and a user friendly GUI.
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

'''
WORLD:
    The game world consists of a theoretically infinite 2-Dimensional grid of orthogonal squares
    For our purposes the grid will have a finite limit, chosen from 3 options by the user
        Large: X x X squares
        Medium: Y x Y squares
        Small: Z x Z squares

RULESETS:
    Rulesets are named using the following format:
    Survival / Birth / States / Neighborhood
    
    For example, Conway's Game of Life has the following ruleset:
    [2, 3] / [3] / 2 / M
    
    If a cell has exactly 2 or 3 neighbors, it will survive to the next generation, otherwise it dies
    A cell is born if it has exactly 3 neighbors
    There are 2 states, alive and dead
    Utilizes the Moore neighborhood


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

REFERENCES:
    Cellular Automata Information:
    www.mirekw.com/ca/index.html

    Game of Life Tutorial:
    https://www.youtube.com/watch?v=GKe1aGQlKDY&list=PLryDJVmh-ww1OZnkZkzlaewDrhHy2Rli2&index=1

    Thorpy Pygame GUI Information:
    http://www.thorpy.org/documentation.html
'''

# imports
from rulesets import *
from neighborhood import *

from time import *
from cell import *
from game_window import *

import pygame, thorpy

# main method
def main():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES
    
    # initialize pygame
    pygame.init()
    
    # create fullscreen window
    world()

    # SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET = random_ruleset()
    SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET = conway()

    print( SURVIVAL )
    print( BIRTH )
    print( STATES )
    print( NEIGHBORHOOD )
    print( RULESET )


'''
RULES
'''
# TODO : Move this method to wherever the user will select the rules from the dropdown menu
# user chooses which ruleset will be used
def rules():
    user_choice = 1  # user determined ruleset
    
    if user_choice == 1:
        conway()


'''
GUI
'''

# creates game window and grid of cells
def world():
    # import globals
    global RUNNING
    
    # create fullscreen window
    window = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN)
    life_window = game_window(window, 0, 200, ATTRIBUTES)
    
    # set window title
    pygame.display.set_caption("Game of Life")
    
    # while the program is running, continue updating the window
    while RUNNING:
        user_input(life_window)
        display(window, life_window)
        update(life_window)
        pygame.display.update()
    pygame.quit()


# displays the windows
def display(window, life_window):
    # set RGB color for background
    window.fill( (200, 200, 200) )
    game_window.display(life_window)


# updates the game_window
def update(life_window):
    # update game_window
    game_window.update(life_window)


# determines when the user clicks the mouse or presses the ESC key to exit the program
def user_input(life_window):
    # import globals
    global RUNNING
    
    # determines if the program should end
    for event in pygame.event.get():
        # program will end if the window is closed
        if event.type == pygame.QUIT:
            RUNNING = False
        
        # detects when the left mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # gets the current mouse position
            mouse_position = pygame.mouse.get_pos()
            
            # determines when the cell should be activated once clicked
            if mouse_in_grid(mouse_position):
                game_window.activate_cell(life_window, mouse_position)
        
        # detects when the right mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # gets the current mouse position
            mouse_position = pygame.mouse.get_pos()
            
            # determines when the cell should be killed once clicked
            if mouse_in_grid(mouse_position):
                game_window.kill_cell(life_window, mouse_position)
        
        # program will end if the ESC key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False


# checks if the mouse is hovering above the grid
def mouse_in_grid(mouse_position):
    # returns true if the mouse is hovering above the grid, otherwise false
    if ( mouse_position[0] >= 0 and mouse_position[0] <= pygame.display.Info().current_w ):
        if ( mouse_position[1] >= 200 and mouse_position[1] <= pygame.display.Info().current_h ):
            return True
    return False


# defines seed
def seed():
    print("This is the seed function")
    
    # randomly fills the world with alive and dead cells
    # TODO: create seed that randomly fills the grid with alive and dead cells


if __name__ == "__main__":
    
    # global variables
    
    # cell attributes
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = "Survival / Birth / States / Neighborhood"
    
    # place all cell attributes into a list
    ATTRIBUTES = [SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET]
    
    # indicates the number of generations
    GENERATION = 0
    
    # indicates how fast the generations progress
    SPEED = 0
    
    # indicates if the program is currently running
    RUNNING = True
    
    # call main method
    main()
