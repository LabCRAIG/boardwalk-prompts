class ReversiBoard:
    def __init__(self):
        # Initialize 8x8 board
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # Set up starting position
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'  # Black goes first
    
    def print_board(self):
        """Print the current state of the board"""
        print("  0 1 2 3 4 5 6 7")
        print(" +-+-+-+-+-+-+-+-+")
        for i in range(8):
            print(f"{i}|", end="")
            for j in range(8):
                print(f"{self.board[i][j]}|", end="")
            print("\n +-+-+-+-+-+-+-+-+")
    
    def is_valid_move(self, row, col):
        """Check if a move is valid for the current player"""
        # Check if position is on the board
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        
        # Check if position is empty
        if self.board[row][col] != ' ':
            return False
        
        # Other player's piece
        other = 'W' if self.current_player == 'B' else 'B'
        
        # Check all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        valid = False
        for dr, dc in directions:
            r, c = row + dr, col + dc
            # Skip if adjacent cell doesn't have opponent's piece
            if not (0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == other):
                continue
                
            # Continue in this direction
            r += dr
            c += dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == ' ':
                    break
                if self.board[r][c] == self.current_player:
                    valid = True
                    break
                r += dr
                c += dc
                
        return valid
    
    def get_valid_moves(self):
        """Return a list of valid moves for the current player"""
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves
    
    def make_move(self, row, col):
        """Make a move and flip appropriate pieces"""
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = self.current_player
        other = 'W' if self.current_player == 'B' else 'B'
        
        # Check all 8 directions and flip pieces
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            pieces_to_flip = []
            r, c = row + dr, col + dc
            
            # Continue in this direction to find pieces to flip
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == other:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
                
            # If we found a boundary piece of current player, flip all pieces
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for flip_r, flip_c in pieces_to_flip:
                    self.board[flip_r][flip_c] = self.current_player
        
        return True
    
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 'W' if self.current_player == 'B' else 'B'
    
    def get_score(self):
        """Count the pieces for each player"""
        black = sum(row.count('B') for row in self.board)
        white = sum(row.count('W') for row in self.board)
        return {'B': black, 'W': white}
    
    def is_game_over(self):
        """Check if the game is over"""
        # Game is over if neither player can make a move
        current_valid = self.get_valid_moves()
        if current_valid:
            return False
            
        # Check if other player has valid moves
        self.switch_player()
        other_valid = self.get_valid_moves()
        self.switch_player()  # Switch back
        
        return not other_valid

def play_reversi():
    game = ReversiBoard()
    
    while not game.is_game_over():
        game.print_board()
        valid_moves = game.get_valid_moves()
        
        if not valid_moves:
            print(f"No valid moves for {game.current_player}. Passing turn.")
            game.switch_player()
            continue
            
        print(f"Player {game.current_player}'s turn.")
        print(f"Valid moves: {valid_moves}")
        
        valid_input = False
        while not valid_input:
            try:
                row = int(input("Enter row (0-7): "))
                col = int(input("Enter column (0-7): "))
                
                if game.is_valid_move(row, col):
                    valid_input = True
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter numbers between 0 and 7.")
        
        game.make_move(row, col)
        game.switch_player()
    
    # Game over
    game.print_board()
    score = game.get_score()
    print(f"Game over! Final score: Black: {score['B']}, White: {score['W']}")
    
    if score['B'] > score['W']:
        print("Black wins!")
    elif score['W'] > score['B']:
        print("White wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    print("Welcome to Reversi!")
    print("Black (B) goes first, White (W) goes second.")
    play_reversi()