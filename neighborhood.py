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

# Moore Neighborhood
def moore():
    print "This is the Moore Neighborhood"


# Von Neumann Neighborhood
def neumann():
    print "This is the Von Neumann Neighborhood"