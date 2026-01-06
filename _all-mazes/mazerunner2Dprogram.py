import tkinter as tk
import sys
import os

# -------- Maze Constants --------
WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'

PLAYER = '@'
BLOCK = '░'

# -------- Ask User for Maze File --------
while True:
    print("Enter the filename of the maze (or LIST or QUIT):")
    filename = input("> ")

    # LIST all maze files
    if filename.upper() == "LIST":
        print("Maze files found in", os.getcwd())
        for file in os.listdir():
            if file.startswith("maze") and file.endswith(".txt"):
                print(" ", file)
        continue

    # QUIT program
    if filename.upper() == "QUIT":
        sys.exit()

    # Check if file exists
    if os.path.exists(filename):
        break

    print("There is no file named", filename)

# -------- Maze Storage --------
maze = {}
playerx = None
playery = None
exitx = None
exity = None

# -------- Read Maze File --------
file = open(filename)
lines = file.readlines()

y = 0
for line in lines:
    WIDTH = len(line.rstrip())
    for x, ch in enumerate(line.rstrip()):
        if ch == START:
            playerx = x
            playery = y
            maze[(x, y)] = EMPTY
        elif ch == EXIT:
            exitx = x
            exity = y
            maze[(x, y)] = EMPTY
        else:
            maze[(x, y)] = ch
    y += 1

HEIGHT = y

# -------- Tkinter Window --------
root = tk.Tk()
root.title("Maze Runner")

maze_label = tk.Label(root, font=("Courier", 16), justify="left")
maze_label.pack()

info = tk.Label(root, text="Use W A S D keys to move")
info.pack()

# -------- Display Maze --------
def displayMaze():
    output = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == (playerx, playery):
                output += PLAYER
            elif (x, y) == (exitx, exity):
                output += 'X'
            elif maze[(x, y)] == WALL:
                output += BLOCK
            else:
                output += ' '
        output += "\n"
    maze_label.config(text=output)

# -------- Movement Logic --------
def move_player(move):
    global playerx, playery

    if move == 'W' and maze[(playerx, playery - 1)] != EMPTY:
        return
    if move == 'S' and maze[(playerx, playery + 1)] != EMPTY:
        return
    if move == 'A' and maze[(playerx - 1, playery)] != EMPTY:
        return
    if move == 'D' and maze[(playerx + 1, playery)] != EMPTY:
        return

    while True:
        if move == 'W':
            playery -= 1
            if maze[(playerx, playery - 1)] == WALL:
                break
            if maze[(playerx - 1, playery)] == EMPTY or maze[(playerx + 1, playery)] == EMPTY:
                break

        elif move == 'S':
            playery += 1
            if maze[(playerx, playery + 1)] == WALL:
                break
            if maze[(playerx - 1, playery)] == EMPTY or maze[(playerx + 1, playery)] == EMPTY:
                break

        elif move == 'A':
            playerx -= 1
            if maze[(playerx - 1, playery)] == WALL:
                break
            if maze[(playerx, playery - 1)] == EMPTY or maze[(playerx, playery + 1)] == EMPTY:
                break

        elif move == 'D':
            playerx += 1
            if maze[(playerx + 1, playery)] == WALL:
                break
            if maze[(playerx, playery - 1)] == EMPTY or maze[(playerx, playery + 1)] == EMPTY:
                break

        if (playerx, playery) == (exitx, exity):
            break

    displayMaze()

    if (playerx, playery) == (exitx, exity):
        maze_label.config(text="YOU REACHED THE EXIT!")
        root.after(2000, root.destroy)

# -------- Keyboard Input --------
def key_press(event):
    key = event.char.upper()
    if key in ['W', 'A', 'S', 'D']:
        move_player(key)

root.bind("<Key>", key_press)

displayMaze()
root.mainloop()
