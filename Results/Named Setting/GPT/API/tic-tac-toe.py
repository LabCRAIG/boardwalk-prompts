from game import Game, Board, is_movement, is_placement, get_move_elements


class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = {0: "X", 1: "O"}  # Player 0 is X, Player 1 is O

    def initial_player(self):
        return 0  # Player X starts

    def validate_move(self, move: str) -> bool:
        # Validate placement moves only
        if not is_placement(move):
            return False

        piece, position = get_move_elements(move)
        row, col = position

        # Check if the move is within bounds and the space is empty
        if 0 <= row < self.board.height and 0 <= col < self.board.width:
            return self.board.layout[row, col] == '_'
        return False

    def perform_move(self, move: str):
        piece, position = get_move_elements(move)
        self.board.place_piece(move)

    def game_finished(self) -> bool:
        layout = self.board.layout

        # Check rows, columns, and diagonals for a win
        for i in range(self.board.height):
            if layout[i, 0] != '_' and all(layout[i, j] == layout[i, 0] for j in range(self.board.width)):
                return True  # Row win

        for j in range(self.board.width):
            if layout[0, j] != '_' and all(layout[i, j] == layout[0, j] for i in range(self.board.height)):
                return True  # Column win

        # Check diagonals
        if layout[0, 0] != '_' and all(layout[i, i] == layout[0, 0] for i in range(self.board.height)):
            return True  # Top-left to bottom-right diagonal win
        if layout[0, self.board.width - 1] != '_' and all(
            layout[i, self.board.width - 1 - i] == layout[0, self.board.width - 1] for i in range(self.board.height)
        ):
            return True  # Top-right to bottom-left diagonal win

        # Check for draw (no empty spaces left)
        if not (layout == '_').any():
            return True

        return False

    def get_winner(self):
        layout = self.board.layout

        # Check rows, columns, and diagonals for a winner
        for i in range(self.board.height):
            if layout[i, 0] != '_' and all(layout[i, j] == layout[i, 0] for j in range(self.board.width)):
                return 0 if layout[i, 0] == "X" else 1  # Row winner

        for j in range(self.board.width):
            if layout[0, j] != '_' and all(layout[i, j] == layout[0, j] for i in range(self.board.height)):
                return 0 if layout[0, j] == "X" else 1  # Column winner

        # Check diagonals
        if layout[0, 0] != '_' and all(layout[i, i] == layout[0, 0] for i in range(self.board.height)):
            return 0 if layout[0, 0] == "X" else 1  # Diagonal winner
        if layout[0, self.board.width - 1] != '_' and all(
            layout[i, self.board.width - 1 - i] == layout[0, self.board.width - 1] for i in range(self.board.height)
        ):
            return 0 if layout[0, self.board.width - 1] == "X" else 1  # Diagonal winner

        # Check for draw
        if not (layout == '_').any():
            return None

    def next_player(self):
        return (self.current_player + 1) % 2  # Alternate between 0 and 1

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {self.players[winner]} wins!")


if __name__ == "__main__":
    # Initialize a 3x3 board for Tic-Tac-Toe
    board = Board((3, 3))
    mygame = TicTacToe(board)
    mygame.game_loop()