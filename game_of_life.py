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

    Thorpy GUI Information:
    http://www.thorpy.org/documentation.html
'''

# imports
import thorpy
from random import *
from time import *

from game_window import *


'''
________________________________________________________________________________________________________________________
                                                MAIN METHOD
________________________________________________________________________________________________________________________
'''

# main method
def main():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES
    
    # initialize pygame
    pygame.init()
    
    # create fullscreen window
    world()


'''
________________________________________________________________________________________________________________________
                                        Graphical User Interface (GUI)
________________________________________________________________________________________________________________________
'''

# creates game window and grid of cells
def world():
    # import globals
    global RUNNING, MENU
    
    # set size of the bar containing the buttons on the top of the screen
    y_offset = 200
    
    # create fullscreen window
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # set RGB color for background
    window.fill((200, 200, 200))
    
    # create window to hold actual game and create the grid
    life_window = game_window(window, 0, y_offset, ATTRIBUTES)
    
    # set window title
    pygame.display.set_caption("Game of Life")
    
    # Thorpy GUI Elements
    # __________________________________________________________________________________________________________________
    # set theme of all thorpy elements
    thorpy.set_theme("human")
    
    # button for selecting which ruleset to use
    ruleset_button = thorpy.make_button("Ruleset", func=rules)

    # button for selecting which seed to use
    seed_button = thorpy.make_button("Seed")
    
    # spacing button that will never be used
    spacing_button_01 = thorpy.make_button("Space")
    
    # button for selecting survival value
    survival_button = thorpy.make_button("Survival")
    
    # button for selecting birth value
    birth_button = thorpy.make_button("Birth")
    
    # button for selecting the number of states each cell has
    states_button = thorpy.make_button("States")

    # button for selecting which neighborhood the cells will use
    neighborhood_button = thorpy.make_button("Neighborhood")

    # spacing button that will never be used
    spacing_button_02 = thorpy.make_button("Space")
    
    # button for selecting how fast the generations will iterate
    speed_button = thorpy.make_button("Speed")

    # button for selecting how large the grid of cells will be
    size_button = thorpy.make_button("Size")
    
    # button for starting and stopping the generations from iterating
    start_button = thorpy.make_button("Play/Pause")
    
    # button for clearing the grid (kills all cells)
    reset_button = thorpy.make_button("Reset")
    
    # list to hold buttons that will be hidden
    hidden_buttons_list = [seed_button,
                           spacing_button_01,
                           survival_button,
                           birth_button,
                           states_button,
                           neighborhood_button,
                           spacing_button_02,]
    
    # hide the buttons in the hidden buttons list
    for button in hidden_buttons_list:
        button.set_visible(False)
        button.set_active(False)
    
    # set the current application
    thorpy.application._CURRENT_APPLICATION = game_window
    
    # create box to hold elements
    box = thorpy.BarBox(elements=[ruleset_button,
                                  seed_button,
                                  spacing_button_01,
                                  survival_button,
                                  birth_button,
                                  states_button,
                                  neighborhood_button,
                                  spacing_button_02,
                                  speed_button,
                                  size_button,
                                  start_button,
                                  reset_button] )

    # set the box to fit the elements
    box.fit_children(margins=(30, 30))

    # set box color and opacity
    box.set_main_color((220, 220, 220, 100))
    
    # labels that will display the global variables
    name_label = thorpy.make_text(NAME)
    survival_label = thorpy.make_text("Survival: " + str(RULESET))
    birth_label = thorpy.make_text("Birth: " + str(RULESET))
    states_label = thorpy.make_text("States: " + str(RULESET))
    neighborhood_label = thorpy.make_text("Nieghborhood: " + str(RULESET))
    ruleset_label = thorpy.make_text("Ruleset: " + str(RULESET))
    
    # list that holds all the labels
    label_list = [name_label, survival_label, birth_label, states_label, neighborhood_label, ruleset_label]
    
    # create another box that will only display selected information
    display_box = thorpy.Box(elements=[name_label,
                                       survival_label,
                                       birth_label,
                                       states_label,
                                       neighborhood_label,
                                       ruleset_label])

    # set the display box to fit the elements
    display_box.fit_children(margins=(30, 30))
    
    # set the position of the display box
    display_box.set_topleft((1000, 0))
    display_box.blit()
    display_box.update()
    
    # set the menu
    MENU = thorpy.Menu(box)
    thorpy.functions.set_current_menu(MENU)

    # set the surface to be used
    for element in MENU.get_population():
        element.surface = window
    
    # set the position of the box
    box.set_topleft((100, 50))
    box.blit()
    box.update()
    # __________________________________________________________________________________________________________________
    
    # while the program is running, continue updating the window
    while RUNNING:
        user_input(life_window, y_offset)
        display(life_window)
        update(life_window, display_box, label_list)
        pygame.display.update()
    pygame.quit()


# displays the window
def display(life_window):
    game_window.display(life_window)


# updates the game_window
def update(life_window, display_box, label_list):
    # update labels
    label_list[0].set_text(NAME)
    label_list[1].set_text("Survival: " + str(SURVIVAL))
    label_list[2].set_text("Birth: " + str(BIRTH))
    label_list[3].set_text("States: " + str(STATES))
    label_list[4].set_text("Neighborhood: " + str(NEIGHBORHOOD))
    label_list[5].set_text("Ruleset: " + str(RULESET))
    # TODO: Fix label alignment within the display box
    # update display_box
    display_box.blit()
    display_box.update()
    
    # update game_window
    game_window.update(life_window)


# determines when the user clicks the mouse or presses the ESC key to exit the program
def user_input(life_window, y_offset):
    # import globals
    global RUNNING
    
    # determines if the program should end
    for event in pygame.event.get():
        # thorpy elements will react to events
        MENU.react(event)
        
        # program will end if the window is closed
        if event.type == pygame.QUIT:
            RUNNING = False
        
        # detects when the left mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # gets the current mouse position
            mouse_position = pygame.mouse.get_pos()
            
            # determines when the cell should be activated once clicked
            if mouse_in_grid(mouse_position, y_offset):
                game_window.activate_cell(life_window, mouse_position)
        
        # detects when the right mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # gets the current mouse position
            mouse_position = pygame.mouse.get_pos()
            
            # determines when the cell should be killed once clicked
            if mouse_in_grid(mouse_position, y_offset):
                game_window.kill_cell(life_window, mouse_position)
        
        # program will end if the ESC key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False


# checks if the mouse is hovering above the grid
def mouse_in_grid(mouse_position, y_offset):
    # returns true if the mouse is hovering above the grid, otherwise false
    if (mouse_position[0] >= 0 and mouse_position[0] <= pygame.display.Info().current_w):
        if (mouse_position[1] >= y_offset and mouse_position[1] <= pygame.display.Info().current_h):
            return True
    return False


'''
________________________________________________________________________________________________________________________
                                                    RULESETS
________________________________________________________________________________________________________________________
'''

# user chooses which ruleset will be used
def rules():
    # list of choices
    choices = [("Conway's Game of Life", conway),
               ("Brian's Brain", brian),
               ("Custom", custom),
               ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select a ruleset to be used:\n", choices)


# Conway's Game of Life Ruleset: [2, 3] / [3] / 2 / M
def conway():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES, NAME
    
    # set name
    NAME = "Conway's Game of Life"
    
    # define rules
    SURVIVAL = [2, 3]
    BIRTH = [3]
    STATES = range(2)
    NEIGHBORHOOD = "M"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)


# Brian's Brain Ruleset: [0] / [2] / 3 / M
def brian():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES, NAME
    
    # set name
    NAME = "Brian's Brain"
    
    # define rules
    SURVIVAL = [0]
    BIRTH = [2]
    STATES = range(3)
    NEIGHBORHOOD = "M"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)


# generates random values for Survival / Birth / States / Neighboorhood
def random_ruleset():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES, NAME
    
    # set name
    NAME = "Random Ruleset"
    
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
    STATES = range(randint(2, 10))
    
    # generate RULESET
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)


# TODO: User choices must be passed as parameters to the custom function
# user defines all values for Survival / Birth / States / Neighboorhood
def custom():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES, NAME
    
    # user must define Neighborhood first to decide domain of Survival and Birth
    # code for user input
    # set name
    NAME = "Custom Ruleset"
    
    # set cell attributes
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "Neighborhood"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)


'''
________________________________________________________________________________________________________________________
                                            SEEDS (Starting Patterns)
________________________________________________________________________________________________________________________
'''

# user chooses which seed will be used
def seed():
    pass

# randomly fills the world with alive and dead cells
# TODO: create seed that randomly fills the grid with alive and dead cells


'''
________________________________________________________________________________________________________________________
                                            OTHER BUTTON FUNCTIONS
________________________________________________________________________________________________________________________
'''

# kills all cells
def reset():
    # call the game_window function to kill the cells
    pass

'''
________________________________________________________________________________________________________________________
                                                START OF PROGRAM
________________________________________________________________________________________________________________________
'''

if __name__ == "__main__":
    
    # global variables
    
    # name of ruleset
    NAME = "Name"
    
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
    
    # menu to be called from thorpy functions
    MENU = None
    
    # call main method
    main()
