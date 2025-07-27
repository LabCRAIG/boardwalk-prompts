class Peridot:
    def __init__(self):
        # Initialize an empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = {'Player 1': 'A', 'Player 2': 'V'}
        self.current_player = 'Player 1'

    def display_board(self):
        # Display the board in a user-friendly format
        print("\nCurrent Board:")
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)
        print()

    def is_valid_move(self, row, col):
        # Check if the selected space is valid and unoccupied
        if 0 <= row < 3 and 0 <= col < 3:
            return self.board[row][col] == ' '
        return False

    def make_move(self, row, col):
        # Place the player's piece on the board
        if self.is_valid_move(row, col):
            self.board[row][col] = self.players[self.current_player]
            return True
        else:
            print("Invalid move! Space is already occupied or out of bounds. Try again.")
            return False

    def check_winner(self):
        # Check rows, columns, and diagonals for a win condition
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

    def is_tie(self):
        # Check if the board is full (tie condition)
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def switch_player(self):
        # Switch to the other player
        self.current_player = 'Player 2' if self.current_player == 'Player 1' else 'Player 1'

    def play(self):
        # Main game loop
        print("Welcome to Peridot! Player 1 uses 'A', Player 2 uses 'V'.")
        self.display_board()

        while True:
            print(f"{self.current_player}'s turn ({self.players[self.current_player]}).")
            try:
                # Get the player's move
                row = int(input("Enter the row (0, 1, or 2): "))
                col = int(input("Enter the column (0, 1, or 2): "))
            except ValueError:
                print("Invalid input! Please enter numbers 0, 1, or 2.")
                continue

            if self.make_move(row, col):
                self.display_board()

                # Check for a winner
                if self.check_winner():
                    print(f"{self.current_player} wins!")
                    break

                # Check for a tie
                if self.is_tie():
                    print("It's a tie!")
                    break

                # Switch to the next player
                self.switch_player()


# Start the game
if __name__ == "__main__":
    game = Peridot()
    game.play()