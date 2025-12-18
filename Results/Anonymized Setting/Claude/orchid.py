from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    PLAYER1 = 0  # Controls A pieces
    PLAYER2 = 1  # Controls B pieces

class Orchid(Game):
    def __init__(self, board):
        super().__init__(board)
        self.player_pieces = {
            Player.PLAYER1.value: 'A',
            Player.PLAYER2.value: 'B'
        }
        # Keep track of how many pieces each player has placed
        self.pieces_placed = {
            Player.PLAYER1.value: 0,
            Player.PLAYER2.value: 12,
            Player.PLAYER2.value: 0
        }
        # Total number of pieces per player
        self.total_pieces = 12
        # Keep track of how many pieces each player has on the board
        self.pieces_on_board = {
            Player.PLAYER1.value: 0,
            Player.PLAYER2.value: 0
        }
        # Flag to determine game phase
        self.placement_phase = True

    def prompt_current_player(self):
        piece_type = self.player_pieces[self.current_player]
        
        if self.placement_phase:
            remaining = self.total_pieces - self.pieces_placed[self.current_player]
            print(f"Player {self.current_player + 1}'s turn ({piece_type})")
            print(f"Placement phase - {remaining} pieces remaining")
            print("Enter two placements with format: X row,col row,col")
            return input("Your move: ")
        else:
            print(f"Player {self.current_player + 1}'s turn ({piece_type})")
            print("Movement phase - enter move with format: row,col row,col")
            return input("Your move: ")

    def validate_move(self, move):
        # Basic validation from parent class
        if not super().validate_move(move):
            print("Invalid coordinates.")
            return False
            
        # During placement phase, two pieces must be placed
        if self.placement_phase:
            # Check if the format is two placements
            parts = move.split()
            if len(parts) != 3:
                print("In placement phase, you must place two pieces with format: X row,col row,col")
                return False
                
            piece_type = parts[0]
            pos1_str = parts[1]
            pos2_str = parts[2]
            
            # Validate piece type belongs to current player
            if piece_type != self.player_pieces[self.current_player]:
                print(f"You can only place {self.player_pieces[self.current_player]} pieces.")
                return False
                
            # Validate both positions
            try:
                pos1 = tuple(map(int, pos1_str.split(',')))
                pos2 = tuple(map(int, pos2_str.split(',')))
            except:
                print("Invalid coordinate format. Use row,col format.")
                return False
                
            # Check if positions are valid (not the middle and empty)
            middle = (self.board.height // 2, self.board.width // 2)
            
            if pos1 == middle or pos2 == middle:
                print("You cannot place a piece in the middle of the board.")
                return False
                
            if self.board.layout[pos1[0]][pos1[1]] != '_':
                print(f"Position {pos1} is already occupied.")
                return False
                
            if self.board.layout[pos2[0]][pos2[1]] != '_':
                print(f"Position {pos2} is already occupied.")
                return False
                
            # Check if the player has enough pieces to place
            if self.pieces_placed[self.current_player] + 2 > self.total_pieces:
                print("You don't have enough pieces left to place.")
                return False
                
            return True
            
        else:  # Movement phase
            if not is_movement(move):
                print("In movement phase, use format: origin_row,origin_col dest_row,dest_col")
                return False
                
            origin, dest = get_move_elements(move)
            
            # Check if origin has player's piece
            if self.board.layout[origin[0]][origin[1]] != self.player_pieces[self.current_player]:
                print("You can only move your own pieces.")
                return False
                
            # Check if destination is empty
            if self.board.layout[dest[0]][dest[1]] != '_':
                print("Destination must be empty.")
                return False
                
            # Check if move is orthogonal
            if origin[0] != dest[0] and origin[1] != dest[1]:
                print("Moves must be orthogonal (same row or same column).")
                return False
                
            # Check if path is clear
            if origin[0] == dest[0]:  # Horizontal move
                start = min(origin[1], dest[1])
                end = max(origin[1], dest[1])
                for col in range(start + 1, end):
                    if self.board.layout[origin[0]][col] != '_':
                        print("Path is not clear for movement.")
                        return False
            else:  # Vertical move
                start = min(origin[0], dest[0])
                end = max(origin[0], dest[0])
                for row in range(start + 1, end):
                    if self.board.layout[row][origin[1]] != '_':
                        print("Path is not clear for movement.")
                        return False
                        
            return True

    def perform_move(self, move):
        if self.placement_phase:
            # Place two pieces
            parts = move.split()
            piece_type = parts[0]
            pos1_str = parts[1]
            pos2_str = parts[2]
            
            # Create and perform two placement moves
            placement1 = f"{piece_type} {pos1_str}"
            placement2 = f"{piece_type} {pos2_str}"
            
            self.board.place_piece(placement1)
            self.board.place_piece(placement2)
            
            # Update pieces placed and on board
            self.pieces_placed[self.current_player] += 2
            self.pieces_on_board[self.current_player] += 2
            
            # Check if placement phase is complete
            if self.pieces_placed[Player.PLAYER1.value] == self.total_pieces and \
               self.pieces_placed[Player.PLAYER2.value] == self.total_pieces:
                self.placement_phase = False
                print("\n--- Placement phase complete. Starting movement phase. ---\n")
        else:
            # Movement phase
            origin, dest = get_move_elements(move)
            
            # Perform the move
            self.board.move_piece(move)
            
            # Check for captures in all four orthogonal directions
            captures = self.check_captures(dest)
            
            # Update pieces on board
            opponent = 1 - self.current_player
            self.pieces_on_board[opponent] -= captures
    
    def check_captures(self, pos):
        """Check for captures in all four orthogonal directions from the position"""
        captures = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        player_piece = self.player_pieces[self.current_player]
        opponent_piece = self.player_pieces[1 - self.current_player]
        
        for dr, dc in directions:
            # Look for opponent's pieces in this direction
            opponent_pieces = []
            r, c = pos[0] + dr, pos[1] + dc
            
            # Collect opponent pieces until we hit a boundary, empty space, or player piece
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r][c] == opponent_piece:
                    opponent_pieces.append((r, c))
                elif self.board.layout[r][c] == player_piece:
                    # Found sandwiching piece, capture all opponent pieces in between
                    for opp_r, opp_c in opponent_pieces:
                        self.board.layout[opp_r][opp_c] = '_'
                    captures += len(opponent_pieces)
                    break
                else:
                    # Found empty space or boundary, no captures
                    break
                    
                r += dr
                c += dc
                
        return captures
    
    def has_valid_moves(self, player):
        """Check if the player has any valid moves"""
        piece = self.player_pieces[player]
        
        # If no pieces on board, no valid moves
        if self.pieces_on_board[player] == 0:
            return False
            
        # Check for each piece of the player
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.layout[r][c] == piece:
                    # Check if this piece can move in any direction
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        # If there's at least one empty space in that direction, the player can move
                        while 0 <= nr < self.board.height and 0 <= nc < self.board.width:
                            if self.board.layout[nr][nc] == '_':
                                return True
                            else:
                                break
                            nr += dr
                            nc += dc
        return False

    def game_finished(self):
        # Game is finished if one player has no pieces left
        if self.pieces_on_board[Player.PLAYER1.value] == 0 or self.pieces_on_board[Player.PLAYER2.value] == 0:
            return True
        
        # If we're in movement phase and both players have no valid moves, game is finished
        if not self.placement_phase:
            if (not self.has_valid_moves(Player.PLAYER1.value) and 
                not self.has_valid_moves(Player.PLAYER2.value)):
                return True
                
        return False

    def get_winner(self):
        if self.pieces_on_board[Player.PLAYER1.value] == 0:
            return Player.PLAYER2.value
        elif self.pieces_on_board[Player.PLAYER2.value] == 0:
            return Player.PLAYER1.value
        else:
            # If both players have no valid moves, the one with more pieces wins
            return Player.PLAYER1.value if self.pieces_on_board[Player.PLAYER1.value] > self.pieces_on_board[Player.PLAYER2.value] else Player.PLAYER2.value

    def next_player(self):
        # If in movement phase and current player has no valid moves, the next player plays again
        if not self.placement_phase:
            next_player = 1 - self.current_player
            if not self.has_valid_moves(next_player):
                print(f"Player {next_player + 1} has no valid moves and passes their turn.")
                return self.current_player
                
        # Otherwise, players alternate normally
        return 1 - self.current_player

    def get_state(self):
        base_state = super().get_state()
        additional_params = [
            self.pieces_placed[Player.PLAYER1.value],
            self.pieces_placed[Player.PLAYER2.value],
            self.pieces_on_board[Player.PLAYER1.value],
            self.pieces_on_board[Player.PLAYER2.value],
            self.placement_phase
        ]
        return (base_state[0], base_state[1], additional_params)

    def finish_message(self, winner):
        print(f"Game over! Player {winner + 1} wins!")
        print(f"Final score - Player 1: {self.pieces_on_board[Player.PLAYER1.value]} pieces, Player 2: {self.pieces_on_board[Player.PLAYER2.value]} pieces")

if __name__ == '__main__':
    board = Board((5, 5))
    game = Orchid(board)
    game.game_loop()
