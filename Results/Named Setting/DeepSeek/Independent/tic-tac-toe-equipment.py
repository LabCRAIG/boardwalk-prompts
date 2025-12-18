import numpy as np

class TicTacToe5x5:
    def __init__(self):
        self.board = np.full((5, 5), ' ')
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("\n  0 1 2 3 4")
        for i, row in enumerate(self.board):
            print(i, end=" ")
            print("|".join(row))
            if i < 4:
                print("  -----")
    
    def make_move(self, row, col):
        if self.game_over:
            print("Game is already over!")
            return False
            
        if row < 0 or row > 4 or col < 0 or col > 4:
            print("Invalid position! Row and column must be between 0 and 4.")
            return False
            
        if self.board[row][col] != ' ':
            print("That position is already taken!")
            return False
            
        self.board[row][col] = self.current_player
        
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
            print(f"Player {self.current_player} wins!")
            return True
            
        if self.check_draw():
            self.game_over = True
            print("It's a draw!")
            return True
            
        self.switch_player()
        return True
    
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_win(self):
        # Check rows
        for row in range(5):
            for col in range(1):
                if (self.board[row][col] == self.current_player and
                    self.board[row][col+1] == self.current_player and
                    self.board[row][col+2] == self.current_player and
                    self.board[row][col+3] == self.current_player and
                    self.board[row][col+4] == self.current_player):
                    return True
        
        # Check columns
        for col in range(5):
            for row in range(1):
                if (self.board[row][col] == self.current_player and
                    self.board[row+1][col] == self.current_player and
                    self.board[row+2][col] == self.current_player and
                    self.board[row+3][col] == self.current_player and
                    self.board[row+4][col] == self.current_player):
                    return True
        
        # Check diagonals (top-left to bottom-right)
        for row in range(1):
            for col in range(1):
                if (self.board[row][col] == self.current_player and
                    self.board[row+1][col+1] == self.current_player and
                    self.board[row+2][col+2] == self.current_player and
                    self.board[row+3][col+3] == self.current_player and
                    self.board[row+4][col+4] == self.current_player):
                    return True
        
        # Check diagonals (top-right to bottom-left)
        for row in range(1):
            for col in range(4, 5):
                if (self.board[row][col] == self.current_player and
                    self.board[row+1][col-1] == self.current_player and
                    self.board[row+2][col-2] == self.current_player and
                    self.board[row+3][col-3] == self.current_player and
                    self.board[row+4][col-4] == self.current_player):
                    return True
        
        return False
    
    def check_draw(self):
        return ' ' not in self.board
    
    def play(self):
        print("Welcome to 5x5 Tic-Tac-Toe!")
        print("Get 5 in a row to win. Enter row and column numbers (0-4).")
        
        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn.")
            
            try:
                row = int(input("Enter row (0-4): "))
                col = int(input("Enter column (0-4): "))
                self.make_move(row, col)
            except ValueError:
                print("Please enter valid numbers between 0 and 4!")
        
        self.print_board()
        if self.winner:
            print(f"Congratulations! Player {self.winner} wins!")
        else:
            print("The game ended in a draw!")

# Start the game
if __name__ == "__main__":
    game = TicTacToe5x5()
    game.play()