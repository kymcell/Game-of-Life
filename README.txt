#
# CS 224 Spring 2019
# Semester Project: The Game of Life
#
# There are infinite possibilities within the realm of cellular automata.
# This program seeks to emulate many of those possibilities through
# completely customizable parameters and a user friendly GUI.
#
# Authors: Kaelan Engholdt, Garrett Kern, Kyle McElligott
# Start Date: 2/25/2019
# Due Date: 5/6/2019
#

Program scripts: 'game_of_life.py', 'game_window.py', 'cell.py', 'neighborhood.py'

GENERAL INFORMATION:
    Cellular automata are fascinating models that use simple rules to produce complex systems that have many real world
    applications including simulation in biology, chemistry, and physics. A cellular automata model consists of a theoretically
    infinite 2-Dimensional grid of cells, with each cell having a finite number of states.  The state of the cell is governed
    by a ruleset, specified by the user.  For a cellular automata model to begin, it must be given a seed (a starting pattern).

WORLD:
    The game world consists of a theoretically infinite 2-Dimensional grid of orthogonal squares
    For the scope of this program, the grid has a finite limit, chosen from multiple options by the user.

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
    Survival means a cell will stay alive (active) until the next generation if it satisfies the neighborhood conditions.
    If the neighborhood conditions are not satisfied, the cell will die (deactivate).

    If a cell has exactly x neighbors, it will survive to the next generation, otherwise it dies.


BIRTH:
    Birth means a cell that is dead (deactive) will be born (activate) in the next generation if it satisfies the neighborhood conditions.
    A cell is considered a neighbor if it is within the specified neighborhood and in the alive (active) state.

    A cell is born if it has exactly x neighbors.


STATES:
    States refers to the number of states that a cell has.
    A cell can theoretically have an infinite number of states, but a limit of 14 is reasonable.

    There are x states, alive, dead, and x-2 states of decay.

    For example, if a cell has 4 states, it has the following behavior:
    0 - Dead    (Graphically, this cell is white)
    1 - Alive   (Graphically, this cell is black)
    2 - Dying   (Graphically, this cell is a color different from all previous colors)
    3 - Dying   (Graphically, this cell is a color different from all previous colors)

    After the final state of decay, the cell will die (deactivate) and return to a value of 0.

    For the purposes of birth, the states of decay (dying) are not considered to be alive.


NEIGHBORHOOD:
    The neighborhood of a cell is defined according to the type of neighborhood it is given.
    There are two main neighborhoods:
        Moore Neighborhood (M): All 8 cells surrounding the central cell both diagonally and orthogonally.
            Domain: {1,2,3,4,5,6,7,8}
        Von Neumann Neighborhood (VN): Only the 4 cells surrounding the central cell orthogonally.
            Domain: {1,2,3,4}

    An additional neighborhood has been added:
        Engholdt Neighborhood (E): Only the 4 cells surrounding the central cell diagonally.
            Domain: {1,2,3,4}

NOTE:
    A domain of 0 is allowed for the Survival value, this means that a living cell will always die in the next generation.


RUNNING THE PROGRAM:

Modules to install:

    Pygame: A Python library for creating graphics based programs and games.
    Download Page: https://www.pygame.org/download.shtml

    ThorPy: A GUI library for Pygame.
    Download Page: http://www.thorpy.org/tutorials/install.html


How to start the program:

    Windows users:
    From command line type 'python game_of_life.py' to run the program.

    Mac users:
    From command line type 'python3 game_of_life.py' to run the program.

    PyCharm users:
    Create a new project and place all files within the project. Install the required modules before starting the program.
    To run the program, click the run button on the 'game_of_life.py' file.


How to use the program:

    When the program begins, the grid consists of white space taking up a large portion of the screen. At the top of the
    screen are buttons for controlling the program, as well as a display area to show user choices. For the program to
    begin, a ruleset must be selected by clicking on the 'Ruleset' button in the upper left and choosing a ruleset.

    There are several premade rulesets that exhibit various behaviors over time. A custom ruleset may also be selected
    for the user to create their own ruleset. If this option is chosen, a 'Neighborhood' button will appear. The user
    must select the neighborhood of the ruleset first in order to define the domain for the survival and birth values.

    After a neighborhood is selected, the 'Survival', 'Birth', and 'States' buttons will appear, allowing the user to
    choose which values to use. Once a value is chosen, that value may be removed from the ruleset by selecting it again
    within its respective window.

    Once a valid ruleset is chosen, either a preset one or a custom one, the 'Seed' and 'Play' butttons will appear. The
    'Seed' button allows the user to choose a starting pattern. Currently, there are only preset seeds for the 'Conway's
    Game of Life' ruleset. All rulesets have the option to produce a random seed, which can sometimes produce interesting
    results while other times causing the population of cells to all fizzle out and die.

    Users can create their own seed by interacting with the grid, and users may also interact with the grid both while
    the game is paused or while it is currently propagating new cells. Left-clicking on cells will make them come alive,
    and each successive left-click will iterate through the number of states for that cell for the current ruleset.
    Right-clicking on any cell will instantly kill it.

    The 'Size' button allows users to specify the size of the grid, while the 'Reset' button will kill all cells in the
    current game world while keeping the current ruleset. All buttons related to the ruleset have a separate 'Information'
    button within their respective selection windows, allowing for quick reminders as to the function of each value in
    the ruleset.

    Once the user is finished utlizing the program, the program may be exited by pressing the 'ESC' key.


How the program was tested:

    This program was tested on both Mac and Windows, with Windows being the most suitable option.
    Cell neighbor creation and deaths were tested through trial and error with a number of different rulesets.

    The program was intended to run on a 1920x1080 resolution screen, and therefore the program may operate
    differently, or may be rendered inoperable, based on the screen resolution.  Given more time, a desirable
    addition to the program would be to add support for other screen resolutions.


Known bugs and problem areas:

    Non-1920x1080 Screen Resolutions:
        An "out of bounds" black bar will appear along the right and bottom sides of the computer screen,
        if clicked the program will crash (if you see the black bar just don't click it, it will not impact
        the functionality of the program otherwise).

    Mac Users:
        A black box can appear around the mouse cursor, this causes no issues other than being a visual annoyance.

    Note:
        On Mac, Python 3 is used instead of Python 2 on Windows. For whatever reason, we were unable to get Pygame to
        run on Mac using Python 2.


References:
    The following references were used in the creation of this project.

    Cellular Automata Information: http://www.mirekw.com/ca/index.html

    ThorPy GUI Documentation: http://www.thorpy.org/documentation.html
