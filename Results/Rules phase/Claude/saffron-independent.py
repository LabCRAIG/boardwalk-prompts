class SaffronGame:
    def __init__(self):
        """Initialize the Saffron game with an 8x8 board and starting pieces."""
        # Create an 8x8 board filled with None
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place initial pieces diagonally opposite in the center
        # A at (3,3) and B at (4,4)
        self.board[3][3] = 'A'
        self.board[4][4] = 'B'
        
        # Keep track of piece positions
        self.a_position = (3, 3)
        self.b_position = (4, 4)
        
        # Player 1 starts
        self.current_player = 1
        
        # Game status
        self.game_over = False
        self.winner = None

    def print_board(self):
        """Display the current state of the board."""
        print("  0 1 2 3 4 5 6 7")
        print(" +-+-+-+-+-+-+-+-+")
        for i in range(8):
            row = f"{i}|"
            for j in range(8):
                cell = self.board[i][j]
                if cell is None:
                    row += " |"
                else:
                    row += f"{cell}|"
            print(row)
            print(" +-+-+-+-+-+-+-+-+")
        print(f"Current player: {self.current_player}")
        
    def is_valid_move(self, row, col):
        """Check if a move to the given position is valid."""
        # Check if position is within the board
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
            
        # Check if the position is empty or has a marker
        cell_content = self.board[row][col]
        if cell_content == 'A' or cell_content == 'B':
            return False
            
        # Check if the move is orthogonal to the current piece
        current_piece_pos = self.a_position if self.current_player == 1 else self.b_position
        row_diff = abs(row - current_piece_pos[0])
        col_diff = abs(col - current_piece_pos[1])
        
        # Move must be exactly one space horizontally, vertically, or diagonally
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
        
    def make_move(self, row, col):
        """Process a player's move to the given position."""
        if self.game_over:
            print("Game is already over!")
            return False
            
        if not self.is_valid_move(row, col):
            print("Invalid move!")
            return False
            
        # Get current piece information
        current_piece = 'A' if self.current_player == 1 else 'B'
        current_marker = 'a' if self.current_player == 1 else 'b'
        current_piece_pos = self.a_position if self.current_player == 1 else self.b_position
        
        # Place a marker at the old position
        self.board[current_piece_pos[0]][current_piece_pos[1]] = current_marker
        
        # Check if the new position has a marker (lose condition)
        if self.board[row][col] == 'a' or self.board[row][col] == 'b':
            # Current player loses
            self.game_over = True
            self.winner = 2 if self.current_player == 1 else 1
            
            # Move the piece anyway to show the losing move
            self.board[row][col] = current_piece
            if self.current_player == 1:
                self.a_position = (row, col)
            else:
                self.b_position = (row, col)
                
            print(f"Player {self.current_player} loses by moving onto a marker!")
            print(f"Player {self.winner} wins!")
            return True
            
        # Move the piece to the new position
        self.board[row][col] = current_piece
        if self.current_player == 1:
            self.a_position = (row, col)
        else:
            self.b_position = (row, col)
            
        # Switch players
        self.current_player = 2 if self.current_player == 1 else 1
        return True
        
    def get_valid_moves(self):
        """Return a list of valid moves for the current player."""
        valid_moves = []
        current_piece_pos = self.a_position if self.current_player == 1 else self.b_position
        row, col = current_piece_pos
        
        # Check all orthogonal positions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(new_row, new_col):
                valid_moves.append((new_row, new_col))
                
        return valid_moves

    def is_game_over(self):
        """Check if the game is over due to no valid moves."""
        if self.game_over:
            return True
            
        # Check if current player has any valid moves
        if not self.get_valid_moves():
            self.game_over = True
            self.winner = 2 if self.current_player == 1 else 1
            print(f"Player {self.current_player} has no valid moves!")
            print(f"Player {self.winner} wins!")
            return True
            
        return False


def play_game():
    """Function to play the Saffron game interactively."""
    game = SaffronGame()
    
    print("Welcome to Saffron!")
    print("Player 1 controls piece A, Player 2 controls piece B.")
    print("Each turn, move your piece one space orthogonally.")
    print("A marker is left behind when a piece moves.")
    print("If a player moves onto a marker, they lose.")
    
    while not game.game_over:
        game.print_board()
        
        # Check if game is over due to no valid moves
        if game.is_game_over():
            break
            
        valid_moves = game.get_valid_moves()
        print(f"Valid moves: {valid_moves}")
        
        try:
            row = int(input(f"Player {game.current_player}, enter row: "))
            col = int(input(f"Player {game.current_player}, enter column: "))
            game.make_move(row, col)
        except ValueError:
            print("Please enter valid numbers.")
    
    # Final board state
    game.print_board()
    if game.winner:
        print(f"Game over! Player {game.winner} wins!")
    
    
if __name__ == "__main__":
    play_game()


# Example usage in a non-interactive way
def example_game():
    """Example of a game played programmatically."""
    game = SaffronGame()
    print("Initial board:")
    game.print_board()
    
    # Make some moves
    moves = [
        (3, 4),  # Player 1 moves A
        (4, 3),  # Player 2 moves B
        (2, 4),  # Player 1 moves A
        (4, 2),  # Player 2 moves B
        (2, 3),  # Player 1 moves A
    ]
    
    for i, (row, col) in enumerate(moves):
        player = (i % 2) + 1
        print(f"\nPlayer {player} moves to ({row}, {col})")
        game.make_move(row, col)
        game.print_board()
        if game.game_over:
            break
            
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("Game is still in progress.")


# Uncomment to run the example game
# example_game()
