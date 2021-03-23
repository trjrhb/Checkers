
# Board
WIDTH = 800
HEIGHT = 800
NUM_TILES = 8
NUM_PIECES_PER_TEAM = 12
WHITE_TEAM = 'W'
RED_TEAM = 'R'
EMPTY_SPACE = "_"

# RGB color codes
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# GUI
FPS = 60
SIZE_OF_BOX = WIDTH // NUM_TILES
PIECE_PADDING = 20
PIECE_OUTLINE = 16

# King's Crown Overlay Image
import pygame
KING_CROWN = pygame.image.load("crown.png")
NEW_CROWN = pygame.transform.scale(KING_CROWN, (SIZE_OF_BOX - PIECE_PADDING - 15, SIZE_OF_BOX - PIECE_PADDING - 15))