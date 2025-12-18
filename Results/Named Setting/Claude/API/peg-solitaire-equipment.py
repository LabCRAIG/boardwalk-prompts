
from game import Game, Board, is_movement, is_placement, get_move_elements
from copy import deepcopy

class PegSolitaire(Game):
    def __init__(self, board):
        super().__init__(board)
        self.valid_moves = []
        self.update_valid_moves()
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
        
        # Parse move elements
        origin, destination = get_move_elements(move)
        
        # Check if origin has a peg
        if self.board.layout[origin[0]][origin[1]] != 'O':
            return False
        
        # Check if destination is empty
        if self.board.layout[destination[0]][destination[1]] != '_':
            return False
        
        # Calculate the midpoint (jumped position)
        midpoint = ((origin[0] + destination[0]) // 2, (origin[1] + destination[1]) // 2)
        
        # Check if midpoint has a peg
        if self.board.layout[midpoint[0]][midpoint[1]] != 'O':
            return False
        
        # Check if the move is exactly 2 spaces in a cardinal direction
        dx = abs(destination[0] - origin[0])
        dy = abs(destination[1] - origin[1])
        if not ((dx == 0 and dy == 2) or (dx == 2 and dy == 0)):
            return False
            
        return True
    
    def perform_move(self, move):
        origin, destination = get_move_elements(move)
        
        # Calculate the midpoint (jumped position)
        midpoint = ((origin[0] + destination[0]) // 2, (origin[1] + destination[1]) // 2)
        
        # Move the peg
        self.board.move_piece(move)
        
        # Remove the jumped peg (replace with blank)
        self.board.place_piece(f"_ {midpoint[0]},{midpoint[1]}")
        
        # Update valid moves after the board changes
        self.update_valid_moves()
    
    def update_valid_moves(self):
        self.valid_moves = []
        height, width = self.board.height, self.board.width
        
        for i in range(height):
            for j in range(width):
                if self.board.layout[i][j] == 'O':
                    # Check all four directions
                    for di, dj in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                        ni, nj = i + di, j + dj
                        mi, mj = i + di//2, j + dj//2
                        
                        if (0 <= ni < height and 0 <= nj < width and 
                            0 <= mi < height and 0 <= mj < width and
                            self.board.layout[ni][nj] == '_' and 
                            self.board.layout[mi][mj] == 'O'):
                            self.valid_moves.append(f"{i},{j} {ni},{nj}")
    
    def game_finished(self):
        return len(self.valid_moves) == 0
    
    def get_winner(self):
        # Count remaining pegs
        remaining_pegs = sum(1 for row in self.board.layout for cell in row if cell == 'O')
        
        if remaining_pegs == 1:
            return 1  # Perfect win
        else:
            return 0  # Game over but not perfect
    
    def next_player(self):
        return 0  # Single player game
    
    def prompt_current_player(self):
        print(f"Remaining pegs: {sum(1 for row in self.board.layout for cell in row if cell == 'O')}")
        print("Valid moves:")
        for i, move in enumerate(self.valid_moves):
            print(f"{i+1}. {move}")
        
        try:
            choice = int(input("Enter move number (or 0 to input manually): "))
            if choice == 0:
                return input("Your move (from_row,from_col to_row,to_col): ")
            else:
                return self.valid_moves[choice-1]
        except (ValueError, IndexError):
            return "invalid"
    
    def finish_message(self, winner):
        pegs_left = sum(1 for row in self.board.layout for cell in row if cell == 'O')
        if pegs_left == 1:
            print("Congratulations! You won with only one peg remaining!")
        else:
            print(f"Game over! You have {pegs_left} pegs remaining.")

if __name__ == '__main__':
    # Create a diamond-shaped board
    size = 7  # Adjust this for a larger/smaller diamond
    board_layout = ""
    
    for i in range(size):
        spaces_before = abs(size//2 - i)
        pegs_count = size - 2 * spaces_before
        
        row = " " * spaces_before + "O" * pegs_count + " " * spaces_before
        board_layout += row + "\n"
    
    # Make the center position empty
    mid = size // 2
    rows = board_layout.strip().split('\n')
    rows[mid] = rows[mid][:mid] + "_" + rows[mid][mid+1:]
    board_layout = "\n".join(rows)
    
    board = Board((size, size), board_layout)
    game = PegSolitaire(board)
    game.game_loop()
