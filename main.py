'''
The goal of this project is to create a classic game of Checkers and have an computer opponent
that will make the appropriate moves to take pieces and try to win.

Features
    - GUI that displays the board and it's pieces
    - Allow the user to control their own pieces and capture others
    - Have an 'AI' like algorithm that plays against the user
'''
import pygame
from constants import *
from board import Board

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


if __name__ == '__main__':
    main()
