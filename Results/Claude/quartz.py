from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Quartz(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 1 uses 'A', Player 2 uses 'V'
        self.player_pieces = {Player.ONE.value: 'A', Player.TWO.value: 'V'}
        # Initialize the board with the starting position
        self.board.place_piece("A 3,3")
        self.board.place_piece("V 3,4")
        self.board.place_piece("A 4,4")
        self.board.place_piece("V 4,3")
    
    def prompt_current_player(self):
        player_name = "Player 1 (A)" if self.current_player == Player.ONE.value else "Player 2 (V)"
        return input(f"{player_name}, your move: ")
    
    def validate_move(self, move):
        # First check if the move is valid according to the board
        if not super().validate_move(move):
            return False
        
        # Only placements are allowed in this game
        if not is_placement(move):
            return False
        
        # Get the piece and position from the move
        piece, position = get_move_elements(move)
        row, col = position
        
        # Check if the piece belongs to the current player
        if piece != self.player_pieces[self.current_player]:
            return False
        
        # Check if the position is available
        if self.board.layout[row][col] != '_':
            return False
        
        # Check if the move captures at least one opponent's piece
        return self._has_valid_capture(row, col)
    
    def _has_valid_capture(self, row, col):
        """Check if placing a piece at (row, col) would capture at least one opponent's piece."""
        current_piece = self.player_pieces[self.current_player]
        opponent_piece = self.player_pieces[1 - self.current_player]
        
        # Directions: horizontal, vertical, and diagonal
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # horizontal and vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonal
        ]
        
        capture_exists = False
        
        for dx, dy in directions:
            x, y = row + dx, col + dy
            # Check if there's at least one opponent piece in this direction
            if not (0 <= x < self.board.height and 0 <= y < self.board.width) or self.board.layout[x][y] != opponent_piece:
                continue
                
            # Keep moving in this direction until we find a blank space, edge, or own piece
            temp_x, temp_y = x, y
            while True:
                temp_x, temp_y = temp_x + dx, temp_y + dy
                
                # If we reached the edge of the board or a blank space, this direction doesn't work
                if not (0 <= temp_x < self.board.height and 0 <= temp_y < self.board.width) or self.board.layout[temp_x][temp_y] == '_':
                    break
                    
                # If we found our own piece, we have a valid capture in this direction
                if self.board.layout[temp_x][temp_y] == current_piece:
                    capture_exists = True
                    break
        
        return capture_exists
    
    def perform_move(self, move):
        # First perform the basic move (place the piece)
        super().perform_move(move)
        
        # Now flip the captured pieces
        piece, position = get_move_elements(move)
        row, col = position
        self._flip_captured_pieces(row, col)
    
    def _flip_captured_pieces(self, row, col):
        """Flip all captured pieces after placing a piece at (row, col)."""
        current_piece = self.player_pieces[self.current_player]
        opponent_piece = self.player_pieces[1 - self.current_player]
        
        # Directions: horizontal, vertical, and diagonal
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # horizontal and vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonal
        ]
        
        for dx, dy in directions:
            # Check if there's at least one opponent piece in this direction
            x, y = row + dx, col + dy
            if not (0 <= x < self.board.height and 0 <= y < self.board.width) or self.board.layout[x][y] != opponent_piece:
                continue
            
            # Keep track of pieces to flip
            pieces_to_flip = []
            temp_x, temp_y = x, y
            
            while True:
                pieces_to_flip.append((temp_x, temp_y))
                temp_x, temp_y = temp_x + dx, temp_y + dy
                
                # If we reached the edge of the board or a blank space, this direction doesn't work
                if not (0 <= temp_x < self.board.height and 0 <= temp_y < self.board.width) or self.board.layout[temp_x][temp_y] == '_':
                    pieces_to_flip = []
                    break
                    
                # If we found our own piece, we have a valid capture line
                if self.board.layout[temp_x][temp_y] == current_piece:
                    break
            
            # Flip all pieces in the capture line
            for flip_x, flip_y in pieces_to_flip:
                self.board.place_piece(f"{current_piece} {flip_x},{flip_y}")
    
    def game_finished(self):
        # Game ends when the board is full or neither player can make a move
        # Check if board is full
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == '_':
                    # Board is not full, check if either player can make a move
                    original_player = self.current_player
                    
                    # Check if current player can make a move
                    if self._player_has_moves():
                        return False
                    
                    # Check if other player can make a move
                    self.current_player = 1 - self.current_player
                    if self._player_has_moves():
                        # Restore original player
                        self.current_player = original_player
                        return False
                    
                    # Restore original player
                    self.current_player = original_player
                    return True
        
        # Board is full
        return True
    
    def _player_has_moves(self):
        """Check if the current player has any valid moves."""
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == '_':
                    if self._has_valid_capture(row, col):
                        return True
        return False
    
    def get_winner(self):
        # Count pieces for each player
        count_p1 = sum(row.count(self.player_pieces[Player.ONE.value]) for row in self.board.layout)
        count_p2 = sum(row.count(self.player_pieces[Player.TWO.value]) for row in self.board.layout)
        
        # Return winner based on piece count
        if count_p1 > count_p2:
            return Player.ONE.value
        elif count_p2 > count_p1:
            return Player.TWO.value
        else:
            return None  # Draw
    
    def next_player(self):
        next_player = 1 - self.current_player
        
        # Check if next player can make a move
        original_player = self.current_player
        self.current_player = next_player
        
        if not self._player_has_moves():
            # If next player can't make a move, it's still the current player's turn
            next_player = original_player
            
        # Restore original player
        self.current_player = original_player
        return next_player
    
    def get_state(self):
        board_layout = deepcopy(self.board.layout)
        current_player = self.current_player
        return (board_layout, current_player, [])
    
    def finish_message(self, winner):
        if winner is None:
            print("Game over! It's a draw!")
        else:
            player_name = "Player 1 (A)" if winner == Player.ONE.value else "Player 2 (V)"
            print(f"Game over! {player_name} wins!")

if __name__ == '__main__':
    board = Board((8, 8))
    mygame = Quartz(board)
    mygame.game_loop()