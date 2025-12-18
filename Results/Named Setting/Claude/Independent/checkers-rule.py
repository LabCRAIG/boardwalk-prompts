
import numpy as np

class CheckersGame:
    # Board representation:
    # 0 = empty
    # 1 = player 1 regular piece
    # 2 = player 2 regular piece
    # 3 = player 1 king
    # 4 = player 2 king

    def __init__(self):
        self.reset_board()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def reset_board(self):
        # Create an 8x8 board
        self.board = np.zeros((8, 8), dtype=int)
        
        # Set up initial positions
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row, col] = 2  # Player 2 pieces
                    
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row, col] = 1  # Player 1 pieces
    
    def print_board(self):
        symbols = {0: '·', 1: '○', 2: '●', 3: '♔', 4: '♚'}
        print("  0 1 2 3 4 5 6 7")
        for row in range(8):
            print(f"{row}", end=" ")
            for col in range(8):
                print(symbols[self.board[row, col]], end=" ")
            print()
        print()
    
    def get_valid_moves(self, player):
        moves = {}
        capture_moves = {}
        has_captures = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row, col]
                
                # Check if the piece belongs to the current player
                if (piece == player) or (piece == player + 2):  # Regular piece or king
                    piece_moves = self._get_piece_moves(row, col)
                    if piece_moves:
                        moves[(row, col)] = piece_moves
                    
                    # Check for captures
                    piece_captures = self._get_piece_captures(row, col)
                    if piece_captures:
                        has_captures = True
                        capture_moves[(row, col)] = piece_captures
        
        # If captures are available, they are mandatory
        return capture_moves if has_captures else moves
    
    def _get_piece_moves(self, row, col):
        piece = self.board[row, col]
        moves = []
        
        # Determine direction based on player
        if piece == 1:  # Player 1 regular piece (moves up)
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:  # Player 2 regular piece (moves down)
            directions = [(1, -1), (1, 1)]
        elif piece in [3, 4]:  # Kings (can move in all diagonal directions)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            return moves
        
        # Check each direction
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row, new_col] == 0:
                moves.append((new_row, new_col))
        
        return moves
    
    def _get_piece_captures(self, row, col):
        piece = self.board[row, col]
        captures = []
        
        if piece == 0:  # Empty square
            return captures
        
        player = 1 if piece in [1, 3] else 2
        opponent = 3 - player  # Opposite player
        
        # Determine directions based on piece type
        if piece == 1:  # Player 1 regular piece
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:  # Player 2 regular piece
            directions = [(1, -1), (1, 1)]
        elif piece in [3, 4]:  # Kings
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Check for captures in each direction
        for dr, dc in directions:
            capture_row, capture_col = row + dr, col + dc
            land_row, land_col = row + 2*dr, col + 2*dc
            
            if (0 <= capture_row < 8 and 0 <= capture_col < 8 and
                0 <= land_row < 8 and 0 <= land_col < 8):
                
                capture_piece = self.board[capture_row, capture_col]
                # Check if there's an opponent's piece to capture and empty space to land
                if ((capture_piece == opponent or capture_piece == opponent + 2) and 
                     self.board[land_row, land_col] == 0):
                    captures.append((land_row, land_col, capture_row, capture_col))
        
        return captures
    
    def make_move(self, from_pos, to_pos):
        row, col = from_pos
        new_row, new_col = to_pos
        
        piece = self.board[row, col]
        self.board[row, col] = 0
        
        # Check if this is a capture move
        if abs(row - new_row) == 2 and abs(col - new_col) == 2:
            capture_row = (row + new_row) // 2
            capture_col = (col + new_col) // 2
            captured_piece = self.board[capture_row, capture_col]
            
            # Special rule: if a king captures another king, both are removed
            if (piece in [3, 4]) and (captured_piece in [3, 4]):
                self.board[capture_row, capture_col] = 0
                # King is not placed on the new position (both are removed)
            else:
                self.board[capture_row, capture_col] = 0
                self.board[new_row, new_col] = piece
                
                # Check for promotion
                if (piece == 1 and new_row == 0) or (piece == 2 and new_row == 7):
                    self.board[new_row, new_col] = piece + 2  # Promote to king
                
                # Check if there are additional captures
                additional_captures = self._get_piece_captures(new_row, new_col)
                if additional_captures:
                    return False  # Game is not over, player must make additional captures
        else:
            self.board[new_row, new_col] = piece
            
            # Check for promotion
            if (piece == 1 and new_row == 0) or (piece == 2 and new_row == 7):
                self.board[new_row, new_col] = piece + 2  # Promote to king
        
        # Switch to the other player
        self.current_player = 3 - self.current_player
        
        # Check if the game is over
        self._check_game_over()
        
        return self.game_over
    
    def _check_game_over(self):
        # Check if any player has no pieces left or no valid moves
        player1_pieces = np.isin(self.board, [1, 3]).any()
        player2_pieces = np.isin(self.board, [2, 4]).any()
        
        if not player1_pieces:
            self.game_over = True
            self.winner = 2
        elif not player2_pieces:
            self.game_over = True
            self.winner = 1
        elif not self.get_valid_moves(self.current_player):
            self.game_over = True
            self.winner = 3 - self.current_player
    
    def play_game(self):
        """Play an interactive game in the console."""
        print("Welcome to Checkers!")
        print("Player 1: ○/♔, Player 2: ●/♚")
        print("Special rule: When a king captures another king, both are removed.")
        
        while not self.game_over:
            print(f"\nPlayer {self.current_player}'s turn")
            self.print_board()
            
            valid_moves = self.get_valid_moves(self.current_player)
            if not valid_moves:
                print(f"Player {self.current_player} has no valid moves!")
                self.winner = 3 - self.current_player
                self.game_over = True
                break
            
            print("Valid moves:")
            for piece, moves in valid_moves.items():
                print(f"Piece at {piece}: {moves}")
            
            try:
                piece_input = input("Select piece (row,col): ")
                from_row, from_col = map(int, piece_input.split(','))
                from_pos = (from_row, from_col)
                
                if from_pos not in valid_moves:
                    print("Invalid piece selection. Try again.")
                    continue
                
                move_input = input("Select destination (row,col): ")
                to_row, to_col = map(int, move_input.split(','))
                to_pos = (to_row, to_col)
                
                # Check if this is a capture move
                is_capture = False
                for move in valid_moves[from_pos]:
                    if isinstance(move, tuple) and len(move) == 4:
                        if (move[0], move[1]) == to_pos:
                            is_capture = True
                            self.make_move(from_pos, to_pos)
                            break
                    elif move == to_pos:
                        self.make_move(from_pos, to_pos)
                        break
                else:
                    print("Invalid move. Try again.")
                    continue
                
            except (ValueError, IndexError):
                print("Invalid input. Use format 'row,col'")
                continue
        
        print("\nGame Over!")
        self.print_board()
        if self.winner:
            print(f"Player {self.winner} wins!")
        else:
            print("The game is a draw!")


# Example usage
if __name__ == "__main__":
    game = CheckersGame()
    game.play_game()
