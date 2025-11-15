from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    PLAYER1 = 0  # Controls uppercase pieces (A-H)
    PLAYER2 = 1  # Controls lowercase pieces (a-h)

class Daisy(Game):
    def __init__(self, board):
        super().__init__(board)
        
        # Initialize piece reserves for both players
        self.reserves = {
            Player.PLAYER1.value: {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9},
            Player.PLAYER2.value: {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        }
        
        # Track if each player's "king" piece is on the board
        self.king_on_board = {
            Player.PLAYER1.value: False,
            Player.PLAYER2.value: False
        }
    
    def prompt_current_player(self):
        player_label = "Player 1 (uppercase)" if self.current_player == Player.PLAYER1.value else "Player 2 (lowercase)"
        reserve_str = self.get_reserve_string(self.current_player)
        
        print(f"\n{player_label}'s turn")
        print(f"Reserve: {reserve_str}")
        print("Enter a move in one of these formats:")
        print("  - Place a piece: 'X r,c' (e.g. 'H 3,4')")
        print("  - Move a piece: 'r1,c1 r2,c2' (e.g. '3,4 5,6')")
        
        return input("Your move: ")
        
    def get_reserve_string(self, player):
        result = []
        for piece, count in sorted(self.reserves[player].items()):
            if count > 0:
                result.append(f"{piece}:{count}")
        return " ".join(result)
        
    def validate_move(self, move):
        if not move:
            print("Please enter a valid move.")
            return False
            
        # First check basic validity from parent
        if not super().validate_move(move):
            print("Invalid coordinates.")
            return False
            
        if is_placement(move):
            # Validate placement move
            piece, position = get_move_elements(move)
            
            # Check if piece belongs to current player
            if self.current_player == Player.PLAYER1.value and not piece.isupper():
                print("Player 1 can only use uppercase pieces (A-H).")
                return False
            elif self.current_player == Player.PLAYER2.value and not piece.islower():
                print("Player 2 can only use lowercase pieces (a-h).")
                return False
                
            # Check if player has the piece in reserve
            if self.reserves[self.current_player].get(piece, 0) <= 0:
                print(f"You don't have any {piece} pieces in your reserve.")
                return False
                
            # Check if the target position is free
            row, col = position
            if self.board.layout[row][col] != '_':
                print("You can only place pieces on empty spaces.")
                return False
                
            return True
            
        elif is_movement(move):
            # Validate movement or capture move
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            # Check if there's a piece at origin
            if self.board.layout[origin_row][origin_col] == '_':
                print("There is no piece at the starting position.")
                return False
                
            piece = self.board.layout[origin_row][origin_col]
            
            # Check if the piece belongs to the current player
            if self.current_player == Player.PLAYER1.value and not piece.isupper():
                print("Player 1 can only move uppercase pieces (A-H).")
                return False
            elif self.current_player == Player.PLAYER2.value and not piece.islower():
                print("Player 2 can only move lowercase pieces (a-h).")
                return False
                
            # Check destination - empty space or opponent's piece
            dest_piece = self.board.layout[dest_row][dest_col]
            is_capture = dest_piece != '_'
            
            if is_capture:
                # Check if it's an opponent's piece
                if self.current_player == Player.PLAYER1.value and dest_piece.isupper():
                    print("You cannot capture your own pieces.")
                    return False
                elif self.current_player == Player.PLAYER2.value and dest_piece.islower():
                    print("You cannot capture your own pieces.")
                    return False
                    
                # Check if the king (A/a) is on the board before allowing capture
                if not self.king_on_board[self.current_player]:
                    print("You must place your king (A/a) on the board before making captures.")
                    return False
            
            # Validate move according to piece movement rules
            if not self.is_valid_piece_move(piece, origin, destination, is_capture):
                return False
                
            return True
        else:
            print("Invalid move format. Use 'X r,c' to place a piece or 'r1,c1 r2,c2' to move a piece.")
            return False
    
    def is_valid_piece_move(self, piece, origin, destination, is_capture):
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Calculate direction and distance
        row_diff = dest_row - origin_row
        col_diff = dest_col - origin_col
        
        # Determine forward direction based on piece case
        forward = -1 if piece.isupper() else 1  # Up for uppercase, down for lowercase
        
        piece_lower = piece.lower()  # Normalize piece type
        
        # Validate based on piece type
        if piece_lower == 'a':  # King - one space in any direction
            return abs(row_diff) <= 1 and abs(col_diff) <= 1
            
        elif piece_lower == 'b':  # Rook - any number of spaces orthogonally
            if row_diff != 0 and col_diff != 0:
                print("B/b can only move orthogonally (horizontally or vertically).")
                return False
                
            # Check if path is clear
            if row_diff == 0:  # Horizontal move
                step = 1 if col_diff > 0 else -1
                for c in range(origin_col + step, dest_col, step):
                    if self.board.layout[origin_row][c] != '_':
                        print("Path is not clear for movement.")
                        return False
            else:  # Vertical move
                step = 1 if row_diff > 0 else -1
                for r in range(origin_row + step, dest_row, step):
                    if self.board.layout[r][origin_col] != '_':
                        print("Path is not clear for movement.")
                        return False
            return True
            
        elif piece_lower == 'c':  # Bishop - any number of spaces diagonally
            if abs(row_diff) != abs(col_diff):
                print("C/c can only move diagonally.")
                return False
                
            # Check if path is clear
            row_step = 1 if row_diff > 0 else -1
            col_step = 1 if col_diff > 0 else -1
            r, c = origin_row + row_step, origin_col + col_step
            while r != dest_row and c != dest_col:
                if self.board.layout[r][c] != '_':
                    print("Path is not clear for movement.")
                    return False
                r += row_step
                c += col_step
            return True
            
        elif piece_lower == 'd':  # Moves one square in any direction except diagonally backwards
            if abs(row_diff) > 1 or abs(col_diff) > 1:
                print("D/d can only move one square.")
                return False
                
            # Check for diagonal backward movement (not allowed)
            if row_diff * forward > 0 and abs(col_diff) == 1:
                print("D/d cannot move diagonally backwards.")
                return False
            return True
                
        elif piece_lower == 'e':  # Moves one square diagonally or one square forward orthogonally
            if abs(row_diff) > 1 or abs(col_diff) > 1:
                print("E/e can only move one square.")
                return False
                
            # Check if it's a valid diagonal move or forward orthogonal
            is_diagonal = abs(row_diff) == 1 and abs(col_diff) == 1
            is_forward_orthogonal = row_diff == forward and col_diff == 0
            
            if not (is_diagonal or is_forward_orthogonal):
                print("E/e can only move diagonally or one square forward orthogonally.")
                return False
            return True
                
        elif piece_lower == 'f':  # Moves two spaces forward and then one space either left or right (like Knight)
            if not ((row_diff == 2 * forward and abs(col_diff) == 1)):
                print("F/f must move two spaces forward and then one space either left or right.")
                return False
            return True
                
        elif piece_lower == 'g':  # Moves any number of spaces only orthogonally forward
            if col_diff != 0 or row_diff * forward <= 0:
                print("G/g can only move forward orthogonally.")
                return False
                
            # Check if path is clear
            step = forward
            for r in range(origin_row + step, dest_row, step):
                if self.board.layout[r][origin_col] != '_':
                    print("Path is not clear for movement.")
                    return False
            return True
                
        elif piece_lower == 'h':  # Moves one space forward orthogonally
            if col_diff != 0 or row_diff != forward:
                print("H/h can only move one space forward orthogonally.")
                return False
            return True
            
        return False
    
    def perform_move(self, move):
        if is_placement(move):
            # Place a piece from reserve
            piece, position = get_move_elements(move)
            
            # Update reserve count
            self.reserves[self.current_player][piece] -= 1
            
            # Place the piece on the board
            self.board.place_piece(move)
            
            # Check if this is the king piece (A/a)
            if piece.lower() == 'a':
                self.king_on_board[self.current_player] = True
                
        elif is_movement(move):
            # Movement or capture
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            moving_piece = self.board.layout[origin_row][origin_col]
            target_space = self.board.layout[dest_row][dest_col]
            
            # Check if this is a capture
            if target_space != '_':
                # Convert the captured piece to the current player's equivalent
                captured_piece = target_space
                equivalent_piece = captured_piece.upper() if self.current_player == Player.PLAYER1.value else captured_piece.lower()
                
                # Add the captured piece to the current player's reserve
                self.reserves[self.current_player][equivalent_piece] += 1
            
            # Move the piece
            self.board.move_piece(move)
    
    def game_finished(self):
        # Check if either king has been captured
        player1_king_piece = 'A'
        player2_king_piece = 'a'
        
        # Search the board for both kings
        player1_king_found = False
        player2_king_found = False
        
        # Check if kings are on the board
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.layout[r][c] == player1_king_piece:
                    player1_king_found = True
                elif self.board.layout[r][c] == player2_king_piece:
                    player2_king_found = True
        
        # If kings were on board but now missing, check reserves
        if not player1_king_found and self.king_on_board[Player.PLAYER1.value]:
            if self.reserves[Player.PLAYER1.value].get('A', 0) == 0:
                return True  # Player 1's king was captured
        
        if not player2_king_found and self.king_on_board[Player.PLAYER2.value]:
            if self.reserves[Player.PLAYER2.value].get('a', 0) == 0:
                return True  # Player 2's king was captured
        
        return False
    
    def get_winner(self):
        # Check if either king has been captured
        player1_king_found = False
        player2_king_found = False
        
        # Check if kings are on the board
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.layout[r][c] == 'A':
                    player1_king_found = True
                elif self.board.layout[r][c] == 'a':
                    player2_king_found = True
        
        # If kings were on board but now missing, check reserves
        if not player1_king_found and self.king_on_board[Player.PLAYER1.value]:
            if self.reserves[Player.PLAYER1.value].get('A', 0) == 0:
                return Player.PLAYER2.value  # Player 2 wins by capturing Player 1's king
        
        if not player2_king_found and self.king_on_board[Player.PLAYER2.value]:
            if self.reserves[Player.PLAYER2.value].get('a', 0) == 0:
                return Player.PLAYER1.value  # Player 1 wins by capturing Player 2's king
        
        return None
    
    def next_player(self):
        # Simply alternates between players
        return (self.current_player + 1) % 2
    
    def get_state(self):
        base_state = super().get_state()
        additional_params = [
            deepcopy(self.reserves),
            deepcopy(self.king_on_board)
        ]
        return (base_state[0], base_state[1], additional_params)
    
    def finish_message(self, winner):
        if winner == Player.PLAYER1.value:
            print("Player 1 (uppercase) wins by capturing the opponent's king (a)!")
        else:
            print("Player 2 (lowercase) wins by capturing the opponent's king (A)!")

if __name__ == '__main__':
    board = Board((9, 9))
    game = Daisy(board)
    game.game_loop()
