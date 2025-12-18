
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    BLACK = 0
    WHITE = 1

class Checkers(Game):
    def __init__(self, board):
        super().__init__(board)
        self.directions = {
            Player.BLACK: [(1, -1), (1, 1)],
            Player.WHITE: [(-1, -1), (-1, 1)]
        }
        self.capture_directions = {
            Player.BLACK: [(2, -2), (2, 2)],
            Player.WHITE: [(-2, -2), (-2, 2)]
        }
        # Add backward directions for kings
        self.king_directions = {
            Player.BLACK: self.directions[Player.BLACK] + self.directions[Player.WHITE],
            Player.WHITE: self.directions[Player.WHITE] + self.directions[Player.BLACK]
        }
        self.king_capture_directions = {
            Player.BLACK: self.capture_directions[Player.BLACK] + self.capture_directions[Player.WHITE],
            Player.WHITE: self.capture_directions[Player.WHITE] + self.capture_directions[Player.BLACK]
        }
        self.piece_chars = {
            Player.BLACK: ['b', 'B'],  # regular, king
            Player.WHITE: ['w', 'W']   # regular, king
        }
        self.captures_available = False
    
    def initial_player(self):
        return Player.BLACK.value
    
    def is_king(self, piece):
        return piece in ['B', 'W']
    
    def get_piece_owner(self, piece):
        if piece in ['b', 'B']:
            return Player.BLACK.value
        elif piece in ['w', 'W']:
            return Player.WHITE.value
        return None
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
        
        origin, destination = get_move_elements(move)
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Check if origin has a piece of the current player
        piece = self.board.layout[o_row][o_col]
        if self.get_piece_owner(piece) != self.current_player:
            return False
        
        # Check if destination is empty
        if self.board.layout[d_row][d_col] != '_':
            return False
        
        # Calculate move direction
        row_diff = d_row - o_row
        col_diff = d_col - o_col
        
        # Check if captures are available
        if self.captures_available:
            # If captures are available, the move must be a capture
            if (row_diff, col_diff) not in self.king_capture_directions[Player(self.current_player)] if self.is_king(piece) else self.capture_directions[Player(self.current_player)]:
                return False
                
            # Check if there's an opponent's piece to capture
            captured_row = o_row + row_diff // 2
            captured_col = o_col + col_diff // 2
            captured_piece = self.board.layout[captured_row][captured_col]
            
            if self.get_piece_owner(captured_piece) != (1 - self.current_player):
                return False
                
            return True
        
        # No captures available, check regular moves
        # First check if this is a single diagonal move
        if self.is_king(piece):
            # Kings can move in any diagonal direction
            if (row_diff, col_diff) not in self.king_directions[Player(self.current_player)]:
                # Check if it's a capture move
                if (row_diff, col_diff) in self.king_capture_directions[Player(self.current_player)]:
                    # Check if there's an opponent's piece to capture
                    captured_row = o_row + row_diff // 2
                    captured_col = o_col + col_diff // 2
                    captured_piece = self.board.layout[captured_row][captured_col]
                    
                    if self.get_piece_owner(captured_piece) == (1 - self.current_player):
                        return True
                return False
        else:
            # Regular pieces can only move forward
            if (row_diff, col_diff) not in self.directions[Player(self.current_player)]:
                # Check if it's a capture move
                if (row_diff, col_diff) in self.capture_directions[Player(self.current_player)]:
                    # Check if there's an opponent's piece to capture
                    captured_row = o_row + row_diff // 2
                    captured_col = o_col + col_diff // 2
                    captured_piece = self.board.layout[captured_row][captured_col]
                    
                    if self.get_piece_owner(captured_piece) == (1 - self.current_player):
                        return True
                return False
                
        return True
    
    def perform_move(self, move):
        origin, destination = get_move_elements(move)
        o_row, o_col = origin
        d_row, d_col = destination
        piece = self.board.layout[o_row][o_col]
        
        # Perform the basic move
        super().perform_move(move)
        
        # Check if it's a capture move
        row_diff = d_row - o_row
        col_diff = d_col - o_col
        
        if abs(row_diff) == 2 and abs(col_diff) == 2:
            captured_row = o_row + row_diff // 2
            captured_col = o_col + col_diff // 2
            captured_piece = self.board.layout[captured_row][captured_col]
            
            # Special rule: if a king captures another king, both are removed
            if self.is_king(piece) and self.is_king(captured_piece):
                # Remove both kings
                self.board.place_piece(f"_ {d_row},{d_col}")
                self.board.place_piece(f"_ {captured_row},{captured_col}")
            else:
                # Regular capture - just remove the captured piece
                self.board.place_piece(f"_ {captured_row},{captured_col}")
        
        # Check for promotion - reaching the opposite end of the board
        if not self.is_king(piece):
            if (self.current_player == Player.BLACK.value and d_row == self.board.height - 1) or \
               (self.current_player == Player.WHITE.value and d_row == 0):
                # Promote to king
                king_piece = 'B' if self.current_player == Player.BLACK.value else 'W'
                self.board.place_piece(f"{king_piece} {d_row},{d_col}")
        
        # Update the captures_available flag for the next player
        self.captures_available = self.player_has_captures(1 - self.current_player)
    
    def player_has_captures(self, player):
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if self.get_piece_owner(piece) == player:
                    capture_dirs = self.king_capture_directions[Player(player)] if self.is_king(piece) else self.capture_directions[Player(player)]
                    
                    for dr, dc in capture_dirs:
                        captured_row = row + dr // 2
                        captured_col = col + dc // 2
                        dest_row = row + dr
                        dest_col = col + dc
                        
                        # Check bounds
                        if 0 <= dest_row < self.board.height and 0 <= dest_col < self.board.width and \
                           0 <= captured_row < self.board.height and 0 <= captured_col < self.board.width:
                            # Check if there's an opponent's piece to capture and the destination is empty
                            captured_piece = self.board.layout[captured_row][captured_col]
                            if self.get_piece_owner(captured_piece) == (1 - player) and \
                               self.board.layout[dest_row][dest_col] == '_':
                                return True
        return False
    
    def player_has_moves(self, player):
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if self.get_piece_owner(piece) == player:
                    move_dirs = self.king_directions[Player(player)] if self.is_king(piece) else self.directions[Player(player)]
                    
                    for dr, dc in move_dirs:
                        dest_row = row + dr
                        dest_col = col + dc
                        
                        # Check bounds
                        if 0 <= dest_row < self.board.height and 0 <= dest_col < self.board.width:
                            # Check if the destination is empty
                            if self.board.layout[dest_row][dest_col] == '_':
                                return True
                    
                    # Also check for captures
                    capture_dirs = self.king_capture_directions[Player(player)] if self.is_king(piece) else self.capture_directions[Player(player)]
                    
                    for dr, dc in capture_dirs:
                        captured_row = row + dr // 2
                        captured_col = col + dc // 2
                        dest_row = row + dr
                        dest_col = col + dc
                        
                        # Check bounds
                        if 0 <= dest_row < self.board.height and 0 <= dest_col < self.board.width and \
                           0 <= captured_row < self.board.height and 0 <= captured_col < self.board.width:
                            # Check if there's an opponent's piece to capture and the destination is empty
                            captured_piece = self.board.layout[captured_row][captured_col]
                            if self.get_piece_owner(captured_piece) == (1 - player) and \
                               self.board.layout[dest_row][dest_col] == '_':
                                return True
        return False
    
    def count_pieces(self, player):
        count = 0
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if self.get_piece_owner(piece) == player:
                    count += 1
        return count
    
    def game_finished(self):
        # Game is finished if one player has no pieces or no valid moves
        black_pieces = self.count_pieces(Player.BLACK.value)
        white_pieces = self.count_pieces(Player.WHITE.value)
        
        if black_pieces == 0 or white_pieces == 0:
            return True
        
        # Check if next player has any valid moves
        next_player = self.next_player()
        return not self.player_has_moves(next_player)
    
    def get_winner(self):
        black_pieces = self.count_pieces(Player.BLACK.value)
        white_pieces = self.count_pieces(Player.WHITE.value)
        
        if black_pieces == 0:
            return Player.WHITE.value
        elif white_pieces == 0:
            return Player.BLACK.value
        
        # If next player has no valid moves, current player wins
        next_player = self.next_player()
        if not self.player_has_moves(next_player):
            return self.current_player
        
        # No winner yet
        return None
    
    def next_player(self):
        return 1 - self.current_player
    
    def finish_message(self, winner):
        if winner == Player.BLACK.value:
            print("Black player wins!")
        else:
            print("White player wins!")
    
    def get_state(self):
        state = super().get_state()
        state[2].append(self.captures_available)
        return state

if __name__ == '__main__':
    # Initialize an 8x8 checkers board
    initial_layout = "_ b _ b _ b _ b\n" + \
                     "b _ b _ b _ b _\n" + \
                     "_ b _ b _ b _ b\n" + \
                     "_ _ _ _ _ _ _ _\n" + \
                     "_ _ _ _ _ _ _ _\n" + \
                     "w _ w _ w _ w _\n" + \
                     "_ w _ w _ w _ w\n" + \
                     "w _ w _ w _ w _"
    
    board = Board((8, 8), initial_layout)
    mygame = Checkers(board)
    mygame.game_loop()
