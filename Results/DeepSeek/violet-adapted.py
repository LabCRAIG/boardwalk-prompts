from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Violet(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.initialize_pieces()
        
    def initialize_pieces(self):
        # Player 2's V pieces
        v_positions = [(0, 3), (0, 6), (3, 0), (3, 9)]
        for row, col in v_positions:
            self.board.place_piece(f"V {row},{col}")
            
        # Player 1's A pieces
        a_positions = [(6, 0), (6, 9), (9, 3), (9, 6)]
        for row, col in a_positions:
            self.board.place_piece(f"A {row},{col}")
    
    def prompt_current_player(self) -> str:
        print(f"Player {self.current_player}'s turn (controls {'A' if self.current_player == 1 else 'V'})")
        print("Enter your move as: 'from_row,from_col to_row,to_col shoot_row,shoot_col'")
        return input("Your move: ")
    
    def validate_move(self, move: str) -> bool:
        try:
            # Split into move and shoot components
            parts = move.split()
            if len(parts) != 3:
                return False
                
            move_part = f"{parts[0]} {parts[1]}"
            shoot_part = parts[2]
            
            # Validate movement part
            if not is_movement(move_part):
                return False
                
            (from_pos, to_pos) = get_move_elements(move_part)
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Check bounds
            if not (0 <= from_row < 10 and 0 <= from_col < 10 and 
                    0 <= to_row < 10 and 0 <= to_col < 10):
                return False
                
            # Check shooter piece belongs to current player
            piece = self.board.layout[from_row, from_col]
            if piece == '_' or piece == ' ':
                return False
            if (self.current_player == 1 and piece != 'A') or (self.current_player == 2 and piece != 'V'):
                return False
                
            # Check destination is empty
            if self.board.layout[to_row, to_col] != '_':
                return False
                
            # Check path is clear for move
            if not self.is_path_clear(from_pos, to_pos):
                return False
                
            # Validate shoot part
            try:
                shoot_pos = tuple(map(int, shoot_part.split(',')))
                shoot_row, shoot_col = shoot_pos
                if not (0 <= shoot_row < 10 and 0 <= shoot_col < 10):
                    return False
                    
                # Check shoot position is empty
                if self.board.layout[shoot_row, shoot_col] != '_':
                    return False
                    
                # Check path is clear for shot
                if not self.is_path_clear(to_pos, shoot_pos):
                    return False
                    
            except:
                return False
                
            return True
            
        except:
            return False
    
    def is_path_clear(self, start, end):
        """Check if path between start and end is clear (orthogonal or diagonal)"""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # Must be moving in straight line
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
            
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] or y != end[1]:
            if self.board.layout[x, y] != '_':
                return False
            x += step_x
            y += step_y
        return True
    
    def perform_move(self, move: str):
        # Split into move and shoot components
        parts = move.split()
        move_part = f"{parts[0]} {parts[1]}"
        shoot_part = parts[2]
        
        # Execute movement
        (from_pos, to_pos) = get_move_elements(move_part)
        self.board.move_piece(move_part)
        
        # Execute shot
        shoot_pos = tuple(map(int, shoot_part.split(',')))
        self.board.place_piece(f"X {shoot_pos[0]},{shoot_pos[1]}")
        
        # Check win condition
        opponent = 3 - self.current_player
        if not self.has_valid_moves(opponent):
            self.game_over = True
            self.winner = self.current_player
        else:
            self.current_player = opponent
    
    def has_valid_moves(self, player):
        """Check if player has any valid moves remaining"""
        piece_char = 'A' if player == 1 else 'V'
        positions = np.argwhere(self.board.layout == piece_char)
        
        for (row, col) in positions:
            # Check all 8 possible directions
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                x, y = row + dx, col + dy
                while 0 <= x < 10 and 0 <= y < 10:
                    if self.board.layout[x, y] == '_':
                        # Found at least one valid move
                        return True
                    elif self.board.layout[x, y] != ' ':
                        # Path blocked
                        break
                    x += dx
                    y += dy
        return False
    
    def game_finished(self) -> bool:
        return hasattr(self, 'game_over') and self.game_over
    
    def get_winner(self):
        return self.winner if hasattr(self, 'winner') else None
    
    def next_player(self) -> int:
        return self.current_player  # Updated in perform_move
    
    def finish_message(self, winner):
        if winner:
            print(f"\nPlayer {winner} wins!")
        else:
            print("\nGame ended in a draw!")


if __name__ == '__main__':
    # Create initial empty board
    layout = ""
    for _ in range(10):
        layout += '_' * 10 + '\n'
    board = Board((10, 10), layout.strip())
    
    # Create and start game
    game = Violet(board)
    game.game_loop()
