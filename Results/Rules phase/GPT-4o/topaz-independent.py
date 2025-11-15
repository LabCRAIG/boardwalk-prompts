class TopazGame:
    def __init__(self):
        # Initialize the 7x7 board with null spaces (None), blank spaces ('_'), and pieces ('A', 'B')
        self.board = [
            [None, '_', None, '_', None, '_', None],
            ['_', None, '_', None, '_', None, '_'],
            [None, '_', None, '_', None, '_', None],
            ['_', None, '_', None, '_', None, '_'],
            [None, '_', None, '_', None, '_', None],
            ['_', None, '_', None, '_', None, '_'],
            [None, '_', None, '_', None, '_', None]
        ]
        self.players = {1: 'A', 2: 'B'}  # Player 1 has 'A', Player 2 has 'B'
        self.pieces_left = {1: 9, 2: 9}  # Each player starts with 9 pieces
        self.phase = 1  # Phase 1: Placing pieces. Phase 2: Moving pieces.
        self.current_player = 1  # Player 1 starts
        self.winner = None  # No winner initially

    def print_board(self):
        # Display the board in a readable format
        for row in self.board:
            print(' '.join(cell if cell is not None else ' ' for cell in row))
        print()

    def is_valid_position(self, x, y):
        # Check if a position is valid (within bounds and not a null space)
        return 0 <= x < 7 and 0 <= y < 7 and self.board[x][y] is not None

    def place_piece(self, x, y):
        # Place a piece on the board during phase 1
        if self.phase != 1:
            raise ValueError("Cannot place pieces in phase 2.")
        if not self.is_valid_position(x, y) or self.board[x][y] != '_':
            raise ValueError("Invalid position to place a piece.")
        piece = self.players[self.current_player]
        self.board[x][y] = piece
        self.pieces_left[self.current_player] -= 1
        self.check_capture(x, y)
        self.check_phase_transition()
        self.switch_turn()

    def move_piece(self, x, y, new_x, new_y):
        # Move a piece during phase 2
        if self.phase != 2:
            raise ValueError("Cannot move pieces in phase 1.")
        if not self.is_valid_position(x, y) or not self.is_valid_position(new_x, new_y):
            raise ValueError("Invalid position.")
        if self.board[x][y] != self.players[self.current_player]:
            raise ValueError("You can only move your own pieces.")
        if self.board[new_x][new_y] != '_':
            raise ValueError("You can only move to a blank space.")
        if abs(x - new_x) + abs(y - new_y) != 1:  # Ensure movement is to an adjacent space
            raise ValueError("You can only move to an adjacent space.")

        # Move the piece
        self.board[x][y] = '_'
        self.board[new_x][new_y] = self.players[self.current_player]
        self.check_capture(new_x, new_y)
        self.check_loss_condition()
        self.switch_turn()

    def check_capture(self, x, y):
        # Check for a capture condition and remove an opponent's piece if met
        piece = self.board[x][y]
        for direction in [(0, 1), (1, 0)]:  # Check rows and columns
            count = 1
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                while self.is_valid_position(nx, ny) and self.board[nx][ny] == piece:
                    count += 1
                    nx += dx
                    ny += dy
            if count >= 3:
                self.capture_piece()
                break

    def capture_piece(self):
        # Allow the current player to remove one opponent's piece
        print(f"Player {self.current_player} captured! Choose a piece to remove.")
        opponent_piece = self.players[3 - self.current_player]
        while True:
            try:
                x, y = map(int, input(f"Enter the position (row, column) of {opponent_piece} to remove: ").split())
                if self.is_valid_position(x, y) and self.board[x][y] == opponent_piece:
                    self.board[x][y] = '_'
                    self.pieces_left[3 - self.current_player] -= 1
                    break
                else:
                    print("Invalid position. Try again.")
            except ValueError:
                print("Invalid input. Enter two integers separated by a space.")

    def check_phase_transition(self):
        # Transition from phase 1 to phase 2 if all pieces have been placed
        if self.pieces_left[1] == 0 and self.pieces_left[2] == 0:
            self.phase = 2
            print("All pieces placed. Transitioning to phase 2: Movement phase.")

    def check_loss_condition(self):
        # Check if a player has lost the game
        for player in [1, 2]:
            if self.pieces_left[player] <= 2:
                self.winner = 3 - player
                break
        else:
            # Check if a player cannot move any pieces
            for player in [1, 2]:
                for x in range(7):
                    for y in range(7):
                        if self.board[x][y] == self.players[player]:
                            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                nx, ny = x + dx, y + dy
                                if self.is_valid_position(nx, ny) and self.board[nx][ny] == '_':
                                    return
                self.winner = 3 - player
                break

    def switch_turn(self):
        # Switch to the other player's turn
        self.current_player = 3 - self.current_player

    def play(self):
        # Start the game loop
        print("Welcome to Topaz!")
        self.print_board()
        while not self.winner:
            print(f"Player {self.current_player}'s turn ({self.players[self.current_player]}).")
            try:
                if self.phase == 1:
                    x, y = map(int, input("Enter the position (row, column) to place your piece: ").split())
                    self.place_piece(x, y)
                else:
                    x, y, new_x, new_y = map(int, input("Enter the position (row, column) of the piece to move and its new position (row, column): ").split())
                    self.move_piece(x, y, new_x, new_y)
                self.print_board()
            except ValueError as e:
                print(e)
        print(f"Player {self.winner} wins!")


if __name__ == "__main__":
    game = TopazGame()
    game.play()