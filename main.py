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
        print(self.squares)


class Game:
    def __init__(self):
        # Console Board
        self.board = Board()
        self.show_lines()

    def show_lines(self):
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)  # screen, color, start_pos, end_pos, width
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQUARE_SIZE, 0), (WIDTH-SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQUARE_SIZE), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)

def main():

    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()


main()
