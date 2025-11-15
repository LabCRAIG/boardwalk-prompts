from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class GamePhase(Enum):
    PLACEMENT = 0
    MOVEMENT = 1

class Topaz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pieces_placed = {Player.ONE: 0, Player.TWO: 0}
        self.pieces_remaining = {Player.ONE: 9, Player.TWO: 9}
        self.phase = GamePhase.PLACEMENT
        self.last_move = None
        self.capture_pending = False
    
    def initial_player(self):
        return Player.ONE.value
    
    def prompt_current_player(self):
        player_char = 'A' if self.current_player == Player.ONE.value else 'B'
        phase_str = "placement" if self.phase == GamePhase.PLACEMENT else "movement"
        
        if self.capture_pending:
            prompt = f"Player {self.current_player + 1} ({player_char}), choose an opponent's piece to capture: "
        else:
            prompt = f"Player {self.current_player + 1} ({player_char}), your {phase_str} move: "
        
        move = input(prompt)
        return move
    
    def validate_move(self, move):
        # Check for basic format validity
        if not super().validate_move(move):
            print("Invalid move format.")
            return False
        
        # Handle capture move
        if self.capture_pending:
            if not is_placement(move):
                print("Capture should be in format 'X Y,Z'")
                return False
            
            piece, pos = get_move_elements(move)
            target_piece = self.board.layout[pos[0]][pos[1]]
            opponent_piece = 'B' if self.current_player == Player.ONE.value else 'A'
            
            if target_piece != opponent_piece:
                print(f"You must capture an opponent's piece ({opponent_piece}).")
                return False
            
            return True
        
        # Phase-specific validation
        if self.phase == GamePhase.PLACEMENT:
            if not is_placement(move):
                print("During placement phase, moves should be in format 'X Y,Z'")
                return False
            
            piece, pos = get_move_elements(move)
            player_piece = 'A' if self.current_player == Player.ONE.value else 'B'
            
            if piece != player_piece:
                print(f"Player {self.current_player + 1} must place {player_piece} pieces.")
                return False
            
            if self.board.layout[pos[0]][pos[1]] != '_':
                print("Piece must be placed on an empty space.")
                return False
            
            # Check if player has pieces left to place
            if self.pieces_placed[Player(self.current_player)] >= 9:
                print(f"Player {self.current_player + 1} has already placed all 9 pieces.")
                return False
            
            return True
        else:  # Movement phase
            if not is_movement(move):
                print("During movement phase, moves should be in format 'Y,Z W,X'")
                return False
            
            origin, dest = get_move_elements(move)
            
            # Check if origin contains player's piece
            player_piece = 'A' if self.current_player == Player.ONE.value else 'B'
            if self.board.layout[origin[0]][origin[1]] != player_piece:
                print(f"You must move your own piece ({player_piece}).")
                return False
            
            # Check if destination is empty
            if self.board.layout[dest[0]][dest[1]] != '_':
                print("Destination must be empty.")
                return False
            
            # Check if destination is adjacent (non-diagonal)
            if not self._is_adjacent(origin, dest):
                print("You can only move to an adjacent space (non-diagonal).")
                return False
            
            return True
    
    def _is_adjacent(self, origin, dest):
        # Check if the destination is adjacent in the same row or column
        # First check if they're in the same row or column
        same_row = origin[0] == dest[0]
        same_col = origin[1] == dest[1]
        
        if not (same_row or same_col):
            return False
            
        # Determine direction of movement
        if same_row:
            step = 1 if dest[1] > origin[1] else -1
            for col in range(origin[1] + step, dest[1] + step, step):
                if col == dest[1]:
                    return True
                # If there's a non-null, non-blank space in between, it's not adjacent
                if 0 <= col < self.board.width and self.board.layout[origin[0]][col] not in ['_', ' ']:
                    return False
        else:  # same_col
            step = 1 if dest[0] > origin[0] else -1
            for row in range(origin[0] + step, dest[0] + step, step):
                if row == dest[0]:
                    return True
                # If there's a non-null, non-blank space in between, it's not adjacent
                if 0 <= row < self.board.height and self.board.layout[row][origin[1]] not in ['_', ' ']:
                    return False
                    
        return True
    
    def perform_move(self, move):
        # Process captures
        if self.capture_pending:
            piece, pos = get_move_elements(move)
            self.board.layout[pos[0]][pos[1]] = '_'
            
            opponent = Player.TWO if self.current_player == Player.ONE.value else Player.ONE
            self.pieces_remaining[opponent] -= 1
            
            self.capture_pending = False
            return
        
        # Perform regular move
        super().perform_move(move)
        self.last_move = move
        
        # Track pieces placed during placement phase
        if self.phase == GamePhase.PLACEMENT:
            self.pieces_placed[Player(self.current_player)] += 1
            
            # Check if we should transition to movement phase
            if self.pieces_placed[Player.ONE] == 9 and self.pieces_placed[Player.TWO] == 9:
                self.phase = GamePhase.MOVEMENT
        
        # Check for captures
        if self._check_capture():
            self.capture_pending = True
    
    def _check_capture(self):
        # Get the position affected by the last move
        if is_placement(self.last_move):
            _, pos = get_move_elements(self.last_move)
        else:  # movement
            _, pos = get_move_elements(self.last_move)
        
        player_piece = 'A' if self.current_player == Player.ONE.value else 'B'
        
        # Check horizontal line
        row, col = pos
        aligned = 0
        # Check to the left
        c = col
        while c >= 0 and self.board.layout[row][c] == player_piece:
            aligned += 1
            c -= 1
        
        # Check to the right
        c = col + 1
        while c < self.board.width and self.board.layout[row][c] == player_piece:
            aligned += 1
            c += 1
        
        if aligned >= 3:
            return True
        
        # Check vertical line
        aligned = 0
        # Check upward
        r = row
        while r >= 0 and self.board.layout[r][col] == player_piece:
            aligned += 1
            r -= 1
        
        # Check downward
        r = row + 1
        while r < self.board.height and self.board.layout[r][col] == player_piece:
            aligned += 1
            r += 1
        
        return aligned >= 3
    
    def next_player(self):
        # If capture is pending, same player continues
        if self.capture_pending:
            return self.current_player
        
        # Otherwise, alternate players
        return (self.current_player + 1) % 2
    
    def game_finished(self):
        # Game can only end during movement phase
        if self.phase != GamePhase.MOVEMENT:
            return False
        
        # If a player has only 2 or fewer pieces left, they lose
        if self.pieces_remaining[Player.ONE] <= 2 or self.pieces_remaining[Player.TWO] <= 2:
            return True
        
        # Check if any player can't move any pieces
        for player_enum in Player:
            player = player_enum.value
            piece = 'A' if player == Player.ONE.value else 'B'
            can_move = False
            
            # Check each position on the board
            for row in range(self.board.height):
                for col in range(self.board.width):
                    if self.board.layout[row][col] != piece:
                        continue
                    
                    # Check if this piece can move to any adjacent position
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_row, new_col = row + dr, col + dc
                        
                        # Skip out-of-bounds positions
                        if not (0 <= new_row < self.board.height and 0 <= new_col < self.board.width):
                            continue
                        
                        # If there's an empty adjacent space, the piece can move
                        if self.board.layout[new_row][new_col] == '_':
                            if self._is_adjacent((row, col), (new_row, new_col)):
                                can_move = True
                                break
                    
                    if can_move:
                        break
                
                if can_move:
                    break
            
            # If a player can't move any piece, they lose
            if not can_move and not self.capture_pending:
                return True
        
        return False
    
    def get_winner(self):
        # The winner is the player with more than 2 pieces
        if self.pieces_remaining[Player.ONE] <= 2:
            return Player.TWO.value
        elif self.pieces_remaining[Player.TWO] <= 2:
            return Player.ONE.value
        
        # Or the player who can still move
        for player_enum in Player:
            player = player_enum.value
            piece = 'A' if player == Player.ONE.value else 'B'
            can_move = False
            
            # Check each position on the board
            for row in range(self.board.height):
                for col in range(self.board.width):
                    if self.board.layout[row][col] != piece:
                        continue
                    
                    # Check if this piece can move to any adjacent position
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_row, new_col = row + dr, col + dc
                        
                        # Skip out-of-bounds positions
                        if not (0 <= new_row < self.board.height and 0 <= new_col < self.board.width):
                            continue
                        
                        # If there's an empty adjacent space, the piece can move
                        if self.board.layout[new_row][new_col] == '_':
                            if self._is_adjacent((row, col), (new_row, new_col)):
                                can_move = True
                                break
                    
                    if can_move:
                        break
                
                if can_move:
                    break
            
            if not can_move and not self.capture_pending:
                return (player + 1) % 2
        
        # This should not happen
        return None
    
    def get_state(self):
        state = super().get_state()
        additional_params = [
            self.phase,
            self.pieces_placed[Player.ONE],
            self.pieces_placed[Player.TWO],
            self.pieces_remaining[Player.ONE],
            self.pieces_remaining[Player.TWO],
            self.capture_pending
        ]
        return (state[0], state[1], additional_params)
    
    def finish_message(self, winner):
        winner_piece = 'A' if winner == Player.ONE.value else 'B'
        print(f"Player {winner + 1} ({winner_piece}) wins!")
        
        if self.pieces_remaining[Player.ONE if winner == Player.TWO.value else Player.TWO] <= 2:
            print("The opponent has 2 or fewer pieces left.")
        else:
            print("The opponent has no valid moves left.")

if __name__ == '__main__':
    # Create the board with the null spaces pattern as specified
    initial_layout = "___    \n___    \n___    \n_______\n___    \n___    \n___    "
    board = Board((7, 7), initial_layout)
    
    # Create and start the game
    topaz_game = Topaz(board)
    topaz_game.game_loop()