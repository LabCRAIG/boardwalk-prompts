import numpy as np

class TicTacToe:
    def __init__(self):
        # Initialize 3x3 board with zeros (empty spaces)
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # Player 1 starts (X)
        self.game_over = False
        self.winner = None
        
    def make_move(self, row, col):
        """Attempt to place a piece at the given position"""
        if self.game_over:
            return False, "Game is already over!"
            
        if not (0 <= row < 3 and 0 <= col < 3):
            return False, "Position out of bounds!"
            
        if self.board[row, col] != 0:
            return False, "Position already occupied!"
            
        # Place the piece
        self.board[row, col] = self.current_player
        
        # Check for win
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
            return True, f"Player {self.current_player} wins!"
            
        # Check for draw
        if np.all(self.board != 0):
            self.game_over = True
            return True, "It's a draw!"
            
        # Switch player
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        return True, f"Player {self.current_player}'s turn"
    
    def check_win(self):
        """Check for a win with modified rules"""
        player = self.current_player
        
        # Check rows
        for i in range(3):
            if np.all(self.board[i, :] == player):
                return True
                
        # Check columns
        for i in range(3):
            if np.all(self.board[:, i] == player):
                return True
                
        # Check for 2x2 squares (there are 4 possible 2x2 squares in a 3x3 grid)
        squares = [
            ((0, 0), (0, 1), (1, 0), (1, 1)),  # Top-left
            ((0, 1), (0, 2), (1, 1), (1, 2)),  # Top-right
            ((1, 0), (1, 1), (2, 0), (2, 1)),  # Bottom-left
            ((1, 1), (1, 2), (2, 1), (2, 2))   # Bottom-right
        ]
        
        for square in squares:
            if all(self.board[r, c] == player for r, c in square):
                return True
                
        return False
    
    def print_board(self):
        """Print the current state of the board"""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        print("  0 1 2")
        for i in range(3):
            print(f"{i}", end=' ')
            for j in range(3):
                print(symbols[self.board[i, j]], end=' ')
            print()
        print()

def play_game():
    game = TicTacToe()
    print("Welcome to Tic-Tac-Toe with modified rules!")
    print("- Rows and columns count for victory")
    print("- Diagonals DO NOT count for victory")
    print("- Filling a 2x2 square with your pieces counts as victory")
    print("- Player 1 uses X, Player 2 uses O")
    print("- Enter moves as 'row col' (both 0-2)")
    print()
    
    game.print_board()
    
    while not game.game_over:
        try:
            move = input(f"Player {game.current_player}'s turn (row col): ")
            row, col = map(int, move.split())
            success, message = game.make_move(row, col)
            if success:
                print(message)
                game.print_board()
            else:
                print(f"Invalid move: {message}")
        except ValueError:
            print("Please enter row and column as numbers separated by space.")
    
    if game.winner:
        print(f"Congratulations! Player {game.winner} wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()