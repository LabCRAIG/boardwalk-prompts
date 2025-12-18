
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    BLACK = 0
    WHITE = 1

class Reversi(Game):
    def __init__(self, board):
        super().__init__(board)
        self.kings_played = {Player.BLACK: False, Player.WHITE: False}
        self.player_pieces = {Player.BLACK: 'B', Player.WHITE: 'W'}
        self.king_pieces = {Player.BLACK: 'K', Player.WHITE: 'Q'}  # Q for white king
        # Set up initial board state
        self.board.place_piece("W 3,3")
        self.board.place_piece("B 3,4")
        self.board.place_piece("B 4,3")
        self.board.place_piece("W 4,4")
    
    def initial_player(self):
        return Player.BLACK.value
    
    def prompt_current_player(self):
        piece = self.player_pieces[Player(self.current_player)]
        king_piece = self.king_pieces[Player(self.current_player)]
        king_status = "" if self.kings_played[Player(self.current_player)] else f" (you can play your king {king_piece})"
        return input(f"Player {piece}'s move{king_status}: ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            print("Invalid coordinates!")
            return False
        
        if not is_placement(move):
            print("You can only place pieces, not move them!")
            return False
        
        piece, position = get_move_elements(move)
        current_player = Player(self.current_player)
        
        # Check if the piece is valid for the current player
        if piece == self.king_pieces[current_player]:
            if self.kings_played[current_player]:
                print("You've already played your king!")
                return False
        elif piece != self.player_pieces[current_player]:
            print("You can only play your own pieces!")
            return False
        
        row, col = position
        
        # Check if position is occupied
        if self.board.layout[row, col] != '_':
            print("That position is already occupied!")
            return False
        
        # Check if the move captures any pieces
        if not self._would_capture(position, piece):
            print("You must capture at least one opponent's piece!")
            return False
            
        return True
    
    def _would_capture(self, position, piece):
        row, col = position
        opponent_piece = self.player_pieces[Player(1 - self.current_player)]
        opponent_king = self.king_pieces[Player(1 - self.current_player)]
        
        # The 8 directions: up, up-right, right, down-right, down, down-left, left, up-left
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        
        captured = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            line = []
            
            # Traverse in this direction
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] in [opponent_piece, opponent_king]:
                    line.append((r, c))
                    r += dr
                    c += dc
                else:
                    break
            
            # If we found opponent pieces and then our own piece, we can capture
            if line and 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] in [self.player_pieces[Player(self.current_player)], 
                                              self.king_pieces[Player(self.current_player)]]:
                    # Check if the line contains the opponent's king
                    if any(self.board.layout[i, j] == opponent_king for i, j in line):
                        # Can't capture a line containing the king
                        continue
                    captured = True
            
        return captured
    
    def perform_move(self, move):
        piece, position = get_move_elements(move)
        
        # If it's a king, mark it as played
        if piece == self.king_pieces[Player(self.current_player)]:
            self.kings_played[Player(self.current_player)] = True
        
        # Place the piece
        super().perform_move(move)
        
        # Capture pieces
        self._capture_pieces(position, piece)
    
    def _capture_pieces(self, position, piece):
        row, col = position
        opponent_piece = self.player_pieces[Player(1 - self.current_player)]
        opponent_king = self.king_pieces[Player(1 - self.current_player)]
        current_piece = self.player_pieces[Player(self.current_player)]
        current_king = self.king_pieces[Player(self.current_player)]
        
        # The 8 directions: up, up-right, right, down-right, down, down-left, left, up-left
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            
            # Traverse in this direction
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] in [opponent_piece, opponent_king]:
                    to_flip.append((r, c))
                    r += dr
                    c += dc
                else:
                    break
            
            # If we found opponent pieces and then our own piece, flip them
            if to_flip and 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] in [current_piece, current_king]:
                    # Check if the line contains the opponent's king
                    if any(self.board.layout[i, j] == opponent_king for i, j in to_flip):
                        # Can't capture a line containing the king
                        continue
                    for flip_r, flip_c in to_flip:
                        # If we're flipping an opponent's piece, make it our regular piece (not a king)
                        self.board.place_piece(f"{current_piece} {flip_r},{flip_c}")
    
    def game_finished(self):
        # Game is finished if neither player can make a valid move
        
        # Save current player
        current = self.current_player
        
        # Check if current player can make a move
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_':
                    # Try regular piece
                    if self._would_capture((row, col), self.player_pieces[Player(self.current_player)]):
                        return False
                    
                    # Try king if not played yet
                    if not self.kings_played[Player(self.current_player)]:
                        if self._would_capture((row, col), self.king_pieces[Player(self.current_player)]):
                            return False
        
        # Switch player to check if they can make a move
        self.current_player = 1 - self.current_player
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_':
                    # Try regular piece
                    if self._would_capture((row, col), self.player_pieces[Player(self.current_player)]):
                        # Restore original player
                        self.current_player = current
                        return False
                    
                    # Try king if not played yet
                    if not self.kings_played[Player(self.current_player)]:
                        if self._would_capture((row, col), self.king_pieces[Player(self.current_player)]):
                            # Restore original player
                            self.current_player = current
                            return False
        
        # Restore original player
        self.current_player = current
        return True
    
    def get_winner(self):
        # Count pieces
        black_count = 0
        white_count = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] in ['B', 'K']:
                    black_count += 1
                elif self.board.layout[row, col] in ['W', 'Q']:
                    white_count += 1
        
        if black_count > white_count:
            return Player.BLACK.value
        elif white_count > black_count:
            return Player.WHITE.value
        else:
            return None  # Draw
    
    def next_player(self):
        next_player = 1 - self.current_player
        
        # Check if next player can make a valid move
        can_move = False
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_':
                    # Try regular piece
                    if self._would_capture((row, col), self.player_pieces[Player(next_player)]):
                        can_move = True
                        break
                    
                    # Try king if not played yet
                    if not self.kings_played[Player(next_player)]:
                        if self._would_capture((row, col), self.king_pieces[Player(next_player)]):
                            can_move = True
                            break
            
            if can_move:
                break
        
        if can_move:
            return next_player
        else:
            # Skip turn if player can't move
            print(f"Player {self.player_pieces[Player(next_player)]} cannot make a valid move. Skipping turn.")
            return self.current_player
    
    def get_state(self):
        state_tuple = super().get_state()
        additional_params = state_tuple[2]
        additional_params.extend([
            self.kings_played[Player.BLACK],
            self.kings_played[Player.WHITE]
        ])
        return (state_tuple[0], state_tuple[1], additional_params)
    
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            piece = self.player_pieces[Player(winner)]
            print(f"Player {piece} wins!")

if __name__ == '__main__':
    board = Board((8, 8))
    mygame = Reversi(board)
    mygame.game_loop()
