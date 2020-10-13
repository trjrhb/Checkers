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
GREY = (128, 128, 128)
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
        self.grid = [[Box(col, row) for row in range(NUM_TILES)] for col in range(NUM_TILES)]
        self.initialize_board()

    def __repr__(self):
        for col in range(NUM_TILES):
            for row in range(NUM_TILES):
                print(str(self.grid[col][row].piece.team), end=" ")
            print("")
        return "\n"

    def initialize_board(self):
        for col in range(NUM_TILES):
            for row in range(NUM_TILES):
                if col < 3:
                    if col % 2 == 0 and row % 2 != 0:
                        self.grid[col][row].piece.team = WHITE_TEAM
                    if col % 2 != 0 and row % 2 == 0:
                        self.grid[col][row].piece.team = WHITE_TEAM
                    self.grid[col][row].piece.direction = 1

                if col >= NUM_TILES - 3:
                    if col % 2 == 0 and row % 2 != 0:
                        self.grid[col][row].piece.team = RED_TEAM
                    if col % 2 != 0 and row % 2 == 0:
                        self.grid[col][row].piece.team = RED_TEAM
                    self.grid[col][row].piece.direction = -1

    def draw(self, win):
        for col in range(NUM_TILES):
            for row in range(NUM_TILES):
                if col % 2 == 0 and row % 2 != 0 or col % 2 != 0 and row % 2 == 0:
                    pygame.draw.rect(win, BLACK, (col * SIZE_OF_BOX, row * SIZE_OF_BOX, SIZE_OF_BOX, SIZE_OF_BOX))
                    self.grid[col][row].draw(win)

    def move_piece(self, from_col, from_row, to_col, to_row):
        print("From: (" + str(from_col) + ", " + str(from_row) + ")")
        print("To: (" + str(to_col) + ", " + str(to_row) + ")")
        selected_piece = self.grid[from_col][from_row].piece
        moves = self.generatePossibleMoves(self.grid[from_col][from_row])

        for possible_move in moves:
            if possible_move.col == to_col and possible_move.row == to_row:
                adj_piece = self.grid[to_col][to_row].piece
                if adj_piece.team == EMPTY_SPACE:
                    self.grid[to_col][to_row].piece, self.grid[from_col][from_row].piece = selected_piece, adj_piece
                    self.promote_to_King(selected_piece, to_col)
                    print("CURR_COL = " + str(to_col))
                else:   # Opponent's Piece is available to be jumped
                    jump_col = (to_col - from_col) * 2
                    jump_row = (to_row - from_row) * 2
                    self.grid[from_col + jump_col][from_row + jump_row].piece, self.grid[from_col][from_row].piece = selected_piece, self.grid[from_col + jump_col][from_row + jump_row].piece
                    self.delete_piece(to_col, to_row)
                    self.promote_to_King(self.grid[from_col + jump_col][from_row + jump_row].piece, from_col + jump_col)
                    print("CURR_COL = " + str(from_col + jump_col))
                    #TODO Add double jump functionality


    def generatePossibleMoves(self, box):
        piece_row = box.row
        piece_col = box.col
        surrounding_pieces = []
        piece = self.get_piece(piece_col, piece_row)

        for col in range(-1, 2, 2):
            for row in range(-1, 2, 2):
                if self.withinBounds(piece_col + col, piece_row + row):  # Empty Space
                    new_piece = self.get_piece(piece_col + col, piece_row + row)
                    adj_piece = self.grid[piece_col + col][piece_row + row]
                    if self.valid_movement_direction(piece_col, piece_col + col, piece.direction) or piece.isKing:
                        if new_piece.team == EMPTY_SPACE:
                            print(adj_piece)
                            surrounding_pieces.append(adj_piece)
                        elif piece.team != new_piece.team:  # Opponent's Piece
                            if self.jumpPossible(col, row, piece_col, piece_row):
                                print(adj_piece)
                                surrounding_pieces.append(adj_piece)
        return surrounding_pieces

    def withinBounds(self, col, row):
        # Validates the input is within the bounds of the board
        if col < 0 or col >= NUM_TILES or row < 0 or row >= NUM_TILES:
            print("Failed to pass bounds check")
            print("Col: " + str(col) + ", Row: " + str(row))
            return False
        return True

    def get_piece(self, col, row):
        return self.grid[col][row].piece

    def delete_piece(self, col, row):
        self.grid[col][row].piece.team = EMPTY_SPACE
        self.grid[col][row].piece.isKing = False
        self.grid[col][row].piece.direction = 0

    def promote_to_King(self, piece, current_col):
        print("PIECE DIR = " + str(piece.direction))
        if piece.direction == -1 and current_col == 0:
            piece.isKing = True
        elif piece.direction == 1 and current_col == NUM_TILES - 1:
            piece.isKing = True

    def valid_movement_direction(self, from_col, to_col, direction):
        if from_col + direction == to_col:
            return True
        return False

    def jumpPossible(self, col_direction, row_direction, col_location, row_location):
        if not self.withinBounds(col_location + (col_direction * 2), row_location + (row_direction * 2)):
            return False

        jump_pieces_team = self.grid[col_location + (col_direction * 2)][row_location + (row_direction * 2)].piece.team

        if jump_pieces_team == EMPTY_SPACE:
            print("CAN JUMP!")
            return True
        return False

    def determine_selection(self, mouse):
        mouse_x = mouse[1]
        mouse_y = mouse[0]
        row = mouse_x // SIZE_OF_BOX
        col = mouse_y // SIZE_OF_BOX
        return [col, row]


class Box:
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.piece = Piece()

    def __repr__(self):
        return "Col: " + str(self.col) + ", Row: " + str(self.row)

    def draw(self, win):
        color = None

        if self.piece.team == EMPTY_SPACE:
            return
        elif self.piece.team == RED_TEAM:
            color = RED
        else:
            color = WHITE

        pygame.draw.ellipse(win, GREY, (self.col * SIZE_OF_BOX + 8,
                                        self.row * SIZE_OF_BOX + 8,
                                        SIZE_OF_BOX - PIECE_OUTLINE, SIZE_OF_BOX - PIECE_OUTLINE))

        pygame.draw.ellipse(win, color, (self.col * SIZE_OF_BOX + PIECE_PADDING // 2,
                                         self.row * SIZE_OF_BOX + PIECE_PADDING // 2,
                                         SIZE_OF_BOX - PIECE_PADDING, SIZE_OF_BOX - PIECE_PADDING))

        if self.piece.isKing:
            win.blit(NEW_CROWN, (self.col * SIZE_OF_BOX + 16, self.row * SIZE_OF_BOX + 12))


class Piece:
    def __init__(self, team=EMPTY_SPACE):
        self.team = team
        self.isKing = False
        self.direction = 0


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    run = True
    key = None
    clock = pygame.time.Clock()
    checker_board = Board()
    print(checker_board)
    selection = None
    destination = None
    while run:
        clock.tick(FPS)
        window.fill(RED)
        checker_board.draw(window)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = checker_board.determine_selection(mouse)
                print(selection)
            if event.type == pygame.MOUSEBUTTONUP:
                destination = checker_board.determine_selection(mouse)
                checker_board.move_piece(selection[0], selection[1], destination[0], destination[1])

        if selection is not None:
            pygame.draw.rect(window, WHITE,
                             (selection[0] * SIZE_OF_BOX, selection[1] * SIZE_OF_BOX, SIZE_OF_BOX, SIZE_OF_BOX), 5)
        if destination is not None:
            pygame.draw.rect(window, WHITE,
                             (destination[0] * SIZE_OF_BOX, destination[1] * SIZE_OF_BOX, SIZE_OF_BOX, SIZE_OF_BOX), 5)
            selection = destination
        pygame.display.update()
    pygame.quit()


main()
