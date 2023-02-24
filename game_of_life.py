import pygame
from pygame import draw
from pygame import Rect as rect
import pygame.freetype
import sys
import random
import copy
import argparse
import os
import tkinter as Tk
from tkinter import *


black = 0, 0, 0
# Get the number of living neighbors for a cell
def neighbors(squares, i, j):
    n = 0
    if i - 1 >= 0 and j - 1 >= 0 and squares[i - 1][j - 1]:
        n += 1

    if j - 1 >= 0 and squares[i][j - 1]:
        n += 1

    if i + 1 < len(squares) and j - 1 >= 0 and squares[i + 1][j - 1]:
        n += 1

    if i + 1 < len(squares) and squares[i + 1][j]:
        n += 1

    if i + 1 < len(squares) and j + 1 < len(squares[0]) and squares[i + 1][j + 1]:
        n += 1

    if j + 1 < len(squares[0]) and squares[i][j + 1]:
        n += 1

    if i - 1 >= 0 and j + 1 < len(squares[0]) and squares[i - 1][j + 1]:
        n += 1

    if i - 1 >= 0 and squares[i - 1][j]:
        n += 1

    return n



# Process game of life rules
def process(squares):
    new_squares = copy.deepcopy(squares)
    for i in range(len(squares)):
        for j in range(len(squares[0])):
            num_neighbors = neighbors(squares, i, j)
            if squares[i][j] == True and num_neighbors != 2 and num_neighbors != 3:
                new_squares[i][j] = False
            if num_neighbors == 3 and not squares[i][j]:
                new_squares[i][j] = True
    return new_squares


# Kill all squares
def clear_squares():
    for i in range(len(squares)):
        for j in range(len(squares[0])):
            squares[i][j] = False


# Assign random living squares
def random_squares(spawn_rate):
    for i in range(len(squares)):
        for j in range(len(squares[0])):
            squares[i][j] = not bool(random.randint(0, spawn_rate))

#show controls
root = Tk()
w = Label(root, text='controls\n'
                     'UP: Play\n'
                     'DOWN:Pause\n'
                     's: quick save\n'
                     'l:Load\n'
                     'RIGHT: Next frame\n'
                     'r: Randomize squeres\n'
                     '+ : increase speed\n'
                     '- : decrease speed\n'
                     't: toggle gridline\n'
                     'q or esc : exit the qame\n'
                     'lmb: add cell\n'
                     'rmb: remove cell\n'
                     'to move to the next part close the window and place the width and height\n')
w.pack()
root.mainloop()




# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--scale", type=int,
                    help="amount of pixels to equal one cell; will impact performance if set too low (default: 20)")
parser.add_argument("--window",
                    help="size of window based on number of pixels, using the format WxH, e.g. 500x1000 (default: 1000x1000)")
parser.add_argument("--size",
                    help="size of window based on number of cells, using the format XxY, e.g. 20x40 (auto-calculates width & height based on scale provided, or default)")
parser.add_argument("--framerate", type=int, help="maximum framerate (default: 60)")
parser.add_argument("--unlimited_framerate", action="store_true", help="disable framerate limiting")
parser.add_argument("--file", help="load cells from file")
args = parser.parse_args()

scale = args.scale or 20
# input for height and width
width = int(input("Enter width: "))
height = int(input("Enter height: "))
framerate = args.framerate or 60
unlimited_framerate = args.unlimited_framerate

pygame.init()

caption_init = "Conway's Game of Life - "
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Set width and height based on specified size
if args.window:
    width = int(args.window.split("x")[0])
    height = int(args.window.split("x")[1])


# Verify width and height are divisible by the scale factor
if width % scale or height % scale:
    sys.exit("Width and/or height are not divisible by the scale factor")

# Set width and height based on specified number of cells in x and y
if args.size:
    width = int(args.size.split("x")[0]) * scale
    height = int(args.size.split("x")[1]) * scale

# Process loading file parameters
if args.file:
    with open(args.file, "r") as f:
        file_lines = f.readlines()

    file_arguments = file_lines[0].split("|")
    scale = int(file_arguments[0])
    width = int(file_arguments[1])
    height = int(file_arguments[2])

    file_lines = file_lines[1:]

black = 0, 0, 0
white = 255, 255, 255
gray = 200, 200, 200
darkgray = 50, 50, 50

# Number of cells in the x and y directions
num_x = int(width / scale)
num_y = int(height / scale)
# Squares for the quick save
saved_squares = [[0] * num_y for _ in range(num_x)]
# Game state
squares = [[0] * num_y for _ in range(num_x)]




# Define the screen surface
screen = pygame.display.set_mode((width, height))


# Game variables
simulate = False
speed = 1
frame = 30
gridlines = True

# Main loop processed each frame
while True:
    frame += 30


    # Process keydown events
    for event in pygame.event.get():

        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            # Play
            if event.key == pygame.K_UP:
                simulate = not simulate
            #pause
            if event.key == pygame.K_DOWN:
                simulate = not simulate
            # increase speed
            if event.unicode == "+":
                speed = 2 * speed

            # decrease speed
            if event.unicode == "-":
                if speed > 1:
                    speed = speed / 2
                else:
                    speed = 1
             # Quick save
            if event.key == pygame.K_s:
                saved_squares = copy.deepcopy(squares)

            # Quick load
            if event.key == pygame.K_l:
                squares = copy.deepcopy(saved_squares)

            # Clear squares
            if event.key == pygame.K_e:
                clear_squares()

            # Random squares
            if event.key == pygame.K_r:
                random_squares(5)

            # Toggle gridlines
            if event.key == pygame.K_t:
                gridlines = not gridlines



            # Next frame
            if event.key == pygame.K_RIGHT:
                squares = process(squares)



            # Quit
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                sys.exit()

    # Get current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Add cell when left clicked
    if pygame.mouse.get_pressed()[0]:
        i = int(mouse_pos[0] / scale)
        j = int(mouse_pos[1] / scale)
        squares[i][j] = True

    # Remove cell when right clicked
    if pygame.mouse.get_pressed()[2]:
        i = int(mouse_pos[0] / scale)
        j = int(mouse_pos[1] / scale)
        squares[i][j] = False

    screen.fill(white)

    # Draw gridlines
    if gridlines:
        for i in range(len(squares) + 1):
            draw.line(screen, gray, (i * scale, 0), (i * scale, height))
        for i in range(len(squares[0]) + 1):
            draw.line(screen, gray, (0, i * scale), (width, i * scale))

    # Draw squares
    for i in range(len(squares)):
        for j in range(len(squares[0])):
            if squares[i][j]:
                draw.rect(screen, black, rect(i * scale, j * scale, scale, scale))

    # Process game of life rules
    if simulate:
        if frame % speed == 0:
            squares = process(squares)

    # Update title bar with game stats
    caption = caption_init + "Speed: 1/%d, FPS: %.0f, %s" % (
    speed, clock.get_fps(), "Playing" if simulate else "Paused")
    pygame.display.set_caption(caption)

    # Highlight selected cell
    if not simulate:
        i = int(mouse_pos[0] / scale)
        j = int(mouse_pos[1] / scale)
        if squares[i][j]:
            draw.rect(screen, darkgray,
                      rect(int(mouse_pos[0] / scale) * scale, int(mouse_pos[1] / scale) * scale, scale, scale))
        else:
            draw.rect(screen, gray,
                      rect(int(mouse_pos[0] / scale) * scale, int(mouse_pos[1] / scale) * scale, scale, scale))

    # Limit to framerate
    if unlimited_framerate:
        clock.tick()
    else:
        clock.tick(framerate)

    # Render screen
    pygame.display.flip()
