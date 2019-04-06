#
# CS 224 Spring 2019
# Semester Project
#
# Defines the neighborhoods to be used in the game_of_life.py
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

'''
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

# defines the Moore Neighborhood
def moore():
    # neighbor positions relative to the current cell centereed at [x, y] of [0, 0]
    moore_neighbors = [ [0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, 1] ]
    
    # defines domain available for the number of neighbors in the Moore Neighborhood
    moore_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    return moore_neighbors, moore_domain


# defines the Von Neumann Neighborhood
def neumann():
    # neighbor positions relative to the current cell centereed at [x, y] of [0, 0]
    neumann_neighbors = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]

    # defines domain available for the number of neighbors in the Von Neumann Neighborhood
    neumann_domain = [0, 1, 2, 3, 4]
    
    return neumann_neighbors, neumann_domain