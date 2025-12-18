import sys

class DiamondPegSolitaire:
    def __init__(self, size=5):
        """
        Initialize a diamond-shaped peg solitaire board.
        Size must be an odd number (default 5, creating a 5x5 diamond).
        """
        if size % 2 != 1:
            raise ValueError("Size must be an odd number")
        
        self.size = size
        self.board = []
        self.empty = 'O'
        self.peg = '●'
        self.removed = ' '
        
        # Create the diamond-shaped board
        mid = size // 2
        for row in range(size):
            cols = size - abs(row - mid) * 2
            offset = abs(row - mid)
            board_row = []
            for col in range(size):
                if col >= offset and col < offset + cols:
                    board_row.append(self.peg)
                else:
                    board_row.append(self.removed)
            self.board.append(board_row)
        
        # Set the center position to empty
        self.board[mid][mid] = self.empty
    
    def __str__(self):
        """String representation of the board for printing"""
        s = []
        for row in self.board:
            s.append(' '.join(row))
        return '\n'.join(s)
    
    def is_valid_position(self, row, col):
        """Check if position is within the diamond"""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        return self.board[row][col] != self.removed
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid"""
        # Check if positions are valid
        if not (self.is_valid_position(from_row, from_col) and 
                self.is_valid_position(to_row, to_col)):
            return False
        
        # Check if moving from peg to empty
        if (self.board[from_row][from_col] != self.peg or 
            self.board[to_row][to_col] != self.empty):
            return False
        
        # Check if moving exactly 2 positions in a straight line
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        if not ((row_diff == 2 and col_diff == 0) or 
                (row_diff == 0 and col_diff == 2)):
            return False
        
        # Check if there's a peg in between
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        
        if not self.is_valid_position(mid_row, mid_col):
            return False
        if self.board[mid_row][mid_col] != self.peg:
            return False
        
        return True
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Execute a move if it's valid"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        # Move the peg
        self.board[from_row][from_col] = self.empty
        self.board[to_row][to_col] = self.peg
        
        # Remove the jumped peg
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        self.board[mid_row][mid_col] = self.empty
        
        return True
    
    def get_possible_moves(self):
        """Return a list of all possible moves in format (from, over, to)"""
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.peg:
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if self.is_valid_move(row, col, new_row, new_col):
                            mid_row, mid_col = row + dr//2, col + dc//2
                            moves.append(((row, col), (mid_row, mid_col), (new_row, new_col)))
        return moves
    
    def is_game_over(self):
        """Check if the game is over (no more valid moves)"""
        return len(self.get_possible_moves()) == 0
    
    def count_pegs(self):
        """Count remaining pegs on the board"""
        return sum(row.count(self.peg) for row in self.board)
    
    def play_interactive(self):
        """Play the game interactively in the console"""
        print("Welcome to Diamond Peg Solitaire!")
        print("Enter moves as 'from_row from_col to_row to_col' (0-based indices)")
        print("Type 'q' to quit or 'h' for help\n")
        
        while True:
            print("\nCurrent board:")
            print(self)
            print(f"Pegs remaining: {self.count_pegs()}")
            
            if self.is_game_over():
                print("\nGame over!")
                if self.count_pegs() == 1:
                    print("Congratulations! You won!")
                else:
                    print(f"Better luck next time. {self.count_pegs()} pegs remain.")
                break
            
            user_input = input("\nEnter your move: ").strip().lower()
            
            if user_input == 'q':
                print("Quitting the game.")
                break
            elif user_input == 'h':
                print("\nHelp:")
                print("Enter moves as four numbers separated by spaces:")
                print("from_row from_col to_row to_col")
                print("Example: '2 2 0 2' to move from (2,2) over (1,2) to (0,2)")
                print("Type 'q' to quit or 'h' for help")
                continue
            
            try:
                coords = list(map(int, user_input.split()))
                if len(coords) != 4:
                    raise ValueError
                from_row, from_col, to_row, to_col = coords
                
                if self.make_move(from_row, from_col, to_row, to_col):
                    print("Move successful!")
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter four numbers or 'q'/'h'.")

if __name__ == "__main__":
    size = 5  # Default size (5x5 diamond)
    if len(sys.argv) > 1:
        try:
            size = int(sys.argv[1])
            if size % 2 != 1 or size < 3:
                raise ValueError
        except ValueError:
            print("Invalid size. Using default size 5 (must be odd number ≥ 3).")
            size = 5
    
    game = DiamondPegSolitaire(size)
    game.play_interactive()