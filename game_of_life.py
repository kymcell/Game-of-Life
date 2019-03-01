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
    2, 3 / 3 / 2 / M
    
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
from random import *


# main method
def main():
    print "This is the main method"
    
    random_ruleset()
    
    print SURVIVAL
    print BIRTH
    print STATES
    print NEIGHBORHOOD
    print RULESET


'''
RULESETS
'''

# user chooses which ruleset will be used
def rules():
    
    user = 1  # user determined ruleset
    
    if user == 1:
        conway()


# Conway's Game of Life Ruleset: 2, 3 / 3 / 2 / M
def conway():
    
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET
    
    # set globals
    SURVIVAL = [2,3]
    BIRTH = [3]
    STATES = range(2)
    NEIGHBORHOOD = "M"
    RULESET = "2, 3 / 3 / 2 / M"


# Brian's Brain Ruleset: 0 / 2 / 3 / M
def brian():
    
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET
    
    # set globals
    SURVIVAL = [0]
    BIRTH = [2]
    STATES = range(3)
    NEIGHBORHOOD = "M"
    RULESET = "0 / 2 / 3 / M"


# generates random values for Survival / Birth / States / Neighboorhood
def random_ruleset():
    
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET
    
    # randomly pick the neighborhood
    option = randint(0,1)
    if (option == 0):
        NEIGHBORHOOD = "M"
    if (option == 1):
        NEIGHBORHOOD = "VN"
    
    # randomly pick SURVIVAL values
    if (NEIGHBORHOOD == "M"):
        upper_bound = 8
    if (NEIGHBORHOOD == "VN"):
        upper_bound = 4
    num_survival = randint(1,upper_bound)
    i = 0
    neighbors = randint(0, upper_bound)
    if (neighbors == 0):
        SURVIVAL.append(neighbors)
        i = num_survival
    while (i < num_survival):
        neighbors = randint(1,upper_bound)
        if (neighbors not in SURVIVAL):
            SURVIVAL.append(neighbors)
            i += 1
    
    # randomly pick BIRTH values
    if (NEIGHBORHOOD == "M"):
        upper_bound = 8
    if (NEIGHBORHOOD == "VN"):
        upper_bound = 4
    num_birth = randint(1,upper_bound)
    i=0
    while (i < num_birth):
        neighbors = randint(1,upper_bound)
        if (neighbors not in BIRTH):
            BIRTH.append(neighbors)
            i += 1
    
    # randomly pick STATES values
    option = randint(2,10)
    STATES = range(option)
    
    # generate RULESET
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(option) + " / " + NEIGHBORHOOD).replace("[", "").replace("]", "")


# user defines all values for Survival / Birth / States / Neighboorhood
def custom():
    print "This is a custom ruleset"
    # user must define Neighborhood first to decide domain of Survival and Birth

    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET


'''
NEIGHBORHOOD
'''

# Moore Neighborhood
def moore():
    print "This is the Moore Neighborhood"


# Von Neumann Neighborhood
def neumann():
    print "This is the Von Neumann Neighborhood"


'''
GUI
'''

# user defines seed
def seed():
    print "This is the seed function"


# randomly fills the world with alive and dead cells
def seed_random():
    print "This is the random seed"


# creates GUI
def world():
    print "This is the world function"


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
