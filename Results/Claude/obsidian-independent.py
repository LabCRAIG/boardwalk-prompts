import os
import time

class Piece:
    def __init__(self, symbol, player):
        self.symbol = symbol
        self.player = player  # 1 or 2
        self.has_moved = False
    
    def __str__(self):
        return self.symbol
    
    def is_valid_move(self, board, start_pos, end_pos):
        # Common validation for all pieces
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Cannot move to a position occupied by own piece
        if board[end_row][end_col] is not None and board[end_row][end_col].player == self.player:
            return False
            
        # Implement specific piece movement validation in subclasses
        return True
        
    def move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Update the has_moved flag
        self.has_moved = True
        
        # Check for pawn promotion
        if self.symbol == 'f' and end_row == 0:
            board[end_row][end_col] = EPiece(self.player)
        elif self.symbol == 'F' and end_row == 7:
            board[end_row][end_col] = EPiece(self.player)
        else:
            board[end_row][end_col] = self
            
        board[start_row][start_col] = None
        return True

class FPiece(Piece):
    def __init__(self, player):
        super().__init__('F' if player == 2 else 'f', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Direction depends on player
        direction = 1 if self.player == 2 else -1
        
        # Normal forward move
        if start_col == end_col and end_row == start_row + direction:
            # Can only move forward to an empty space
            return board[end_row][end_col] is None
        
        # Double move for first move
        if not self.has_moved and start_col == end_col and end_row == start_row + 2 * direction:
            # Ensure path is clear
            middle_row = start_row + direction
            return (board[middle_row][start_col] is None and 
                    board[end_row][end_col] is None)
        
        # Diagonal capture
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            # Can only move diagonally if capturing
            return (board[end_row][end_col] is not None and 
                    board[end_row][end_col].player != self.player)
                    
        return False

class APiece(Piece):
    def __init__(self, player):
        super().__init__('A' if player == 2 else 'a', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Must move orthogonally
        if start_row != end_row and start_col != end_col:
            return False
            
        # Check if path is clear
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
        else:  # Vertical move
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False
                    
        return True

class CPiece(Piece):
    def __init__(self, player):
        super().__init__('C' if player == 2 else 'c', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Must move diagonally
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
            
        # Check if path is clear
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        
        row, col = start_row + row_step, start_col + col_step
        while (row, col) != (end_row, end_col):
            if board[row][col] is not None:
                return False
            row += row_step
            col += col_step
            
        return True

class BPiece(Piece):
    def __init__(self, player):
        super().__init__('B' if player == 2 else 'b', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Knight-like move (L shape)
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class EPiece(Piece):
    def __init__(self, player):
        super().__init__('E' if player == 2 else 'e', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Can move diagonally or orthogonally
        is_diagonal = abs(start_row - end_row) == abs(start_col - end_col)
        is_orthogonal = start_row == end_row or start_col == end_col
        
        if not (is_diagonal or is_orthogonal):
            return False
            
        # Check if path is clear
        if is_diagonal:
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            
            row, col = start_row + row_step, start_col + col_step
            while (row, col) != (end_row, end_col):
                if board[row][col] is not None:
                    return False
                row += row_step
                col += col_step
        else:  # Orthogonal
            if start_row == end_row:  # Horizontal move
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] is not None:
                        return False
            else:  # Vertical move
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] is not None:
                        return False
                    
        return True

class DPiece(Piece):
    def __init__(self, player):
        super().__init__('D' if player == 2 else 'd', player)
    
    def is_valid_move(self, board, start_pos, end_pos):
        if not super().is_valid_move(board, start_pos, end_pos):
            return False
            
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Can move one space in any direction
        return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 1
        self.winner = None
        self.initialize_board()
        
    def initialize_board(self):
        # Initialize Player 2's pieces (top two rows)
        self.board[0] = [
            APiece(2), BPiece(2), CPiece(2), DPiece(2),
            EPiece(2), CPiece(2), BPiece(2), APiece(2)
        ]
        self.board[1] = [FPiece(2) for _ in range(8)]
        
        # Initialize Player 1's pieces (bottom two rows)
        self.board[6] = [FPiece(1) for _ in range(8)]
        self.board[7] = [
            APiece(1), BPiece(1), CPiece(1), DPiece(1),
            EPiece(1), CPiece(1), BPiece(1), APiece(1)
        ]
    
    def display_board(self):
        clear_screen()
        print("  a b c d e f g h")
        print(" ┌─────────────┐")
        for i in range(8):
            print(f"{8-i}│", end="")
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    print(f"{piece.symbol} ", end="")
                else:
                    # Checkerboard pattern for empty squares
                    print("▒ " if (i + j) % 2 else "· ", end="")
            print(f"│{8-i}")
        print(" └─────────────┘")
        print("  a b c d e f g h")
        print(f"\nCurrent player: {'◯' if self.current_player == 1 else '●'} (Player {self.current_player})")
    
    def is_valid_position(self, pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece(self, pos):
        row, col = pos
        if not self.is_valid_position((row, col)):
            return None
        return self.board[row][col]
    
    def make_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        piece = self.board[start_row][start_col]
        
        # Check if it's a valid piece for the current player
        if piece is None or piece.player != self.current_player:
            return False
        
        # Check if the move is valid for this piece
        if not piece.is_valid_move(self.board, start_pos, end_pos):
            return False
            
        # Check if capturing king, which would end the game
        end_piece = self.board[end_row][end_col]
        if end_piece and end_piece.symbol in ('D', 'd'):
            self.winner = self.current_player
        
        # Move the piece
        piece.move(self.board, start_pos, end_pos)
        
        # Switch players
        self.current_player = 3 - self.current_player  # Toggles between 1 and 2
        
        return True
    
    def is_game_over(self):
        return self.winner is not None

    def get_winner(self):
        return self.winner

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_position(pos_str):
    """Convert chess notation (e.g., 'e4') to board coordinates (row, col)."""
    if len(pos_str) != 2:
        return None
    
    col = ord(pos_str[0].lower()) - ord('a')
    row = 8 - int(pos_str[1])
    
    if not (0 <= row < 8 and 0 <= col < 8):
        return None
        
    return row, col

def main():
    game = Game()
    
    while not game.is_game_over():
        game.display_board()
        
        player_name = "◯ (lowercase)" if game.current_player == 1 else "● (uppercase)"
        print(f"\nPlayer {game.current_player} {player_name}'s turn")
        
        try:
            start_pos_str = input("Enter the position of the piece to move (e.g., e2): ")
            if start_pos_str.lower() == 'quit':
                break
                
            start_pos = parse_position(start_pos_str)
            if start_pos is None:
                print("Invalid position format. Use letter (a-h) followed by number (1-8).")
                time.sleep(1.5)
                continue
                
            piece = game.get_piece(start_pos)
            if piece is None:
                print("No piece at that position.")
                time.sleep(1.5)
                continue
                
            if piece.player != game.current_player:
                print("That's not your piece.")
                time.sleep(1.5)
                continue
                
            end_pos_str = input("Enter the destination position (e.g., e4): ")
            if end_pos_str.lower() == 'quit':
                break
                
            end_pos = parse_position(end_pos_str)
            if end_pos is None:
                print("Invalid position format. Use letter (a-h) followed by number (1-8).")
                time.sleep(1.5)
                continue
                
            if not game.make_move(start_pos, end_pos):
                print("Invalid move. Try again.")
                time.sleep(1.5)
                
        except ValueError:
            print("Invalid input. Try again.")
            time.sleep(1.5)
            
    if game.get_winner():
        game.display_board()
        winner_name = "◯ (lowercase)" if game.winner == 1 else "● (uppercase)"
        print(f"\nGame Over! Player {game.winner} {winner_name} wins!")
    else:
        print("\nGame ended.")

if __name__ == "__main__":
    main()