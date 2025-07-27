from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Quartz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.player_pieces = {Player.ONE: 'A', Player.TWO: 'V'}
        self.current_player = self.initial_player()

    def initial_player(self):
        return Player.ONE

    def validate_move(self, move):
        # First check if the move is a valid format and within board bounds
        if not super().validate_move(move):
            return False
        
        # For Quartz, we only allow placement moves
        if not is_placement(move):
            print("Only placement moves are allowed in Quartz.")
            return False
        
        piece, (row, col) = get_move_elements(move)
        
        # Check if the piece belongs to the current player
        player_piece = self.player_pieces[self.current_player]
        if piece != player_piece:
            print(f"Player {self.current_player.name} can only place {player_piece} pieces.")
            return False
        
        # Check if the space is empty
        if self.board.layout[row][col] != '_':
            print("This space is already occupied.")
            return False
        
        # Check if the move would flip any opponent pieces
        return self._would_flip_pieces(row, col, player_piece)
    
    def _would_flip_pieces(self, row, col, player_piece):
        # Identify the opponent's piece
        opponent_piece = self.player_pieces[Player.TWO if self.current_player == Player.ONE else Player.ONE]
        
        # Check in all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        found_valid_direction = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            # First look for opponent pieces
            while (0 <= r < self.board.height and 0 <= c < self.board.width and 
                   self.board.layout[r][c] == opponent_piece):
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            
            # Then check if we found one of our own pieces at the end
            if (0 <= r < self.board.height and 0 <= c < self.board.width and 
                self.board.layout[r][c] == player_piece and pieces_to_flip):
                found_valid_direction = True
                break
        
        return found_valid_direction
    
    def perform_move(self, move):
        # Place the piece on the board
        super().perform_move(move)
        
        # Get the coordinates and piece type that was just placed
        piece, (row, col) = get_move_elements(move)
        
        # Flip opponent pieces in all directions
        self._flip_pieces(row, col, piece)
    
    def _flip_pieces(self, row, col, player_piece):
        # Identify the opponent's piece
        opponent_piece = self.player_pieces[Player.TWO if self.current_player == Player.ONE else Player.ONE]
        
        # Check in all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            # First look for opponent pieces
            while (0 <= r < self.board.height and 0 <= c < self.board.width and 
                   self.board.layout[r][c] == opponent_piece):
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            
            # Then check if we found one of our own pieces at the end
            if (0 <= r < self.board.height and 0 <= c < self.board.width and 
                self.board.layout[r][c] == player_piece and pieces_to_flip):
                # Flip all pieces in this direction
                for flip_r, flip_c in pieces_to_flip:
                    flip_move = f"{player_piece} {flip_r},{flip_c}"
                    self.board.place_piece(flip_move)
    
    def prompt_current_player(self):
        player_piece = self.player_pieces[self.current_player]
        valid_moves = self._get_valid_moves()
        
        print(f"Player {self.current_player.name}'s turn ({player_piece})")
        
        if valid_moves:
            print("Valid moves:", valid_moves)
            try:
                row = int(input("Enter row (0-7): "))
                col = int(input("Enter column (0-7): "))
                return f"{player_piece} {row},{col}"
            except ValueError:
                print("Please enter valid numbers.")
                return self.prompt_current_player()
        else:
            print(f"No valid moves for Player {self.current_player.name}. Passing turn.")
            return "PASS"
    
    def _get_valid_moves(self):
        valid_moves = []
        player_piece = self.player_pieces[self.current_player]
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                # Skip occupied spaces
                if self.board.layout[row][col] != '_':
                    continue
                
                # Check if placing a piece here would flip any opponent pieces
                if self._would_flip_pieces(row, col, player_piece):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def game_finished(self):
        # Check if the board is full
        if '_' not in ''.join(''.join(row) for row in self.board.layout):
            return True
        
        # Check if both players have no valid moves
        current_player_moves = self._get_valid_moves()
        if not current_player_moves:
            # Temporarily switch players to check other player's moves
            temp_player = self.current_player
            self.current_player = Player.TWO if self.current_player == Player.ONE else Player.ONE
            other_player_moves = self._get_valid_moves()
            self.current_player = temp_player  # Restore original player
            
            # If neither player has valid moves, the game is finished
            if not other_player_moves:
                return True
        
        return False
    
    def get_winner(self):
        # Count the pieces for each player
        count_a = sum(row.count('A') for row in self.board.layout)
        count_v = sum(row.count('V') for row in self.board.layout)
        
        if count_a > count_v:
            return Player.ONE
        elif count_v > count_a:
            return Player.TWO
        else:
            return None  # Draw
    
    def next_player(self):
        next_player = Player.TWO if self.current_player == Player.ONE else Player.ONE
        
        # Check if the next player has any valid moves
        temp_player = self.current_player
        self.current_player = next_player
        next_player_moves = self._get_valid_moves()
        self.current_player = temp_player  # Restore original player
        
        # If the next player has no valid moves, it remains the current player's turn
        if not next_player_moves:
            return self.current_player
        
        return next_player
    
    def get_state(self):
        state_tuple = super().get_state()
        # No additional state variables needed for this game
        return state_tuple
    
    def finish_message(self, winner):
        count_a = sum(row.count('A') for row in self.board.layout)
        count_v = sum(row.count('V') for row in self.board.layout)
        
        print(f"Final score - Player ONE (A): {count_a}, Player TWO (V): {count_v}")
        
        if winner is None:
            print("Game ended in a draw!")
        else:
            print(f"Player {winner.name} wins!")


if __name__ == '__main__':
    # Create initial layout for Quartz board
    # The center 2x2 square has 2 A's and 2 V's on diagonals
    initial_layout = ""
    for i in range(8):
        for j in range(8):
            if (i == 3 and j == 3) or (i == 4 and j == 4):
                initial_layout += 'A'
            elif (i == 3 and j == 4) or (i == 4 and j == 3):
                initial_layout += 'V'
            else:
                initial_layout += '_'
        if i < 7:  # Don't add newline after the last row
            initial_layout += '\n'
    
    board = Board((8, 8), initial_layout)
    game = Quartz(board)
    game.game_loop()