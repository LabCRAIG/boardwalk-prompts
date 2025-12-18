from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Reversi(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 1 is 'B' (Black), Player 2 is 'W' (White)
        self.current_player = 1
        self.valid_moves_cache = None
        
    def initial_player(self):
        return 1  # Black moves first in Reversi
    
    def prompt_current_player(self):
        player_char = 'B' if self.current_player == 1 else 'W'
        return input(f"Player {self.current_player} ({player_char}) move (row,col): ")
    
    def validate_move(self, move):
        # First check if the move is in correct format (D,D)
        if not (move.replace(',', '').isdigit() and move.count(',') == 1):
            return False
            
        try:
            row, col = map(int, move.split(','))
        except:
            return False
            
        # Check if position is on board
        if not (0 <= row < self.board.height and 0 <= col < self.board.width):
            return False
            
        # Check if position is empty
        if self.board.layout[row, col] != '_':
            return False
            
        # Check if move flips at least one opponent piece
        player_char = 'B' if self.current_player == 1 else 'W'
        opponent_char = 'W' if self.current_player == 1 else 'B'
        
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0), (1,1)]
        
        valid = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.board.height and 0 <= c < self.board.width and 
                self.board.layout[r, c] == opponent_char):
                # Move in this direction until we find our own piece
                r += dr
                c += dc
                while 0 <= r < self.board.height and 0 <= c < self.board.width:
                    if self.board.layout[r, c] == player_char:
                        valid = True
                        break
                    elif self.board.layout[r, c] == '_':
                        break
                    r += dr
                    c += dc
        
        return valid
    
    def perform_move(self, move):
        row, col = map(int, move.split(','))
        player_char = 'B' if self.current_player == 1 else 'W'
        opponent_char = 'W' if self.current_player == 1 else 'B'
        
        # Place the piece
        self.board.place_piece(f"{player_char} {row},{col}")
        
        # Flip opponent's pieces in all valid directions
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0), (1,1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] == opponent_char:
                    to_flip.append((r, c))
                elif self.board.layout[r, c] == player_char:
                    # Flip all pieces in to_flip
                    for flip_r, flip_c in to_flip:
                        self.board.place_piece(f"{player_char} {flip_r},{flip_c}")
                    break
                else:  # Empty space
                    break
                    
                r += dr
                c += dc
    
    def game_finished(self):
        # Game is finished if neither player can make a valid move
        for player in [1, 2]:
            if self.has_valid_move(player):
                return False
        return True
    
    def has_valid_move(self, player):
        # Check if the player has any valid moves
        player_char = 'B' if player == 1 else 'W'
        opponent_char = 'W' if player == 1 else 'B'
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_':
                    # Check if this is a valid move
                    directions = [(-1,-1), (-1,0), (-1,1),
                                 (0,-1),          (0,1),
                                 (1,-1),  (1,0), (1,1)]
                    
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if (0 <= r < self.board.height and 0 <= c < self.board.width and 
                            self.board.layout[r, c] == opponent_char):
                            # Move in this direction until we find our own piece
                            r += dr
                            c += dc
                            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                                if self.board.layout[r, c] == player_char:
                                    return True
                                elif self.board.layout[r, c] == '_':
                                    break
                                r += dr
                                c += dc
        return False
    
    def get_winner(self):
        # Count pieces
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')
        
        if black_count > white_count:
            return 1
        elif white_count > black_count:
            return 2
        else:
            return None  # Draw
    
    def next_player(self):
        # Switch to other player if they have valid moves
        next_p = 2 if self.current_player == 1 else 1
        if self.has_valid_move(next_p):
            return next_p
        # Otherwise stay with current player if they have moves
        elif self.has_valid_move(self.current_player):
            return self.current_player
        # Otherwise game will end
        else:
            return next_p
    
    def finish_message(self, winner):
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')
        
        print(f"\nGame over! Final score - Black: {black_count}, White: {white_count}")
        if winner is None:
            print("The game ended in a draw!")
        else:
            print(f"Player {winner} ({'Black' if winner == 1 else 'White'}) wins!")

if __name__ == '__main__':
    # Initialize board with starting position for Reversi
    initial_layout = """________
________
________
___WB___
___BW___
________
________
________"""
    
    board = Board((8, 8), initial_layout)
    game = Reversi(board)
    game.game_loop()