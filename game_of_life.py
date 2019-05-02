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
    For our purposes the grid will have a finite limit, chosen from multiple options by the user

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
from game_window import *


'''
________________________________________________________________________________________________________________________
                                                MAIN METHOD
________________________________________________________________________________________________________________________
'''

# main method
def main():
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
    global RUNNING, FPS, PAUSED, MENU, \
        life_window, box, survival_button, birth_button, states_button, neighborhood_button, start_button, \
        ruleset_selected, survival_selected, birth_selected, states_selected, neighborhood_selected
    
    # set clock
    clock = pygame.time.Clock()
    
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
    seed_button = thorpy.make_button("Seed", func=seed)
    
    # spacing button that will never be used
    spacing_button_01 = thorpy.make_button("Space")
    
    # button for selecting survival value
    survival_button = thorpy.make_button("Survival", func=survival)
    
    # button for selecting birth value
    birth_button = thorpy.make_button("Birth", func=birth)
    
    # button for selecting the number of states each cell has
    states_button = thorpy.make_button("States", func=states)

    # button for selecting which neighborhood the cells will use
    neighborhood_button = thorpy.make_button("Neighborhood", func=neighborhood)

    # spacing button that will never be used
    spacing_button_02 = thorpy.make_button("Space")

    # button for selecting how large the grid of cells will be
    size_button = thorpy.make_button("Size", func=size)
    
    # button for starting and stopping propagation of cells
    start_button = thorpy.make_button(" Play ", func=play_pause)
    
    # set start button color
    start_button.set_font_color( (0, 0, 255) )
    
    # button for clearing the grid (kills all cells)
    reset_button = thorpy.make_button("Reset", func=reset)
    
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
                                  size_button,
                                  start_button,
                                  reset_button] )

    # set the box to fit the elements
    box.fit_children(margins=(30, 30))

    # set box color and opacity
    box.set_main_color((220, 220, 220, 100))
    
    # labels that will display the global variables
    name_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    survival_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    birth_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    states_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    neighborhood_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    ruleset_label = thorpy.make_text("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    
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

    # get screen resolution
    resolution = pygame.display.Info()

    # set width and height
    width = resolution.current_w
    height = resolution.current_h
    
    # set the position of the display box
    display_box.set_topleft((width / 2, y_offset / 20))
    display_box.blit()
    display_box.update()
    
    # set the menu
    MENU = thorpy.Menu(box)
    thorpy.functions.set_current_menu(MENU)

    # set the surface to be used
    for element in MENU.get_population():
        element.surface = window
    
    # set the position of the box
    box.set_topleft((width / 20, y_offset / 4))
    box.blit()
    box.blit()
    box.blit()
    box.blit()
    box.update()
    # __________________________________________________________________________________________________________________
    
    # while the program is running, continue updating the window (this is the main loop)
    while RUNNING:
        user_input(y_offset)
        if survival_selected and birth_selected and states_selected and neighborhood_selected:
            ruleset_selected = True
        else:
            ruleset_selected = False
        if ruleset_selected == True:
            start_button.set_visible(True)
            start_button.set_active(True)
        else:
            start_button.set_visible(False)
            start_button.set_visible(False)
        if PAUSED == True:
            paused_display()
            paused_update(display_box, label_list)
        if PAUSED == False:
            display()
            update(display_box, label_list)
        pygame.display.update()
        clock.tick(FPS)
        box.blit()
        box.update()
    pygame.quit()


# runs when the game is paused
def paused_display():
    # import globals
    global life_window
    
    game_window.display(life_window)


# runs when the game is paused
def paused_update(display_box, label_list):
    # import globals
    global life_window, SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES
    
    # update ruleset
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # update labels
    label_list[0].set_text(NAME)
    label_list[1].set_text("Survival: " + str(SURVIVAL))
    label_list[2].set_text("Birth: " + str(BIRTH))
    label_list[3].set_text("States: " + str(STATES))
    label_list[4].set_text("Neighborhood: " + str(NEIGHBORHOOD))
    label_list[5].set_text("Ruleset: " + str(RULESET))
    
    # update display_box
    display_box.blit()
    display_box.update()
    
    # update attribute list
    ATTRIBUTES = [SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET]
    
    # update game_window
    game_window.update(life_window, ATTRIBUTES)


# displays the window
def display():
    # import globals
    global life_window
    
    game_window.display(life_window)


# updates the game_window
def update(display_box, label_list):
    # import globals
    global life_window, SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET, ATTRIBUTES
    
    # update ruleset
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # update labels
    label_list[0].set_text(NAME)
    label_list[1].set_text("Survival: " + str(SURVIVAL))
    label_list[2].set_text("Birth: " + str(BIRTH))
    label_list[3].set_text("States: " + str(STATES))
    label_list[4].set_text("Neighborhood: " + str(NEIGHBORHOOD))
    label_list[5].set_text("Ruleset: " + str(RULESET))
    
    # update display_box
    display_box.blit()
    display_box.update()
    
    # update attribute list
    ATTRIBUTES = [SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET]
    
    # update game_window
    game_window.update(life_window, ATTRIBUTES)
    game_window.evaluate(life_window)


# determines when the user clicks the mouse or presses the ESC key to exit the program
def user_input(y_offset):
    # import globals
    global RUNNING, life_window
    
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
    # pause propagation
    pause()
    
    # list of choices
    choices = [("Conway's Game of Life", conway),
               ("Brian's Brain", brian),
               ("Custom", custom),
               ("Information", ruleset_info),
               ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select a ruleset to be used:\n", choices)

def ruleset_info():
    # launch info window
    thorpy.launch_nonblocking_alert("RULESETS:\n",
                                 "Rulesets are named using the following format:\n" +
                                 "Survival / Birth / States / Neighborhood\n\n" +
                                 "For example, Conway's Game of Life has the following ruleset:\n" +
                                 "[2, 3] / [3] / 2 / M\n\n" +
                                 "If a cell has exactly 2 or 3 neighbors, it will survive to\n" +
                                 "the next generation, otherwise it dies.\n" +
                                 "A cell is born if it has exactly 3 neighbors.\n" +
                                 "There are 2 states, alive and dead.\n" +
                                 "Utilizes the Moore neighborhood.\n")


# Conway's Game of Life Ruleset: [2, 3] / [3] / 2 / M
def conway():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, NAME, \
        survival_button, birth_button, states_button, neighborhood_button, \
        survival_selected, birth_selected, states_selected, neighborhood_selected
    
    # set name
    NAME = "Conway's Game of Life"
    
    # define rules
    SURVIVAL = [2, 3]
    BIRTH = [3]
    STATES = range(2)
    NEIGHBORHOOD = "M"

    # find the new neighbors
    life_window.neighbor_finder(NEIGHBORHOOD)

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

    # set global booleans
    survival_selected = True
    birth_selected = True
    states_selected = True
    neighborhood_selected = True
    
    # make list of buttons to be inactive
    inactive_list = [neighborhood_button, survival_button, birth_button, states_button]

    # make other buttons inactive
    for button in inactive_list:
        button.set_active(False)
        button.set_visible(False)
        button.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.update()


# Brian's Brain Ruleset: [0] / [2] / 3 / M
def brian():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, NAME, \
        survival_button, birth_button, states_button, neighborhood_button, \
        survival_selected, birth_selected, states_selected, neighborhood_selected
    
    # set name
    NAME = "Brian's Brain"
    
    # define rules
    SURVIVAL = [0]
    BIRTH = [2]
    STATES = range(3)
    NEIGHBORHOOD = "M"
    
    # find the new neighbors
    life_window.neighbor_finder(NEIGHBORHOOD)
    
    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

    # set global booleans
    survival_selected = True
    birth_selected = True
    states_selected = True
    neighborhood_selected = True
    
    # make list of buttons to be inactive
    inactive_list = [neighborhood_button, survival_button, birth_button, states_button]
    
    # make other buttons inactive
    for button in inactive_list:
        button.set_active(False)
        button.set_visible(False)
        button.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.update()


# generates random values for Survival / Birth / States / Neighboorhood
def random_ruleset():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, NAME, \
        survival_button, birth_button, states_button, neighborhood_button, \
        survival_selected, birth_selected, states_selected, neighborhood_selected
    
    # set name
    NAME = "Random Ruleset"

    # find the new neighbors
    life_window.neighbor_finder(NEIGHBORHOOD)
    
    # randomly pick the neighborhood
    option = randint(0, 1)
    if (option == 0):
        NEIGHBORHOOD = "M"
    if (option == 1):
        NEIGHBORHOOD = "VN"
    
    # holds upper bound
    upper_bound = 0
    
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

    # make list of buttons to be inactive
    inactive_list = [neighborhood_button, survival_button, birth_button, states_button]

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

    # set global booleans
    survival_selected = True
    birth_selected = True
    states_selected = True
    neighborhood_selected = True

    # make other buttons inactive
    for button in inactive_list:
        button.set_active(False)
        button.set_visible(False)
        button.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.update()


# user defines all values for Survival / Birth / States / Neighboorhood
def custom():
    # import globals
    global SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, NAME, \
        box, survival_button, birth_button, states_button, neighborhood_button, \
        survival_selected, birth_selected, states_selected, neighborhood_selected
    
    # set name
    NAME = "Custom Ruleset"
    
    # set global booleans
    survival_selected = False
    birth_selected = False
    states_selected = False
    neighborhood_selected = False
    
    # set cell attributes
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "None"
    
    # make neighborhood button active
    neighborhood_button.set_visible(True)
    neighborhood_button.set_active(True)
    neighborhood_button.blit()
    
    # reset cells
    reset()
    
    # make list of buttons to be inactive
    inactive_list = [survival_button, birth_button, states_button]
    
    # make other buttons inactive
    for button in inactive_list:
        button.set_active(False)
        button.set_visible(False)
        button.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.blit()
        box.update()


'''
________________________________________________________________________________________________________________________
                                            SEEDS (Starting Patterns)
________________________________________________________________________________________________________________________
'''

# user chooses which seed will be used
def seed():
    # pause propagation
    pause()
    
    # TODO: Finish this function and other choices


# randomly fills the world with alive and dead cells
def seed_random():
    pass # TODO: Delete this line and finish the function


'''
________________________________________________________________________________________________________________________
                                                 SURVIVAL
________________________________________________________________________________________________________________________
'''

# user chooses survival values to be used
def survival():
    # import globals
    global NEIGHBORHOOD

    # pause propagation
    pause()
    
    # list of choices
    choices = []
    
    # set choices for Moore neighborhood
    if NEIGHBORHOOD == "M":
        # list of choices
        choices = [(" 0 ", sur_0),
                   (" 1 ", sur_1),
                   (" 2 ", sur_2),
                   (" 3 ", sur_3),
                   (" 4 ", sur_4),
                   (" 5 ", sur_5),
                   (" 6 ", sur_6),
                   (" 7 ", sur_7),
                   (" 8 ", sur_8),
                   ("Information", survival_info),
                   ("Cancel", None)]
    
    # set choices for Von Neumann neighborhood
    if NEIGHBORHOOD == "VN":
        # list of choices
        choices = [(" 0 ", sur_0),
                   (" 1 ", sur_1),
                   (" 2 ", sur_2),
                   (" 3 ", sur_3),
                   (" 4 ", sur_4),
                   ("Information", survival_info),
                   ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select survival values to be added or removed:\n", choices)


def survival_info():
    # launch info window
    thorpy.launch_nonblocking_alert("SURVIVAL:\n",
                                    "Survival means a cell will stay alive (active) until the next\n" +
                                    "generation if it satisfies the neighborhood conditions.\n" +
                                    "If the neighborhood conditions are not satisfied, the cell\n" +
                                    "will die (deactivate).\n\n" +
                                    "If a cell has exactly x neighbors, it will survive to\n" +
                                    "the next generation, otherwise it dies.\n\n" +
                                    "Note:\n" +
                                    "A domain of 0 is allowed for the Survival value, this means\n" +
                                    "that a living cell will always die in the next generation.")


# survival functions
# ______________________________________________________________________________________________________________________
# adds or removes survival value of 0
def sur_0():
    # import globals
    global SURVIVAL, survival_selected

    # boolean indicating if the value has been removed
    removed = False
    
    # set global boolean
    survival_selected = True
    
    # removes 0 if it is present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
        removed = True

    # adds 0 if it is not present
    if 0 not in SURVIVAL and removed == False:
        SURVIVAL = []
        SURVIVAL.append(0)

# adds or removes survival value of 1
def sur_1():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 1 if it is present
    if 1 in SURVIVAL:
        SURVIVAL.remove(1)
        removed = True
    
    # adds 1 if it is not present
    if 1 not in SURVIVAL and removed == False:
        SURVIVAL.append(1)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 2
def sur_2():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 2 if it is present
    if 2 in SURVIVAL:
        SURVIVAL.remove(2)
        removed = True
    
    # adds 2 if it is not present
    if 2 not in SURVIVAL and removed == False:
        SURVIVAL.append(2)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 3
def sur_3():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 3 if it is present
    if 3 in SURVIVAL:
        SURVIVAL.remove(3)
        removed = True
    
    # adds 3 if it is not present
    if 3 not in SURVIVAL and removed == False:
        SURVIVAL.append(3)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 4
def sur_4():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 4 if it is present
    if 4 in SURVIVAL:
        SURVIVAL.remove(4)
        removed = True
    
    # adds 4 if it is not present
    if 4 not in SURVIVAL and removed == False:
        SURVIVAL.append(4)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 5
def sur_5():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 5 if it is present
    if 5 in SURVIVAL:
        SURVIVAL.remove(5)
        removed = True
    
    # adds 5 if it is not present
    if 5 not in SURVIVAL and removed == False:
        SURVIVAL.append(5)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 6
def sur_6():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 6 if it is present
    if 6 in SURVIVAL:
        SURVIVAL.remove(6)
        removed = True
    
    # adds 6 if it is not present
    if 6 not in SURVIVAL and removed == False:
        SURVIVAL.append(6)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 7
def sur_7():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 7 if it is present
    if 7 in SURVIVAL:
        SURVIVAL.remove(7)
        removed = True
    
    # adds 7 if it is not present
    if 7 not in SURVIVAL and removed == False:
        SURVIVAL.append(7)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# adds or removes survival value of 8
def sur_8():
    # import globals
    global SURVIVAL, survival_selected
    
    # boolean indicating if the value has been removed
    removed = False
    
    # set global boolean
    survival_selected = True
    
    # removes 0 once other numbers are present
    if 0 in SURVIVAL:
        SURVIVAL.remove(0)
    
    # removes 8 if it is present
    if 8 in SURVIVAL:
        SURVIVAL.remove(8)
        removed = True
    
    # adds 8 if it is not present
    if 8 not in SURVIVAL and removed == False:
        SURVIVAL.append(8)
    
    # sorts the list in ascending order
    SURVIVAL.sort()

# ______________________________________________________________________________________________________________________


'''
________________________________________________________________________________________________________________________
                                                  BIRTH
________________________________________________________________________________________________________________________
'''

# user chooses birth values to be used
def birth():
    # import globals
    global NEIGHBORHOOD

    # pause propagation
    pause()
    
    # list of choices
    choices = []
    
    # set choices for Moore neighborhood
    if NEIGHBORHOOD == "M":
        # list of choices
        choices = [(" 1 ", bir_1),
                   (" 2 ", bir_2),
                   (" 3 ", bir_3),
                   (" 4 ", bir_4),
                   (" 5 ", bir_5),
                   (" 6 ", bir_6),
                   (" 7 ", bir_7),
                   (" 8 ", bir_8),
                   ("Information", birth_info),
                   ("Cancel", None)]
    
    # set choices for Von Neumann neighborhood
    if NEIGHBORHOOD == "VN":
        # list of choices
        choices = [(" 1 ", bir_1),
                   (" 2 ", bir_2),
                   (" 3 ", bir_3),
                   (" 4 ", bir_4),
                   ("Information", birth_info),
                   ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select birth values to be added or removed:\n", choices)


def birth_info():
    # launch info window
    thorpy.launch_nonblocking_alert("BIRTH:\n",
                                    "Birth means a cell that is dead (deactive) will be born (activate)\n" +
                                    "in the next generation if it satisfies the neighborhood conditions.\n" +
                                    "A cell is considered a neighbor if it is within the specified\n" +
                                    "neighborhood and in the alive (active) state.\n\n" +
                                    "A cell is born if it has exactly x neighbors.")


# birth functions
# ______________________________________________________________________________________________________________________
# adds or removes birth value of 1
def bir_1():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 1 if it is present
    if 1 in BIRTH:
        BIRTH.remove(1)
        removed = True
    
    # adds 1 if it is not present
    if 1 not in BIRTH and removed == False:
        BIRTH.append(1)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 2
def bir_2():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 2 if it is present
    if 2 in BIRTH:
        BIRTH.remove(2)
        removed = True
    
    # adds 2 if it is not present
    if 2 not in BIRTH and removed == False:
        BIRTH.append(2)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 3
def bir_3():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 3 if it is present
    if 3 in BIRTH:
        BIRTH.remove(3)
        removed = True
    
    # adds 3 if it is not present
    if 3 not in BIRTH and removed == False:
        BIRTH.append(3)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 4
def bir_4():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 4 if it is present
    if 4 in BIRTH:
        BIRTH.remove(4)
        removed = True
    
    # adds 4 if it is not present
    if 4 not in BIRTH and removed == False:
        BIRTH.append(4)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 5
def bir_5():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 5 if it is present
    if 5 in BIRTH:
        BIRTH.remove(5)
        removed = True
    
    # adds 5 if it is not present
    if 5 not in BIRTH and removed == False:
        BIRTH.append(5)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 6
def bir_6():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 6 if it is present
    if 6 in BIRTH:
        BIRTH.remove(6)
        removed = True
    
    # adds 6 if it is not present
    if 6 not in BIRTH and removed == False:
        BIRTH.append(6)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 7
def bir_7():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 7 if it is present
    if 7 in BIRTH:
        BIRTH.remove(7)
        removed = True
    
    # adds 7 if it is not present
    if 7 not in BIRTH and removed == False:
        BIRTH.append(7)
    
    # sorts the list in ascending order
    BIRTH.sort()

# adds or removes birth value of 8
def bir_8():
    # import globals
    global BIRTH, birth_selected
    
    # boolean indicating if the value has been removed
    removed = False

    # set global boolean
    birth_selected = True
    
    # removes 0 once other numbers are present
    if 0 in BIRTH:
        BIRTH.remove(0)
    
    # removes 8 if it is present
    if 8 in BIRTH:
        BIRTH.remove(8)
        removed = True
    
    # adds 8 if it is not present
    if 8 not in BIRTH and removed == False:
        BIRTH.append(8)
    
    # sorts the list in ascending order
    BIRTH.sort()

# ______________________________________________________________________________________________________________________


'''
________________________________________________________________________________________________________________________
                                                  STATES
________________________________________________________________________________________________________________________
'''

# user chooses how many states each cell will have
def states():
    # pause propagation
    pause()
    
    # list of choices
    choices = [(" 2 ", sta_2),
               (" 3 ", sta_3),
               (" 4 ", sta_4),
               (" 5 ", sta_5),
               (" 6 ", sta_6),
               (" 7 ", sta_7),
               (" 8 ", sta_8),
               (" 9 ", sta_9),
               ("10", sta_10),
               ("Information", states_info),
               ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select how many states each cell will have:\n", choices)


def states_info():
    # launch info window
    thorpy.launch_nonblocking_alert("STATES:\n",
                                    "States refers to the number of states that a cell has.\n" +
                                    "A cell can theoretically have an infinite number of states.\n\n" +
                                    "There are x states, alive, dead, and x-2 states of decay.\n\n" +
                                    "For example, if a cell has 4 states, it has the following behavior:\n" +
                                    "0 - Dead    (Graphically, this cell is white)\n" +
                                    "1 - Alive   (Graphically, this cell is black)\n" +
                                    "2 - Dying   (Graphically, this cell is a unique color)\n" +
                                    "3 - Dying   (Graphically, this cell is a unique color)\n\n" +
                                    "After the final state of decay, the cell will die (deactivate)\n" +
                                    "and return to a value of 0.\n\n" +
                                    "For the purposes of birth, the states of decay (dying) are not\n" +
                                    "considered to be alive.")


# state functions
# ______________________________________________________________________________________________________________________
# sets the number of states to 2
def sta_2():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(2)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 3
def sta_3():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(3)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 4
def sta_4():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(4)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 5
def sta_5():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(5)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 6
def sta_6():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(6)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 7
def sta_7():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(7)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 8
def sta_8():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(8)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 9
def sta_9():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(9)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# sets the number of states to 10
def sta_10():
    # import globals
    global STATES, states_selected
    
    # set states value
    STATES = range(10)

    # set global boolean
    states_selected = True

    # kill cells that are not part of the current ruleset
    life_window.equalize(STATES)

# ______________________________________________________________________________________________________________________


'''
________________________________________________________________________________________________________________________
                                               NEIGHBORHOOD
________________________________________________________________________________________________________________________
'''

# user chooses neighborhood
def neighborhood():
    # pause propagation
    pause()
    
    # list of choices
    choices = [("Moore Neighborhood (M)", moore_neighborhood),
               ("Von Neumann Neighborhood (VN)", neumann_neighborhood),
               ("Information", neighborhood_info),
               ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select a neighborhood to be used by the cells:\n", choices)


def neighborhood_info():
    # launch info window
    thorpy.launch_nonblocking_alert("NEIGHBORHOOD:\n",
                                    "The neighborhood of a cell is defined according to the type of\n" +
                                    "neighborhood it is given.\n\n" +
                                    "There are two main neighborhoods:\n\n" +
                                    "Moore Neighborhood (M): All 8 cells surrounding the central cell\n" +
                                    "both diagonally and orthogonally.\n\n" +
                                    "Von Neumann Neighborhood (VN): Only the 4 cells surrounding the\n" +
                                    "central cell orthogonally.")


def moore_neighborhood():
    # import globals
    global life_window, neighborhood_selected, NEIGHBORHOOD, survival_button, birth_button, states_button
    
    # set neighborhood
    NEIGHBORHOOD = "M"

    # set global boolean
    neighborhood_selected = True
    
    # find the new neighbors
    life_window.neighbor_finder(NEIGHBORHOOD)
    
    # make list of buttons to be active
    active_list = [survival_button, birth_button, states_button]
    
    # make other buttons active
    for button in active_list:
        button.set_visible(True)
        button.set_active(True)
        button.blit()


def neumann_neighborhood():
    # import globals
    global life_window, neighborhood_selected, SURVIVAL, BIRTH, NEIGHBORHOOD, survival_button, birth_button, states_button
    
    # set neighborhood
    NEIGHBORHOOD = "VN"
    
    # set global boolean
    neighborhood_selected = True
    
    # define invalid domain values
    invalid_domain = [5,6,7,8]
    
    # remove invalid domain values from SURVIVAL and BIRTH
    for value in invalid_domain:
        if value in SURVIVAL:
            SURVIVAL.remove(value)
        if value in BIRTH:
            BIRTH.remove(value)

    # find the new neighbors
    life_window.neighbor_finder(NEIGHBORHOOD)
    
    # make list of buttons to be active
    active_list = [survival_button, birth_button, states_button]
    
    # make other buttons active
    for button in active_list:
        button.set_visible(True)
        button.set_active(True)
        button.blit()


'''
________________________________________________________________________________________________________________________
                                            OTHER BUTTON FUNCTIONS
________________________________________________________________________________________________________________________
'''

# user chooses how large the grid of cells will be
def size():
    # import globals
    global life_window
    
    # pause propagation
    pause()
    
    # list of choices
    choices = [("48", col_48),
               ("96", col_96),
               ("120", col_120),
               ("192", col_192),
               ("240", col_240),
               ("Cancel", None)]
    
    # launches choice window
    thorpy.launch_blocking_choices("Select a number of columns for the grid:\n", choices)


# column functions
# ______________________________________________________________________________________________________________________
# resizes the grid to 48 columns
def col_48():
    life_window.resize(48)

# resizes the grid to 96 columns
def col_96():
    life_window.resize(96)

# resizes the grid to 120 columns
def col_120():
    life_window.resize(120)

# resizes the grid to 192 columns
def col_192():
    life_window.resize(192)

# resizes the grid to 240 columns
def col_240():
    life_window.resize(240)

# ______________________________________________________________________________________________________________________


# user may pause and play the propagation of generations
def play_pause():
    # import globals
    global PAUSED, start_button, box
    
    # switch paused global
    PAUSED = not PAUSED
    
    # switch text on button
    if PAUSED == True:
        start_button.set_text("Play")
        start_button.set_font_color( (0, 0, 255) )
    if PAUSED == False:
        start_button.set_text("Pause")
        start_button.set_font_color( (255, 0, 0) )
    
    # blit button to screen
    box.blit()

# pause propagation
def pause():
    # import globals
    global PAUSED
    
    # set paused global
    PAUSED = True

    # switch text on button
    if PAUSED == True:
        start_button.set_text("Play")
        start_button.set_font_color( (0, 0, 255) )

    # blit button to screen
    box.blit()

# kills all cells
def reset():
    # import globals
    global life_window
    
    # call the life_window reset function
    life_window.reset()


'''
________________________________________________________________________________________________________________________
                                                START OF PROGRAM
________________________________________________________________________________________________________________________
'''

if __name__ == "__main__":
    
    # global variables
    
    # name of ruleset
    NAME = "Please select a ruleset."
    
    # cell attributes
    SURVIVAL = []
    BIRTH = []
    STATES = []
    NEIGHBORHOOD = "None"
    RULESET = (str(SURVIVAL) + " / " + str(BIRTH) + " / " + str(len(STATES)) + " / " + NEIGHBORHOOD)
    
    # place all cell attributes into a list
    ATTRIBUTES = [SURVIVAL, BIRTH, STATES, NEIGHBORHOOD, RULESET]
    
    # indicates how fast the generations progress
    FPS = 60
    
    # indicates if the program is currently running
    RUNNING = True
    
    # indicates if the program is paused
    PAUSED = True
    
    # menu to be called from thorpy functions
    MENU = None
    
    # window holding the grid
    life_window = None
    
    # box holding the buttons
    box = None
    
    # global buttons
    survival_button = None
    birth_button = None
    states_button = None
    neighborhood_button = None
    start_button = None
    
    # global booleans
    ruleset_selected = False
    survival_selected = False
    birth_selected = False
    states_selected = False
    neighborhood_selected = False
    
    # call main method
    main()
