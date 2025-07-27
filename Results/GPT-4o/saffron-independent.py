class SaffronGame:
    def __init__(self):
        # Initialize an 8x8 board
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # Place initial pieces
        self.board[3][3] = 'A'  # Player 1's piece
        self.board[4][4] = 'B'  # Player 2's piece
        self.positions = {'A': (3, 3), 'B': (4, 4)}  # Track positions of A and B
        self.current_player = 1  # Player 1 starts

    def print_board(self):
        # Display the board
        for row in self.board:
            print(' '.join(row))
        print()

    def is_valid_move(self, x, y):
        # Check if the move is within bounds and not occupied by the opponent's piece
        return 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == '.'

    def move_piece(self, piece, new_x, new_y):
        # Get the current position of the piece
        current_x, current_y = self.positions[piece]

        # Check if the move is valid
        if not self.is_valid_move(new_x, new_y):
            print(f"Invalid move by Player {self.current_player}. Try again.")
            return False

        # Check if the player loses by moving onto a marker
        if self.board[new_x][new_y] in ['a', 'b']:
            print(f"Player {self.current_player} loses! Moved onto a marker.")
            return True  # Game over

        # Place a marker on the current position
        self.board[current_x][current_y] = 'a' if piece == 'A' else 'b'

        # Move the piece to the new position
        self.board[new_x][new_y] = piece
        self.positions[piece] = (new_x, new_y)

        return False  # Game continues

    def play_turn(self):
        # Get the current player's piece
        piece = 'A' if self.current_player == 1 else 'B'

        # Print the board
        print(f"Player {self.current_player}'s turn:")
        self.print_board()

        # Get the move from the player
        try:
            new_x, new_y = map(int, input(f"Enter the new position for {piece} (row and column): ").split())
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")
            return False

        # Attempt to move the piece
        if self.move_piece(piece, new_x, new_y):
            return True  # Game over

        # Switch to the next player
        self.current_player = 2 if self.current_player == 1 else 1
        return False  # Game continues

    def play_game(self):
        print("Welcome to Saffron!")
        print("Players take turns moving their pieces. First player to step on a marker loses.")
        print("Initial board setup:")
        self.print_board()

        # Main game loop
        while True:
            if self.play_turn():
                print(f"Game over! Player {3 - self.current_player} wins!")
                break


# Run the game
if __name__ == "__main__":
    game = SaffronGame()
    game.play_game()