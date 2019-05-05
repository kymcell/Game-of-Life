#
# CS 224 Spring 2019
# Semester Project: The Game of Life
#
# Defines the neighborhoods to be used in the game_of_life.py
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

# defines the Moore Neighborhood
def moore():
    # neighbor positions relative to the current cell centereed at [x, y] of [0, 0]
    moore_neighbors = [ [0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1] ]
    
    return moore_neighbors


# defines the Von Neumann Neighborhood
def neumann():
    # neighbor positions relative to the current cell centereed at [x, y] of [0, 0]
    neumann_neighbors = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    
    return neumann_neighbors


# defines the Engholdt Neighborhood
def engholdt():
    # neighbor positions relative to the current cell centereed at [x, y] of [0, 0]
    engholdt_neighbors = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
    
    return engholdt_neighbors