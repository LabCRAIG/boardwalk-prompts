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
        self.phase = "placement"  # placement, movement, or flying
        self.mill_formed = False
        self.current_player = Player.WHITE.value

    def initial_player(self):
        return Player.WHITE.value

    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        if self.phase == "placement":
            prompt = f"Player {player_name} (Placement): "
        elif self.phase == "movement" or self.phase == "flying":
            prompt = f"Player {player_name} (Movement): "
        return input(prompt)

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        try:
            if is_placement(move):
                if self.phase != "placement":
                    return False
                
                piece, (row, col) = get_move_elements(move)
                player_char = 'W' if self.current_player == Player.WHITE.value else 'B'
                
                if piece != player_char:
                    return False
                
                # Check if position is empty
                if self.board.layout[row, col] != '_':
                    return False
                
                # Check if player has pieces left to place
                if (self.current_player == Player.WHITE.value and self.white_pieces <= 0) or \
                   (self.current_player == Player.BLACK.value and self.black_pieces <= 0):
                    return False
                
                return True

            elif is_movement(move):
                if self.phase not in ["movement", "flying"]:
                    return False
                
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                
                # Check if moving own piece
                player_char = 'W' if self.current_player == Player.WHITE.value else 'B'
                if self.board.layout[from_row, from_col] != player_char:
                    return False
                
                # Check if destination is empty
                if self.board.layout[to_row, to_col] != '_':
                    return False
                
                # Check if valid move (adjacent or flying)
                if self.phase == "movement":
                    if not self._are_positions_adjacent(from_row, from_col, to_row, to_col):
                        return False
                
                return True

            else:
                # Check for removal move (after mill formation)
                if self.mill_formed and move.count(' ') == 0 and move.count(',') == 1:
                    try:
                        coords = move.split(',')
                        row, col = int(coords[0]), int(coords[1])
                        
                        # Check if position has opponent's piece
                        opponent_char = 'B' if self.current_player == Player.WHITE.value else 'W'
                        if self.board.layout[row, col] == opponent_char:
                            # Check if piece is not in mill (or all pieces are in mills)
                            if not self._is_piece_in_mill(row, col) or self._all_pieces_in_mills(opponent_char):
                                return True
                    except:
                        return False
                
                return False

        except (ValueError, IndexError):
            return False

    def perform_move(self, move):
        if self.mill_formed and move.count(' ') == 0 and move.count(',') == 1:
            # Remove opponent's piece
            coords = move.split(',')
            row, col = int(coords[0]), int(coords[1])
            opponent_char = 'B' if self.current_player == Player.WHITE.value else 'W'
            self.board.layout[row, col] = '_'
            
            if opponent_char == 'W':
                self.white_on_board -= 1
            else:
                self.black_on_board -= 1
                
            self.mill_formed = False
            return

        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            
            if piece == 'W':
                self.white_pieces -= 1
                self.white_on_board += 1
            else:
                self.black_pieces -= 1
                self.black_on_board += 1
                
            # Check for mill formation
            if self._check_mill_formation(row, col, piece):
                self.mill_formed = True
            else:
                self.mill_formed = False

        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            piece = self.board.layout[from_row, from_col]
            self.board.layout[from_row, from_col] = '_'
            self.board.layout[to_row, to_col] = piece
            
            # Check for mill formation
            if self._check_mill_formation(to_row, to_col, piece):
                self.mill_formed = True
            else:
                self.mill_formed = False

        # Update game phase
        self._update_game_phase()

    def game_finished(self):
        # Game ends when a player has less than 3 pieces or cannot make a move
        if self.white_on_board < 3 or self.black_on_board < 3:
            return True
        
        # Check if current player has valid moves
        if not self._has_valid_moves():
            return True
            
        return False

    def get_winner(self):
        if self.white_on_board < 3:
            return Player.BLACK.value
        elif self.black_on_board < 3:
            return Player.WHITE.value
        elif not self._has_valid_moves():
            # Current player cannot move, so opponent wins
            return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        return None

    def next_player(self):
        if self.mill_formed:
            return self.current_player  # Same player gets another turn for removal
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value

    def round_counter(self):
        if self.mill_formed:
            return self.round  # Same round for removal move
        return self.round + 1

    def finish_message(self, winner):
        if winner is not None:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"Player {winner_name} wins!")
        else:
            print("The game ended in a draw!")

    def get_state(self):
        base_state = super().get_state()
        additional_params = [
            self.white_pieces,
            self.black_pieces,
            self.white_on_board,
            self.black_on_board,
            self.phase,
            self.mill_formed
        ]
        return (base_state[0], base_state[1], additional_params)

    def _are_positions_adjacent(self, r1, c1, r2, c2):
        # Define valid connections for Nine Men's Morris board
        connections = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 0): [(0, 0), (3, 1), (6, 0)],
            (3, 1): [(1, 1), (3, 0), (3, 2), (5, 1)],
            (3, 2): [(2, 2), (3, 1), (3, 4), (4, 2)],
            (3, 4): [(2, 4), (3, 2), (3, 5), (4, 4)],
            (3, 5): [(1, 5), (3, 4), (3, 6), (5, 5)],
            (3, 6): [(0, 6), (3, 5), (6, 6)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (5, 3)],
            (4, 4): [(3, 4), (4, 3)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(4, 3), (5, 1), (5, 5), (6, 3)],
            (5, 5): [(3, 5), (5, 3)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(5, 3), (6, 0), (6, 6)],
            (6, 6): [(3, 6), (6, 3)]
        }
        
        return (r2, c2) in connections.get((r1, c1), [])

    def _check_mill_formation(self, row, col, piece):
        # Check horizontal mills
        if col % 3 == 0:  # Left column of mill
            if (self.board.layout[row, col] == piece and 
                self.board.layout[row, col+1] == piece and 
                self.board.layout[row, col+2] == piece):
                return True
        elif col % 3 == 2:  # Right column of mill
            if (self.board.layout[row, col] == piece and 
                self.board.layout[row, col-1] == piece and 
                self.board.layout[row, col-2] == piece):
                return True
        
        # Check vertical mills
        if row % 3 == 0:  # Top row of mill
            if (self.board.layout[row, col] == piece and 
                self.board.layout[row+1, col] == piece and 
                self.board.layout[row+2, col] == piece):
                return True
        elif row % 3 == 2:  # Bottom row of mill
            if (self.board.layout[row, col] == piece and 
                self.board.layout[row-1, col] == piece and 
                self.board.layout[row-2, col] == piece):
                return True
        
        # Check special center mills (for the inner rings)
        if (row, col) == (1, 3) or (row, col) == (3, 1) or (row, col) == (3, 5) or (row, col) == (5, 3):
            # Check all four directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                r1, c1 = row + dr, col + dc
                r2, c2 = row - dr, col - dc
                if (0 <= r1 < 7 and 0 <= c1 < 7 and 0 <= r2 < 7 and 0 <= c2 < 7 and
                    self.board.layout[r1, c1] == piece and self.board.layout[r2, c2] == piece):
                    return True
        
        return False

    def _is_piece_in_mill(self, row, col):
        piece = self.board.layout[row, col]
        if piece == '_':
            return False
        return self._check_mill_formation(row, col, piece)

    def _all_pieces_in_mills(self, piece_char):
        # Check if all opponent's pieces are in mills
        for row in range(7):
            for col in range(7):
                if self.board.layout[row, col] == piece_char:
                    if not self._is_piece_in_mill(row, col):
                        return False
        return True

    def _update_game_phase(self):
        if self.phase == "placement" and self.white_pieces == 0 and self.black_pieces == 0:
            self.phase = "movement"
        
        # Check if flying phase (player has only 3 pieces left)
        if self.phase == "movement":
            if (self.current_player == Player.WHITE.value and self.white_on_board <= 3) or \
               (self.current_player == Player.BLACK.value and self.black_on_board <= 3):
                self.phase = "flying"

    def _has_valid_moves(self):
        player_char = 'W' if self.current_player == Player.WHITE.value else 'B'
        
        if self.phase == "placement":
            # Check if any empty spaces remain
            return np.any(self.board.layout == '_')
        
        elif self.phase == "movement":
            # Check if any piece can move to adjacent empty space
            for row in range(7):
                for col in range(7):
                    if self.board.layout[row, col] == player_char:
                        # Check adjacent positions
                        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            new_row, new_col = row + dr, col + dc
                            if (0 <= new_row < 7 and 0 <= new_col < 7 and 
                                self.board.layout[new_row, new_col] == '_' and
                                self._are_positions_adjacent(row, col, new_row, new_col)):
                                return True
        
        elif self.phase == "flying":
            # Check if any empty space exists (can fly anywhere)
            return np.any(self.board.layout == '_')
        
        return False

if __name__ == '__main__':
    # Create Nine Men's Morris board (7x7 with specific layout)
    board_layout = """\
_ _ _ _ _ _ _
 _ _ _ _ _ _ 
  _ _ _ _ _  
_ _ _ _ _ _ _
  _ _ _ _ _  
 _ _ _ _ _ _ 
_ _ _ _ _ _ _"""
    
    board = Board((7, 7), board_layout)
    mygame = NineMensMorris(board)
    mygame.game_loop()