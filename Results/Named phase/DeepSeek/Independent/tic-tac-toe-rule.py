import numpy as np

class ModifiedTicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), ' ')
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("\n  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} {'|'.join(row)}")
            if i < 2:
                print("  -----")
        print()
    
    def make_move(self, row, col):
        if self.game_over:
            print("Game is already over!")
            return False
            
        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Invalid position! Row and column must be 0, 1, or 2.")
            return False
            
        if self.board[row, col] != ' ':
            print("That position is already taken!")
            return False
            
        self.board[row, col] = self.current_player
        
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
        # Check rows and columns (original rules without diagonals)
        for i in range(3):
            if all(self.board[i, :] == self.current_player):  # Check row
                return True
            if all(self.board[:, i] == self.current_player):  # Check column
                return True
        
        # Check for 2x2 squares (new rule)
        for i in range(2):
            for j in range(2):
                # Check each 2x2 block
                if (self.board[i, j] == self.current_player and
                    self.board[i, j+1] == self.current_player and
                    self.board[i+1, j] == self.current_player and
                    self.board[i+1, j+1] == self.current_player):
                    return True
                    
        return False
    
    def check_draw(self):
        return ' ' not in self.board
    
    def play(self):
        print("Welcome to Modified Tic-Tac-Toe!")
        print("Rules:")
        print("- Diagonals don't count for victory")
        print("- Filling any 2×2 square with your pieces wins the game")
        print("- Enter row and column numbers (0-2) separated by space")
        
        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            
            try:
                move = input("Enter your move (row col): ").split()
                if len(move) != 2:
                    print("Please enter exactly two numbers separated by space!")
                    continue
                    
                row, col = map(int, move)
                self.make_move(row, col)
                
            except ValueError:
                print("Please enter valid numbers (0-2)!")
        
        self.print_board()
        if self.winner:
            print(f"Congratulations! Player {self.winner} wins!")
        else:
            print("The game ended in a draw!")

# Start the game
if __name__ == "__main__":
    game = ModifiedTicTacToe()
    game.play()