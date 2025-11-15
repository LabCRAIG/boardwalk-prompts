from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Saffron(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 1's piece is 'A', Player 2's piece is 'B'
        self.pieces = ['A', 'B']
        # Player 1's marker is 'a', Player 2's marker is 'b'
        self.markers = ['a', 'b']
        
    def initial_player(self):
        return Player.ONE.value
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
            
        origin, destination = get_move_elements(move)
        
        # Check if origin has the current player's piece
        player_piece = self.pieces[self.current_player]
        if self.board.layout[origin] != player_piece:
            return False
            
        # Check if destination is empty (blank)
        if self.board.layout[destination] != '_':
            return False
            
        # Check if the move is orthogonal (only one coordinate changes by 1)
        row_diff = abs(origin[0] - destination[0])
        col_diff = abs(origin[1] - destination[1])
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
            
        return True
    
    def perform_move(self, move):
        origin, destination = get_move_elements(move)
        
        # First move the piece
        super().perform_move(move)
        
        # Then place the marker at the origin
        marker = self.markers[self.current_player]
        marker_move = f"{marker} {origin[0]},{origin[1]}"
        self.board.place_piece(marker_move)
    
    def game_finished(self):
        # Game finishes if any player has moved their piece onto a marker
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] in self.pieces:
                    # Look at the 4 orthogonal directions
                    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ni, nj = i + di, j + dj
                        # Check if the position is valid
                        if 0 <= ni < self.board.height and 0 <= nj < self.board.width:
                            # If there's a marker in an adjacent space, the player has to move onto it next turn
                            if self.board.layout[ni, nj] in self.markers:
                                # Check if there's at least one other valid move
                                has_valid_moves = False
                                for di2, dj2 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                                    ni2, nj2 = i + di2, j + dj2
                                    if (di, dj) != (di2, dj2) and 0 <= ni2 < self.board.height and 0 <= nj2 < self.board.width:
                                        if self.board.layout[ni2, nj2] == '_':
                                            has_valid_moves = True
                                            break
                                if not has_valid_moves:
                                    return True
        
        # Check if any player has already moved onto a marker
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] in self.pieces:
                    piece_idx = self.pieces.index(self.board.layout[i, j])
                    player_idx = (piece_idx + 1) % 2  # Player who just moved
                    # Check if the player's piece is on a marker
                    for marker in self.markers:
                        if self.previous_position_had_marker(i, j, piece_idx, player_idx):
                            return True
        
        return False
    
    def previous_position_had_marker(self, i, j, piece_idx, player_idx):
        # This is a helper method to check if the current piece position had a marker in the previous state
        # We deduce this by checking if there are markers adjacent to the piece
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.board.height and 0 <= nj < self.board.width:
                if self.board.layout[ni, nj] == self.markers[player_idx]:
                    return True
        return False
    
    def get_winner(self):
        # The player who just moved loses if they landed on a marker
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] in self.pieces:
                    piece_idx = self.pieces.index(self.board.layout[i, j])
                    player_idx = piece_idx
                    if self.previous_position_had_marker(i, j, piece_idx, (player_idx + 1) % 2):
                        # The current player lost, so the other player wins
                        return (player_idx + 1) % 2
        
        # If no one has won yet, check if any player has no valid moves
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] == self.pieces[self.current_player]:
                    has_valid_moves = False
                    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.board.height and 0 <= nj < self.board.width:
                            if self.board.layout[ni, nj] == '_':
                                has_valid_moves = True
                                break
                    if not has_valid_moves:
                        # Current player has no valid moves, so the other player wins
                        return (self.current_player + 1) % 2
        
        return None
    
    def next_player(self):
        return (self.current_player + 1) % 2
    
    def get_state(self):
        base_state = super().get_state()
        return (base_state[0], base_state[1], base_state[2])
    
    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("The game ended in a draw.")

if __name__ == '__main__':
    # Create an 8x8 board with initial setup
    initial_layout = ""
    for i in range(8):
        for j in range(8):
            if i == 3 and j == 3:
                initial_layout += "A"
            elif i == 4 and j == 4:
                initial_layout += "B"
            else:
                initial_layout += "_"
        if i < 7:  # Don't add newline after the last row
            initial_layout += "\n"
    
    board = Board((8, 8), initial_layout)
    game = Saffron(board)
    game.game_loop()