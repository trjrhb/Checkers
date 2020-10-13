'''
The goal of this project is to create a classic game of Checkers and have an computer opponent
that will make the appropriate moves to take pieces and try to win.

Features
    - GUI that displays the board and it's pieces
    - Allow the user to control their own pieces and capture others
    - Have an 'AI' like algorithm that plays against the user
'''
import pygame

WIDTH = 800
HEIGHT = 900
NUM_TILES = 8
NUM_PIECES_PER_TEAM = 12

class Board:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.grid = [[Box(row, col) for col in range(NUM_TILES)] for row in range(NUM_TILES)]
        self.initialize_board()

    def __repr__(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                print(str(self.grid[row][col].value), end=" ")
            print("")
        return "\n"

    def initialize_board(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                if row < 3:
                    if row % 2 == 0 and col % 2 != 0:
                        self.grid[row][col].value = "W"
                    if row % 2 != 0 and col % 2 == 0:
                        self.grid[row][col].value = "W"

                if row >= NUM_TILES - 3:
                    if row % 2 == 0 and col % 2 != 0:
                        self.grid[row][col].value = "R"
                    if row % 2 != 0 and col % 2 == 0:
                        self.grid[row][col].value = "R"

class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.value = '0'

class Piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = None
        self.isKing = False


def main():
    checker_board = Board()
    print(checker_board)


main()
