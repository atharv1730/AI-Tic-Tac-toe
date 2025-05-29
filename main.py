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
FONT = pygame.font.SysFont("comicsans", 60)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.marked_squares = 0

    def final_state(self, show=False):
        # vertical wins
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def is_square_empty(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        return [(row, col) for row in range(ROWS) for col in range(COLUMNS) if self.is_square_empty(row, col)]

    def is_full(self):
        return self.marked_squares == 9

    def is_empty(self):
        return self.marked_squares == 0


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_AI(self, board):
        empty_squares = board.get_empty_squares()
        return None if not empty_squares else random.choice(empty_squares)

    def minimax(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None
        elif case == 2:
            return -1, None
        elif board.is_full():
            return 0, None

        best_move = None

        if maximizing:
            max_eval = -float('inf')
            for (row, col) in board.get_empty_squares():
                temp = copy.deepcopy(board)
                temp.mark_square(row, col, 1)
                eval, _ = self.minimax(temp, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for (row, col) in board.get_empty_squares():
                temp = copy.deepcopy(board)
                temp.mark_square(row, col, self.player)
                eval, _ = self.minimax(temp, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.random_AI(main_board)
        else:
            eval, move = self.minimax(main_board, False)

        if move:
            print(f'AI has chosen to mark the square at {move} with an eval of: {eval}')
        return move


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.gamemode = 'ai'
        self.running = True
        self.player = 1
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_figure(row, col)
        self.change_player()

    def show_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    def draw_figure(self, row, col):
        if self.player == 1:
            start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        else:
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def change_player(self):
        self.player = 1 if self.player == 2 else 2

    def display_result(self, winner):
        if winner == 0:
            text = "It's a Draw!"
            
        elif winner == 1:
            text = "Player Wins!"

        else:
            text = "AI Wins!"


        label = FONT.render(text, True, (255, 0, 0))
        label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(label, label_rect)

    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai
    game.gamemode = "ai"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.is_square_empty(row, col):
                    game.make_move(row, col)
                    winner = board.final_state(show=True)
                    if winner != 0 or board.is_full():
                        game.display_result(winner)
                        game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()

        if game.gamemode == "ai" and ai.player == game.player and game.running:
            pygame.display.update()
            move = ai.eval(board)
            if move:
                row, col = move
                game.make_move(row, col)
                winner = board.final_state(show=True)
                if winner != 0 or board.is_full():
                    game.display_result(winner)
                    game.running = False

        pygame.display.update()


main()
