from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Amethyst(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.last_capture_pos = None  # Track position of piece that made a capture
        
        # Initialize the board according to the setup
        initial_layout = (
            " O O O O\n"
            "O O O O \n"
            " O O O O\n"
            "_ _ _ _ \n"
            " _ _ _ _\n"
            "A A A A \n"
            " A A A A\n"
            "A A A A "
        )
        self.board = Board((8, 8), initial_layout)
        
    def get_piece_direction(self, piece):
        if piece == 'A':
            return -1  # Only moves upward (decreasing row)
        elif piece == 'O':
            return 1   # Only moves downward (increasing row)
        elif piece in ('Â', 'Ô'):
            return 0  # Can move both directions
        return None
        
    def is_own_piece(self, piece):
        if self.current_player == 1:
            return piece in ('A', 'Â')
        else:
            return piece in ('O', 'Ô')
            
    def can_promote(self, row, col):
        piece = self.board.layout[row][col]
        if piece == 'A' and row == 0:
            return True
        if piece == 'O' and row == self.board.height - 1:
            return True
        return False
        
    def promote_piece(self, row, col):
        piece = self.board.layout[row][col]
        if piece == 'A':
            self.board.place_piece(f"Â {row},{col}")
        elif piece == 'O':
            self.board.place_piece(f"Ô {row},{col}")
            
    def get_valid_moves(self, row, col, must_capture=False):
        moves = []
        piece = self.board.layout[row][col]
        if piece == ' ' or piece == '_':
            return moves
            
        # Check if we're forced to capture with this piece
        if must_capture and (row, col) != self.last_capture_pos:
            return moves
            
        # Determine allowed move directions
        directions = []
        piece_dir = self.get_piece_direction(piece)
        if piece_dir == -1:  # A (up only)
            directions.append((-1, -1))
            directions.append((-1, 1))
        elif piece_dir == 1:  # O (down only)
            directions.append((1, -1))
            directions.append((1, 1))
        else:  # Â or Ô (both directions)
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
            
        # Check for regular moves and captures
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                if self.board.layout[new_row][new_col] == '_':
                    if not must_capture:
                        moves.append((new_row, new_col, False))
                elif not self.is_own_piece(self.board.layout[new_row][new_col]):
                    # Check if we can capture
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if (0 <= jump_row < self.board.height and 
                        0 <= jump_col < self.board.width and
                        self.board.layout[jump_row][jump_col] == '_'):
                        moves.append((jump_row, jump_col, True))
                        
        return moves
        
    def has_any_valid_move(self, player):
        # Check if player has any valid moves (including captures)
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if (player == 1 and piece in ('A', 'Â')) or (player == 2 and piece in ('O', 'Ô')):
                    if self.get_valid_moves(row, col) or self.get_valid_moves(row, col, must_capture=True):
                        return True
        return False
        
    def count_pieces(self, player):
        count = 0
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if (player == 1 and piece in ('A', 'Â')) or (player == 2 and piece in ('O', 'Ô')):
                    count += 1
        return count
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_placement(move):
            return False  # No piece placements allowed in Amethyst
            
        if is_movement(move):
            (start_row, start_col), (end_row, end_col) = get_move_elements(move)
            
            # Basic position validation
            if not (0 <= start_row < self.board.height and 0 <= start_col < self.board.width and
                    0 <= end_row < self.board.height and 0 <= end_col < self.board.width):
                return False
                
            piece = self.board.layout[start_row][start_col]
            if piece == ' ' or piece == '_':
                return False
                
            if not self.is_own_piece(piece):
                return False
                
            # Check if we must capture
            must_capture = self.last_capture_pos is not None
            valid_moves = self.get_valid_moves(start_row, start_col, must_capture)
            
            # Check if the move is in valid moves
            for valid_move in valid_moves:
                if valid_move[0] == end_row and valid_move[1] == end_col:
                    return True
                    
        return False
        
    def perform_move(self, move):
        (start_row, start_col), (end_row, end_col) = get_move_elements(move)
        piece = self.board.layout[start_row][start_col]
        
        # Check if this is a capture move
        is_capture = abs(start_row - end_row) == 2
        
        # Perform the move
        self.board.move_piece(f"{start_row},{start_col} {end_row},{end_col}")
        
        # Handle captures
        if is_capture:
            # Remove the captured piece
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.board.place_piece(f"_ {mid_row},{mid_col}")
            self.last_capture_pos = (end_row, end_col)
            
        # Check for promotion
        if self.can_promote(end_row, end_col):
            self.promote_piece(end_row, end_col)
            
        # Reset capture tracking if no more captures
        if not is_capture or not self.get_valid_moves(end_row, end_col, must_capture=True):
            self.last_capture_pos = None
            self.current_player = 3 - self.current_player  # Switch player
            
    def game_finished(self):
        opponent = 3 - self.current_player
        return (self.count_pieces(opponent) == 0 or 
                not self.has_any_valid_move(opponent))
                
    def get_winner(self):
        opponent = 3 - self.current_player
        if self.count_pieces(opponent) == 0 or not self.has_any_valid_move(opponent):
            return self.current_player
        return None
        
    def next_player(self):
        return self.current_player  # Handled in perform_move due to capture rules
        
    def prompt_current_player(self):
        print(f"Player {self.current_player}'s turn")
        if self.last_capture_pos:
            print(f"Must continue capturing with piece at {self.last_capture_pos}")
        return input("Enter your move (format: 'start_row,start_col end_row,end_col'): ")
        
    def finish_message(self, winner):
        print(f"\nPlayer {winner} wins!")
        print("Final board:")


if __name__ == '__main__':
    initial_layout = (
        " O O O O\n"
        "O O O O \n"
        " O O O O\n"
        "_ _ _ _ \n"
        " _ _ _ _\n"
        "A A A A \n"
        " A A A A\n"
        "A A A A "
    )
    board = Board((8, 8), initial_layout)
    game = Amethyst(board)
    game.game_loop()
