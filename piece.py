from constants import *

class Piece:
    def __init__(self, team=EMPTY_SPACE):
        self.team = team
        self.isKing = False
        self.direction = 0
