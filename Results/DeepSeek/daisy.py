from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    P1 = 1
    P2 = 2

class Daisy(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = Player.P1
        self.round = 1
        # Reserve counts: A-H for P1, a-h for P2
        self.reserves = {
            Player.P1: {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9},
            Player.P2: {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        }
        self.can_capture = {Player.P1: False, Player.P2: False}

    def prompt_current_player(self):
        player_str = "Player 1" if self.current_player == Player.P1 else "Player 2"
        return input(f"{player_str}'s move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        try:
            if is_placement(move):
                piece, (x, y) = get_move_elements(move)
                if self.current_player == Player.P1:
                    if piece not in self.reserves[Player.P1] or self.reserves[Player.P1][piece] <= 0:
                        return False
                else:
                    if piece not in self.reserves[Player.P2] or self.reserves[Player.P2][piece] <= 0:
                        return False
                return self.board.layout[x, y] == '_'

            elif is_movement(move):
                (x1, y1), (x2, y2) = get_move_elements(move)
                piece = self.board.layout[x1, y1]
                
                # Check if piece belongs to current player
                if (self.current_player == Player.P1 and piece.islower()) or \
                   (self.current_player == Player.P2 and piece.isupper()):
                    return False

                # Check destination
                target = self.board.layout[x2, y2]
                if target != '_' and (target.isupper() and self.current_player == Player.P1 or 
                                     target.islower() and self.current_player == Player.P2):
                    return False
                
                # Check capture permission
                if target != '_' and not self.can_capture[self.current_player]:
                    return False

                # Check piece movement rules
                dx, dy = x2 - x1, y2 - y1
                return self.is_valid_move(piece, x1, y1, dx, dy)

        except:
            return False
        return False

    def is_valid_move(self, piece, x1, y1, dx, dy):
        piece_type = piece.upper()
        if piece_type == 'A':
            return abs(dx) <= 1 and abs(dy) <= 1
        elif piece_type == 'B':
            if dx != 0 and dy != 0:
                return False
            step_x = np.sign(dx)
            step_y = np.sign(dy)
            for i in range(1, max(abs(dx), abs(dy))):
                x = x1 + i * step_x
                y = y1 + i * step_y
                if self.board.layout[x, y] != '_':
                    return False
            return True
        elif piece_type == 'C':
            if abs(dx) != abs(dy):
                return False
            step_x = np.sign(dx)
            step_y = np.sign(dy)
            for i in range(1, abs(dx)):
                x = x1 + i * step_x
                y = y1 + i * step_y
                if self.board.layout[x, y] != '_':
                    return False
            return True
        elif piece_type == 'D':
            if piece == 'D':
                return (abs(dx) == 1 and dy == 0) or (dx == -1 and abs(dy) == 1)
            else:  # d
                return (abs(dx) == 1 and dy == 0) or (dx == 1 and abs(dy) == 1)
        elif piece_type == 'E':
            if piece == 'E':
                return (abs(dx) == 1 and abs(dy) == 1) or (dx == -1 and dy == 0)
            else:  # e
                return (abs(dx) == 1 and abs(dy) == 1) or (dx == 1 and dy == 0)
        elif piece_type == 'F':
            if piece == 'F':
                return dx == -2 and abs(dy) == 1
            else:  # f
                return dx == 2 and abs(dy) == 1
        elif piece_type == 'G':
            if piece == 'G':
                return dx < 0 and dy == 0
            else:  # g
                return dx > 0 and dy == 0
        elif piece_type == 'H':
            if piece == 'H':
                return dx == -1 and dy == 0
            else:  # h
                return dx == 1 and dy == 0
        return False

    def perform_move(self, move):
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            if self.current_player == Player.P1:
                self.reserves[Player.P1][piece] -= 1
                if piece == 'A':
                    self.can_capture[Player.P1] = True
            else:
                self.reserves[Player.P2][piece] -= 1
                if piece == 'a':
                    self.can_capture[Player.P2] = True

        elif is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            target = self.board.layout[x2, y2]
            
            if target != '_':  # Capture
                captured = target
                if self.current_player == Player.P1:
                    self.reserves[Player.P1][captured.upper()] += 1
                else:
                    self.reserves[Player.P2][captured.lower()] += 1
            
            self.board.move_piece(move)

    def game_finished(self):
        # Check if A or a has been captured
        a_exists = 'a' in self.board.layout
        A_exists = 'A' in self.board.layout
        return not a_exists or not A_exists

    def get_winner(self):
        if 'a' not in self.board.layout:
            return Player.P1
        elif 'A' not in self.board.layout:
            return Player.P2
        return None

    def next_player(self):
        return Player.P2 if self.current_player == Player.P1 else Player.P1

    def finish_message(self, winner):
        if winner == Player.P1:
            print("Player 1 wins by capturing the 'a' piece!")
        else:
            print("Player 2 wins by capturing the 'A' piece!")

if __name__ == '__main__':
    board = Board((9, 9))
    game = Daisy(board)
    game.game_loop()
