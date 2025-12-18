class TangerineGame:
    def __init__(self):
        self.board_size = 6
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("\n   " + " ".join(str(i) for i in range(self.board_size)))
        for i, row in enumerate(self.board):
            print(f"{i} |" + "|".join(cell for cell in row) + "|")
        print()
        
    def is_valid_move(self, row, col, piece_type):
        # Check if position is within bounds
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False
            
        # Check if space is free
        if self.board[row][col] != ' ':
            return False
            
        # Check adjacent space based on piece type
        if piece_type == 'H':
            if col + 1 >= self.board_size or self.board[row][col + 1] != ' ':
                return False
        elif piece_type == 'V':
            if row - 1 < 0 or self.board[row - 1][col] != ' ':
                return False
                
        return True
        
    def place_piece(self, row, col, piece_type):
        if piece_type == 'H':
            self.board[row][col] = 'H'
            self.board[row][col + 1] = 'H'
        elif piece_type == 'V':
            self.board[row][col] = 'V'
            self.board[row - 1][col] = 'V'
            
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        
    def check_game_over(self):
        # Check if current player has any valid moves left
        piece_type = 'H' if self.current_player == 1 else 'V'
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, piece_type):
                    return False
                    
        # If we get here, no valid moves left for current player
        self.game_over = True
        self.winner = 2 if self.current_player == 1 else 1
        return True
        
    def play(self):
        print("Welcome to Tangerine!")
        print("Player 1 places H pieces (horizontal)")
        print("Player 2 places V pieces (vertical)")
        print("Enter your move as 'row col' (e.g., '2 3')")
        
        while not self.game_over:
            self.print_board()
            piece_type = 'H' if self.current_player == 1 else 'V'
            print(f"Player {self.current_player}'s turn ({piece_type})")
            
            # Get player input
            while True:
                try:
                    move = input("Enter your move (row col): ").strip().split()
                    if len(move) != 2:
                        raise ValueError
                    row, col = map(int, move)
                    
                    if self.is_valid_move(row, col, piece_type):
                        self.place_piece(row, col, piece_type)
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter two numbers separated by space.")
            
            # Check if game is over
            if self.check_game_over():
                self.print_board()
                print(f"Player {self.winner} wins! Player {self.current_player} has no valid moves.")
            else:
                self.switch_player()
                
if __name__ == "__main__":
    game = TangerineGame()
    game.play()