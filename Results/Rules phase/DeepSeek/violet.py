from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Violet(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        try:
            if is_movement(move):
                (origin, dest), _ = get_move_elements(move), None
                piece = self.board.layout[origin[0], origin[1]]
                
                # Check if piece belongs to current player
                if (self.current_player == 1 and piece != 'A') or (self.current_player == 2 and piece != 'V'):
                    return False
                
                # Check if path is clear
                if not self._is_path_clear(origin, dest):
                    return False
                    
            elif is_placement(move):
                piece, pos = get_move_elements(move)
                if piece != 'X':
                    return False
                # X placement will be validated during perform_move
            else:
                return False
                
            return True
        except:
            return False
    
    def _is_path_clear(self, origin, dest):
        dx = dest[0] - origin[0]
        dy = dest[1] - origin[1]
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return False  # Not actually moving
            
        x_step = dx // steps
        y_step = dy // steps
        
        for i in range(1, steps):
            x = origin[0] + i * x_step
            y = origin[1] + i * y_step
            if self.board.layout[x, y] != '_':
                return False
        return True
    
    def perform_move(self, move):
        if is_movement(move):
            origin, dest = get_move_elements(move)
            self.board.move_piece(move)
            
            # Now prompt for X placement
            valid_x = False
            while not valid_x:
                print(self.board)
                x_move = input(f"Player {self.current_player}, place X from ({dest[0]},{dest[1]}): ")
                if is_placement(x_move):
                    x_piece, x_pos = get_move_elements(x_move)
                    if x_piece == 'X' and self._is_path_clear(dest, x_pos):
                        if self.board.layout[x_pos[0], x_pos[1]] == '_':
                            self.board.place_piece(x_move)
                            valid_x = True
    
    def game_finished(self):
        # Check if current player has any valid moves left
        piece = 'A' if self.current_player == 1 else 'V'
        positions = np.argwhere(self.board.layout == piece)
        
        for pos in positions:
            origin = tuple(pos)
            # Check all possible destinations
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    x, y = origin[0] + dx, origin[1] + dy
                    while 0 <= x < 10 and 0 <= y < 10:
                        if self.board.layout[x, y] == '_':
                            return False
                        if self.board.layout[x, y] != '_':
                            break
                        x += dx
                        y += dy
        return True
    
    def get_winner(self):
        return 2 if self.current_player == 1 else 1
    
    def next_player(self):
        return 2 if self.current_player == 1 else 1
    
    def prompt_current_player(self):
        piece = 'A' if self.current_player == 1 else 'V'
        return input(f"Player {self.current_player}, move {piece}: ")
    
    def finish_message(self, winner):
        print(f"\nPlayer {winner} wins! Player {2 if winner == 1 else 1} has no valid moves left.")

if __name__ == '__main__':
    # Create initial board
    layout = np.full((10, 10), '_', dtype=str)
    
    # Place initial pieces
    initial_v = [(0,3), (0,6), (3,0), (3,9)]
    initial_a = [(6,0), (6,9), (9,3), (9,6)]
    
    for pos in initial_v:
        layout[pos[0], pos[1]] = 'V'
    for pos in initial_a:
        layout[pos[0], pos[1]] = 'A'
    
    board = Board((10, 10), '\n'.join(''.join(row) for row in layout))
    game = Violet(board)
    game.game_loop()