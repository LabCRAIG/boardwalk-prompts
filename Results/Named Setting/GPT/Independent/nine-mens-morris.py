
class NineMensMorris:
    def __init__(self):
        # Initialize the board with empty spaces
        self.board = [
            [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' '],
            [' ', 'O', ' ', ' ', ' ', ' ', ' ', 'O', ' '],
            ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
            [' ', ' ', ' ', 'O', ' ', 'O', ' ', ' ', ' '],
            ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
            [' ', ' ', ' ', 'O', ' ', 'O', ' ', ' ', ' '],
            ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
            [' ', 'O', ' ', ' ', ' ', ' ', ' ', 'O', ' '],
            [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
        ]

        self.players = ['X', 'O']  # Two players: X and O
        self.current_player = 'X'  # X always starts
        self.phase = 'placing'  # Game starts in the placing phase
        self.pieces_to_place = {'X': 9, 'O': 9}  # Pieces left to place
        self.pieces_on_board = {'X': 0, 'O': 0}  # Pieces currently on the board

    def print_board(self):
        # Display the board in a human-readable format
        for row in self.board:
            print(' '.join(row))
        print()

    def is_valid_position(self, row, col):
        # Check if a position is valid (within bounds and a valid slot)
        return 0 <= row < 9 and 0 <= col < 9 and self.board[row][col] == 'O'

    def place_piece(self, row, col):
        # Place a piece on the board
        if self.is_valid_position(row, col):
            self.board[row][col] = self.current_player
            self.pieces_to_place[self.current_player] -= 1
            self.pieces_on_board[self.current_player] += 1
            return True
        return False

    def switch_player(self):
        # Switch to the other player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def check_mill(self, row, col):
        # Check if placing a piece forms a mill (three in a row)
        player = self.current_player

        # All possible mills on the board
        mills = [
            [(0, 2), (0, 4), (0, 6)], [(2, 0), (4, 0), (6, 0)],
            [(8, 2), (8, 4), (8, 6)], [(2, 8), (4, 8), (6, 8)],
            [(1, 1), (4, 1), (7, 1)], [(1, 7), (4, 7), (7, 7)],
            [(3, 3), (4, 3), (5, 3)], [(3, 5), (4, 5), (5, 5)]
        ]

        for mill in mills:
            if (row, col) in mill:
                if all(self.board[r][c] == player for r, c in mill):
                    return True
        return False

    def capture_piece(self, row, col):
        # Capture an opponent's piece
        opponent = 'X' if self.current_player == 'O' else 'O'
        if 0 <= row < 9 and 0 <= col < 9 and self.board[row][col] == opponent:
            self.board[row][col] = 'O'
            self.pieces_on_board[opponent] -= 1
            return True
        return False

    def move_piece(self, start_row, start_col, end_row, end_col):
        # Move a piece from one position to another
        if self.board[start_row][start_col] == self.current_player and self.is_valid_position(end_row, end_col):
            self.board[start_row][start_col] = 'O'
            self.board[end_row][end_col] = self.current_player
            return True
        return False

    def is_game_over(self):
        # Check if the game is over (a player has less than three pieces)
        return self.pieces_on_board['X'] < 3 or self.pieces_on_board['O'] < 3

    def play(self):
        # Main game loop
        while not self.is_game_over():
            self.print_board()
            print(f"{self.current_player}'s turn ({self.phase} phase)")

            if self.phase == 'placing':
                print(f"Pieces to place: {self.pieces_to_place[self.current_player]}")
                row, col = map(int, input("Enter row and column to place your piece (e.g., 3 4): ").split())
                if self.place_piece(row, col):
                    if self.check_mill(row, col):
                        print(f"{self.current_player} formed a mill! Capture an opponent's piece.")
                        capture_row, capture_col = map(int, input("Enter row and column to capture (e.g., 3 4): ").split())
                        self.capture_piece(capture_row, capture_col)
                    if self.pieces_to_place['X'] == 0 and self.pieces_to_place['O'] == 0:
                        self.phase = 'moving'
                    self.switch_player()
                else:
                    print("Invalid position. Try again.")

            elif self.phase == 'moving':
                print(f"Pieces on board: {self.pieces_on_board[self.current_player]}")
                start_row, start_col = map(int, input("Enter row and column of piece to move (e.g., 3 4): ").split())
                end_row, end_col = map(int, input("Enter row and column to move to (e.g., 3 5): ").split())
                if self.move_piece(start_row, start_col, end_row, end_col):
                    if self.check_mill(end_row, end_col):
                        print(f"{self.current_player} formed a mill! Capture an opponent's piece.")
                        capture_row, capture_col = map(int, input("Enter row and column to capture (e.g., 3 4): ").split())
                        self.capture_piece(capture_row, capture_col)
                    self.switch_player()
                else:
                    print("Invalid move. Try again.")

        # Game over
        self.print_board()
        if self.pieces_on_board['X'] < 3:
            print("O wins!")
        else:
            print("X wins!")


# Run the game
if __name__ == "__main__":
    game = NineMensMorris()
    game.play()
