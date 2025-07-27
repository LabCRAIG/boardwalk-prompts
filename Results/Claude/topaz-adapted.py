from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import IntEnum

class Player(IntEnum):
    ONE = 1
    TWO = 2

class TopazGame(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        # The Game class already initializes round = 1 and calls initial_player()
        # Player 1 has A's, Player 2 has B's
        self.player_pieces = {Player.ONE: 'A', Player.TWO: 'B'}
        # Each player starts with 9 pieces
        self.pieces_left = {Player.ONE: 9, Player.TWO: 9}
        # Track pieces on board
        self.pieces_on_board = {Player.ONE: 0, Player.TWO: 0}
        # Phase 1: Placement, Phase 2: Movement
        self.phase = 1
        # Capture flag
        self.pending_capture = False
        
    def initial_player(self) -> int:
        # Player 1 starts
        return Player.ONE
    
    def prompt_current_player(self) -> str:
        """Custom prompt based on game phase and player."""
        player_symbol = self.player_pieces[self.current_player]
        
        if self.pending_capture:
            print(f"Player {self.current_player} ({player_symbol}) can capture an opponent's piece!")
            row = input("Enter row of piece to capture: ")
            col = input("Enter column of piece to capture: ")
            # Format as placement move with a special "X" marker for capture
            return f"X {row},{col}"
        
        if self.phase == 1:
            print(f"Phase: Placement (Player {self.current_player} ({player_symbol}) has {self.pieces_left[self.current_player]} pieces left)")
            row = input("Enter row to place piece: ")
            col = input("Enter column to place piece: ")
            # Format as placement move with player's piece
            return f"{player_symbol} {row},{col}"
        else:  # Phase 2
            print(f"Phase: Movement (Player {self.current_player} ({player_symbol}))")
            from_row = input("Enter row of piece to move: ")
            from_col = input("Enter column of piece to move: ")
            to_row = input("Enter row to move to: ")
            to_col = input("Enter column to move to: ")
            # Format as movement move
            return f"{from_row},{from_col} {to_row},{to_col}"

    def validate_move(self, move: str) -> bool:
        """Verify if the move is valid according to game rules."""
        if not super().validate_move(move):
            print("Invalid coordinates.")
            return False
        
        # Handle capture move
        if move.startswith("X "):
            return self.validate_capture(move)
        
        # Phase 1: Placement validation
        if self.phase == 1:
            if not is_placement(move):
                print("You must place a piece in phase 1.")
                return False
                
            piece, (row, col) = get_move_elements(move)
            
            # Check if the piece belongs to the current player
            if piece != self.player_pieces[self.current_player]:
                print(f"You can only place {self.player_pieces[self.current_player]} pieces.")
                return False
                
            # Check if the position is blank
            if self.board.layout[row][col] != '_':
                print("You can only place a piece on a blank space.")
                return False
                
            # Check if player has pieces left to place
            if self.pieces_left[self.current_player] <= 0:
                print("You have no pieces left to place.")
                return False
                
            return True
            
        # Phase 2: Movement validation
        elif self.phase == 2:
            if not is_movement(move):
                print("You must move a piece in phase 2.")
                return False
                
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            
            # Check if the piece belongs to the current player
            if self.board.layout[from_row][from_col] != self.player_pieces[self.current_player]:
                print("You can only move your own pieces.")
                return False
                
            # Check if destination is blank
            if self.board.layout[to_row][to_col] != '_':
                print("You can only move to a blank space.")
                return False
                
            # Check if move is to an adjacent space (same row or column)
            if not self.are_adjacent(from_row, from_col, to_row, to_col):
                print("You can only move to an adjacent space in the same row or column.")
                return False
                
            return True
            
        return False

    def validate_capture(self, move: str) -> bool:
        """Validate a capture move."""
        if not self.pending_capture:
            print("No capture is pending.")
            return False
            
        # Extract capture position
        _, (row, col) = get_move_elements(move[2:])  # Remove "X " prefix
        
        # Get opponent's piece symbol
        opponent = Player.ONE if self.current_player == Player.TWO else Player.TWO
        opponent_piece = self.player_pieces[opponent]
        
        # Check if the position contains an opponent's piece
        if self.board.layout[row][col] != opponent_piece:
            print("You can only capture your opponent's pieces.")
            return False
            
        return True

    def are_adjacent(self, from_row, from_col, to_row, to_col) -> bool:
        """Check if two positions are adjacent (closest blank spaces in same row/column)."""
        # Must be in same row or column
        if from_row != to_row and from_col != to_col:
            return False
            
        # Check if they are the closest blank spaces
        if from_row == to_row:  # Same row
            start, end = min(from_col, to_col), max(from_col, to_col)
            for col in range(start + 1, end):
                # Skip null spaces
                if self.board.layout[from_row][col] == ' ':
                    continue
                # If there's a blank space between, not adjacent
                if self.board.layout[from_row][col] == '_':
                    return False
            return True
        else:  # Same column
            start, end = min(from_row, to_row), max(from_row, to_row)
            for row in range(start + 1, end):
                # Skip null spaces
                if self.board.layout[row][from_col] == ' ':
                    continue
                # If there's a blank space between, not adjacent
                if self.board.layout[row][from_col] == '_':
                    return False
            return True

    def perform_move(self, move: str):
        """Update the board and game state according to the move."""
        # Handle capture move
        if move.startswith("X "):
            _, (row, col) = get_move_elements(move[2:])  # Remove "X " prefix
            self.board.layout[row][col] = '_'
            
            # Update piece count for captured player
            opponent = Player.ONE if self.current_player == Player.TWO else Player.TWO
            self.pieces_on_board[opponent] -= 1
            
            # Reset capture flag
            self.pending_capture = False
            return
        
        # Handle placement move
        if self.phase == 1:
            # Call the parent method to place the piece
            super().perform_move(move)
            
            piece, (row, col) = get_move_elements(move)
            self.pieces_left[self.current_player] -= 1
            self.pieces_on_board[self.current_player] += 1
            
            # Check for capture condition
            if self.check_capture(row, col):
                self.pending_capture = True
            
            # Check for phase transition
            if self.pieces_left[Player.ONE] == 0 and self.pieces_left[Player.TWO] == 0:
                self.phase = 2
                print("All pieces placed. Moving to movement phase!")
        
        # Handle movement move
        elif self.phase == 2:
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            
            # Call the parent method to move the piece
            super().perform_move(move)
            
            # Check for capture condition at new position
            if self.check_capture(to_row, to_col):
                self.pending_capture = True
    
    def check_capture(self, row, col) -> bool:
        """Check if placing/moving a piece creates a capture condition."""
        piece = self.player_pieces[self.current_player]
        
        # Check horizontal (row)
        count = 0
        for c in range(len(self.board.layout[0])):
            if self.board.layout[row][c] == piece:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
        
        # Check vertical (column)
        count = 0
        for r in range(len(self.board.layout)):
            if self.board.layout[r][col] == piece:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
        
        return False
    
    def can_player_move(self, player) -> bool:
        """Check if a player can move any of their pieces."""
        player_piece = self.player_pieces[player]
        
        for r in range(len(self.board.layout)):
            for c in range(len(self.board.layout[0])):
                # If this is the player's piece
                if self.board.layout[r][c] == player_piece:
                    # Check all four directions
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
                    
                    for dr, dc in directions:
                        row, col = r, c
                        while True:
                            row += dr
                            col += dc
                            
                            # Check if out of bounds
                            if not (0 <= row < len(self.board.layout) and 0 <= col < len(self.board.layout[0])):
                                break
                                
                            # Skip null spaces
                            if self.board.layout[row][col] == ' ':
                                continue
                                
                            # If found a blank space, player can move
                            if self.board.layout[row][col] == '_':
                                return True
                                
                            # Hit another piece, stop searching in this direction
                            break
        
        return False
    
    def next_player(self) -> int:
        """Determine the next player to move."""
        # If there's a pending capture, don't change player
        if self.pending_capture:
            return self.current_player
            
        # Otherwise, alternate between players
        return Player.TWO if self.current_player == Player.ONE else Player.ONE
    
    def game_finished(self) -> bool:
        """Check if the game has ended."""
        # Only check in phase 2
        if self.phase != 2:
            return False
            
        # Check if either player has only 2 or fewer pieces
        if self.pieces_on_board[Player.ONE] <= 2 or self.pieces_on_board[Player.TWO] <= 2:
            return True
            
        # Check if current player can't move any pieces
        if not self.can_player_move(self.current_player):
            return True
            
        return False
    
    def get_winner(self) -> int:
        """Determine the winner of the game."""
        # If a player has 2 or fewer pieces, they lose
        if self.pieces_on_board[Player.ONE] <= 2:
            return Player.TWO
        if self.pieces_on_board[Player.TWO] <= 2:
            return Player.ONE
            
        # If a player can't move, they lose
        if not self.can_player_move(self.current_player):
            return Player.TWO if self.current_player == Player.ONE else Player.ONE
            
        # If no winner yet
        return None
    
    def get_state(self) -> tuple:
        """Return the current game state."""
        state = super().get_state()
        # Add additional game state variables
        state[2].extend([
            self.phase,
            self.pieces_left[Player.ONE],
            self.pieces_left[Player.TWO],
            self.pieces_on_board[Player.ONE],
            self.pieces_on_board[Player.TWO],
            self.pending_capture
        ])
        return state
    
    def finish_message(self, winner):
        """Display a custom end-of-game message."""
        print(f"Game over! Player {winner} ({self.player_pieces[winner]}) wins!")
        
        if self.pieces_on_board[Player.ONE if winner == Player.TWO else Player.ONE] <= 2:
            print(f"Player {Player.ONE if winner == Player.TWO else Player.ONE} has only 2 or fewer pieces left.")
        else:
            print(f"Player {Player.ONE if winner == Player.TWO else Player.ONE} cannot move any pieces.")

if __name__ == '__main__':
    # Create the 7x7 board with the checkerboard pattern of null spaces
    layout = """\
 __ __ 
__ _ __
 __ __ 
__ _ __
 __ __ 
__ _ __
 __ __ 
"""
    board = Board((7, 7), layout)
    
    # Create the game and start it
    topaz_game = TopazGame(board)
    topaz_game.game_loop()