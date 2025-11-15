
from game import Game, Board, is_placement, get_move_elements

# Enum for players
class Players:
    PLAYER_X = 0
    PLAYER_O = 1

# Tic-Tac-Toe with modified rules
class TicTacToeModified(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.board = board

    def validate_move(self, move: str) -> bool:
        # Validate placement move
        if not is_placement(move):
            return False

        # Get piece and position
        piece, (row, col) = get_move_elements(move)

        # Check if piece belongs to current player
        if (self.current_player == Players.PLAYER_X and piece != 'X') or \
           (self.current_player == Players.PLAYER_O and piece != 'O'):
            return False

        # Check if position is within bounds and blank
        if row < 0 or row >= self.board.height or \
           col < 0 or col >= self.board.width or \
           self.board.layout[row, col] != '_':
            return False

        return True

    def perform_move(self, move: str):
        # Place the piece on the board
        self.board.place_piece(move)

    def game_finished(self) -> bool:
        # Check for 2x2 square victory condition
        for row in range(self.board.height - 1):
            for col in range(self.board.width - 1):
                square = {self.board.layout[row, col],
                          self.board.layout[row + 1, col],
                          self.board.layout[row, col + 1],
                          self.board.layout[row + 1, col + 1]}
                if len(square) == 1 and '_' not in square:
                    return True

        # Check for draw (no blank spaces left)
        if '_' not in self.board.layout:
            return True

        return False

    def get_winner(self) -> int:
        # Check for 2x2 square victory condition
        for row in range(self.board.height - 1):
            for col in range(self.board.width - 1):
                square = {self.board.layout[row, col],
                          self.board.layout[row + 1, col],
                          self.board.layout[row, col + 1],
                          self.board.layout[row + 1, col + 1]}
                if len(square) == 1 and '_' not in square:
                    # Return the winner based on the piece
                    return Players.PLAYER_X if 'X' in square else Players.PLAYER_O

        # If the board is full and no winner, it's a draw
        return None

    def next_player(self) -> int:
        # Alternate between players
        return Players.PLAYER_X if self.current_player == Players.PLAYER_O else Players.PLAYER_O

if __name__ == '__main__':
    # Create a 3x3 board for Tic-Tac-Toe
    board = Board((3, 3))
    mygame = TicTacToeModified(board)
    mygame.game_loop()
