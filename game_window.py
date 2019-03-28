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
    For our purposes the grid will have a finite limit, chosen from 3 options by the user
        Large: X x X squares
        Medium: Y x Y squares
        Small: Z x Z squares
'''

# imports
import pygame
from cell import *

class game_window():
    # constructor
    def __init__(self, screen, x_offset, y_offset, ATTRIBUTES):
        # iniitialize screen
        self.screen = screen
        
        # position game_window
        vector = pygame.math.Vector2
        self.pos = vector(x_offset, y_offset)
        
        # get screen resolution
        resolution = pygame.display.Info()
        
        # set width and height
        self.width = resolution.current_w
        self.height = resolution.current_h - y_offset
        
        # set surface where the grid will be placed and the game of life will be played
        self.image = pygame.Surface( (self.width, self.height) )
        self.rect = self.image.get_rect()
        
        # set rows and columns
        cols = 48
        rows = cols * self.height / self.width
        
        # get cell_width
        cell_width = self.width / cols
        
        # create grid of cell objects
        self.grid = [ [cell(self.image, i, j, cell_width, ATTRIBUTES) for i in range(cols) ] for j in range(rows) ]
    
    
    def display(self):
        # set RGB color for background
        self.image.fill( (0, 0, 0) )
        
        # call cell display
        for row in self.grid:
            for cell in row:
                cell.display()
        
        # display game_window
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
    
    def update(self):
        # set top left corner as reference
        self.rect.topleft = self.pos
        
        # call cell update
        for row in self.grid:
            for cell in row:
                cell.update()
