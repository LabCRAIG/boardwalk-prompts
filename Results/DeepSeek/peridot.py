from game import Game, Board, is_placement, get_move_elements
from copy import deepcopy

# Game subclass definition
class Peridot(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if not is_placement(move):
            return False

        piece, (row, col) = get_move_elements(move)
        if self.current_player == 1 and piece != 'A':
            return False
        if self.current_player == 2 and piece != 'V':
            return False

        if self.board.layout[row][col] != '_':
            return False

        return True

    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)

    def game_finished(self):
        # Check rows
        for row in self.board.layout:
            if all(cell == 'A' for cell in row):
                return True
            if all(cell == 'V' for cell in row):
                return True

        # Check columns
        for col in range(self.board.width):
            if all(self.board.layout[row][col] == 'A' for row in range(self.board.height)):
                return True
            if all(self.board.layout[row][col] == 'V' for row in range(self.board.height)):
                return True

        # Check diagonals
        if all(self.board.layout[i][i] == 'A' for i in range(3)):
            return True
        if all(self.board.layout[i][i] == 'V' for i in range(3)):
            return True
        if all(self.board.layout[i][2 - i] == 'A' for i in range(3)):
            return True
        if all(self.board.layout[i][2 - i] == 'V' for i in range(3)):
            return True

        # Check for tie (no blank spaces left)
        if all(cell != '_' for row in self.board.layout for cell in row):
            return True

        return False

    def get_winner(self):
        # Check rows
        for row in self.board.layout:
            if all(cell == 'A' for cell in row):
                return 1
            if all(cell == 'V' for cell in row):
                return 2

        # Check columns
        for col in range(self.board.width):
            if all(self.board.layout[row][col] == 'A' for row in range(self.board.height)):
                return 1
            if all(self.board.layout[row][col] == 'V' for row in range(self.board.height)):
                return 2

        # Check diagonals
        if all(self.board.layout[i][i] == 'A' for i in range(3)):
            return 1
        if all(self.board.layout[i][i] == 'V' for i in range(3)):
            return 2
        if all(self.board.layout[i][2 - i] == 'A' for i in range(3)):
            return 1
        if all(self.board.layout[i][2 - i] == 'V' for i in range(3)):
            return 2

        # If no winner and the board is full, it's a tie
        if all(cell != '_' for row in self.board.layout for cell in row):
            return None

        return None

    def next_player(self):
        return 2 if self.current_player == 1 else 1

    def finish_message(self, winner):
        if winner is None:
            print("It's a tie!")
        else:
            print(f"Player {winner} wins!")

if __name__ == '__main__':
    board = Board((3, 3))
    mygame = Peridot(board)
    mygame.game_loop()