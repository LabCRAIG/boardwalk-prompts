import sys

class PegSolitaire:
    def __init__(self, board_type='english'):
        """Initialize the game board"""
        self.board_types = {
            'english': [
                [' ', ' ', 'X', 'X', 'X', ' ', ' '],
                [' ', ' ', 'X', 'X', 'X', ' ', ' '],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'O', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                [' ', ' ', 'X', 'X', 'X', ' ', ' '],
                [' ', ' ', 'X', 'X', 'X', ' ', ' ']
            ],
            'european': [
                [' ', ' ', 'X', 'X', 'X', ' ', ' '],
                [' ', 'X', 'X', 'X', 'X', 'X', ' '],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'O', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                [' ', 'X', 'X', 'X', 'X', 'X', ' '],
                [' ', ' ', 'X', 'X', 'X', ' ', ' ']
            ]
        }
        
        if board_type.lower() in self.board_types:
            self.board = [row[:] for row in self.board_types[board_type.lower()]]
        else:
            self.board = [row[:] for row in self.board_types['english']]
        
        self.size = len(self.board)
        self.pegs_remaining = sum(row.count('X') for row in self.board)
        self.directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

    def print_board(self):
        """Print the current game board"""
        print("\n   " + " ".join(str(i) for i in range(self.size)))
        for i, row in enumerate(self.board):
            print(f"{i}  " + " ".join(cell for cell in row))
        print(f"\nPegs remaining: {self.pegs_remaining}\n")

    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_valid_move(self, start_row, start_col, direction):
        """Check if a move is valid"""
        # Check if start position has a peg
        if not self.is_valid_position(start_row, start_col) or self.board[start_row][start_col] != 'X':
            return False
        
        # Get direction vector
        dr, dc = self.directions.get(direction, (0, 0))
        if dr == 0 and dc == 0:  # Invalid direction
            return False
        
        # Calculate mid and end positions
        mid_row, mid_col = start_row + dr, start_col + dc
        end_row, end_col = start_row + 2*dr, start_col + 2*dc
        
        # Check if positions are valid and have correct pegs
        if (self.is_valid_position(mid_row, mid_col) and 
            self.is_valid_position(end_row, end_col) and 
            self.board[mid_row][mid_col] == 'X' and 
            self.board[end_row][end_col] == 'O'):
            return True
        
        return False

    def make_move(self, start_row, start_col, direction):
        """Execute a valid move"""
        if not self.is_valid_move(start_row, start_col, direction):
            return False
        
        dr, dc = self.directions[direction]
        
        # Update the board
        self.board[start_row][start_col] = 'O'  # Remove starting peg
        self.board[start_row + dr][start_col + dc] = 'O'  # Remove jumped peg
        self.board[start_row + 2*dr][start_col + 2*dc] = 'X'  # Place peg in new position
        
        self.pegs_remaining -= 1
        return True

    def is_game_over(self):
        """Check if the game is over (no more valid moves)"""
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 'X':
                    for direction in self.directions:
                        if self.is_valid_move(row, col, direction):
                            return False
        return True

    def has_won(self):
        """Check if player has won (only one peg left in center)"""
        center = self.size // 2
        return (self.pegs_remaining == 1 and 
                self.board[center][center] == 'X')

    def get_possible_moves(self):
        """Return a list of all possible moves"""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 'X':
                    for direction in self.directions:
                        if self.is_valid_move(row, col, direction):
                            moves.append((row, col, direction))
        return moves

def get_user_input(prompt, valid_options=None):
    """Helper function to get and validate user input"""
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")

def play_game():
    """Main game loop"""
    print("Welcome to Peg Solitaire!")
    
    # Choose board type
    board_type = get_user_input(
        "Choose board type (English/European): ", 
        ['english', 'european']
    )
    
    game = PegSolitaire(board_type)
    
    while True:
        game.print_board()
        
        if game.is_game_over():
            if game.has_won():
                print("Congratulations! You won!")
            else:
                print("Game over! No more valid moves.")
            break
        
        # Show possible moves
        moves = game.get_possible_moves()
        print("Possible moves:")
        for i, (row, col, direction) in enumerate(moves, 1):
            print(f"{i}: Move peg at ({row}, {col}) {direction}")
        
        # Get user move choice
        choice = get_user_input(
            "Enter move number or 'q' to quit: ",
            [str(i) for i in range(1, len(moves)+1)] + ['q']
        )
        
        if choice == 'q':
            print("Thanks for playing!")
            break
        
        # Execute the chosen move
        row, col, direction = moves[int(choice)-1]
        if game.make_move(row, col, direction):
            print(f"Moved peg from ({row}, {col}) {direction}")
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    play_game()