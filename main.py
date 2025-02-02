import sys
import pygame
from constants import *
import numpy as np

# Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))

    def mark_square(self, row, col, player):
        self.squares[row][col] = player

    def is_square_empty(self, row, col):
        return self.squares[row][col] == 0

class Game:
    def __init__(self):
        # Console Board
        self.board = Board()
        self.player = 1
        self.show_lines()

    def show_lines(self):
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)  # screen, color, start_pos, end_pos, width
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQUARE_SIZE, 0), (WIDTH-SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQUARE_SIZE), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)


    def chnage_player(self):
        self.player = 1 if self.player == 2 else 2

def main():

    game = Game()
    board = game.board
    player = game.player
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If screen is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE   # y axis
                col = pos[0] // SQUARE_SIZE   # x axis

                if board.is_square_empty(row, col):
                    board.mark_square(row, col, player)
                    game.chnage_player()
        
        pygame.display.update()


main()
