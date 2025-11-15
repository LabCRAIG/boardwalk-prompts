from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Amethyst(Game):
    def __init__(self, board):
        super().__init__(board)
        self.must_continue_capturing = False
        self.last_moved_piece_pos = None
        self.move_directions = {
            'A': [(-1, -1), (-1, 1)],  # A can only move upward diagonally
            'O': [(1, -1), (1, 1)],    # O can only move downward diagonally
            'Â': [(-1, -1), (-1, 1), (1, -1), (1, 1)],  # Â can move in any diagonal direction
            'Ô': [(-1, -1), (-1, 1), (1, -1), (1, 1)]   # Ô can move in any diagonal direction
        }
        self.player_pieces = {
            Player.ONE: ['A', 'Â'],
            Player.TWO: ['O', 'Ô']
        }
    
    def initial_player(self):
        return Player.ONE.value
    
    def prompt_current_player(self):
        player_name = "ONE" if self.current_player == Player.ONE.value else "TWO"
        if self.must_continue_capturing:
            row, col = self.last_moved_piece_pos
            return input(f"Player {player_name} must continue capturing with piece at {row},{col}: ")
        return input(f"Player {player_name}'s move: ")
    
    def get_state(self):
        state = super().get_state()
        return (state[0], state[1], [self.must_continue_capturing, self.last_moved_piece_pos])
    
    def validate_move(self, move):
        if not super().validate_move(move):
            print("Invalid move format or out of bounds.")
            return False
        
        # If player must continue capturing, enforce that the origin is the last moved piece
        if self.must_continue_capturing:
            if not is_movement(move):
                print("You must continue capturing with the same piece.")
                return False
                
            origin, _ = get_move_elements(move)
            if origin != self.last_moved_piece_pos:
                print(f"You must continue capturing with the piece at {self.last_moved_piece_pos}.")
                return False
            
            # Must be a capture move
            if not self._is_capture_move(move):
                print("You must make another capture.")
                return False
        
        # For regular placement, ensure the piece belongs to the current player
        if is_placement(move):
            piece, _ = get_move_elements(move)
            allowed_pieces = self.player_pieces[Player(self.current_player)]
            if piece not in allowed_pieces:
                print(f"Player {self.current_player + 1} can only place {', '.join(allowed_pieces)} pieces.")
                return False
        
        # For movement, check that the piece belongs to the current player and the move is valid
        if is_movement(move):
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            # Check if origin has a piece belonging to the current player
            piece_at_origin = self.board.layout[origin_row][origin_col]
            if piece_at_origin not in self.player_pieces[Player(self.current_player)]:
                print("You can only move your own pieces.")
                return False
            
            # Check if destination is empty
            if self.board.layout[dest_row][dest_col] != '_':
                print("Destination must be empty.")
                return False
            
            # Check if the move is a standard move or a capture move
            is_standard_move = self._is_standard_move(move)
            is_capture = self._is_capture_move(move)
            
            if not (is_standard_move or is_capture):
                print("Invalid move direction or distance.")
                return False
        
        return True
    
    def _is_standard_move(self, move):
        """Check if the move is a standard one-space diagonal move in the allowed direction."""
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        piece = self.board.layout[origin_row][origin_col]
        row_diff = dest_row - origin_row
        col_diff = dest_col - origin_col
        
        # Check if the move is one space diagonally
        if abs(row_diff) == 1 and abs(col_diff) == 1:
            direction = (row_diff, col_diff)
            return direction in self.move_directions[piece]
        
        return False
    
    def _is_capture_move(self, move):
        """Check if the move is a valid capture move."""
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        piece = self.board.layout[origin_row][origin_col]
        row_diff = dest_row - origin_row
        col_diff = dest_col - origin_col
        
        # Check if the move is two spaces diagonally
        if abs(row_diff) == 2 and abs(col_diff) == 2:
            direction = (row_diff // 2, col_diff // 2)
            
            # Check if the direction is allowed for this piece
            if direction not in self.move_directions[piece]:
                return False
            
            # Check if there's an opponent's piece in between
            mid_row = origin_row + direction[0]
            mid_col = origin_col + direction[1]
            mid_piece = self.board.layout[mid_row][mid_col]
            
            opponent_pieces = self.player_pieces[Player(1 - self.current_player)]
            return mid_piece in opponent_pieces
        
        return False
    
    def perform_move(self, move):
        captured = False
        
        if is_movement(move):
            origin, destination = get_move_elements(move)
            
            # Check if this is a capture move
            if self._is_capture_move(move):
                captured = True
                # Remove the captured piece
                mid_row = (origin[0] + destination[0]) // 2
                mid_col = (origin[1] + destination[1]) // 2
                # Place a blank at the captured position
                self.board.place_piece(f"_ {mid_row},{mid_col}")
            
            # Perform the move
            self.board.move_piece(move)
            
            # Check for promotion
            piece = self.board.layout[destination[0]][destination[1]]
            if piece == 'A' and destination[0] == 0:  # A reached top row
                self.board.place_piece(f"Â {destination[0]},{destination[1]}")
            elif piece == 'O' and destination[0] == 7:  # O reached bottom row
                self.board.place_piece(f"Ô {destination[0]},{destination[1]}")
            
            # Store the last moved piece position for potential continued captures
            self.last_moved_piece_pos = destination
            
            # Check if more captures are possible with this piece
            self.must_continue_capturing = captured and self._has_capture_moves(destination)
        else:
            # For placement (though not used in normal gameplay)
            super().perform_move(move)
    
    def _has_capture_moves(self, position):
        """Check if the piece at the given position has any possible capture moves."""
        row, col = position
        piece = self.board.layout[row][col]
        
        for direction in self.move_directions[piece]:
            # Check adjacent square in this direction
            adj_row = row + direction[0]
            adj_col = col + direction[1]
            
            if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                adj_piece = self.board.layout[adj_row][adj_col]
                opponent_pieces = self.player_pieces[Player(1 - self.current_player)]
                
                if adj_piece in opponent_pieces:
                    # Check landing square
                    land_row = adj_row + direction[0]
                    land_col = adj_col + direction[1]
                    
                    if 0 <= land_row < 8 and 0 <= land_col < 8 and self.board.layout[land_row][land_col] == '_':
                        return True
        
        return False
    
    def next_player(self):
        # If player must continue capturing, don't change players
        if self.must_continue_capturing:
            return self.current_player
        
        # Otherwise, alternate players
        return 1 - self.current_player
    
    def game_finished(self):
        # Check if any player has no more pieces
        player_one_pieces = 0
        player_two_pieces = 0
        
        for row in self.board.layout:
            for cell in row:
                if cell in self.player_pieces[Player.ONE]:
                    player_one_pieces += 1
                elif cell in self.player_pieces[Player.TWO]:
                    player_two_pieces += 1
        
        if player_one_pieces == 0 or player_two_pieces == 0:
            return True
        
        # Check if current player has no valid moves
        has_valid_moves = False
        player_pieces = self.player_pieces[Player(self.current_player)]
        
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                if piece in player_pieces:
                    # Check standard moves
                    for direction in self.move_directions[piece]:
                        dest_row = row + direction[0]
                        dest_col = col + direction[1]
                        
                        if 0 <= dest_row < 8 and 0 <= dest_col < 8 and self.board.layout[dest_row][dest_col] == '_':
                            has_valid_moves = True
                            break
                    
                    # Check capture moves
                    for direction in self.move_directions[piece]:
                        adj_row = row + direction[0]
                        adj_col = col + direction[1]
                        
                        if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                            adj_piece = self.board.layout[adj_row][adj_col]
                            opponent_pieces = self.player_pieces[Player(1 - self.current_player)]
                            
                            if adj_piece in opponent_pieces:
                                land_row = adj_row + direction[0]
                                land_col = adj_col + direction[1]
                                
                                if 0 <= land_row < 8 and 0 <= land_col < 8 and self.board.layout[land_row][land_col] == '_':
                                    has_valid_moves = True
                                    break
                    
                    if has_valid_moves:
                        break
                
            if has_valid_moves:
                break
        
        return not has_valid_moves
    
    def get_winner(self):
        # Count pieces for each player
        player_one_pieces = 0
        player_two_pieces = 0
        
        for row in self.board.layout:
            for cell in row:
                if cell in self.player_pieces[Player.ONE]:
                    player_one_pieces += 1
                elif cell in self.player_pieces[Player.TWO]:
                    player_two_pieces += 1
        
        # If a player has no pieces, the other player wins
        if player_one_pieces == 0:
            return Player.TWO.value
        if player_two_pieces == 0:
            return Player.ONE.value
        
        # If current player has no valid moves, the other player wins
        return 1 - self.current_player
    
    def finish_message(self, winner):
        player_name = "ONE" if winner == Player.ONE.value else "TWO"
        print(f"Player {player_name} wins!")

if __name__ == '__main__':
    # Initialize the board with the given layout
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