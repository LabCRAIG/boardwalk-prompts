from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
import numpy as np
import copy

# Enum for players
class Players(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

# Topaz game implementation
class Topaz(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.phase = 1  # Phase 1: Placement, Phase 2: Movement
        self.pieces_left = {Players.PLAYER_1: 9, Players.PLAYER_2: 9}  # Pieces left to place
        self.pieces_on_board = {Players.PLAYER_1: 0, Players.PLAYER_2: 0}  # Pieces on board
    
    def initial_player(self):
        return Players.PLAYER_1

    def next_player(self):
        return Players.PLAYER_2 if self.current_player == Players.PLAYER_1 else Players.PLAYER_1

    def validate_move(self, move: str) -> bool:
        if self.phase == 1 and is_placement(move):
            piece, (row, col) = get_move_elements(move)
            if self.pieces_left[self.current_player] == 0:
                return False
            if piece not in ("A", "B") or self.board.layout[row, col] != "_":
                return False
            return True
        elif self.phase == 2 and is_movement(move):
            (start_row, start_col), (end_row, end_col) = get_move_elements(move)
            if self.board.layout[start_row, start_col] != ("A" if self.current_player == Players.PLAYER_1 else "B"):
                return False
            if abs(end_row - start_row) + abs(end_col - start_col) != 1:  # Ensure adjacent move
                return False
            if self.board.layout[end_row, end_col] != "_":  # Ensure destination is blank
                return False
            return True
        return False

    def perform_move(self, move: str):
        if self.phase == 1 and is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_left[self.current_player] -= 1
            self.pieces_on_board[self.current_player] += 1
            if sum(self.pieces_left.values()) == 0:  # All pieces placed
                self.phase = 2
        elif self.phase == 2 and is_movement(move):
            (start_row, start_col), (end_row, end_col) = get_move_elements(move)
            self.board.move_piece(move)
        # Check for capture condition
        if self.check_capture():
            self.remove_opponent_piece()

    def check_capture(self) -> bool:
        layout = self.board.layout
        for row in range(self.board.height):
            for col in range(self.board.width):
                if layout[row, col] in ("A", "B"):
                    # Check horizontal
                    if (col <= self.board.width - 3 and
                        layout[row, col] == layout[row, col + 1] == layout[row, col + 2]):
                        return True
                    # Check vertical
                    if (row <= self.board.height - 3 and
                        layout[row, col] == layout[row + 1, col] == layout[row + 2, col]):
                        return True
        return False

    def remove_opponent_piece(self):
        valid = False
        while not valid:
            print("Capture condition met! Select an opponent's piece to remove.")
            move = input("Enter the coordinates of the piece to remove (e.g., '3,3'): ")
            try:
                row, col = map(int, move.split(","))
                opponent_piece = "A" if self.current_player == Players.PLAYER_2 else "B"
                if self.board.layout[row, col] == opponent_piece:
                    self.board.place_piece(f"_ {row},{col}")
                    self.pieces_on_board[self.next_player()] -= 1
                    valid = True
                else:
                    print("Invalid selection. Try again.")
            except:
                print("Invalid input. Try again.")

    def game_finished(self) -> bool:
        return False
        for player in Players:
            if self.pieces_on_board[player] <= 2:  # Less than or equal to 2 pieces
                return True
        # Check if any player has no valid moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] in ("A", "B"):
                    piece_owner = Players.PLAYER_1 if self.board.layout[row, col] == "A" else Players.PLAYER_2
                    if piece_owner == self.current_player:
                        # Check adjacent spaces
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            r, c = row + dr, col + dc
                            if 0 <= r < self.board.height and 0 <= c < self.board.width:
                                if self.board.layout[r, c] == "_":
                                    return False
        return True

    def get_winner(self):
        if self.pieces_on_board[Players.PLAYER_1] <= 2 or not self.can_move(Players.PLAYER_1):
            return Players.PLAYER_2.value
        if self.pieces_on_board[Players.PLAYER_2] <= 2 or not self.can_move(Players.PLAYER_2):
            return Players.PLAYER_1.value
        return None

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("The game is a draw.")

    def can_move(self, player):
        piece_char = "A" if player == Players.PLAYER_1 else "B"
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == piece_char:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        r, c = row + dr, col + dc
                        if 0 <= r < self.board.height and 0 <= c < self.board.width:
                            if self.board.layout[r, c] == "_":
                                return True
        return False

if __name__ == '__main__':
    initial_layout = (
        "_  _  _\n"
        " _ _ _ \n"
        "  ___  \n"
        "___ ___\n"
        "  ___  \n"
        " _ _ _ \n"
        "_  _  _"
    )
    board = Board((7, 7), initial_layout)
    game = Topaz(board)
    game.game_loop()