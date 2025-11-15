from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

class AmethystGame(Game):
    def __init__(self, board):
        super().__init__(board)
        # Additional state variables
        self.capture_in_progress = False
        self.capturing_piece_pos = None
        self.player1_pieces = set()  # Track player 1's pieces (A and Â)
        self.player2_pieces = set()  # Track player 2's pieces (O and Ô)
        
        # Initialize piece tracking sets
        self._init_piece_tracking()
    
    def _init_piece_tracking(self):
        """Initialize sets to track each player's pieces based on current board layout"""
        self.player1_pieces.clear()
        self.player2_pieces.clear()
        
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                if piece in {'A', 'Â'}:
                    self.player1_pieces.add((row, col))
                elif piece in {'O', 'Ô'}:
                    self.player2_pieces.add((row, col))
    
    def initial_player(self):
        """Return the first player to play (Player 1)"""
        return Player.PLAYER_1.value
    
    def prompt_current_player(self):
        """Prompt the current player for their move"""
        if self.capture_in_progress:
            print(f"Player {self.current_player + 1} must continue capturing with piece at "
                  f"{self.capturing_piece_pos[0]},{self.capturing_piece_pos[1]}")
            row, col = self.capturing_piece_pos
            moves = self._get_valid_moves(row, col)
            capture_moves = [move for move in moves if move[2]]  # Filter captures
            
            print("Available capture moves:")
            for i, (r, c, _) in enumerate(capture_moves):
                print(f"{i+1}: {r},{c}")
            
            choice = int(input("Choose a move (enter the number): ")) - 1
            while choice < 0 or choice >= len(capture_moves):
                choice = int(input("Invalid choice. Try again: ")) - 1
            
            end_row, end_col, _ = capture_moves[choice]
            return f"{row},{col} {end_row},{col}"
        else:
            # Regular turn
            print(f"Player {self.current_player + 1}'s turn")
            
            # Check for forced captures
            capture_moves = self._get_all_capture_moves()
            if capture_moves:
                print("You must make a capture.")
                
                # List pieces that can capture
                print("Pieces that can capture:")
                piece_positions = list(capture_moves.keys())
                for i, (r, c) in enumerate(piece_positions):
                    print(f"{i+1}: {r},{c} ({self.board.layout[r][c]})")
                
                piece_choice = int(input("Choose a piece (enter the number): ")) - 1
                while piece_choice < 0 or piece_choice >= len(piece_positions):
                    piece_choice = int(input("Invalid choice. Try again: ")) - 1
                
                row, col = piece_positions[piece_choice]
                
                # List capture moves for chosen piece
                moves = capture_moves[(row, col)]
                print("Available capture moves:")
                for i, (r, c, _) in enumerate(moves):
                    print(f"{i+1}: {r},{c}")
                
                move_choice = int(input("Choose a move (enter the number): ")) - 1
                while move_choice < 0 or move_choice >= len(moves):
                    move_choice = int(input("Invalid choice. Try again: ")) - 1
                
                end_row, end_col, _ = moves[move_choice]
                return f"{row},{col} {end_row},{end_col}"
            else:
                # Regular moves
                all_moves = self._get_all_valid_moves()
                
                # List pieces that can move
                print("Pieces that can move:")
                piece_positions = list(all_moves.keys())
                for i, (r, c) in enumerate(piece_positions):
                    print(f"{i+1}: {r},{c} ({self.board.layout[r][c]})")
                
                piece_choice = int(input("Choose a piece (enter the number): ")) - 1
                while piece_choice < 0 or piece_choice >= len(piece_positions):
                    piece_choice = int(input("Invalid choice. Try again: ")) - 1
                
                row, col = piece_positions[piece_choice]
                
                # List moves for chosen piece
                moves = all_moves[(row, col)]
                print("Available moves:")
                for i, (r, c, is_cap) in enumerate(moves):
                    move_type = "capture" if is_cap else "move"
                    print(f"{i+1}: {r},{c} ({move_type})")
                
                move_choice = int(input("Choose a move (enter the number): ")) - 1
                while move_choice < 0 or move_choice >= len(moves):
                    move_choice = int(input("Invalid choice. Try again: ")) - 1
                
                end_row, end_col, _ = moves[move_choice]
                return f"{row},{col} {end_row},{end_col}"
    
    def validate_move(self, move):
        """Verify if the move is valid according to the rules"""
        # Check if the move has valid format and coordinates
        if not super().validate_move(move):
            return False
        
        # We only use movements in this game, not placements
        if not is_movement(move):
            return False
        
        # Extract the movement coordinates
        origin, destination = get_move_elements(move)
        start_row, start_col = origin
        end_row, end_col = destination
        
        # Check if the piece belongs to the current player
        piece = self.board.layout[start_row][start_col]
        current_player_pieces = {'A', 'Â'} if self.current_player == Player.PLAYER_1.value else {'O', 'Ô'}
        if piece not in current_player_pieces:
            return False
        
        # If a capture is in progress, the player must continue capturing with the same piece
        if self.capture_in_progress and (start_row, start_col) != self.capturing_piece_pos:
            return False
        
        # Get all valid moves for the selected piece
        valid_moves = self._get_valid_moves(start_row, start_col)
        # Extract just the destination coordinates from valid moves for easy comparison
        valid_destinations = [(r, c) for r, c, _ in valid_moves]
        
        # Check if the destination is a valid move
        if (end_row, end_col) not in valid_destinations:
            return False
        
        # If there are captures available, player must make a capture
        all_captures = self._get_all_capture_moves()
        if all_captures and not self._is_capture_move(start_row, start_col, end_row, end_col):
            # There are captures available but this move isn't a capture
            return False
        
        return True
    
    def perform_move(self, move):
        """Perform the move and update the game state"""
        # Extract the movement coordinates
        origin, destination = get_move_elements(move)
        start_row, start_col = origin
        end_row, end_col = destination
        
        # Determine if this is a capture move
        is_capture = self._is_capture_move(start_row, start_col, end_row, end_col)
        
        # Get the moving piece
        piece = self.board.layout[start_row][start_col]
        player_pieces = self.player1_pieces if piece in {'A', 'Â'} else self.player2_pieces
        
        # Call the Board's move_piece method
        self.board.move_piece(move)
        
        # Update piece tracking
        player_pieces.remove((start_row, start_col))
        player_pieces.add((end_row, end_col))
        
        # Handle capture
        if is_capture:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board.layout[mid_row][mid_col]
            
            # Remove captured piece by placing a blank
            self.board.place_piece(f"_ {mid_row},{mid_col}")
            
            # Update piece tracking for captured piece
            if captured_piece in {'A', 'Â'}:
                self.player1_pieces.remove((mid_row, mid_col))
            else:
                self.player2_pieces.remove((mid_row, mid_col))
        
        # Handle promotion
        if piece == 'A' and end_row == 0:
            # Promote A to Â
            self.board.place_piece(f"Â {end_row},{end_col}")
        elif piece == 'O' and end_row == 7:
            # Promote O to Ô
            self.board.place_piece(f"Ô {end_row},{end_col}")
        
        # Check for additional captures
        additional_captures = False
        if is_capture:
            moves = self._get_valid_moves(end_row, end_col)
            capture_moves = [move for move in moves if move[2]]
            if capture_moves:
                additional_captures = True
                self.capture_in_progress = True
                self.capturing_piece_pos = (end_row, end_col)
            else:
                self.capture_in_progress = False
                self.capturing_piece_pos = None
        
        if not additional_captures and not self.capture_in_progress:
            # Switch players if no more captures
            self.capture_in_progress = False
            self.capturing_piece_pos = None
    
    def _is_capture_move(self, start_row, start_col, end_row, end_col):
        """Determine if a move is a capture based on coordinates"""
        # Capture moves jump 2 spaces diagonally
        return abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2
    
    def _is_valid_position(self, row, col):
        """Check if a position is within the board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def _is_blank_space(self, row, col):
        """Check if a position is a blank space on the board"""
        return self._is_valid_position(row, col) and self.board.layout[row][col] == '_'
    
    def _is_opponent_piece(self, row, col):
        """Check if a position contains an opponent's piece"""
        if not self._is_valid_position(row, col):
            return False
        
        piece = self.board.layout[row][col]
        current_player = self.current_player
        
        if current_player == Player.PLAYER_1.value:
            return piece in {'O', 'Ô'}
        else:  # Player 2
            return piece in {'A', 'Â'}
    
    def _get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        moves = []
        if not self._is_valid_position(row, col):
            return moves
        
        piece = self.board.layout[row][col]
        
        # Regular moves (1 step diagonally)
        directions = []
        if piece in {'A', 'Â', 'Ô'}:  # These pieces can move up
            directions.extend([(-1, -1), (-1, 1)])
        if piece in {'O', 'Â', 'Ô'}:  # These pieces can move down
            directions.extend([(1, -1), (1, 1)])
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self._is_blank_space(new_row, new_col):
                moves.append((new_row, new_col, False))  # False indicates not a capture
        
        # Captures (2 steps diagonally, jumping over opponent)
        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            if self._is_opponent_piece(mid_row, mid_col):
                end_row, end_col = mid_row + dr, mid_col + dc
                if self._is_blank_space(end_row, end_col):
                    moves.append((end_row, end_col, True))  # True indicates a capture
        
        return moves
    
    def _get_all_valid_moves(self):
        """Get all valid moves for the current player"""
        all_moves = {}
        player_pieces = self.player1_pieces if self.current_player == Player.PLAYER_1.value else self.player2_pieces
        
        # If a capture is in progress, only the capturing piece can move
        if self.capture_in_progress:
            row, col = self.capturing_piece_pos
            moves = self._get_valid_moves(row, col)
            if moves:
                all_moves[(row, col)] = moves
            return all_moves
        
        # Otherwise, check all pieces
        for row, col in player_pieces:
            moves = self._get_valid_moves(row, col)
            if moves:
                all_moves[(row, col)] = moves
                
        return all_moves
    
    def _get_all_capture_moves(self):
        """Get all moves that result in a capture for the current player"""
        all_captures = {}
        all_moves = self._get_all_valid_moves()
        
        for piece_pos, moves in all_moves.items():
            capture_moves = [move for move in moves if move[2]]  # Filter captures
            if capture_moves:
                all_captures[piece_pos] = capture_moves
                
        return all_captures
    
    def game_finished(self):
        """Check if the game is over"""
        # Game is over if a player has no pieces or no valid moves
        return self.get_winner() is not None
    
    def get_winner(self):
        """Determine the winner of the game, if any"""
        # Check if any player has no pieces left
        if not self.player1_pieces:
            return Player.PLAYER_2.value
        if not self.player2_pieces:
            return Player.PLAYER_1.value
        
        # Check if current player has no valid moves
        all_moves = self._get_all_valid_moves()
        if not all_moves:
            # Current player can't move, so the other player wins
            return Player.PLAYER_2.value if self.current_player == Player.PLAYER_1.value else Player.PLAYER_1.value
        
        # Game not over
        return None
    
    def next_player(self):
        """Determine the next player to move"""
        # If a capture is in progress, same player continues
        if self.capture_in_progress:
            return self.current_player
        
        # Otherwise, switch players
        return Player.PLAYER_2.value if self.current_player == Player.PLAYER_1.value else Player.PLAYER_1.value
    
    def get_state(self):
        """Return the current game state"""
        additional_state = [
            self.capture_in_progress,
            self.capturing_piece_pos,
            deepcopy(self.player1_pieces),
            deepcopy(self.player2_pieces)
        ]
        
        state = super().get_state()
        state[2].extend(additional_state)
        return state
    
    def finish_message(self, winner):
        """Display the game over message"""
        print(f"Game over! Player {winner + 1} wins!")


def create_initial_board():
    """Create the initial board layout string for the Amethyst game"""
    # Initialize with all alternating blank spaces
    layout = []
    for row in range(8):
        row_line = ""
        for col in range(8):
            # Create a checkerboard pattern with blanks '_' and nulls ' '
            if (row + col) % 2 == 0:
                row_line += '_'  # Playable space
            else:
                row_line += ' '  # Non-playable space
        layout.append(row_line)
    
    # Place Player 2 pieces (O) at the top
    for row in range(3):
        row_chars = list(layout[row])
        for col in range(8):
            if (row + col) % 2 == 0:
                row_chars[col] = 'O'
        layout[row] = ''.join(row_chars)
    
    # Place Player 1 pieces (A) at the bottom
    for row in range(5, 8):
        row_chars = list(layout[row])
        for col in range(8):
            if (row + col) % 2 == 0:
                row_chars[col] = 'A'
        layout[row] = ''.join(row_chars)
    
    return '\n'.join(layout)


if __name__ == '__main__':
    # Create initial board layout
    initial_layout = create_initial_board()
    
    # Create the board and game
    board = Board((8, 8), initial_layout)
    game = AmethystGame(board)
    
    # Display welcome message
    print("Welcome to Amethyst!")
    print("Player 1: A, Â (move upward)")
    print("Player 2: O, Ô (move downward)")
    print("Â and Ô can move both up and down")
    
    # Start the game
    game.game_loop()