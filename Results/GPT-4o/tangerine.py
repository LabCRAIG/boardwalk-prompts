from game import Game, Board, is_placement, get_move_elements
import numpy as np

class Tangerine(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: "H", 1: "V"}  # Player 1 uses 'H', Player 2 uses 'V'

    def initial_player(self):
        return 0  # Player 1 starts

    def prompt_current_player(self):
        return input(f"Player {self.current_player + 1} ({self.players[self.current_player]}), your move (format: X Y): ")

    def validate_move(self, move: str) -> bool:
        if not is_placement(move):  # Move must be a placement
            return False

        piece, (x, y) = get_move_elements(move)
        if piece != self.players[self.current_player]:  # Must place the correct piece
            return False

        if not (0 <= x < self.board.height and 0 <= y < self.board.width):  # Check bounds
            return False
        
        if piece == "H":  # Horizontal piece validation
            if y + 1 >= self.board.width or self.board.layout[x, y] != "_" or self.board.layout[x, y + 1] != "_":
                return False
        elif piece == "V":  # Vertical piece validation
            if x - 1 < 0 or self.board.layout[x, y] != "_" or self.board.layout[x - 1, y] != "_":
                return False

        return True

    def perform_move(self, move: str):
        piece, (x, y) = get_move_elements(move)
        if piece == "H":  # Place horizontal piece
            self.board.layout[x, y] = "H"
            self.board.layout[x, y + 1] = "H"
        elif piece == "V":  # Place vertical piece
            self.board.layout[x, y] = "V"
            self.board.layout[x - 1, y] = "V"

    def game_finished(self) -> bool:
        # Check if the current player can make any valid move
        for x in range(self.board.height):
            for y in range(self.board.width):
                # Check horizontal piece placement
                if self.players[self.current_player] == "H" and y + 1 < self.board.width:
                    if self.board.layout[x, y] == "_" and self.board.layout[x, y + 1] == "_":
                        return False  # A valid move exists
                # Check vertical piece placement
                if self.players[self.current_player] == "V" and x - 1 >= 0:
                    if self.board.layout[x, y] == "_" and self.board.layout[x - 1, y] == "_":
                        return False  # A valid move exists
        return True  # No valid moves left

    def get_winner(self):
        # The winner is the other player since the current player has no moves
        return 1 - self.current_player

    def finish_message(self, winner):
        print(f"Player {winner + 1} ({self.players[winner]}) wins!")

    def next_player(self):
        return 1 - self.current_player  # Alternate players


if __name__ == "__main__":
    board = Board((6, 6))  # Initialize a 6x6 board
    tangerine = Tangerine(board)
    tangerine.game_loop()