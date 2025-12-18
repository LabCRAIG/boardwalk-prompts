from game import Game, Board, is_movement, is_placement, get_move_elements

class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 is X, Player 2 is O

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            if self.board.layout[row][col] != '_':
                return False
            return piece.upper() in ('X', 'O')
        elif is_movement(move):
            return False  # Tic-Tac-Toe doesn't involve moving pieces
        else:
            return False

    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
        # No need to handle movement since Tic-Tac-Toe is placement only

    def game_finished(self):
        # Check rows
        for row in range(3):
            if self.board.layout[row][0] != '_' and \
               self.board.layout[row][0] == self.board.layout[row][1] == self.board.layout[row][2]:
                return True

        # Check columns
        for col in range(3):
            if self.board.layout[0][col] != '_' and \
               self.board.layout[0][col] == self.board.layout[1][col] == self.board.layout[2][col]:
                return True

        # Check diagonals
        if self.board.layout[0][0] != '_' and \
           self.board.layout[0][0] == self.board.layout[1][1] == self.board.layout[2][2]:
            return True
        if self.board.layout[0][2] != '_' and \
           self.board.layout[0][2] == self.board.layout[1][1] == self.board.layout[2][0]:
            return True

        # Check for draw
        return '_' not in self.board.layout.flatten()

    def get_winner(self):
        # Check rows
        for row in range(3):
            if self.board.layout[row][0] != '_' and \
               self.board.layout[row][0] == self.board.layout[row][1] == self.board.layout[row][2]:
                return 1 if self.board.layout[row][0] == 'X' else 2

        # Check columns
        for col in range(3):
            if self.board.layout[0][col] != '_' and \
               self.board.layout[0][col] == self.board.layout[1][col] == self.board.layout[2][col]:
                return 1 if self.board.layout[0][col] == 'X' else 2

        # Check diagonals
        if self.board.layout[0][0] != '_' and \
           self.board.layout[0][0] == self.board.layout[1][1] == self.board.layout[2][2]:
            return 1 if self.board.layout[0][0] == 'X' else 2
        if self.board.layout[0][2] != '_' and \
           self.board.layout[0][2] == self.board.layout[1][1] == self.board.layout[2][0]:
            return 1 if self.board.layout[0][2] == 'X' else 2

        return None  # Draw

    def next_player(self):
        return 2 if self.current_player == 1 else 1

    def prompt_current_player(self):
        player_symbol = 'X' if self.current_player == 1 else 'O'
        return input(f"Player {self.current_player} ({player_symbol}), enter your move (e.g., 'X 1,1'): ")

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} wins!")

if __name__ == '__main__':
    board = Board((3, 3))
    game = TicTacToe(board)
    game.game_loop()