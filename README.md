# Game-of-life-J.-H.-Conway

Introduction

The game of life was formulated by J. H. Conway¹ in 1970. It is a simulation of
life cycle of bacteria on a two-dimensional grid. Starting from an initial template and applying a set of simple rules, future generations of bacteria are simulated. In figure 1
a snippet of gameplay is shown. In this work, the creation is requested
of an application that will demonstrate that particular simulation.

![image](https://user-images.githubusercontent.com/115406856/221260069-3e0662b8-3b30-4e26-9dbd-40bac783fa8e.png)

Description of the problem

The game of life unfolds on an infinite two-dimensional grid of cells with each cell having
8 neighboring cells (top, bottom, left, right and diagonal). As part of the work the grid will have
finite dimensions (eg 40 × 80) and will continue from the right edge to the left edge and from
lower edge to the upper edge of the grid. The game progresses in steps and in each step:

1. Any live cell with less than 2 live neighbors dies.

2. Any live cell with 2 or 3 live neighbors survives.

3. Any live cell with more than 3 live neighbors dies.

4. Every dead cell with exactly 3 live neighbors becomes alive.

The game is started with an initial pattern which in the present work will be randomly generated giving a probability of initial activation of each cell separately (e.g. 5%). The rules
of each evolution step are applied to all cells using only the state of the grid
of the previous step.

Requests

It is requested to develop a program which for initialization values ​​that will be entered by the user
(grid dimensions, activation probability of each cell in the original grid) will display the original
grid. Then provide the following functionality:

1. If the right arrow of the keyboard is pressed to move forward one step.

2. If the up arrow of the keyboard is pressed, the automatic execution of steps will start.

3. If the down arrow of the keyboard is pressed to stop the automatic execution of steps if the
program is in auto step mode.
