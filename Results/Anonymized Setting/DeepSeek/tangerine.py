from game import Game, Board, is_placement, get_move_elements
from copy import deepcopy

class Tangerine(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        piece, (row, col) = get_move_elements(move)
        if self.current_player == 1 and piece != 'H':
            return False
        if self.current_player == 2 and piece != 'V':
            return False

        # Check if the required spaces are free
        if piece == 'H':
            if col + 1 >= self.board.width or self.board.layout[row, col] != '_' or self.board.layout[row, col + 1] != '_':
                return False
        elif piece == 'V':
            if row - 1 < 0 or self.board.layout[row, col] != '_' or self.board.layout[row - 1, col] != '_':
                return False
        return True

    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        if piece == 'H':
            self.board.place_piece(f'H {row},{col}')
            self.board.place_piece(f'H {row},{col + 1}')
        elif piece == 'V':
            self.board.place_piece(f'V {row},{col}')
            self.board.place_piece(f'V {row - 1},{col}')

    def game_finished(self):
        # Check if either player has no valid moves
        for player in [1, 2]:
            piece = 'H' if player == 1 else 'V'
            for row in range(self.board.height):
                for col in range(self.board.width):
                    if piece == 'H' and col + 1 < self.board.width:
                        if self.board.layout[row, col] == '_' and self.board.layout[row, col + 1] == '_':
                            return False
                    if piece == 'V' and row - 1 >= 0:
                        if self.board.layout[row, col] == '_' and self.board.layout[row - 1, col] == '_':
                            return False
        return True

    def get_winner(self):
        # Check if the current player has no valid moves
        piece = 'H' if self.current_player == 1 else 'V'
        for row in range(self.board.height):
            for col in range(self.board.width):
                if piece == 'H' and col + 1 < self.board.width:
                    if self.board.layout[row, col] == '_' and self.board.layout[row, col + 1] == '_':
                        return None  # Game is not finished yet
                if piece == 'V' and row - 1 >= 0:
                    if self.board.layout[row, col] == '_' and self.board.layout[row - 1, col] == '_':
                        return None  # Game is not finished yet
        # If no moves are available for the current player, the other player wins
        return 2 if self.current_player == 1 else 1

    def next_player(self):
        return 2 if self.current_player == 1 else 1

    def prompt_current_player(self):
        piece = 'H' if self.current_player == 1 else 'V'
        return input(f"Player {self.current_player} ({piece}), your move (e.g., 'H 0,0' or 'V 5,5'): ")

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner} wins!")
        else:
            print("The game is a draw!")

if __name__ == '__main__':
    board = Board((6, 6))
    mygame = Tangerine(board)
    mygame.game_loop()