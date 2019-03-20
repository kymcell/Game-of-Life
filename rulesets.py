#
# CS 224 Spring 2019
# Semester Project
#
# Defines the rulesets to be used in the game_of_life.py
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

'''
RULESETS:
    Rulesets are named using the following format:
    Survival / Birth / States / Neighboorhood
    
    For example, Conway's Game of Life has the following ruleset:
    [2, 3] / [3] / 2 / M
    
    If a cell has exactly 2 or 3 neighbors, it will survive to the next generation, otherwise it dies
    A cell is born if it has exactly 3 neighbors
    There are 2 states, alive and dead
    Utilizes the Moore neighborhood
'''

# imports
from random import *


# Conway's Game of Life Ruleset: [2, 3] / [3] / 2 / M
def conway():
    # define rules
    SURVIVAL = [2, 3]
    BIRTH = [3]
    STATES = range(2)
    NEIGHBORHOOD = "M"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # return rules
    return SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET


# Brian's Brain Ruleset: [0] / [2] / 3 / M
def brian():
    # define rules
    SURVIVAL = [0]
    BIRTH = [2]
    STATES = range(3)
    NEIGHBORHOOD = "M"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # return rules
    return SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET


# generates random values for Survival / Birth / States / Neighboorhood
def random_ruleset():
    # define rules
    SURVIVAL = []
    BIRTH = []
    
    # randomly pick the neighborhood
    option = randint(0, 1)
    if (option == 0):
        NEIGHBORHOOD = "M"
    if (option == 1):
        NEIGHBORHOOD = "VN"
    
    # randomly pick SURVIVAL values
    if (NEIGHBORHOOD == "M"):
        upper_bound = 8
    if (NEIGHBORHOOD == "VN"):
        upper_bound = 4
    num_survival = randint(1, upper_bound)
    i = 0
    neighbors = randint(0, upper_bound)
    if (neighbors == 0):
        SURVIVAL.append(neighbors)
        i = num_survival
    while (i < num_survival):
        neighbors = randint(1, upper_bound)
        if (neighbors not in SURVIVAL):
            SURVIVAL.append(neighbors)
            i += 1
    
    # randomly pick BIRTH values
    if (NEIGHBORHOOD == "M"):
        upper_bound = 8
    if (NEIGHBORHOOD == "VN"):
        upper_bound = 4
    num_birth = randint(1, upper_bound)
    i = 0
    while (i < num_birth):
        neighbors = randint(1, upper_bound)
        if (neighbors not in BIRTH):
            BIRTH.append(neighbors)
            i += 1
    
    # randomly pick STATES values
    STATES = range(randint(2,10))
    
    # generate RULESET
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # return rules
    return SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET


# TODO: User choices must be passed as parameters to the custom function
# user defines all values for Survival / Birth / States / Neighboorhood
def custom():
    # user must define Neighborhood first to decide domain of Survival and Birth
    # code for user input
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # return rules
    return SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET
