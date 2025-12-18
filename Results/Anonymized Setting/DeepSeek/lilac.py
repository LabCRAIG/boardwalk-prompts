from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    V = 1  # Player 1 controls V's
    A = 2  # Player 2 controls A's and Â

class Lilac(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = Player.V  # Player 1 starts
        self.centroid = (3, 3)  # Center position for Â

    def prompt_current_player(self):
        player_name = "Player 1 (V)" if self.current_player == Player.V else "Player 2 (A/Â)"
        return input(f"{player_name}'s move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            
            # Check if moving own piece
            piece = self.board.layout[from_row, from_col]
            if (self.current_player == Player.V and piece != 'V') or \
               (self.current_player == Player.A and piece not in ['A', 'Â']):
                return False

            # Check if moving orthogonally one space
            if not ((abs(from_row - to_row) == 1 and from_col == to_col) or 
                    (abs(from_col - to_col) == 1 and from_row == to_row)):
                return False

            # Check destination is blank
            if self.board.layout[to_row, to_col] != '_':
                return False

            # Special rule for Â - can only be in center unless moving out
            if piece == 'Â' and (from_row, from_col) == self.centroid:
                return True  # Allowed to move out
            elif piece == 'Â' and (from_row, from_col) != self.centroid:
                return False  # Can't move back in

            return True

        return False  # Only movements allowed in this game

    def perform_move(self, move):
        (from_row, from_col), (to_row, to_col) = get_move_elements(move)
        moving_piece = self.board.layout[from_row, from_col]
        
        # Move the piece
        self.board.move_piece(move)
        
        # Check for captures
        self.check_captures(to_row, to_col)
        
        # Check if Â moved to border (Player 2 win condition)
        if moving_piece == 'Â' and (to_row in (0, 6) or to_col in (0, 6)):
            return

    def check_captures(self, row, col):
        # Check all four orthogonal directions for sandwiches
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row - dr, col - dc
            
            # Check if positions are within bounds
            if 0 <= r1 < 7 and 0 <= c1 < 7 and 0 <= r2 < 7 and 0 <= c2 < 7:
                p1 = self.board.layout[r1, c1]
                p2 = self.board.layout[r2, c2]
                middle = self.board.layout[row, col]
                
                # Check sandwich condition
                if (p1 == 'V' and p2 == 'V' and middle in ['A', 'Â']) or \
                   (p1 in ['A', 'Â'] and p2 in ['A', 'Â'] and middle == 'V'):
                    self.board.layout[row, col] = '_'  # Capture the piece

    def game_finished(self):
        # Check if Â was captured (Player 1 wins)
        if 'Â' not in self.board.layout:
            return True
            
        # Check if Â reached border (Player 2 wins)
        for i in range(7):
            if (self.board.layout[0, i] == 'Â' or self.board.layout[6, i] == 'Â' or
                self.board.layout[i, 0] == 'Â' or self.board.layout[i, 6] == 'Â'):
                return True
                
        return False

    def get_winner(self):
        # Player 1 wins if Â was captured
        if 'Â' not in self.board.layout:
            return Player.V
            
        # Player 2 wins if Â reached border
        for i in range(7):
            if (self.board.layout[0, i] == 'Â' or self.board.layout[6, i] == 'Â' or
                self.board.layout[i, 0] == 'Â' or self.board.layout[i, 6] == 'Â'):
                return Player.A
                
        return None

    def next_player(self):
        return Player.A if self.current_player == Player.V else Player.V

    def finish_message(self, winner):
        if winner == Player.V:
            print("Player 1 (V) wins by capturing the Â!")
        else:
            print("Player 2 (A) wins by moving the Â to the border!")

if __name__ == '__main__':
    initial_layout = (
        "__VVV__\n"
        "___V___\n"
        "V_AAA_V\n"
        "VVAÂAVV\n"
        "V_AAA_V\n"
        "___V___\n"
        "__VVV__"
    )
    board = Board((7, 7), initial_layout)
    game = Lilac(board)
    game.game_loop()