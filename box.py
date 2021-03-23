import pygame
from constants import *
from piece import Piece

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
