from game import Game, Board, is_movement, is_placement, get_move_elements
from copy import deepcopy
import numpy as np

class Topaz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.phase = 1  # 1: Placement phase, 2: Movement phase
        self.pieces_remaining = {0: 9, 1: 9}  # Player 1: A, Player 2: B
        self.player_pieces = {0: 'A', 1: 'B'}

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        elements = get_move_elements(move)
        if self.phase == 1:
            if not is_placement(move):
                return False
            piece, (row, col) = elements
            if piece != self.player_pieces[self.current_player]:
                return False
            if self.board.layout[row][col] != '_':
                return False
        else:
            if not is_movement(move):
                return False
            (src_row, src_col), (dest_row, dest_col) = elements
            if self.board.layout[src_row][src_col] != self.player_pieces[self.current_player]:
                return False
            if self.board.layout[dest_row][dest_col] != '_':
                return False
            if not self.is_adjacent(src_row, src_col, dest_row, dest_col):
                return False  # Only adjacent moves allowed
        return True

    def is_adjacent(self, src_row, src_col, dest_row, dest_col):
        # Check if the destination is the closest blank, non-null space in the same row or column
        if src_row == dest_row:
            # Same row, check columns
            step = 1 if dest_col > src_col else -1
            for col in range(src_col + step, dest_col + step, step):
                if self.board.layout[src_row][col] != '_':
                    return False
            return True
        elif src_col == dest_col:
            # Same column, check rows
            step = 1 if dest_row > src_row else -1
            for row in range(src_row + step, dest_row + step, step):
                if self.board.layout[row][src_col] != '_':
                    return False
            return True
        return False

    def perform_move(self, move):
        elements = get_move_elements(move)
        if self.phase == 1:
            piece, (row, col) = elements
            self.board.place_piece(move)
            self.pieces_remaining[self.current_player] -= 1
            if self.pieces_remaining[0] == 0 and self.pieces_remaining[1] == 0:
                self.phase = 2
        else:
            (src_row, src_col), (dest_row, dest_col) = elements
            self.board.move_piece(move)
        
        # Check for capture condition
        if self.check_capture(move):
            self.handle_capture()

    def check_capture(self, move):
        elements = get_move_elements(move)
        if self.phase == 1:
            _, (row, col) = elements
            return self.check_three_in_a_row(row, col)
        else:
            _, (dest_row, dest_col) = elements
            return self.check_three_in_a_row(dest_row, dest_col)

    def check_three_in_a_row(self, row, col):
        piece = self.board.layout[row][col]
        if piece == '_' or piece == ' ':
            return False

        # Check row
        count = 1
        left = col - 1
        while left >= 0 and self.board.layout[row][left] == piece:
            count += 1
            left -= 1
        right = col + 1
        while right < self.board.width and self.board.layout[row][right] == piece:
            count += 1
            right += 1
        if count >= 3:
            return True

        # Check column
        count = 1
        up = row - 1
        while up >= 0 and self.board.layout[up][col] == piece:
            count += 1
            up -= 1
        down = row + 1
        while down < self.board.height and self.board.layout[down][col] == piece:
            count += 1
            down += 1
        return count >= 3

    def handle_capture(self):
        print(f"Player {self.current_player} triggered a capture!")
        opponent = 1 - self.current_player
        valid_pieces = []
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == self.player_pieces[opponent]:
                    valid_pieces.append((row, col))
        if valid_pieces:
            print("Select a piece to capture (row, col):")
            for i, (row, col) in enumerate(valid_pieces):
                print(f"{i}: ({row}, {col})")
            choice = int(input("Enter your choice: "))
            row, col = valid_pieces[choice]
            self.board.layout[row][col] = '_'

    def game_finished(self):
        # Win/loss conditions can only be determined in the second phase
        if self.phase != 2:
            return False

        # Check if a player has fewer than 3 pieces
        counts = {0: 0, 1: 0}
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if piece == 'A':
                    counts[0] += 1
                elif piece == 'B':
                    counts[1] += 1
        if counts[0] < 3 or counts[1] < 3:
            return True

        # Check if a player cannot move
        for player in [0, 1]:
            if not self.can_player_move(player):
                return True
        return False

    def can_player_move(self, player):
        piece = self.player_pieces[player]
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == piece:
                    # Check adjacent positions
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                            if self.board.layout[new_row][new_col] == '_':
                                return True
        return False

    def get_winner(self):
        # Win/loss conditions can only be determined in the second phase
        if self.phase != 2:
            return None

        counts = {0: 0, 1: 0}
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if piece == 'A':
                    counts[0] += 1
                elif piece == 'B':
                    counts[1] += 1
        if counts[0] < 3 or not self.can_player_move(0):
            return 1
        elif counts[1] < 3 or not self.can_player_move(1):
            return 0
        return None

    def next_player(self):
        return 1 - self.current_player

    def initial_player(self):
        return 0

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner} wins!")
        else:
            print("The game is a draw!")


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
    mygame = Topaz(board)
    mygame.game_loop()