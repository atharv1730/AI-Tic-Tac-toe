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
        self.empty_squares = self.squares
        self.marked_squares = 0

    def final_state(self):
        # Vertical win
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col] 
            
        # Horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
            
        # Ascending diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]
        
        # Descending diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player

    def is_square_empty(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.is_square_empty(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0

class AI:
    pass

class Game:
    def __init__(self):
        # Console Board
        self.board = Board()
        # self.ai = AI()
        self.gamemode = 'pvp' # PvP or AI
        self.running = True
        self.player = 1
        self.show_lines()

    def show_lines(self):
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)  # screen, color, start_pos, end_pos, width
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQUARE_SIZE, 0), (WIDTH-SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQUARE_SIZE), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)

    def draw_figure(self, row, col):
        if self.player == 1:
            # Draw an X
            # Descending diagonal
            start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE) # x, y
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE) # x, y
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH) # screen, color, start_pos, end_pos, width
            
            # Ascending diagonal
            start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE) # x, y
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE) # x, y
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        else:
            # Draw an O
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2) # x, y
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def change_player(self):
        self.player = 1 if self.player == 2 else 2

def main():

    game = Game()
    board = game.board
    
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
                    board.mark_square(row, col, game.player)
                    game.draw_figure(row, col)
                    game.change_player()
        
        pygame.display.update()


main()
