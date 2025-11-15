from game import Game, Board, is_movement, is_placement, get_move_elements

class Checkers(Game):
    # Player enums
    PLAYER_RED = 0
    PLAYER_BLACK = 1
    
    def __init__(self, board):
        super().__init__(board)
        self.capture_mandatory = True
        self.multiple_jumps = True
        self.last_move_was_jump = False
        self.must_continue_jumping = False
        self.last_jump_position = None
        
    def initial_player(self):
        return self.PLAYER_RED
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_movement(move):
            from_pos, to_pos = get_move_elements(move)
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Check if piece belongs to current player
            piece = self.board.layout[from_row, from_col]
            if not self._is_players_piece(piece):
                return False
                
            # Check if destination is blank
            if self.board.layout[to_row, to_col] != '_':
                return False
                
            # Check if move is valid for the piece type
            if not self._is_valid_move(from_pos, to_pos, piece):
                return False
                
            # Check capture rules
            if self.capture_mandatory:
                if self._has_capture_available():
                    if not self._is_capture_move(from_pos, to_pos):
                        return False
                elif self._is_capture_move(from_pos, to_pos):
                    return False
                    
            # Check for multiple jumps
            if self.must_continue_jumping:
                if from_pos != self.last_jump_position:
                    return False
                if not self._is_capture_move(from_pos, to_pos):
                    return False
                    
            return True
            
        return False
    
    def _is_players_piece(self, piece):
        if self.current_player == self.PLAYER_RED:
            return piece in ['r', 'R']
        else:
            return piece in ['b', 'B']
    
    def _is_valid_move(self, from_pos, to_pos, piece):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check direction for regular pieces
        if piece.lower() == piece:  # Regular piece (not king)
            if self.current_player == self.PLAYER_RED:
                if to_row >= from_row:  # Red moves downward
                    return False
            else:
                if to_row <= from_row:  # Black moves upward
                    return False
        
        # Check if move is diagonal
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        if row_diff != col_diff:
            return False
            
        # Check distance
        if row_diff > 2:
            return False
            
        # Check for captures
        if row_diff == 2:
            # This is a jump, check if there's an opponent piece to capture
            jump_row = (from_row + to_row) // 2
            jump_col = (from_col + to_col) // 2
            jumped_piece = self.board.layout[jump_row, jump_col]
            
            if jumped_piece == '_' or jumped_piece == ' ':
                return False
                
            if self.current_player == self.PLAYER_RED:
                if jumped_piece not in ['b', 'B']:
                    return False
            else:
                if jumped_piece not in ['r', 'R']:
                    return False
                    
        return True
    
    def _is_capture_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        return abs(to_row - from_row) == 2
    
    def _has_capture_available(self):
        # Check all pieces of current player for capture moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if self._is_players_piece(piece):
                    if self._can_capture_from((row, col)):
                        return True
        return False
    
    def _can_capture_from(self, position):
        row, col = position
        piece = self.board.layout[row, col]
        
        # Check all possible capture directions
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        if piece.lower() == piece:  # Regular piece
            if self.current_player == self.PLAYER_RED:
                directions = [(-2, -2), (-2, 2)]  # Only upward for red
            else:
                directions = [(2, -2), (2, 2)]    # Only downward for black
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.board.height and 
                0 <= new_col < self.board.width and
                self.board.layout[new_row, new_col] == '_'):
                
                # Check if jump is valid
                jump_row, jump_col = row + dr//2, col + dc//2
                if (0 <= jump_row < self.board.height and 
                    0 <= jump_col < self.board.width):
                    
                    jumped_piece = self.board.layout[jump_row, jump_col]
                    if jumped_piece != '_' and jumped_piece != ' ':
                        if self.current_player == self.PLAYER_RED:
                            if jumped_piece in ['b', 'B']:
                                return True
                        else:
                            if jumped_piece in ['r', 'R']:
                                return True
        return False
    
    def perform_move(self, move):
        from_pos, to_pos = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board.layout[from_row, from_col]
        
        # Handle capture
        if abs(to_row - from_row) == 2:
            # Remove captured piece
            cap_row = (from_row + to_row) // 2
            cap_col = (from_col + to_col) // 2
            self.board.layout[cap_row, cap_col] = '_'
            self.last_move_was_jump = True
            
            # Check for promotion
            if self._should_promote(to_row, piece):
                piece = piece.upper()  # Promote to king
        else:
            self.last_move_was_jump = False
            
        # Move the piece
        self.board.layout[to_row, to_col] = piece
        self.board.layout[from_row, from_col] = '_'
        
        # Handle multiple jumps
        if self.last_move_was_jump and self.multiple_jumps:
            if self._can_capture_from(to_pos):
                self.must_continue_jumping = True
                self.last_jump_position = to_pos
                return  # Don't change player yet
                
        self.must_continue_jumping = False
        self.last_jump_position = None
    
    def _should_promote(self, row, piece):
        if piece.lower() == 'r' and row == 0:  # Red reaches top row
            return True
        if piece.lower() == 'b' and row == self.board.height - 1:  # Black reaches bottom row
            return True
        return False
    
    def game_finished(self):
        # Check if current player has no pieces
        if not self._has_pieces(self.current_player):
            return True
            
        # Check if current player has no valid moves
        if not self._has_valid_moves():
            return True
            
        return False
    
    def _has_pieces(self, player):
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if player == self.PLAYER_RED and piece in ['r', 'R']:
                    return True
                if player == self.PLAYER_BLACK and piece in ['b', 'B']:
                    return True
        return False
    
    def _has_valid_moves(self):
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if self._is_players_piece(piece):
                    if self._has_valid_moves_from((row, col)):
                        return True
        return False
    
    def _has_valid_moves_from(self, position):
        row, col = position
        piece = self.board.layout[row, col]
        
        # Check regular moves
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.lower() == piece:  # Regular piece
            if self.current_player == self.PLAYER_RED:
                directions = [(-1, -1), (-1, 1)]  # Only upward for red
            else:
                directions = [(1, -1), (1, 1)]    # Only downward for black
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.board.height and 
                0 <= new_col < self.board.width and
                self.board.layout[new_row, new_col] == '_'):
                
                # Create a test move
                test_move = f"{row},{col} {new_row},{new_col}"
                if self.validate_move(test_move):
                    return True
        
        # Check capture moves
        return self._can_capture_from(position)
    
    def get_winner(self):
        if not self._has_pieces(self.PLAYER_RED):
            return self.PLAYER_BLACK
        if not self._has_pieces(self.PLAYER_BLACK):
            return self.PLAYER_RED
            
        if not self._has_valid_moves():
            # Current player has no valid moves, so opponent wins
            return 1 - self.current_player
            
        return None
    
    def next_player(self):
        if self.must_continue_jumping:
            return self.current_player
        return 1 - self.current_player
    
    def round_counter(self):
        if self.must_continue_jumping:
            return self.round
        return self.round + 1
    
    def prompt_current_player(self):
        player_name = "Red" if self.current_player == self.PLAYER_RED else "Black"
        return input(f"Player {player_name}'s move: ")
    
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "Red" if winner == self.PLAYER_RED else "Black"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    # Create initial checkers board layout
    initial_layout = """ b b b b
    b b b b
    b b b b
    _ _ _ _
    _ _ _ _
    r r r r
    r r r r
    r r r r"""
    
    board = Board((8, 8), initial_layout)
    mygame = Checkers(board)
    mygame.game_loop()