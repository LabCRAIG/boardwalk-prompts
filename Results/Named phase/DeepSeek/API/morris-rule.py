from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    WHITE = 0
    BLACK = 1

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        self.white_pieces = 9
        self.black_pieces = 9
        self.white_on_board = 0
        self.black_on_board = 0
        self.phase = "placement"  # placement, movement, flying
        self.mills = set()
        
    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"Player {player_name}'s move: ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        try:
            if self.phase == "placement":
                if not is_placement(move):
                    return False
                piece, (row, col) = get_move_elements(move)
                if piece != ('W' if self.current_player == Player.WHITE.value else 'B'):
                    return False
                if self.board.layout[row, col] != '_':
                    return False
                return True
                    
            else:  # movement or flying
                if not is_movement(move):
                    return False
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                
                # Check if moving own piece
                current_piece = 'W' if self.current_player == Player.WHITE.value else 'B'
                if self.board.layout[from_row, from_col] != current_piece:
                    return False
                    
                # Check if destination is empty
                if self.board.layout[to_row, to_col] != '_':
                    return False
                    
                # For movement phase (not flying), check adjacent move
                if self.phase == "movement":
                    if not self._are_adjacent((from_row, from_col), (to_row, to_col)):
                        return False
                        
                return True
                
        except (ValueError, IndexError):
            return False
    
    def _are_adjacent(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) + abs(c1 - c2) == 1 and (r1 == r2 or c1 == c2)
    
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            
            if self.current_player == Player.WHITE.value:
                self.white_pieces -= 1
                self.white_on_board += 1
            else:
                self.black_pieces -= 1
                self.black_on_board += 1
                
            # Check for mill formation
            mill_formed = self._check_mill_formation((row, col))
            if mill_formed:
                print("Mill formed! You can remove an opponent's piece.")
                self._handle_mill_removal((row, col))
                
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            move_str = f"{from_row},{from_col} {to_row},{to_col}"
            self.board.move_piece(move_str)
            
            # Check for mill formation
            mill_formed = self._check_mill_formation((to_row, to_col))
            if mill_formed:
                print("Mill formed! You can remove an opponent's piece.")
                self._handle_mill_removal((to_row, to_col))
        
        # Update game phase
        self._update_phase()
    
    def _check_mill_formation(self, position):
        row, col = position
        piece = self.board.layout[row, col]
        
        # Check horizontal mill
        if col % 2 == 0:  # Even columns are potential horizontal mill positions
            if (self.board.layout[row, 0] == piece and 
                self.board.layout[row, 3] == piece and 
                self.board.layout[row, 6] == piece):
                square = self._get_square_for_position(position)
                self.mills.add(('horizontal', row, square))
                return True
        
        # Check vertical mill  
        if row % 2 == 0:  # Even rows are potential vertical mill positions
            if (self.board.layout[0, col] == piece and 
                self.board.layout[3, col] == piece and 
                self.board.layout[6, col] == piece):
                square = self._get_square_for_position(position)
                self.mills.add(('vertical', col, square))
                return True
                
        return False
    
    def _get_square_for_position(self, position):
        row, col = position
        if row in [0, 6] or col in [0, 6]:
            return "outer"
        elif row in [1, 5] or col in [1, 5]:
            return "middle"
        else:
            return "inner"
    
    def _handle_mill_removal(self, mill_position):
        mill_square = self._get_square_for_position(mill_position)
        
        while True:
            try:
                remove_move = input("Enter position to remove (row,col): ")
                row, col = map(int, remove_move.split(','))
                
                # Check if valid removal
                opponent_piece = 'B' if self.current_player == Player.WHITE.value else 'W'
                if (self.board.layout[row, col] == opponent_piece and 
                    self._get_square_for_position((row, col)) == mill_square and
                    not self._is_in_mill((row, col))):
                    
                    self.board.layout[row, col] = '_'
                    if self.current_player == Player.WHITE.value:
                        self.black_on_board -= 1
                    else:
                        self.white_on_board -= 1
                    break
                else:
                    print("Invalid removal! Must remove opponent's piece from the same square and not in a mill.")
            except (ValueError, IndexError):
                print("Invalid format! Use row,col")
    
    def _is_in_mill(self, position):
        row, col = position
        piece = self.board.layout[row, col]
        
        # Check horizontal mill
        if col % 2 == 0:
            if (self.board.layout[row, 0] == piece and 
                self.board.layout[row, 3] == piece and 
                self.board.layout[row, 6] == piece):
                return True
        
        # Check vertical mill
        if row % 2 == 0:
            if (self.board.layout[0, col] == piece and 
                self.board.layout[3, col] == piece and 
                self.board.layout[6, col] == piece):
                return True
                
        return False
    
    def _update_phase(self):
        if self.white_on_board == 9 and self.black_on_board == 9:
            self.phase = "movement"
        
        # Check for flying phase
        if (self.current_player == Player.WHITE.value and self.white_on_board == 3) or \
           (self.current_player == Player.BLACK.value and self.black_on_board == 3):
            self.phase = "flying"
    
    def game_finished(self):
        if self.white_on_board < 3 or self.black_on_board < 3:
            return True
            
        # Check if current player has no valid moves
        current_piece = 'W' if self.current_player == Player.WHITE.value else 'B'
        for row in range(7):
            for col in range(7):
                if self.board.layout[row, col] == current_piece:
                    if self._has_valid_moves((row, col)):
                        return False
        return True
    
    def _has_valid_moves(self, position):
        row, col = position
        if self.phase == "flying":
            return True  # Can move anywhere
            
        # Check adjacent positions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < 7 and 0 <= new_col < 7 and 
                self.board.layout[new_row, new_col] == '_'):
                return True
        return False
    
    def get_winner(self):
        if self.white_on_board < 3:
            return Player.BLACK.value
        elif self.black_on_board < 3:
            return Player.WHITE.value
        return None
    
    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
    
    def initial_player(self):
        return Player.WHITE.value

if __name__ == '__main__':
    # Create the Nine Men's Morris board layout
    layout = """\
_ _ _ _ _ _ _
 _ _ _ _ _ _ 
  _ _ _ _ _  
_ _ _ _ _ _ _
  _ _ _ _ _  
 _ _ _ _ _ _ 
_ _ _ _ _ _ _"""
    
    board = Board((7, 7), layout)
    mygame = NineMensMorris(board)
    mygame.game_loop()