import numpy as np
import sys

class PegSolitaire:
    def __init__(self):
        # Board representation:
        # 0 = invalid position, 1 = peg, 2 = empty
        self.board = np.array([
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]
        ], dtype=int)
        
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def print_board(self):
        """Print the current board state"""
        print("  0 1 2 3 4 5 6")
        for i in range(7):
            row_str = f"{i} "
            for j in range(7):
                if self.board[i, j] == 0:
                    row_str += "  "
                elif self.board[i, j] == 1:
                    row_str += "● "
                else:  # self.board[i, j] == 2
                    row_str += "○ "
            print(row_str)

    def is_valid_move(self, start, end):
        """Check if a move is valid"""
        start_row, start_col = start
        end_row, end_col = end
        
        # Check if positions are within bounds
        if not (0 <= start_row < 7 and 0 <= start_col < 7 and 
                0 <= end_row < 7 and 0 <= end_col < 7):
            return False
        
        # Check if start has a peg and end is empty
        if self.board[start_row, start_col] != 1 or self.board[end_row, end_col] != 2:
            return False
        
        # Check if move is exactly two steps in one direction
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        
        if (abs(row_diff) == 2 and col_diff == 0) or (row_diff == 0 and abs(col_diff) == 2):
            # Check if there's a peg to jump over
            mid_row = start_row + row_diff // 2
            mid_col = start_col + col_diff // 2
            
            if self.board[mid_row, mid_col] == 1:
                return True
        
        return False

    def make_move(self, start, end):
        """Execute a valid move"""
        if self.is_valid_move(start, end):
            start_row, start_col = start
            end_row, end_col = end
            
            # Calculate middle peg position
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            
            # Update board
            self.board[start_row, start_col] = 2  # Remove starting peg
            self.board[mid_row, mid_col] = 2      # Remove jumped peg
            self.board[end_row, end_col] = 1      # Place peg at destination
            return True
        return False

    def get_possible_moves(self):
        """Get all possible moves from the current board state"""
        moves = []
        for row in range(7):
            for col in range(7):
                if self.board[row, col] == 1:  # If there's a peg
                    for dr, dc in self.directions:
                        end_row, end_col = row + 2*dr, col + 2*dc
                        if self.is_valid_move((row, col), (end_row, end_col)):
                            moves.append(((row, col), (end_row, end_col)))
        return moves

    def count_pegs(self):
        """Count the number of pegs remaining on the board"""
        return np.sum(self.board == 1)

    def is_game_over(self):
        """Check if the game is over according to the modified win condition"""
        # If only two pegs remain and they can't capture each other, the game is won
        if self.count_pegs() == 2:
            # Check if the two pegs can capture each other
            pegs = [(i, j) for i in range(7) for j in range(7) if self.board[i, j] == 1]
            
            # Try all possible moves between the two pegs
            for i in range(2):
                for dr, dc in self.directions:
                    # Try to move peg i to capture the other peg
                    start = pegs[i]
                    end = (pegs[i][0] + 2*dr, pegs[i][1] + 2*dc)
                    
                    # If this move would capture the other peg, the game is not over
                    if (0 <= end[0] < 7 and 0 <= end[1] < 7 and 
                        self.board[end[0], end[1]] == 2 and  # End is empty
                        (pegs[1-i][0] == start[0] + dr and pegs[1-i][1] == start[1] + dc)):  # Other peg is in the middle
                        return False
            
            # No possible captures between the two pegs
            return True
        
        # If no moves are possible regardless of peg count, the game is over
        return len(self.get_possible_moves()) == 0

    def play(self):
        """Main game loop"""
        print("Welcome to Peg Solitaire!")
        print("The goal is to leave only two pegs that cannot capture each other.")
        print("Enter moves as 'start_row start_col end_row end_col'")
        print("For example: '3 1 3 3' to move from (3,1) to (3,3)")
        
        while True:
            print("\nCurrent board:")
            self.print_board()
            
            if self.is_game_over():
                if self.count_pegs() == 2:
                    print("Congratulations! You won with two pegs that cannot capture each other.")
                else:
                    print("Game over! No more moves possible.")
                break
            
            moves = self.get_possible_moves()
            print(f"\nPossible moves: {len(moves)}")
            
            # Get user input
            try:
                user_input = input("Enter your move (or 'quit' to exit): ").strip()
                if user_input.lower() == 'quit':
                    print("Thanks for playing!")
                    break
                
                coords = list(map(int, user_input.split()))
                if len(coords) != 4:
                    print("Please enter exactly four numbers.")
                    continue
                
                start = (coords[0], coords[1])
                end = (coords[2], coords[3])
                
                if self.make_move(start, end):
                    print("Move executed successfully.")
                else:
                    print("Invalid move. Please try again.")
                    
            except ValueError:
                print("Please enter valid numbers.")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                break

if __name__ == "__main__":
    game = PegSolitaire()
    game.play()