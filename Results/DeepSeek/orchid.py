from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Orchid(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1
        self.phase = 1  # 1: placement phase, 2: movement phase
        self.pieces_remaining = {1: 12, 2: 12}
        self.pieces_on_board = {1: 0, 2: 0}
        
    def prompt_current_player(self):
        if self.phase == 1:
            return input(f"Player {self.current_player}, place two pieces (format: 'X D,D Y D,D'): ")
        else:
            return input(f"Player {self.current_player}, move a piece (format: 'D,D D,D'): ")
    
    def validate_move(self, move):
        if self.phase == 1:
            try:
                # Split into two placement moves
                move1, move2 = move.split()[:2], move.split()[2:]
                move1 = ' '.join(move1)
                move2 = ' '.join(move2)
                
                if not (is_placement(move1) and is_placement(move2)):
                    return False
                
                piece1, pos1 = get_move_elements(move1)
                piece2, pos2 = get_move_elements(move2)
                
                # Validate pieces belong to current player
                if (self.current_player == 1 and piece1 != 'A') or (self.current_player == 2 and piece1 != 'B'):
                    return False
                if (self.current_player == 1 and piece2 != 'A') or (self.current_player == 2 and piece2 != 'B'):
                    return False
                
                # Validate positions
                x1, y1 = pos1
                x2, y2 = pos2
                if not (0 <= x1 < 5 and 0 <= y1 < 5 and 0 <= x2 < 5 and 0 <= y2 < 5):
                    return False
                if (x1 == 2 and y1 == 2) or (x2 == 2 and y2 == 2):  # Center is forbidden
                    return False
                if self.board.layout[x1, y1] != '_' or self.board.layout[x2, y2] != '_':
                    return False
                
                return True
            except:
                return False
        else:
            if not is_movement(move):
                return False
            
            (x1, y1), (x2, y2) = get_move_elements(move)
            
            # Validate positions
            if not (0 <= x1 < 5 and 0 <= y1 < 5 and 0 <= x2 < 5 and 0 <= y2 < 5):
                return False
            
            # Validate piece belongs to current player
            piece = self.board.layout[x1, y1]
            if (self.current_player == 1 and piece != 'A') or (self.current_player == 2 and piece != 'B'):
                return False
            
            # Validate destination is empty
            if self.board.layout[x2, y2] != '_':
                return False
            
            # Validate orthogonal movement
            if x1 != x2 and y1 != y2:
                return False
            
            # Validate no pieces in path (for any distance movement)
            step_x = 0 if x1 == x2 else (1 if x2 > x1 else -1)
            step_y = 0 if y1 == y2 else (1 if y2 > y1 else -1)
            
            current_x, current_y = x1 + step_x, y1 + step_y
            while current_x != x2 or current_y != y2:
                if self.board.layout[current_x, current_y] != '_':
                    return False
                current_x += step_x
                current_y += step_y
            
            return True
    
    def perform_move(self, move):
        if self.phase == 1:
            # Split into two placement moves
            move1, move2 = move.split()[:2], move.split()[2:]
            move1 = ' '.join(move1)
            move2 = ' '.join(move2)
            
            piece1, pos1 = get_move_elements(move1)
            piece2, pos2 = get_move_elements(move2)
            
            self.board.place_piece(move1)
            self.board.place_piece(move2)
            
            self.pieces_remaining[self.current_player] -= 2
            self.pieces_on_board[self.current_player] += 2
            
            # Check if we should switch to phase 2
            if self.pieces_remaining[1] == 0 and self.pieces_remaining[2] == 0:
                self.phase = 2
        else:
            (x1, y1), (x2, y2) = get_move_elements(move)
            self.board.move_piece(move)
            
            # Check for captures in all 4 directions
            opponent = 2 if self.current_player == 1 else 1
            opponent_piece = 'B' if self.current_player == 1 else 'A'
            player_piece = 'A' if self.current_player == 1 else 'B'
            captured = False
            
            # Directions: up, down, left, right
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x2 + dx, y2 + dy
                to_capture = []
                
                while 0 <= nx < 5 and 0 <= ny < 5:
                    if self.board.layout[nx, ny] == opponent_piece:
                        to_capture.append((nx, ny))
                        nx += dx
                        ny += dy
                    elif self.board.layout[nx, ny] == player_piece and to_capture:
                        # Capture all pieces in to_capture list
                        for cx, cy in to_capture:
                            self.board.layout[cx, cy] = '_'
                            self.pieces_on_board[opponent] -= 1
                            captured = True
                        break
                    else:
                        break
            
            # If no captures, check if player has any valid moves left
            if not captured and not self.has_valid_moves():
                return  # Player passes turn
    
    def has_valid_moves(self):
        if self.phase == 1:
            return True  # Always can place in phase 1
        
        player_piece = 'A' if self.current_player == 1 else 'B'
        # Check all pieces of current player for possible moves
        for x in range(5):
            for y in range(5):
                if self.board.layout[x, y] == player_piece:
                    # Check all orthogonal directions
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        while 0 <= nx < 5 and 0 <= ny < 5:
                            if self.board.layout[nx, ny] == '_':
                                return True
                            if self.board.layout[nx, ny] != '_':
                                break
                            nx += dx
                            ny += dy
        return False
    
    def game_finished(self):
        return self.pieces_on_board[1] == 0 or self.pieces_on_board[2] == 0
    
    def get_winner(self):
        if self.pieces_on_board[1] == 0:
            return 2
        elif self.pieces_on_board[2] == 0:
            return 1
        return None
    
    def next_player(self):
        return 2 if self.current_player == 1 else 1
    
    def finish_message(self, winner):
        print(f"\nPlayer {winner} has captured all opponent pieces and wins the game!")

if __name__ == '__main__':
    board = Board((5, 5))
    mygame = Orchid(board)
    mygame.game_loop()
