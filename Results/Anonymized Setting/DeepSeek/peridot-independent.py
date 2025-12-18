class Peridot:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("\n  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} {'|'.join(row)}")
            if i < 2:
                print("  -----")
    
    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
            
        piece = 'A' if self.current_player == 1 else 'V'
        self.board[row][col] = piece
        
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif self.is_board_full():
            self.game_over = True
        else:
            self.current_player = 2 if self.current_player == 1 else 1
            
        return True
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] != ' ' and all(cell == row[0] for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] != ' ' and all(self.board[row][col] == self.board[0][col] for row in range(3)):
                return True
        
        # Check diagonals
        if self.board[0][0] != ' ' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
        if self.board[0][2] != ' ' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True
        
        return False
    
    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)
    
    def play(self):
        print("Welcome to Peridot!")
        print("Player 1: A | Player 2: V")
        print("Enter your moves as row,col (e.g., 1,2)")
        
        while not self.game_over:
            self.print_board()
            player = self.current_player
            piece = 'A' if player == 1 else 'V'
            
            while True:
                try:
                    move = input(f"Player {player} ({piece}), enter your move: ")
                    row, col = map(int, move.split(','))
                    if self.make_move(row, col):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter your move as row,col (e.g., 1,2)")
        
        self.print_board()
        if self.winner:
            print(f"Player {self.winner} wins!")
        else:
            print("It's a tie!")

# Start the game
if __name__ == "__main__":
    game = Peridot()
    game.play()