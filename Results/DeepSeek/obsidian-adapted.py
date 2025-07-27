from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Obsidian(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.piece_moved = {
            'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False,
            'a': False, 'b': False, 'c': False, 'd': False, 'e': False, 'f': False
        }

    def initial_player(self):
        return 1

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_movement(move):
            (start_x, start_y), (end_x, end_y) = get_move_elements(move)
            piece = self.board.layout[start_x][start_y]
            
            if piece == '_' or not self.is_own_piece(piece):
                return False
            
            valid_moves = self.get_valid_moves(start_x, start_y, piece)
            return (end_x, end_y) in valid_moves
        return False

    def is_own_piece(self, piece):
        if self.current_player == 1:
            return piece.islower()
        return piece.isupper()

    def is_opponent_piece(self, piece):
        if piece == '_' or piece == ' ':
            return False
        return not self.is_own_piece(piece)

    def get_valid_moves(self, x, y, piece):
        moves = []
        piece_type = piece.lower()
        
        if piece_type == 'f':
            direction = -1 if self.current_player == 1 else 1
            # Forward move
            if self.is_valid_position(x + direction, y) and self.board.layout[x + direction][y] == '_':
                moves.append((x + direction, y))
                # Initial double move
                if not self.piece_moved[piece] and self.is_valid_position(x + 2*direction, y) and self.board.layout[x + 2*direction][y] == '_':
                    moves.append((x + 2*direction, y))
            # Captures
            for dy in [-1, 1]:
                if self.is_valid_position(x + direction, y + dy):
                    target = self.board.layout[x + direction][y + dy]
                    if self.is_opponent_piece(target):
                        moves.append((x + direction, y + dy))
        
        elif piece_type == 'a':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            moves = self.get_sliding_moves(x, y, directions)
        
        elif piece_type == 'c':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves = self.get_sliding_moves(x, y, directions)
        
        elif piece_type == 'b':
            possible_moves = [
                (x+2, y+1), (x+2, y-1),
                (x-2, y+1), (x-2, y-1),
                (x+1, y+2), (x+1, y-2),
                (x-1, y+2), (x-1, y-2)
            ]
            moves = [(nx, ny) for nx, ny in possible_moves 
                     if self.is_valid_position(nx, ny) and 
                     (self.board.layout[nx][ny] == '_' or 
                      self.is_opponent_piece(self.board.layout[nx][ny]))]
        
        elif piece_type == 'e':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves = self.get_sliding_moves(x, y, directions)
        
        elif piece_type == 'd':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves = [(x + dx, y + dy) for dx, dy in directions
                     if self.is_valid_position(x + dx, y + dy) and
                     (self.board.layout[x + dx][y + dy] == '_' or
                      self.is_opponent_piece(self.board.layout[x + dx][y + dy]))]
        
        return moves

    def get_sliding_moves(self, x, y, directions):
        moves = []
        for dx, dy in directions:
            for step in range(1, 8):
                nx, ny = x + dx*step, y + dy*step
                if not self.is_valid_position(nx, ny):
                    break
                if self.board.layout[nx][ny] == '_':
                    moves.append((nx, ny))
                elif self.is_opponent_piece(self.board.layout[nx][ny]):
                    moves.append((nx, ny))
                    break
                else:
                    break
        return moves

    def is_valid_position(self, x, y):
        return 0 <= x < self.board.height and 0 <= y < self.board.width

    def perform_move(self, move):
        (start_x, start_y), (end_x, end_y) = get_move_elements(move)
        piece = self.board.layout[start_x][start_y]
        
        # Check for capture of D/d
        target_piece = self.board.layout[end_x][end_y]
        if self.is_opponent_piece(target_piece) and target_piece.lower() == 'd':
            self.board.move_piece(move)
            return
        
        # Regular move
        self.board.move_piece(move)
        self.piece_moved[piece] = True
        
        # Check for pawn promotion
        if piece.lower() == 'f':
            if (self.current_player == 1 and end_x == 0) or (self.current_player == 2 and end_x == 7):
                promoted_piece = 'e' if self.current_player == 1 else 'E'
                self.board.place_piece(f"{promoted_piece} {end_x},{end_y}")
                self.piece_moved[promoted_piece] = True

    def game_finished(self):
        # Check if any D/d was captured
        d_exists = {'d': False, 'D': False}
        for row in self.board.layout:
            for piece in row:
                if piece == 'd':
                    d_exists['d'] = True
                elif piece == 'D':
                    d_exists['D'] = True
        return not d_exists['d'] or not d_exists['D']

    def get_winner(self):
        d_exists = {'d': False, 'D': False}
        for row in self.board.layout:
            for piece in row:
                if piece == 'd':
                    d_exists['d'] = True
                elif piece == 'D':
                    d_exists['D'] = True
        
        if not d_exists['d']:
            return 2  # Player 2 wins
        elif not d_exists['D']:
            return 1  # Player 1 wins
        return None

    def next_player(self):
        return 3 - self.current_player  # Switches between 1 and 2

    def prompt_current_player(self):
        return input(f"Player {self.current_player}, enter your move (e.g., '1,2 2,2'): ")

    def finish_message(self, winner):
        print(f"\nGame over! Player {winner} wins!")

if __name__ == '__main__':
    # Create initial board layout
    layout = (
        "ABCDECBA\n"
        "FFFFFFFF\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "ffffffff\n"
        "abcdecba"
    )
    board = Board((8, 8), layout)
    game = Obsidian(board)
    game.game_loop()
