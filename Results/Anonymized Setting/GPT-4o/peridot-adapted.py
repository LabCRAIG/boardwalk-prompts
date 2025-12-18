from game import Game, Board, is_placement, get_move_elements


class Peridot(Game):
    def __init__(self, board):
        # Call the superclass constructor and initialize any extra attributes
        super().__init__(board)
        self.players = {0: "A", 1: "V"}  # Player 1 uses "A", Player 2 uses "V"

    def initial_player(self):
        # Player 1 starts
        return 0

    def prompt_current_player(self):
        # Prompt the current player to input their move
        print(f"Player {self.current_player + 1}'s turn ({self.players[self.current_player]}).")
        return input("Enter your move (e.g., 'A 1,1'): ")

    def validate_move(self, move):
        # Check if the move is a valid placement
        if not is_placement(move):
            print("Invalid move format! Use 'X D,D' (e.g., 'A 1,1').")
            return False

        piece, (row, col) = get_move_elements(move)

        # Ensure the piece matches the current player's piece
        if piece != self.players[self.current_player]:
            print(f"Invalid piece! Player {self.current_player + 1} must place '{self.players[self.current_player]}'.")
            return False

        # Ensure the position is valid and unoccupied
        if row < 0 or col < 0 or row >= self.board.height or col >= self.board.width:
            print("Invalid move! Position is out of bounds.")
            return False

        if self.board.layout[row, col] != '_':  # Check if the space is blank
            print("Invalid move! Space is already occupied.")
            return False

        # If all checks pass, the move is valid
        return True

    def perform_move(self, move):
        # Place the piece on the board
        self.board.place_piece(move)

    def game_finished(self):
        # Check if a player has won or if the game is a tie
        return self.check_winner() or self.is_tie()

    def get_winner(self):
        # Return the current player if they have won, otherwise return None
        if self.check_winner():
            return self.current_player
        return None

    def next_player(self):
        # Switch to the other player
        return 1 - self.current_player

    def check_winner(self):
        # Check rows, columns, and diagonals for a win condition
        layout = self.board.layout
        for i in range(3):
            # Check rows
            if layout[i, 0] == layout[i, 1] == layout[i, 2] != '_':
                return True
            # Check columns
            if layout[0, i] == layout[1, i] == layout[2, i] != '_':
                return True

        # Check diagonals
        if layout[0, 0] == layout[1, 1] == layout[2, 2] != '_':
            return True
        if layout[0, 2] == layout[1, 1] == layout[2, 0] != '_':
            return True

        return False

    def is_tie(self):
        # Check if the board is full (tie condition)
        return not any('_' in row for row in self.board.layout)

    def finish_message(self, winner):
        # Print a message at the end of the game
        if winner is not None:
            print(f"Player {winner + 1} ({self.players[winner]}) wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    # Initialize the board with a blank 3x3 layout
    board_layout = "_ _ _\n_ _ _\n_ _ _"    
    board = Board((3, 3), layout=board_layout)

    # Create and start the game
    game = Peridot(board)
    game.game_loop()