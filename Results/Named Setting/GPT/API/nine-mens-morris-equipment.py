
from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        self.phase = 1  # Phase 1: Placement; Phase 2: Movement
        self.pieces = {0: 9, 1: 9}  # Pieces left to place for each player
        self.captured = {0: 0, 1: 0}  # Pieces captured by each player

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if self.phase == 1:  # Placement phase
            if not is_placement(move):
                return False
            piece, (row, col) = get_move_elements(move)
            if piece != 'X' and piece != 'O':  # Ensure valid piece type
                return False
            if self.board.layout[row, col] != '_':  # Ensure the space is blank
                return False
            return True
        elif self.phase == 2:  # Movement phase
            if not is_movement(move):
                return False
            (start_row, start_col), (end_row, end_col) = get_move_elements(move)
            if self.board.layout[start_row, start_col] not in ('X', 'O'):
                return False  # Ensure the piece at the start position is valid
            if self.board.layout[end_row, end_col] != '_':
                return False  # Ensure the destination is blank
            if not self.is_adjacent((start_row, start_col), (end_row, end_col)):
                return False  # Ensure the move is to an adjacent position
            return True

    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces[self.current_player] -= 1
            if self.check_mill(row, col, piece):
                self.capture_piece()
            if sum(self.pieces.values()) == 0:
                self.phase = 2  # Transition to the movement phase
        elif is_movement(move):
            (start_row, start_col), (end_row, end_col) = get_move_elements(move)
            self.board.move_piece(move)
            if self.check_mill(end_row, end_col, self.board.layout[end_row, end_col]):
                self.capture_piece()

    def game_finished(self):
        return any(self.captured[player] >= 7 for player in [0, 1])

    def get_winner(self):
        for player in [0, 1]:
            if self.captured[player] >= 7:
                return 1 - player
        return None

    def check_mill(self, row, col, piece):
        # Check rows, columns, and diagonals for a mill (three in a row)
        directions = [
            [(row, col - 1), (row, col + 1)],  # Horizontal
            [(row - 1, col), (row + 1, col)],  # Vertical
            [(row - 1, col - 1), (row + 1, col + 1)],  # Main diagonal
            [(row - 1, col + 1), (row + 1, col - 1)],  # Anti-diagonal
        ]
        for direction in directions:
            if all(
                0 <= r < self.board.height and
                0 <= c < self.board.width and
                self.board.layout[r, c] == piece
                for r, c in direction
            ):
                return True
        return False

    def capture_piece(self):
        while True:
            print("Mill formed! Capture an opponent's piece.")
            move = self.prompt_current_player()
            if is_placement(move):
                piece, (row, col) = get_move_elements(move)
                if (
                    self.board.layout[row, col] in ('X', 'O') and
                    self.board.layout[row, col] != ('X' if self.current_player == 0 else 'O')
                ):
                    self.board.place_piece(f"_ {row},{col}")
                    self.captured[self.current_player] += 1
                    break
                else:
                    print("Invalid capture. Try again.")

    def is_adjacent(self, start, end):
        sr, sc = start
        er, ec = end
        return (abs(sr - er) == 1 and sc == ec) or (abs(sc - ec) == 1 and sr == er)

    def next_player(self):
        return 1 - self.current_player

    def finish_message(self, winner):
        print(f"Player {winner} wins the game!")

if __name__ == '__main__':
    # Create a 7x7 board with a center space
    layout = (
        "       \n"
        "   _   \n"
        "   _   \n"
        "___X___\n"
        "   X   \n"
        "   X   \n"
        "       "
    )
    board = Board((7, 7), layout)
    mygame = NineMensMorris(board)
    mygame.game_loop()
