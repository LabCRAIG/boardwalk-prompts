from game import Game, Board, is_movement, get_move_elements

class Lilac(Game):
    def __init__(self, board: Board):
        # Initialize the game state
        super().__init__(board)
        self.current_player = 0  # Player 1 starts (0 for Player 1, 1 for Player 2)
        self.round = 1

    def initial_player(self) -> int:
        # Player 1 (0) starts
        return 0

    def validate_move(self, move: str) -> bool:
        # Validate if the move is legal
        if not super().validate_move(move):
            return False  # Check if move is within bounds

        # Parse the move
        if is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
        else:
            return False  # Only movements are allowed in Lilac

        # Check if the source and destination are valid
        piece = self.board.layout[x1, y1]
        target = self.board.layout[x2, y2]

        if target != "_":
            return False  # Target must be empty
        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False  # Must move orthogonally one space

        # Check if the piece belongs to the current player
        if self.current_player == 0 and piece != "V":
            return False  # Player 1 can only move V
        if self.current_player == 1 and piece not in ["A", "Â"]:
            return False  # Player 2 can only move A or Â

        # Special rule for Â: it cannot leave the center unless moving within the boundaries
        if piece == "Â" and (x2, y2) == (3, 3):
            return True  # Â can stay in the center
        if piece == "Â" and (x2, y2) != (3, 3):
            return True  # Â can move normally elsewhere

        return True

    def perform_move(self, move: str):
        # Execute the move
        if is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            piece = self.board.layout[x1, y1]

            # Move the piece
            self.board.move_piece(move)

            # Check for captures
            self.capture_pieces(x2, y2)

            # Check for win conditions
            #self.check_win_conditions()

    def capture_pieces(self, x: int, y: int):
        # Capture any orthogonally sandwiched pieces
        opponent = "A" if self.current_player == 0 else "V"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            mx, my = x + 2 * dx, y + 2 * dy

            if 0 <= nx < 7 and 0 <= ny < 7 and 0 <= mx < 7 and 0 <= my < 7:
                if self.board.layout[nx, ny] == opponent and self.board.layout[mx, my] == self.board.layout[x, y]:
                    # Capture the opponent's piece
                    self.board.layout[nx, ny] = "_"

    def game_finished(self) -> bool:
        # Check if the game is over
        for x in range(7):
            for y in range(7):
                if self.board.layout[x, y] == "Â":
                    # Player 2 wins if Â is on the border
                    if x == 0 or x == 6 or y == 0 or y == 6:
                        return True
        # Player 1 wins if Â is no longer on the board
        return not any("Â" in row for row in self.board.layout)

    def get_winner(self) -> int:
        # Determine the winner
        for x in range(7):
            for y in range(7):
                if self.board.layout[x, y] == "Â":
                    # Player 2 wins if Â is on the border
                    if x == 0 or x == 6 or y == 0 or y == 6:
                        return 1  # Player 2 wins
        # Player 1 wins if Â is no longer on the board
        return 0 if not any("Â" in row for row in self.board.layout) else None

    def next_player(self) -> int:
        # Alternate between Player 1 (0) and Player 2 (1)
        return 1 - self.current_player

    def finish_message(self, winner):
        # Print the end-of-game message
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("The game is a draw.")

if __name__ == '__main__':
    # Define the initial board layout
    initial_layout = (
        "__VVV__\n"
        "___V___\n"
        "V_AAA_V\n"
        "VVAÂAVV\n"
        "V_AAA_V\n"
        "___V___\n"
        "__VVV__"
    )

    # Create the board and start the game
    board = Board((7, 7), initial_layout)
    game = Lilac(board)
    game.game_loop()