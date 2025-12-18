from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Daisy(Game):
    def __init__(self, board):
        super().__init__(board)
        # Initialize reserves and game state
        self.reserves = {
            1: {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9},
            2: {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        }
        self.has_placed_a = {1: False, 2: False}
        
    def prompt_current_player(self):
        print(f"Player {self.current_player}'s turn. Reserve: {self.reserves[self.current_player]}")
        return input("Your move (place X Y or move X1 Y1 X2 Y2): ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            return self._validate_placement(piece, x, y)
        elif is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            return self._validate_movement(x1, y1, x2, y2)
        return False
    
    def _validate_placement(self, piece, x, y):
        # Check piece is in reserve
        if piece not in self.reserves[self.current_player] or self.reserves[self.current_player][piece] <= 0:
            return False
        
        # Check position is blank
        if self.board.layout[y][x] != '_':
            return False
            
        # Mark if placing A/a
        if piece.lower() == 'a':
            self.has_placed_a[self.current_player] = True
        return True
    
    def _validate_movement(self, x1, y1, x2, y2):
        # Check origin has piece belonging to current player
        piece = self.board.layout[y1][x1]
        if piece == '_' or piece == ' ':
            return False
        if (self.current_player == 1 and not piece.isupper()) or (self.current_player == 2 and piece.isupper()):
            return False
        
        # Check destination is valid
        if self.board.layout[y2][x2] == ' ':
            return False
            
        # Check capture rules
        target = self.board.layout[y2][x2]
        if target != '_':
            if (self.current_player == 1 and target.isupper()) or (self.current_player == 2 and not target.isupper()):
                return False
            if not self.has_placed_a[self.current_player]:
                return False
        
        # Check piece movement rules
        return self._is_valid_piece_move(piece, x1, y1, x2, y2)
    
    def _is_valid_piece_move(self, piece, x1, y1, x2, y2):
        piece_type = piece.lower()
        dx, dy = x2 - x1, y2 - y1
        
        if piece_type == 'a':
            # A/a: moves one space in any direction
            return abs(dx) <= 1 and abs(dy) <= 1 and (dx != 0 or dy != 0)
        
        elif piece_type == 'b':
            # B/b: moves any number orthogonally (rook-like)
            if dx != 0 and dy != 0:
                return False
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
            x, y = x1 + step_x, y1 + step_y
            while x != x2 or y != y2:
                if self.board.layout[y][x] != '_':
                    return False
                x += step_x
                y += step_y
            return True
        
        elif piece_type == 'c':
            # C/c: moves any number diagonally (bishop-like)
            if abs(dx) != abs(dy):
                return False
            step_x = 1 if dx > 0 else -1
            step_y = 1 if dy > 0 else -1
            x, y = x1 + step_x, y1 + step_y
            while x != x2 or y != y2:
                if self.board.layout[y][x] != '_':
                    return False
                x += step_x
                y += step_y
            return True
        
        elif piece_type == 'd':
            # D/d: moves one square in any direction except diagonally backward
            forward = -1 if piece.isupper() else 1
            if abs(dx) > 1 or abs(dy) > 1 or (dx == 0 and dy == 0):
                return False
            # Check for diagonally backward
            if dx != 0 and dy != 0 and dy == forward:
                return False
            return True
        
        elif piece_type == 'e':
            # E/e: moves one square diagonally or one square forward orthogonally
            forward = -1 if piece.isupper() else 1
            if abs(dx) == 1 and abs(dy) == 1:
                return True
            if dx == 0 and dy == forward:
                return True
            return False
        
        elif piece_type == 'f':
            # F/f: moves two forward, then one left/right (knight-like but restricted)
            forward = -1 if piece.isupper() else 1
            return (abs(dx) == 1 and dy == 2 * forward)
        
        elif piece_type == 'g':
            # G/g: moves any number orthogonally forward (forward-only rook)
            forward = -1 if piece.isupper() else 1
            if dx == 0:
                if (dy > 0 and piece.isupper()) or (dy < 0 and not piece.isupper()):
                    return False
                step = -1 if dy < 0 else 1
                y = y1 + step
                while y != y2:
                    if self.board.layout[y][x1] != '_':
                        return False
                    y += step
                return True
            elif dy == 0:
                step = 1 if dx > 0 else -1
                x = x1 + step
                while x != x2:
                    if self.board.layout[y1][x] != '_':
                        return False
                    x += step
                return True
            return False
        
        elif piece_type == 'h':
            # H/h: moves one space forward orthogonally (pawn-like)
            forward = -1 if piece.isupper() else 1
            return dx == 0 and dy == forward
        
        return False
    
    def perform_move(self, move):
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            self.reserves[self.current_player][piece] -= 1
        elif is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            target = self.board.layout[y2][x2]
            
            # Handle capture
            if target != '_':
                # Convert captured piece to current player's type
                captured = target.lower() if self.current_player == 1 else target.upper()
                self.reserves[self.current_player][captured] += 1
                
                # Check win condition
                if (self.current_player == 1 and target == 'a') or (self.current_player == 2 and target == 'A'):
                    self._winner = self.current_player
            
            self.board.move_piece(move)
    
    def game_finished(self):
        return self._winner is not None
    
    def get_winner(self):
        return self._winner
    
    def next_player(self):
        return 3 - self.current_player  # Switches between 1 and 2
    
    def finish_message(self, winner):
        print(f"\nPlayer {winner} wins!")

if __name__ == '__main__':
    # Initialize empty 9x9 board
    board = Board((9, 9))
    game = Daisy(board)
    game.game_loop()
