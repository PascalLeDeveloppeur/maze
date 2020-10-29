# maze

## Goal
You are MacGyver and you are locked in a maze.
You must collect all the items from the maze then reach the guard to escape.
If you reach the guard without having collected all the objects,
you lose the game. Otherwise, you win.


## How to play:

launch the game: python3 maze

move the hero: use the keyboard arrows

Quit the game (not the program): press Q key

Quit the program: press escape key or click on the cross button


## How to create a map (maze)

Create a txt file called "map1.txt". In this one, put "X" to represent the walls,
 "." for the paths, an "E" for the exit (the guard) and an "S"
 to place the hero. The items are placed randomly.
**The maze must be a rectangle !**

Put the "map1.txt" file in "assets/map"

Here an example of a "map1.txt" file:

X...XXX...XX...
X.X..E.X.X...X.
..XXXXXX.X.X...
X...X.X....XXX.
..XXX.XXX.X...S
X.XXX....XXXXX.
...X..XX.......
XX.XXX.X.XXXXXX
X..............
X.XXX...XXXX.X.
..X....X..X....
X..XXXX.....X..
...........XX.X
XX.XXXXXXXXX...
X....X.........