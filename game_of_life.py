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
    Survival / Birth / States / Neighboorhood
    
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
    
    A cell is born if it has exactly x neighboors


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
        Moore Neighboorhood (M): All 8 cells surrounding the central cell both diagonally and orthogonally
            Domain: {1,2,3,4,5,6,7,8}
        Von Neumann Neighborhood (VN): Only the 4 cells surrounding the central cell orthogonally
            Domain: {1,2,3,4}

NOTE:
    A domain of 0 is allowed for the Survival value, this means that a living cell will always die in the next generation

REFERENCES:
www.mirekw.com/ca/index.html
'''

# imports
from rulesets import *
from neighborhood import *
from Tkinter import *
from random import *
from time import *
from cell import *


# main method
def main():
    
    SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET = random_ruleset()
    
    print SURVIVAL
    print BIRTH
    print STATES
    print NEIGHBORHOOD
    print RULESET
    
    world()


'''
RULES
'''

# user chooses which ruleset will be used
def rules():
    user = 1  # user determined ruleset
    
    if user == 1:
        conway()


'''
GUI
'''

# user defines seed
def seed():
    print "This is the seed function"


# randomly fills the world with alive and dead cells
def seed_random():
    print "This is the random seed"


'''
Tkinter Colors:
http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
'''
# creates grid
def world():
    # create window
    window = Tk()
    
    # rows and columns for grid
    cols = 80
    rows = 40
    
    # create 2D list of cell objects, passing appropriate parameters
    grid_list = [cell(SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, window) for i in range(cols) for j in range(rows)]
    
    # create grid
    for i in range(rows):
        for j in range(cols):
            grid_list[i][j].grid(row=i, col=j)
    
    # display window
    window.mainloop()


'''
MAIN
'''

if __name__ == "__main__":
    
    # global variables
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = "Survival / Birth / States / Neighborhood"
    
    GENERATION = 0
    SPEED = 0
    
    main()
