from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
import numpy as np
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Saffron(Game):
    def __init__(self, board: Board):
        """Initialize the Saffron game with the provided board."""
        super().__init__(board)
        # Track positions of the main pieces for easy access
        self.a_position = (3, 3)
        self.b_position = (4, 4)
        # Game status tracking
        self.game_finished_flag = False
        self.winner = None

    def validate_move(self, move: str) -> bool:
        """Verify if the specified move is valid according to Saffron rules."""
        # Use parent validation to check if coordinates are within board boundaries
        if not super().validate_move(move):
            return False

        if not is_movement(move):
            return False

        # Get origin and destination coordinates
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination

        # Check if origin contains the current player's piece
        current_piece = 'A' if self.current_player == Player.ONE.value else 'B'
        if self.board.layout[origin_row][origin_col] != current_piece:
            return False

        # Check if destination is empty (not occupied by A, B, a, or b)
        dest_content = self.board.layout[dest_row][dest_col]
        if dest_content != '_':
            # We allow moving onto markers since this is handled in perform_move
            # as a loss condition
            if dest_content in ['A', 'B']:
                return False

        # Check if the move is orthogonal (exactly one space horizontally or vertically)
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False

        return True

    def perform_move(self, move: str):
        """Execute the move and update the game state according to Saffron rules."""
        # Get origin and destination coordinates
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination

        # Get current player's marker
        current_piece = 'A' if self.current_player == Player.ONE.value else 'B'
        current_marker = 'a' if self.current_player == Player.ONE.value else 'b'

        # Check if destination has a marker (loss condition)
        dest_content = self.board.layout[dest_row][dest_col]
        if dest_content in ['a', 'b']:
            # Current player loses by moving onto a marker
            self.game_finished_flag = True
            self.winner = Player.TWO.value if self.current_player == Player.ONE.value else Player.ONE.value
        
        # Move the piece (this will place a blank at the origin)
        self.board.move_piece(move)
        
        # Place the appropriate marker at the origin position
        marker_move = f"{current_marker} {origin_row},{origin_col}"
        self.board.place_piece(marker_move)

        # Update position trackers
        if self.current_player == Player.ONE.value:
            self.a_position = destination
        else:
            self.b_position = destination

    def game_finished(self) -> bool:
        """Check if the game has ended."""
        if self.game_finished_flag:
            return True
            
        # Check if current player has any valid moves
        current_piece_pos = self.a_position if self.current_player == Player.ONE.value else self.b_position
        row, col = current_piece_pos
        
        # Check all orthogonal directions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            
            # Skip if out of bounds
            if not (0 <= new_row < self.board.height and 0 <= new_col < self.board.width):
                continue
                
            # Check if the position is valid to move to (not occupied by the other player's piece)
            content = self.board.layout[new_row][new_col]
            other_piece = 'B' if self.current_player == Player.ONE.value else 'A'
            if content != other_piece:
                # We found at least one valid move
                return False
                
        # No valid moves found, current player loses
        self.game_finished_flag = True
        self.winner = Player.TWO.value if self.current_player == Player.ONE.value else Player.ONE.value
        return True

    def get_winner(self) -> int:
        """Return the winner of the game."""
        return self.winner

    def next_player(self) -> int:
        """Return the player that will play next."""
        return Player.TWO.value if self.current_player == Player.ONE.value else Player.ONE.value

    def initial_player(self) -> int:
        """Return the first player to act."""
        return Player.ONE.value

    def get_state(self) -> tuple:
        """Return the current game state."""
        base_state = super().get_state()
        # Add our custom state variables to the state tuple
        additional_params = base_state[2] + [self.a_position, self.b_position, self.game_finished_flag, self.winner]
        return (base_state[0], base_state[1], additional_params)

    def prompt_current_player(self) -> str:
        """Prompts the current player to input a move."""
        player_name = "1" if self.current_player == Player.ONE.value else "2"
        piece = "A" if self.current_player == Player.ONE.value else "B"
        piece_pos = self.a_position if self.current_player == Player.ONE.value else self.b_position
        
        # Display valid moves for the player
        valid_moves = []
        row, col = piece_pos
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            
            # Skip if out of bounds
            if not (0 <= new_row < self.board.height and 0 <= new_col < self.board.width):
                continue
                
            # Check if the position is valid to move to
            other_piece = 'B' if self.current_player == Player.ONE.value else 'A'
            if self.board.layout[new_row][new_col] != other_piece:
                valid_moves.append((new_row, new_col))
        
        print(f"Player {player_name}'s turn ({piece}). Your piece is at {piece_pos}")
        print(f"Valid moves: {valid_moves}")
        
        try:
            # Get row and column input from the player
            row = int(input(f"Enter row: "))
            col = int(input(f"Enter column: "))
            
            # Format the move string according to the game's API
            return f"{piece_pos[0]},{piece_pos[1]} {row},{col}"
        except ValueError:
            print("Please enter valid numbers.")
            # Return an obviously invalid move that will fail validation
            return "invalid move"

    def finish_message(self, winner):
        """Print a message at the end of the game."""
        player_name = "1" if winner == Player.ONE.value else "2"
        print(f"Game over! Player {player_name} wins!")

if __name__ == '__main__':
    # Create initial board layout
    # The board is 8x8 with pieces A and B at (3,3) and (4,4)
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

    # Create board and game
    board = Board((8, 8), initial_layout)
    game = Saffron(board)
    
    # Start the game
    game.game_loop()
