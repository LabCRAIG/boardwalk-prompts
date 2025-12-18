
class PegSolitaire:
    def __init__(self, board_type="english"):
        """Initialize the peg solitaire board.
        
        Args:
            board_type (str): Type of board layout ("english" is default)
        """
        self.board = self._initialize_board(board_type)
        self.moves = []
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    def _initialize_board(self, board_type):
        """Create the initial board configuration.
        
        Args:
            board_type (str): Type of board layout
            
        Returns:
            list: 2D representation of the board
        """
        if board_type == "english":
            # English board is 7x7 with some invalid positions in corners
            board = [
                [None, None, 1, 1, 1, None, None],
                [None, None, 1, 1, 1, None, None],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [None, None, 1, 1, 1, None, None],
                [None, None, 1, 1, 1, None, None]
            ]
            return board
        elif board_type == "european":
            # European board is 7x7
            board = [
                [None, None, 1, 1, 1, None, None],
                [None, 1, 1, 1, 1, 1, None],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [None, 1, 1, 1, 1, 1, None],
                [None, None, 1, 1, 1, None, None]
            ]
            return board
        else:
            # Default to english
            return self._initialize_board("english")
    
    def display_board(self):
        """Print the current state of the board."""
        symbols = {None: ' ', 0: '.', 1: 'O'}
        print("  " + " ".join(str(i) for i in range(len(self.board[0]))))
        
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(symbols[cell] for cell in row))
        print()
    
    def is_valid_position(self, row, col):
        """Check if a position is within the board boundaries and is a valid cell.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if the position is valid, False otherwise
        """
        if (0 <= row < len(self.board) and 
            0 <= col < len(self.board[0]) and 
            self.board[row][col] is not None):
            return True
        return False
    
    def get_valid_moves(self):
        """Find all valid moves on the current board.
        
        Returns:
            list: List of valid moves as tuples (from_row, from_col, to_row, to_col)
        """
        valid_moves = []
        
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                # Check if there's a peg at this position
                if not self.is_valid_position(row, col) or self.board[row][col] != 1:
                    continue
                
                # Check all four directions
                for dr, dc in self.directions:
                    # Position of the jumped peg
                    middle_row, middle_col = row + dr, col + dc
                    
                    # Position where the peg will land
                    target_row, target_col = row + 2*dr, col + 2*dc
                    
                    # Check if the move is valid
                    if (self.is_valid_position(middle_row, middle_col) and 
                        self.is_valid_position(target_row, target_col) and 
                        self.board[middle_row][middle_col] == 1 and 
                        self.board[target_row][target_col] == 0):
                        valid_moves.append((row, col, target_row, target_col))
        
        return valid_moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move on the board.
        
        Args:
            from_row (int): Starting row
            from_col (int): Starting column
            to_row (int): Target row
            to_col (int): Target column
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Calculate the middle position (jumped peg)
        middle_row = (from_row + to_row) // 2
        middle_col = (from_col + to_col) // 2
        
        # Check if move is valid
        if ((to_row, to_col) not in [(from_row+2, from_col), (from_row-2, from_col), 
                                    (from_row, from_col+2), (from_row, from_col-2)]):
            print("Invalid move: Can only move 2 spaces horizontally or vertically.")
            return False
            
        if not self.is_valid_position(from_row, from_col) or self.board[from_row][from_col] != 1:
            print("Invalid move: No peg at the starting position.")
            return False
            
        if not self.is_valid_position(middle_row, middle_col) or self.board[middle_row][middle_col] != 1:
            print("Invalid move: No peg to jump over.")
            return False
            
        if not self.is_valid_position(to_row, to_col) or self.board[to_row][to_col] != 0:
            print("Invalid move: Target position is not empty.")
            return False
        
        # Make the move
        self.board[from_row][from_col] = 0  # Remove peg from starting position
        self.board[middle_row][middle_col] = 0  # Remove jumped peg
        self.board[to_row][to_col] = 1  # Place peg at target position
        
        # Record the move
        self.moves.append((from_row, from_col, to_row, to_col))
        
        return True
    
    def count_pegs(self):
        """Count the number of pegs left on the board.
        
        Returns:
            int: Number of pegs
        """
        count = 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    count += 1
        return count
    
    def is_game_over(self):
        """Check if the game is over.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return len(self.get_valid_moves()) == 0
    
    def is_win(self):
        """Check if the game is won according to modified rules.
        
        Returns:
            bool: True if game is won (2 pegs left that can't capture each other), False otherwise
        """
        # Game is won if there are exactly 2 pegs left and no valid moves
        return self.count_pegs() == 2 and self.is_game_over()


def play_game():
    """Interactive function to play the game."""
    print("Welcome to Peg Solitaire!")
    print("The goal is to end with exactly 2 pegs that cannot capture each other.")
    
    board_type = input("Choose board type (english/european) [default: english]: ").lower() or "english"
    game = PegSolitaire(board_type)
    
    while not game.is_game_over():
        game.display_board()
        print(f"Pegs remaining: {game.count_pegs()}")
        
        valid_moves = game.get_valid_moves()
        print(f"Valid moves available: {len(valid_moves)}")
        
        # Display some valid moves as suggestions
        if valid_moves:
            print("Suggested moves (from_row, from_col, to_row, to_col):")
            for i, move in enumerate(valid_moves[:5]):  # Show up to 5 suggestions
                print(f"{i+1}. {move}")
        
        try:
            move_input = input("Enter your move as 'from_row from_col to_row to_col' (or 'q' to quit): ")
            
            if move_input.lower() == 'q':
                print("Quitting game...")
                break
                
            # Parse move
            from_row, from_col, to_row, to_col = map(int, move_input.split())
            
            # Make the move
            if not game.make_move(from_row, from_col, to_row, to_col):
                print("Invalid move. Try again.")
                
        except ValueError:
            print("Invalid input. Please enter four integers separated by spaces.")
        except KeyboardInterrupt:
            print("\nQuitting game...")
            break
    
    # Game over
    game.display_board()
    pegs_left = game.count_pegs()
    
    print(f"Game over! Pegs remaining: {pegs_left}")
    
    if game.is_win():
        print("Congratulations! You won the game with 2 pegs that cannot capture each other.")
    else:
        print("Game over. You didn't win this time.")


if __name__ == "__main__":
    play_game()
