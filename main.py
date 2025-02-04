import sys
import pygame
from constants import *
import numpy as np
import random
import copy

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
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
        self.marked_squares += 1

    def is_square_empty(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = [(row, col) for row in range(ROWS) for col in range(COLUMNS) if self.is_square_empty(row, col)]
        return empty_squares

    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0


class AI:
    def __init__(self, level=1, player=2):  # Level 0: Random AI, Level 1: Minimax AI
        self.level = level
        self.player = player

    def random_AI(self, board):
        empty_squares = board.get_empty_squares()
        if not empty_squares:  # Check if the board is full
            return None
        return random.choice(empty_squares)  # Choose a random move safely
    

    def minimax(self, board, maximizing):
        # Terminal state
        case = board.final_state()
        
        # If player wins
        if case == 1:
            return 1, None
        
        # If AI wins
        elif case == 2:
            return -1, None
        
        # If it's a draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100 # Can be anything more than 1
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
            
        else:
            min_eval = 100 # Can be anything more than 1
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random_AI(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col



class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.gamemode = 'ai'  # PvP or AI
        self.running = True
        self.player = 1
        self.show_lines()

    def show_lines(self):
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def draw_figure(self, row, col):
        if self.player == 1:
            # Draw X
            start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        else:
            # Draw O
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def change_player(self):
        self.player = 1 if self.player == 2 else 2


def main():
    game = Game()
    board = game.board
    ai = game.ai
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If screen is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE  # y-axis
                col = pos[0] // SQUARE_SIZE  # x-axis

                if board.is_square_empty(row, col):
                    board.mark_square(row, col, game.player)
                    game.draw_figure(row, col)
                    game.change_player()

        if game.gamemode == "ai" and ai.player == game.player:
            pygame.display.update()

            move = ai.eval(board)
            if move != (-1, -1):  # Ensure AI has a move to make
                row, col = move
                board.mark_square(row, col, ai.player)
                game.draw_figure(row, col)
                game.change_player()

        pygame.display.update()


main()
