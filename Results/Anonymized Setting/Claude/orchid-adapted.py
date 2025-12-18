from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import IntEnum
from copy import deepcopy

class Player(IntEnum):
    ONE = 0
    TWO = 1

class Orchid(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        
        # Piece counts for each player
        self.player_pieces = [12, 12]  # pieces still in play
        self.player_hand = [12, 12]    # pieces still to be placed
        
        # Current game phase (1 = placement, 2 = movement)
        self.phase = 1
        
        # Middle position is (2, 2)
        self.middle = (2, 2)
    
    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False
        
        if self.phase == 1:
            # In placement phase, we can only place pieces
            if not is_placement(move):
                print("In placement phase, you can only place pieces.")
                return False
            
            piece, position = get_move_elements(move)
            
            # Check if it's the right player's piece
            expected_piece = 'A' if self.current_player == Player.ONE else 'B'
            if piece != expected_piece:
                print(f"You must place your own pieces ({expected_piece}).")
                return False
            
            # Check if position is the middle
            if position == self.middle:
                print("Cannot place a piece in the middle!")
                return False
            
            # Check if position is already occupied
            if self.board.layout[position] != '_':
                print("Position already occupied!")
                return False
            
            return True
            
        else:  # Phase 2 (movement)
            if not is_movement(move):
                print("In movement phase, you can only move pieces.")
                return False
            
            origin, destination = get_move_elements(move)
            
            # Check if the origin position has the player's piece
            expected_piece = 'A' if self.current_player == Player.ONE else 'B'
            if self.board.layout[origin] != expected_piece:
                print("You must select your own piece!")
                return False
            
            # Check if the destination is empty
            if self.board.layout[destination] != '_':
                print("Destination is not empty!")
                return False
            
            # Check if the movement is orthogonal
            if origin[0] != destination[0] and origin[1] != destination[1]:
                print("Movement must be orthogonal!")
                return False
            
            # Check if the path is clear
            if not self._is_path_clear(origin, destination):
                print("Path is not clear!")
                return False
            
            return True
    
    def _is_path_clear(self, origin, destination):
        """Check if the path between origin and destination is clear"""
        r1, c1 = origin
        r2, c2 = destination
        
        # Determine direction
        dr = 0 if r1 == r2 else (1 if r2 > r1 else -1)
        dc = 0 if c1 == c2 else (1 if c2 > c1 else -1)
        
        # Check each step along the path
        r, c = r1, c1
        while True:
            r += dr
            c += dc
            
            if (r, c) == destination:
                return True
                
            if self.board.layout[r, c] != '_':
                return False
    
    def perform_move(self, move: str):
        super().perform_move(move)
        
        if self.phase == 1:
            # Decrement pieces in hand
            self.player_hand[self.current_player] -= 1
            
            # Check if all pieces have been placed
            if sum(self.player_hand) == 0:
                self.phase = 2
                print("\nAll pieces placed! Moving to movement phase.")
        else:  # Phase 2
            # Check for captures after moving
            # Get the destination position from the move
            if is_movement(move):
                _, destination = get_move_elements(move)
                self._check_captures(destination)
    
    def _check_captures(self, position):
        """Check and handle captures after a move"""
        row, col = position
        current_piece = 'A' if self.current_player == Player.ONE else 'B'
        opponent_piece = 'B' if self.current_player == Player.ONE else 'A'
        opponent_player = Player.TWO if self.current_player == Player.ONE else Player.ONE
        
        # Check in all 4 orthogonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            # Check if there's an opponent's piece in this direction
            captured_positions = []
            r, c = row, col
            
            # Move in the direction to find opponent pieces
            while True:
                r += dr
                c += dc
                
                # If out of bounds or empty space, break
                if not (0 <= r < self.board.height and 0 <= c < self.board.width) or self.board.layout[r, c] == '_':
                    break
                
                # If we find our own piece after opponent pieces, we have a capture
                if self.board.layout[r, c] == current_piece and captured_positions:
                    # Capture all opponent pieces between
                    for capture_row, capture_col in captured_positions:
                        placement_move = f"_ {capture_row},{capture_col}"
                        self.board.place_piece(placement_move)
                        self.player_pieces[opponent_player] -= 1
                    break
                
                # If we find opponent's piece, add to potential captures
                if self.board.layout[r, c] == opponent_piece:
                    captured_positions.append((r, c))
    
    def game_finished(self) -> bool:
        # Check if any player has lost all their pieces
        if self.player_pieces[Player.ONE] == 0 or self.player_pieces[Player.TWO] == 0:
            return True
        
        # If we're in phase 2 and both players have passed (no valid moves)
        if self.phase == 2 and not self._has_valid_moves():
            return True
            
        return False
    
    def get_winner(self) -> int:
        if self.player_pieces[Player.ONE] == 0:
            return Player.TWO
        elif self.player_pieces[Player.TWO] == 0:
            return Player.ONE
        return None  # Draw
    
    def next_player(self) -> int:
        # If in phase 1, or if current player has valid moves in phase 2,
        # switch to the other player
        if self.phase == 1 or self._has_valid_moves():
            return Player.TWO if self.current_player == Player.ONE else Player.ONE
        
        # If in phase 2 and no valid moves, keep the same player
        # (simulates passing the turn)
        print(f"Player {self.current_player + 1} has no valid moves and passes.")
        return self.current_player
    
    def _has_valid_moves(self) -> bool:
        """Check if current player has any valid moves in phase 2"""
        if self.phase != 2:
            return True
            
        piece = 'A' if self.current_player == Player.ONE else 'B'
        
        # Check all positions for the player's pieces
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == piece:
                    # Check in all 4 orthogonal directions
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    
                    for dr, dc in directions:
                        r, c = row, col
                        while True:
                            r += dr
                            c += dc
                            # Check if position is on board
                            if not (0 <= r < self.board.height and 0 <= c < self.board.width):
                                break
                            # Check if position is free
                            if self.board.layout[r, c] == '_':
                                return True  # Found at least one valid move
                            else:
                                break  # Hit a piece, can't move further in this direction
        
        return False
    
    def prompt_current_player(self) -> str:
        player_name = "Player 1 (A)" if self.current_player == Player.ONE else "Player 2 (B)"
        
        if self.phase == 1:
            print(f"\n{player_name}'s turn (Placement Phase)")
            print(f"Pieces left to place: {self.player_hand[self.current_player]}")
            
            # In phase 1, players place two pieces at a time
            if self.player_hand[self.current_player] > 0:
                try:
                    piece = 'A' if self.current_player == Player.ONE else 'B'
                    row = int(input("Enter row: "))
                    col = int(input("Enter column: "))
                    return f"{piece} {row},{col}"
                except ValueError:
                    print("Please enter valid numbers for row and column.")
                    return self.prompt_current_player()
        else:  # Phase 2
            print(f"\n{player_name}'s turn (Movement Phase)")
            print(f"Player 1 (A) has {self.player_pieces[Player.ONE]} pieces")
            print(f"Player 2 (B) has {self.player_pieces[Player.TWO]} pieces")
            
            try:
                # Select origin position
                row1 = int(input("Select piece row: "))
                col1 = int(input("Select piece column: "))
                
                # Show valid moves for this piece
                valid_moves = self._get_valid_moves(row1, col1)
                if not valid_moves:
                    print("This piece has no valid moves. Choose another piece.")
                    return self.prompt_current_player()
                
                print("Valid moves:")
                for i, (move_row, move_col) in enumerate(valid_moves):
                    print(f"{i+1}: ({move_row}, {move_col})")
                
                # Select destination
                move_idx = int(input("Select move number: ")) - 1
                if 0 <= move_idx < len(valid_moves):
                    row2, col2 = valid_moves[move_idx]
                    return f"{row1},{col1} {row2},{col2}"
                else:
                    print("Invalid move selection!")
                    return self.prompt_current_player()
            except ValueError:
                print("Please enter valid numbers.")
                return self.prompt_current_player()
    
    def _get_valid_moves(self, row, col):
        """Get all valid orthogonal moves for a piece"""
        if not (0 <= row < self.board.height and 0 <= col < self.board.width):
            return []
            
        piece = 'A' if self.current_player == Player.ONE else 'B'
        if self.board.layout[row, col] != piece:
            return []
        
        valid_moves = []
        
        # Check in all 4 orthogonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                # Check if position is on board
                if not (0 <= r < self.board.height and 0 <= c < self.board.width):
                    break
                # Check if position is free
                if self.board.layout[r, c] == '_':
                    valid_moves.append((r, c))
                else:
                    break
        
        return valid_moves
    
    def get_state(self) -> tuple:
        state = super().get_state()
        # Add additional state variables
        state[2].extend([self.phase, self.player_pieces, self.player_hand])
        return state
    
    def initial_player(self) -> int:
        return Player.ONE
    
    def finish_message(self, winner):
        if winner == Player.ONE:
            print("Player 1 (A) wins by capturing all opponent pieces!")
        elif winner == Player.TWO:
            print("Player 2 (B) wins by capturing all opponent pieces!")
        else:
            print("The game ends in a draw!")


if __name__ == '__main__':
    print("Welcome to Orchid!")
    print("Player 1 controls A pieces, Player 2 controls B pieces")
    print("Phase 1: Each player places two pieces per turn")
    print("Phase 2: Move pieces orthogonally to capture opponent pieces")
    print("Win by capturing all opponent pieces")
    
    board = Board((5, 5))
    game = Orchid(board)
    game.game_loop()