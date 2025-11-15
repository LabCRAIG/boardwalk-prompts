from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy
from enum import IntEnum

class Player(IntEnum):
    PLAYER1 = 0
    PLAYER2 = 1

class DaisyGame(Game):
    def __init__(self, board):
        super().__init__(board)
        # Initialize player reserves
        self.p1_reserve = {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9}
        self.p2_reserve = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        
        # Track if kings are on board
        self.p1_king_placed = False
        self.p2_king_placed = False

    def initial_player(self):
        return Player.PLAYER1

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        # Check if it's a valid placement or movement
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            
            # Check if the piece belongs to the current player
            if self.current_player == Player.PLAYER1 and not piece.isupper():
                return False
            if self.current_player == Player.PLAYER2 and not piece.islower():
                return False
            
            # Check if the piece is available in the player's reserve
            if self.current_player == Player.PLAYER1:
                if piece not in self.p1_reserve or self.p1_reserve[piece] <= 0:
                    return False
            else:
                if piece not in self.p2_reserve or self.p2_reserve[piece] <= 0:
                    return False
            
            # Check if the position is empty
            if self.board.layout[row, col] != '_':
                return False
                
            return True
            
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            
            # Check if the origin position has a piece
            if self.board.layout[from_row, from_col] == '_':
                return False
                
            # Check if the piece belongs to the current player
            piece = self.board.layout[from_row, from_col]
            if self.current_player == Player.PLAYER1 and not piece.isupper():
                return False
            if self.current_player == Player.PLAYER2 and not piece.islower():
                return False
                
            # Check if the destination is valid
            valid_moves = self.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                return False
                
            # Check if this is a capture and if so, whether the player can capture
            target = self.board.layout[to_row, to_col]
            if target != '_':  # This is a capture
                if (self.current_player == Player.PLAYER1 and not self.p1_king_placed) or \
                   (self.current_player == Player.PLAYER2 and not self.p2_king_placed):
                    return False
                    
            return True
            
        return False

    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            
            # Update the board
            super().perform_move(move)
            
            # Update reserves and tracking
            if self.current_player == Player.PLAYER1:
                self.p1_reserve[piece] -= 1
                if piece == 'A':
                    self.p1_king_placed = True
            else:
                self.p2_reserve[piece] -= 1
                if piece == 'a':
                    self.p2_king_placed = True
                
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            piece = self.board.layout[from_row, from_col]
            target = self.board.layout[to_row, to_col]
            
            # Handle capture
            if target != '_':
                if target == 'a' and self.current_player == Player.PLAYER1:
                    self.winner = Player.PLAYER1
                elif target == 'A' and self.current_player == Player.PLAYER2:
                    self.winner = Player.PLAYER2
                
                # Add captured piece to reserve (converting to the appropriate type)
                equivalent_piece = target.upper() if self.current_player == Player.PLAYER1 else target.lower()
                if self.current_player == Player.PLAYER1:
                    self.p1_reserve[equivalent_piece] += 1
                else:
                    self.p2_reserve[equivalent_piece] += 1
            
            # Update the board
            super().perform_move(move)

    def prompt_current_player(self):
        # Print current player info and reserves
        player_name = "Player 1" if self.current_player == Player.PLAYER1 else "Player 2"
        piece_set = "uppercase (A-H)" if self.current_player == Player.PLAYER1 else "lowercase (a-h)"
        print(f"\n{player_name}'s turn (controlling {piece_set} pieces)")
        
        # Show reserves
        if self.current_player == Player.PLAYER1:
            print("\nPlayer 1 Reserve:")
            for piece, count in self.p1_reserve.items():
                if count > 0:
                    print(f"{piece}: {count}", end="  ")
        else:
            print("\nPlayer 2 Reserve:")
            for piece, count in self.p2_reserve.items():
                if count > 0:
                    print(f"{piece}: {count}", end="  ")
        print("\n")
        
        # Player selects action
        print("Select action:")
        print("1. Place a piece from reserve")
        print("2. Move a piece on the board")
        
        action = input("Enter choice (1 or 2): ").strip()
        
        if action == '1':  # Place a piece
            # Show available pieces
            available = self.p1_reserve if self.current_player == Player.PLAYER1 else self.p2_reserve
            print("Available pieces in reserve:")
            for piece, count in available.items():
                if count > 0:
                    print(f"{piece}: {count}", end="  ")
            print()
            
            # Get piece and position
            piece = input("Enter piece to place: ").strip()
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                return f"{piece} {row},{col}"
            except ValueError:
                print("Invalid input. Row and column must be numbers.")
                return self.prompt_current_player()
                
        elif action == '2':  # Move a piece
            try:
                from_row = int(input("Enter row of piece to move: "))
                from_col = int(input("Enter column of piece to move: "))
                
                # Validate selection
                if not (0 <= from_row < self.board.height and 0 <= from_col < self.board.width):
                    print("Position out of bounds.")
                    return self.prompt_current_player()
                
                piece = self.board.layout[from_row, from_col]
                if piece == '_':
                    print("No piece at that position.")
                    return self.prompt_current_player()
                
                if (self.current_player == Player.PLAYER1 and piece.islower()) or \
                   (self.current_player == Player.PLAYER2 and piece.isupper()):
                    print("That's not your piece.")
                    return self.prompt_current_player()
                
                # Show valid moves
                valid_moves = self.get_valid_moves(from_row, from_col)
                if not valid_moves:
                    print("No valid moves for this piece.")
                    return self.prompt_current_player()
                
                print("Valid moves:")
                for i, (r, c) in enumerate(valid_moves):
                    target = "_" if self.board.layout[r, c] == '_' else self.board.layout[r, c]
                    print(f"{i+1}: ({r}, {c}) {target}")
                
                # Select move
                move_idx = int(input("Select move number: ")) - 1
                if 0 <= move_idx < len(valid_moves):
                    to_row, to_col = valid_moves[move_idx]
                    return f"{from_row},{from_col} {to_row},{to_col}"
                else:
                    print("Invalid move selection.")
                    return self.prompt_current_player()
                
            except ValueError:
                print("Invalid input. Please enter numbers.")
                return self.prompt_current_player()
        
        else:
            print("Invalid action. Please enter 1 or 2.")
            return self.prompt_current_player()

    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        piece = self.board.layout[row, col]
        
        # Check if position is valid and contains a piece
        if not (0 <= row < self.board.height and 0 <= col < self.board.width) or piece == '_':
            return []
        
        # Check if piece belongs to current player
        if (self.current_player == Player.PLAYER1 and piece.islower()) or \
           (self.current_player == Player.PLAYER2 and piece.isupper()):
            return []
        
        valid_moves = []
        # Determine piece type (normalize to uppercase for comparison)
        piece_type = piece.upper()
        
        # For player 1 (uppercase), forward is up (-1 in row)
        # For player 2 (lowercase), forward is down (+1 in row)
        forward_dir = -1 if piece.isupper() else 1
        
        # Handle movement based on piece type
        if piece_type == 'A':  # A, a: moves one space in any direction
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.board.height and 0 <= c < self.board.width:
                    # Can move to empty space or capture
                    target = self.board.layout[r, c]
                    if target == '_' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'B':  # B, b: moves any number of spaces orthogonally
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if not (0 <= r < self.board.height and 0 <= c < self.board.width):
                        break
                    target = self.board.layout[r, c]
                    if target == '_':
                        valid_moves.append((r, c))
                    elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'C':  # C, c: moves any number of spaces diagonally
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if not (0 <= r < self.board.height and 0 <= c < self.board.width):
                        break
                    target = self.board.layout[r, c]
                    if target == '_':
                        valid_moves.append((r, c))
                    elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'D':  # D, d: moves one square in any direction except diagonally backwards
            # All directions except diagonally backward
            directions = [
                (forward_dir, 0),  # Forward
                (0, 1), (0, -1),    # Left and right
                (forward_dir, 1), (forward_dir, -1)  # Diagonally forward
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.board.height and 0 <= c < self.board.width:
                    target = self.board.layout[r, c]
                    if target == '_' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'E':  # E, e: moves one square diagonally or one square forward orthogonally
            # Diagonally in any direction or forward orthogonally
            directions = [
                (forward_dir, 0),  # Forward
                (1, 1), (1, -1), (-1, 1), (-1, -1)  # All diagonals
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.board.height and 0 <= c < self.board.width:
                    target = self.board.layout[r, c]
                    if target == '_' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'F':  # F, f: moves two spaces forward and then one space either left or right
            # Forward two then left or right one (like knight but only forward)
            r = row + (2 * forward_dir)
            if 0 <= r < self.board.height:
                for c in [col - 1, col + 1]:
                    if 0 <= c < self.board.width:
                        target = self.board.layout[r, c]
                        if target == '_' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                            valid_moves.append((r, c))
        
        elif piece_type == 'G':  # G, g: moves any number of spaces only orthogonally forward
            # Any number of spaces forward
            r, c = row, col
            while True:
                r += forward_dir
                if not (0 <= r < self.board.height):
                    break
                target = self.board.layout[r, c]
                if target == '_':
                    valid_moves.append((r, c))
                elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    valid_moves.append((r, c))
                    break
                else:
                    break
        
        elif piece_type == 'H':  # H, h: moves one space forward orthogonally
            # One space forward
            r = row + forward_dir
            c = col
            if 0 <= r < self.board.height:
                target = self.board.layout[r, c]
                if target == '_' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    valid_moves.append((r, c))
        
        return valid_moves

    def game_finished(self):
        # Check if someone has won (this is set in perform_move when a king is captured)
        if hasattr(self, 'winner'):
            return True
        return False

    def get_winner(self):
        # Return the winner (if game is finished)
        if hasattr(self, 'winner'):
            return self.winner
        return None

    def next_player(self):
        # Switch player (1->2, 2->1)
        return Player.PLAYER2 if self.current_player == Player.PLAYER1 else Player.PLAYER1

    def finish_message(self, winner):
        player_name = "Player 1" if winner == Player.PLAYER1 else "Player 2"
        print(f"{player_name} wins!")

    def get_state(self):
        # Add game-specific state information to the tuple
        base_state = super().get_state()
        additional_params = base_state[2] + [
            self.p1_reserve, 
            self.p2_reserve,
            self.p1_king_placed,
            self.p2_king_placed
        ]
        return (base_state[0], base_state[1], additional_params)


if __name__ == '__main__':
    # Create a 9x9 board with all blank spaces
    board = Board((9, 9))
    
    # Create and run the Daisy game
    game = DaisyGame(board)
    
    # Print welcome message
    print("Welcome to Daisy!")
    print("Player 1 controls uppercase pieces (A-H)")
    print("Player 2 controls lowercase pieces (a-h)")
    print("Win by capturing your opponent's king (A or a)")
    
    # Start the game
    game.game_loop()
