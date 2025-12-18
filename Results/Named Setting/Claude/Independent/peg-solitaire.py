import os

class PegSolitaire:
    def __init__(self):
        # Initialize the board with the standard English layout
        # 0 = invalid position, 1 = peg, 2 = empty
        self.board = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]
        ]
        self.moves = []  # To track moves for undo functionality
        
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_board(self):
        """Display the current board state."""
        print("  0 1 2 3 4 5 6")
        for i, row in enumerate(self.board):
            print(f"{i} ", end="")
            for cell in row:
                if cell == 0:
                    print("  ", end="")
                elif cell == 1:
                    print("O ", end="")
                elif cell == 2:
                    print(". ", end="")
            print()
        print()
        
    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Check if a move is valid."""
        # Check if positions are on the board
        if not (0 <= start_row < 7 and 0 <= start_col < 7 and 
                0 <= end_row < 7 and 0 <= end_col < 7):
            return False
            
        # Check if start has a peg and end is empty
        if not (self.board[start_row][start_col] == 1 and 
                self.board[end_row][end_col] == 2):
            return False
            
        # Check if the move is horizontal or vertical and exactly 2 spaces apart
        if start_row == end_row and abs(start_col - end_col) == 2:
            # Check if there's a peg in between
            middle_col = (start_col + end_col) // 2
            return self.board[start_row][middle_col] == 1
        elif start_col == end_col and abs(start_row - end_row) == 2:
            # Check if there's a peg in between
            middle_row = (start_row + end_row) // 2
            return self.board[middle_row][start_col] == 1
        
        return False
        
    def make_move(self, start_row, start_col, end_row, end_col):
        """Execute a move if it's valid."""
        if self.is_valid_move(start_row, start_col, end_row, end_col):
            # Save the move for undo
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            self.moves.append((start_row, start_col, middle_row, middle_col, end_row, end_col))
            
            # Update the board
            self.board[start_row][start_col] = 2  # Empty the start
            self.board[middle_row][middle_col] = 2  # Remove the jumped peg
            self.board[end_row][end_col] = 1  # Place the peg at the end
            return True
        return False
        
    def undo_move(self):
        """Undo the last move."""
        if not self.moves:
            print("No moves to undo.")
            return False
            
        # Get the last move
        start_row, start_col, middle_row, middle_col, end_row, end_col = self.moves.pop()
        
        # Restore the board state
        self.board[start_row][start_col] = 1  # Put peg back at start
        self.board[middle_row][middle_col] = 1  # Restore jumped peg
        self.board[end_row][end_col] = 2  # Remove peg from end
        return True
        
    def get_valid_moves(self):
        """Get all valid moves for the current board state."""
        valid_moves = []
        for row in range(7):
            for col in range(7):
                # Check each of the four directions (up, down, left, right)
                directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                for d_row, d_col in directions:
                    end_row, end_col = row + d_row, col + d_col
                    if self.is_valid_move(row, col, end_row, end_col):
                        valid_moves.append((row, col, end_row, end_col))
        return valid_moves
        
    def is_game_over(self):
        """Check if the game is over (no more valid moves)."""
        return len(self.get_valid_moves()) == 0
        
    def count_pegs(self):
        """Count the number of pegs remaining on the board."""
        return sum(row.count(1) for row in self.board)
        
    def play(self):
        """Main game loop."""
        while not self.is_game_over():
            self.clear_screen()
            self.print_board()
            
            print(f"Pegs remaining: {self.count_pegs()}")
            print("Enter move as 'start_row start_col end_row end_col' (e.g., '3 1 3 3')")
            print("Or 'u' to undo, 'h' for hint, 'q' to quit")
            
            command = input("> ").strip().lower()
            
            if command == 'q':
                print("Quitting game. Thanks for playing!")
                return
            elif command == 'u':
                if not self.undo_move():
                    input("Press Enter to continue...")
            elif command == 'h':
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    hint = valid_moves[0]
                    print(f"Hint: Move from ({hint[0]},{hint[1]}) to ({hint[2]},{hint[3]})")
                else:
                    print("No valid moves available.")
                input("Press Enter to continue...")
            else:
                try:
                    coords = list(map(int, command.split()))
                    if len(coords) != 4:
                        raise ValueError
                    
                    start_row, start_col, end_row, end_col = coords
                    
                    if not self.make_move(start_row, start_col, end_row, end_col):
                        print("Invalid move. Try again.")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid input. Try again.")
                    input("Press Enter to continue...")
        
        # Game over
        self.clear_screen()
        self.print_board()
        pegs_left = self.count_pegs()
        print(f"Game over! You have {pegs_left} peg(s) remaining.")
        
        if pegs_left == 1:
            print("Congratulations! You won the game!")
        else:
            print("Try again to get down to just one peg!")
        
        input("Press Enter to exit...")

# Start the game
if __name__ == "__main__":
    game = PegSolitaire()
    game.play()