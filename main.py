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
HEIGHT = 800
NUM_TILES = 8
NUM_PIECES_PER_TEAM = 12
WHITE_TEAM = 'W'
RED_TEAM = 'R'
EMPTY_SPACE = "_"

# RGB
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128)
# GUI
FPS = 60
SIZE_OF_BOX = WIDTH // NUM_TILES
PIECE_PADDING = 20
PIECE_OUTLINE = 16
KING_CROWN = pygame.image.load("crown.png")
NEW_CROWN = pygame.transform.scale(KING_CROWN, (SIZE_OF_BOX - PIECE_PADDING - 15, SIZE_OF_BOX - PIECE_PADDING - 15))

class Board:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.grid = [[Box(row, col) for row in range(NUM_TILES)] for col in range(NUM_TILES)]
        self.initialize_board()

    def __repr__(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                print(str(self.grid[row][col].piece.team), end=" ")
            print("")
        return "\n"

    def initialize_board(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                if row < 3:
                    if row % 2 == 0 and col % 2 != 0:
                        self.grid[row][col].piece.team = WHITE_TEAM
                    if row % 2 != 0 and col % 2 == 0:
                        self.grid[row][col].piece.team = WHITE_TEAM

                if row >= NUM_TILES - 3:
                    if row % 2 == 0 and col % 2 != 0:
                        self.grid[row][col].piece.team = RED_TEAM
                    if row % 2 != 0 and col % 2 == 0:
                        self.grid[row][col].piece.team = RED_TEAM

    def draw(self, win):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                if row % 2 == 0 and col % 2 != 0 or row % 2 != 0 and col % 2 == 0:
                    pygame.draw.rect(win, BLACK, (row * SIZE_OF_BOX, col * SIZE_OF_BOX, SIZE_OF_BOX, SIZE_OF_BOX))
                    self.grid[col][row].draw(win)

    def move_piece(self, from_row, from_col, to_row, to_col):
        if self.acceptable_move(to_row, to_col):
            # Swap Pieces
            print("swapping")
            self.grid[to_row][to_col].piece, self.grid[from_row][from_col].piece = self.grid[from_row][from_col].piece, \
                                                                                   self.grid[to_row][to_col].piece

    def acceptable_move(self, row, col):
        # Validates the input is within the bounds of the board
        if row < 0 or row >= NUM_TILES:
            return False
        if col < 0 or col >= NUM_TILES:
            return False
        # Checks to see if the space is empty before moving
        if self.grid[row][col].piece.team != EMPTY_SPACE:
            return False
        return True


class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.piece = Piece(row, col, EMPTY_SPACE)

    def draw(self, win):
        piece_team = self.piece.team
        color = None
        if piece_team == EMPTY_SPACE:
            return
        elif self.piece.team == RED_TEAM:
            color = RED
        else:
            color = WHITE

        pygame.draw.ellipse(win, GREY, (self.piece.row * SIZE_OF_BOX + 8,
                                         self.piece.col * SIZE_OF_BOX + 8,
                                         SIZE_OF_BOX - PIECE_OUTLINE, SIZE_OF_BOX - PIECE_OUTLINE))

        pygame.draw.ellipse(win,color, (self.piece.row * SIZE_OF_BOX + PIECE_PADDING // 2,
                                        self.piece.col * SIZE_OF_BOX + PIECE_PADDING // 2,
                                        SIZE_OF_BOX - PIECE_PADDING, SIZE_OF_BOX- PIECE_PADDING))

        if self.piece.isKing:
            win.blit(NEW_CROWN, (self.row * SIZE_OF_BOX + 16,self.col * SIZE_OF_BOX + 12))


class Piece:
    def __init__(self, row, col, team):
        self.row = row
        self.col = col
        self.team = team
        self.isKing = False

def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    run = True
    key = None
    clock = pygame.time.Clock()
    checker_board = Board()
    print(checker_board)

    while run:
        clock.tick(FPS)
        window.fill(RED)
        checker_board.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()
    pygame.quit()
main()
