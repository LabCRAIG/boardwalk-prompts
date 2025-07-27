from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    PLAYER_1 = 0  # Controls A's
    PLAYER_2 = 1  # Controls V's

class Violet(Game):
    def __init__(self, board):
        super().__init__(board)
        self.piece_shot = False  # Flag to track if a player has shot an X after moving
        self.last_moved_piece_pos = None  # Track position of the last moved piece for shooting
        self.player_pieces = {
            Player.PLAYER_1.value: 'A',
            Player.PLAYER_2.value: 'V'
        }
    
    def initial_player(self):
        return Player.PLAYER_1.value
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # If we're in the X-shooting phase
        if self.piece_shot is False and self.last_moved_piece_pos is not None:
            # Check if the move is a placement of an X
            if not is_placement(move):
                return False
            
            piece, dest = get_move_elements(move)
            if piece != 'X':
                return False
            
            # Check if destination is empty
            dest_y, dest_x = dest
            if self.board.layout[dest_y][dest_x] != '_':
                return False
                
            # Check if the destination is in line of sight of the last moved piece
            shooter_y, shooter_x = self.last_moved_piece_pos
            
            # Check if the move is orthogonal or diagonal from the shooter
            is_orthogonal = shooter_x == dest_x or shooter_y == dest_y
            is_diagonal = abs(shooter_x - dest_x) == abs(shooter_y - dest_y)
            
            if not (is_orthogonal or is_diagonal):
                return False
                
            # Check if path is clear
            direction_y = 0 if shooter_y == dest_y else (1 if dest_y > shooter_y else -1)
            direction_x = 0 if shooter_x == dest_x else (1 if dest_x > shooter_x else -1)
            
            curr_y, curr_x = shooter_y + direction_y, shooter_x + direction_x
            while (curr_y, curr_x) != dest:
                if self.board.layout[curr_y][curr_x] != '_':
                    return False
                curr_y += direction_y
                curr_x += direction_x
                
            return True
        else:
            # We're in the piece-moving phase
            if not is_movement(move):
                return False
                
            origin, dest = get_move_elements(move)
            origin_y, origin_x = origin
            dest_y, dest_x = dest
            
            # Check if origin has the current player's piece
            player_piece = self.player_pieces[self.current_player]
            if self.board.layout[origin_y][origin_x] != player_piece:
                return False
                
            # Check if destination is empty
            if self.board.layout[dest_y][dest_x] != '_':
                return False
                
            # Check if the move is orthogonal or diagonal
            is_orthogonal = origin_x == dest_x or origin_y == dest_y
            is_diagonal = abs(origin_x - dest_x) == abs(origin_y - dest_y)
            
            if not (is_orthogonal or is_diagonal):
                return False
                
            # Check if path is clear
            direction_y = 0 if origin_y == dest_y else (1 if dest_y > origin_y else -1)
            direction_x = 0 if origin_x == dest_x else (1 if dest_x > origin_x else -1)
            
            curr_y, curr_x = origin_y + direction_y, origin_x + direction_x
            while (curr_y, curr_x) != dest:
                if self.board.layout[curr_y][curr_x] != '_':
                    return False
                curr_y += direction_y
                curr_x += direction_x
                
            return True
    
    def perform_move(self, move):
        if self.piece_shot is False and self.last_moved_piece_pos is not None:
            # We're in the X-shooting phase
            super().perform_move(move)
            self.piece_shot = True
        else:
            # We're in the piece-moving phase
            super().perform_move(move)
            origin, dest = get_move_elements(move)
            self.last_moved_piece_pos = dest
            self.piece_shot = False
    
    def prompt_current_player(self):
        player_name = "Player 1 (A)" if self.current_player == Player.PLAYER_1.value else "Player 2 (V)"
        
        if self.piece_shot is False and self.last_moved_piece_pos is not None:
            shooter_y, shooter_x = self.last_moved_piece_pos
            return input(f"{player_name}, shoot an X from your piece at ({shooter_y},{shooter_x}): ")
        else:
            return input(f"{player_name}, move one of your pieces: ")
    
    def get_state(self):
        state = super().get_state()
        return (state[0], state[1], [self.piece_shot, self.last_moved_piece_pos])
    
    def game_finished(self):
        # Check if current player can make any valid moves
        player_piece = self.player_pieces[self.current_player]
        
        # Find all pieces of the current player
        for y in range(self.board.height):
            for x in range(self.board.width):
                if self.board.layout[y][x] == player_piece:
                    # Check if this piece can move anywhere
                    for dir_y in [-1, 0, 1]:
                        for dir_x in [-1, 0, 1]:
                            if dir_y == 0 and dir_x == 0:
                                continue
                                
                            # Check in this direction
                            curr_y, curr_x = y + dir_y, x + dir_x
                            while (0 <= curr_y < self.board.height and 
                                   0 <= curr_x < self.board.width):
                                if self.board.layout[curr_y][curr_x] == '_':
                                    # Found a valid move
                                    return False
                                else:
                                    # Hit an obstacle, stop checking this direction
                                    break
                                curr_y += dir_y
                                curr_x += dir_x
        
        # If we get here, no valid moves were found
        return True
    
    def get_winner(self):
        # The player who cannot move loses, so the winner is the other player
        return (self.current_player + 1) % 2
    
    def next_player(self):
        # Only change players after both moving a piece and shooting an X
        if self.piece_shot:
            return (self.current_player + 1) % 2
        else:
            return self.current_player
            
    def finish_message(self, winner):
        winner_name = "Player 1 (A)" if winner == Player.PLAYER_1.value else "Player 2 (V)"
        print(f"{winner_name} wins! The other player has no valid moves left.")

if __name__ == '__main__':
    # Initialize board with initial setup
    initial_layout = ('__________\n'
                      '___V__V___\n'
                      '__________\n'
                      'V________V\n'
                      '__________\n'
                      '__________\n'
                      'A________A\n'
                      '__________\n'
                      '__________\n'
                      '___A__A___')
    
    board = Board((10, 10), initial_layout)
    game = Violet(board)
    game.game_loop()