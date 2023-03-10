# Challenge:
# 1. Show vector and human at the same time (about 1% of squares for each).
# 2. Move the humans to the right each tick
# 3. Build a wall on the right so the humans can't go any further and stop at the wall.

import pygame, sys
from pygame.locals import *
import random

# Number of frames per second
FPS = int(input('FPS is:'))

# define constants for humans and infected people (vectors) for more readable code
empty = 0
human = 1
vector = 2
blackSquare = 3
wall = 4
doctor = 5
Vaccinated = 6

# ****************************************************Grid Directions*********************************
UP = (0, -1)
DOWN = (0, +1)
LEFT = (-1, 0)
RIGHT = (1, 0)

##Sets size of grid
WINDOWWIDTH = int(input('WINDOWWIDTH is :'))
WINDOWHEIGHT = int(input('WINDOWHEIGHT is :'))
CELLSIZE = int(input('CELLSIZE is :'))

# Check to see if the width and height are multiples of the cell size.
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

# Determine number of cells in horizonatl and vertical plane
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)  # number of cells wide
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)  # Number of cells high

# set up the colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
Purple = (128, 0, 128)
Yellow = (255, 255, 0)


################################
# USER Functions CODE in this area
#
#
#
#
# Draws the grid lines
def drawGrid():
    # Exclude white so grid doesn't disapear
    lineColour = BLACK

    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, lineColour, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, lineColour, (0, y), (WINDOWWIDTH, y))


# Creates an dictionary index of all the cells
# Sets all cells as blank (0 = white)
# Note: The grid is actually a single straight line of values
# the illusion of a grid is achieved by knowing at which value the next line starts
def blankGrid():
    gridDict = {}
    # creates dictionary for all cells
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            gridDict[(x, y)] = 0  # Sets cells as white
    return gridDict


# Colours the cells
# we can add more rules for different colors
def colourGrid(item, world):
    (xloc, yloc) = item  # This is the grid location to colour sent in the TUPLE item.
    state = world[item]  # here we read the state from the grid location.

    # work out the coordinates to draw the rectagle so it aligns with the grid.

    y = yloc * CELLSIZE  # translates array into grid size
    x = xloc * CELLSIZE  # translates array into grid size

    #####********************** ADDED a rule for cells that contain a 1 becoming green

    if state == human:
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    if state == empty:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if state == vector:
        pygame.draw.rect(DISPLAYSURF, RED, (x, y, CELLSIZE, CELLSIZE))
    if state == blackSquare:
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, CELLSIZE,
                                              CELLSIZE))  # add new colour rule to colorGrid function we will create a blacksquare around central cell
    if state == wall:
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (x, y, CELLSIZE, CELLSIZE))
    if state == doctor:
        pygame.draw.rect(DISPLAYSURF, Yellow, (x, y, CELLSIZE, CELLSIZE))
    if state == Vaccinated:
        pygame.draw.rect(DISPLAYSURF, Purple, (x, y, CELLSIZE, CELLSIZE))
    return None


# For this function we try to change a grid location
# cell is a tuple example (4,5)
# direction is a tuple, example (-1,0)

# Test if the new position is OK.  ( 4-1, 5-0). = 3,5
# If it is OK, then return the new tuple (3,5)
# If it is not OK (hit a wall), return the original tuple (4,5)

def move(cell, direction):  #####****** NEW FUNCTION CHANGE HAPPENS HERE MOVEMENT****####
    moveTo = (cell[0] + direction[0], cell[1] + direction[1])
    if isNotWall(moveTo):  ### NOTE WALL ##
        return moveTo
    return cell


##### This is the function that moves time along
# This is where we update the contents of the grid

#### This is the function that moves time along
def tick(world):
    newTick = world.copy()

    humancount = 0
    vectorcount = 0

    # go through each item/cell in the grid
    for item in world:
        if world[item] == human:  # if human
            if 1 < getVectorNeighbours(item, world) < 4:
                newTick[item] = vector
                vectorcount += 1
            elif getVectorNeighbours(item, world) > 3:
                newTick[item] = empty

            elif getDoctorNeighbours(item, world) > 1:
                humancount += 1
                newTick[item] = empty
                newTick[returnRandomNMoveDirection(item, newTick)] = Vaccinated
            else:
                humancount += 1
                newTick[item] = empty
                newTick[returnRandomNMoveDirection(item, newTick)] = human
        elif world[item] == vector:  # if vector we want to move it
            if getDoctorNeighbours(item, world) > 1:
                humancount += 1
                newTick[item] = empty
                newTick[returnRandomNMoveDirection(item, newTick)] = Vaccinated
            elif 0 < getDoctorNeighbours(item, world) < 2:
                newTick[item] = empty
            elif getVectorNeighbours(item, world) > 7:
                newTick[item] = empty
            else:
                newTick[item] = empty  # empty current cell
                newTick[returnRandomNMoveDirection(item, newTick)] = vector  # move if we can in random direction
                vectorcount += 1
        elif world[item] == doctor:
            if 3 < getVectorNeighbours(item, world) < 6:
                newTick[item] = vector
                vectorcount += 1
            elif getVectorNeighbours(item, world) > 5:
                newTick[item] = empty
            else:
                humancount += 1
                newTick[item] = empty
                newTick[returnRandomNMoveDirection(item, newTick)] = doctor

        elif world[item] == Vaccinated:
            if 2< getVectorNeighbours(item, world) < 6:
                newTick[item] = vector
                vectorcount += 1
            elif getVectorNeighbours(item, world) > 5:
                newTick[item] = empty
            elif getDoctorNeighbours(item, world) > 4:
                newTick[item] = doctor
                humancount += 1
            else:
                humancount += 1
                newTick[item] = empty
                newTick[returnRandomNMoveDirection(item, newTick)] = Vaccinated

    if humancount == 0:
        print('vector is win !')
    if vectorcount == 0:
        print('human is win !')
    print("Human count = ", humancount, "Vector count = ", vectorcount)
    return newTick


# Generate random population                                    ######???????????????BIG CHANGE HERE WITH NEW VARIABLE????????????##
def placeRandomPerson(world, probability, person):  ######???????????????We got rid of placeRandomhumanswith new variable??????##

    for item in world:  # for every cell in world
        count = 0
        if random.uniform(0, 1) < probability:  # if a random number beween 0 and 1 is less than probability
            world[item] = person  # make the cell a creature

    return world


# is a cell inside the world                           ###???????????WE ARE GOING TO BUILD A WALL ON THE RIGHT?????????###
def isNotWall(checkCell):
    if checkCell[0] < CELLWIDTH and checkCell[0] >= 0:  # Check x locaation is within the grid
        if checkCell[1] < CELLHEIGHT and checkCell[1] >= 0:  # Check y locaation is within the grid
            return True  # This is a valid grid location
    return False  # This is not a valid grid location


# Determines how many vector neighbours there are around a cell
# This code was in tick in the previous version.
# It does a check around the cell looking for vectors
def getVectorNeighbours(item, world):
    neighbours = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            checkCell = (item[0] + x, item[1] + y)
            if isNotWall(checkCell):
                if world[checkCell] == vector:
                    neighbours += 1
                    colourGrid(item, world)
    return neighbours


def getDoctorNeighbours(item, world):
    neighbours = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            checkCell = (item[0] + x, item[1] + y)
            if isNotWall(checkCell):
                if world[checkCell] == doctor:
                    neighbours += 1
                    colourGrid(item, world)
    return neighbours


def getVaccinatedNeighbours(item, world):
    neighbours = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            checkCell = (item[0] + x, item[1] + y)
            if isNotWall(checkCell):
                if world[checkCell] == Vaccinated:
                    neighbours += 1
                    colourGrid(item, world)
    return neighbours


# NEW FUNCTION CODE BELOW
""" # We also need a function to generate a random direction

#we then use this function to move the vectors
# We also need a function to generate a random direction

"""


# selects a direction at random if it is not valid returns the static position
def returnRandomNMoveDirection(cell, nextWorld):
    x = random.randint(-1, 1)
    y = random.randint(-1, 1)
    checkCell = (cell[0] + x, cell[1] + y)
    if x == 0 and y == 0:  # didn't move, just return the initial location
        return cell
    if isValidDirection(checkCell, nextWorld):  # New function to check if new location empty
        return checkCell
    return cell


# NEW CODE BELOW
""" The isValidDirection function will take a cell and check if it is empty and not a wall. we will use the newtick world
# to check for validity that way we dont get crashes as vectors move. if we just used world two vectors might merge into the same square
# on the next tick
"""


def isValidDirection(checkCell, nextWorld):
    if isNotWall(checkCell) and nextWorld[checkCell] == empty:
        return True
    else:
        return False


# main function
def main():
    #    Part 1 - setup the py game defaults.

    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Grid example')

    # background color
    DISPLAYSURF.fill(WHITE)

    #    Part 2 - Populate the world by creating and populating the dictionary.

    # This is where our people will live: this is the world
    world = blankGrid()  # creates dictionary and populates the grid with empty spaces
    world = placeRandomPerson(world, 0.2, human)  # Assign random humans
    world = placeRandomPerson(world, 0.02, vector)  # Assign random humans    ##NOTE THIS CHANGE HERE###
    world = placeRandomPerson(world, 0.075, wall)
    world = placeRandomPerson(world, 0.01, doctor)

    #    Part 3 - Draw the grid and the contents of the grid and display it
    # Colours the cells in the grid at the start of each simulation all will be blank/White for this simulation
    for item in world:
        colourGrid(item, world)

    # draw to the screen the created blank grid
    drawGrid()
    pygame.display.update()

    done = False
    #    Part 4 - loop through the program. This is controlled by the Frames Per second FPS variable

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

                # Part 4.1 Update the dictionary that describes the world with any changes we want to make
        world = tick(world)

        # Part 4.2 Colour grid based on the updates we made to the dictionary
        for item in world:
            colourGrid(item, world)
            # draw the grid on the display
        drawGrid()

        # Part 4.3 Show the new display on the screen
        pygame.display.update()

        # Part 4.4. Wait for the next tick to pass before continuing. The FPS controls the speed of the game
        FPSCLOCK.tick(FPS)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()
