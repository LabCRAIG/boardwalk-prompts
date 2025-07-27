from game import Game, Board, is_placement, get_move_elements
import numpy as np

class Quartz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Using 1 for A, 2 for V
        self.game_over = False
        
    def initial_player(self):
        return 1  # Player 1 (A) starts
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_placement(move):
            return False
            
        piece, (row, col) = get_move_elements(move)
        
        # Verify correct piece for current player
        if (self.current_player == 1 and piece != 'A') or (self.current_player == 2 and piece != 'V'):
            return False
            
        # Check if space is empty
        if self.board.layout[row, col] != '_':
            return False
            
        # Check all 8 directions for a valid line
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]:
            if self._check_direction(row, col, dr, dc):
                return True
        return False
    
    def _check_direction(self, row, col, dr, dc):
        """Check if there's a valid line in a specific direction"""
        opponent = 'V' if self.current_player == 1 else 'A'
        r, c = row + dr, col + dc
        found_opponent = False
        
        while 0 <= r < self.board.height and 0 <= c < self.board.width:
            if self.board.layout[r, c] == opponent:
                found_opponent = True
                r += dr
                c += dc
            elif self.board.layout[r, c] == ('A' if self.current_player == 1 else 'V') and found_opponent:
                return True
            else:
                break
        return False
    
    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)
        
        # Flip opponent's pieces in all valid directions
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]:
            self._flip_direction(row, col, dr, dc)
        
        # Check if game is over after this move
        self._check_game_over()
    
    def _flip_direction(self, row, col, dr, dc):
        """Flip opponent's pieces in a valid direction"""
        opponent = 'V' if self.current_player == 1 else 'A'
        to_flip = []
        r, c = row + dr, col + dc
        
        while 0 <= r < self.board.height and 0 <= c < self.board.width:
            if self.board.layout[r, c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            elif self.board.layout[r, c] == ('A' if self.current_player == 1 else 'V'):
                for flip_r, flip_c in to_flip:
                    flip_move = f"{'A' if self.current_player == 1 else 'V'} {flip_r},{flip_c}"
                    self.board.place_piece(flip_move)
                break
            else:
                break
    
    def next_player(self):
        # Temporarily switch to check if next player has moves
        next_p = 2 if self.current_player == 1 else 1
        original_player = self.current_player
        self.current_player = next_p
        
        has_moves = any(
            self.validate_move(f"{'A' if next_p == 1 else 'V'} {row},{col}")
            for row in range(self.board.height)
            for col in range(self.board.width)
            if self.board.layout[row, col] == '_'
        )
        
        self.current_player = original_player
        
        if has_moves:
            return next_p
        return original_player  # If no moves, same player goes again
    
    def game_finished(self):
        # Game ends if board is full or neither player can move
        empty_spaces = np.sum(self.board.layout == '_')
        if empty_spaces == 0:
            return True
            
        # Check if both players can't move
        current_can_move = any(
            self.validate_move(f"{'A' if self.current_player == 1 else 'V'} {row},{col}")
            for row in range(self.board.height)
            for col in range(self.board.width)
            if self.board.layout[row, col] == '_'
        )
        
        opponent = 2 if self.current_player == 1 else 1
        opponent_can_move = any(
            self.validate_move(f"{'A' if opponent == 1 else 'V'} {row},{col}")
            for row in range(self.board.height)
            for col in range(self.board.width)
            if self.board.layout[row, col] == '_'
        )
        
        return not current_can_move and not opponent_can_move
    
    def get_winner(self):
        a_count = np.sum(self.board.layout == 'A')
        v_count = np.sum(self.board.layout == 'V')
        
        if a_count > v_count:
            return 1
        elif v_count > a_count:
            return 2
        return None  # Tie
    
    def prompt_current_player(self):
        return input(f"Player {'A' if self.current_player == 1 else 'V'}, enter your move (e.g. 'A 3,4' or 'V 4,5'): ")
    
    def finish_message(self, winner):
        if winner is None:
            print("\nGame ended in a tie!")
        else:
            print(f"\nPlayer {'A' if winner == 1 else 'V'} wins!")

if __name__ == '__main__':
    # Initialize board with center pieces
    initial_layout = """\
________
________
________
___AV___
___VA___
________
________
________"""
    
    board = Board((8, 8), initial_layout)
    game = Quartz(board)
    
    print("Welcome to Quartz!")
    print("Player 1: A, Player 2: V")
    print("Enter moves in format 'A 3,4' or 'V 4,5'")
    print("Type 'quit' to exit\n")
    
    game.game_loop()