# MazeSolver

This is a python implementation of solving mazes, utilizing pygame and what I learned when building the application for Conway's Game of Life. It implements the same idea of using `sprites` to represent each cell of our matrix/grid. 

In general a:

* Green Cell: Start cell
* Red Cell: Target cell
* Grey Cell: Wall cell
* White Cell: Visited cell

Where the keybinds for the game are:
* **s** : Places start node at mouse position
* **e** : Places target node at mouse position
* **LEFT CLICK**: While user holds left-click down, places walls continuously at mouse position until released
* **RIGHT CLICK**: While uesr holds right-click down, removes walls continuously at mouse position until released
* **BACKSPACE**: resets board to a empty board
* **d**: Performs depth first search
* **b**: Performs breadth first search

Below displays an example populated grid and depth-first search performed on the same grid:

!(img/maze1.png?raw=true)

!(img/solved_maze1.png?raw=true)

 
