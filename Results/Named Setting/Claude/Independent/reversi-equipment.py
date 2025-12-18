
import numpy as np

class Reversi:
    def __init__(self):
        # 8x8 board: 0 = empty, 1 = black, 2 = white
        self.board = np.zeros((8, 8), dtype=int)
        
        # Initial setup (center 4 pieces)
        self.board[3, 3] = 2
        self.board[3, 4] = 1
        self.board[4, 3] = 1
        self.board[4, 4] = 2
        
        # Black plays first
        self.current_player = 1
        
        # Define restricted corner squares
        self.restricted_squares = [
            (0, 0), (0, 1), (1, 0), (1, 1),           # Top-left corner
            (0, 6), (0, 7), (1, 6), (1, 7),           # Top-right corner
            (6, 0), (6, 1), (7, 0), (7, 1),           # Bottom-left corner
            (6, 6), (6, 7), (7, 6), (7, 7)            # Bottom-right corner
        ]
    
    def print_board(self):
        """Print the current board state"""
        symbols = {0: "·", 1: "●", 2: "○"}
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row_str = f"{i} "
            for j in range(8):
                row_str += symbols[self.board[i, j]] + " "
            print(row_str)
        print()
        print(f"Black (●): {np.sum(self.board == 1)}")
        print(f"White (○): {np.sum(self.board == 2)}")
    
    def get_opponent(self, player):
        """Return the opponent of the given player"""
        return 3 - player  # 1 -> 2, 2 -> 1
    
    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        # Check if the position is in bounds
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        
        # Check if position is in restricted corner squares
        if (row, col) in self.restricted_squares:
            return False
        
        # Check if the position is already occupied
        if self.board[row, col] != 0:
            return False
        
        # Check if the move would flip any opponent's pieces
        opponent = self.get_opponent(self.current_player)
        
        # Define all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        
        valid = False
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8) or self.board[r, c] != opponent:
                continue
            
            # Continue in this direction
            r += dr
            c += dc
            found_own = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r, c] == 0:
                    break
                if self.board[r, c] == self.current_player:
                    found_own = True
                    break
                r += dr
                c += dc
            
            if found_own:
                valid = True
                break
        
        return valid
    
    def get_valid_moves(self):
        """Get all valid moves for the current player"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, row, col):
        """Make a move at the given position"""
        if not self.is_valid_move(row, col):
            return False
        
        # Place the piece
        self.board[row, col] = self.current_player
        
        # Flip opponent's pieces
        opponent = self.get_opponent(self.current_player)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                     (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            # Check this direction
            pieces_to_flip = []
            r, c = row + dr, col + dc
            
            # Collect opponent pieces in this direction
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            
            # If we found our own piece at the end, flip all collected pieces
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.current_player and pieces_to_flip:
                for flip_r, flip_c in pieces_to_flip:
                    self.board[flip_r, flip_c] = self.current_player
        
        # Switch player
        self.current_player = opponent
        
        # If the next player has no valid moves, switch back
        if not self.get_valid_moves():
            self.current_player = self.get_opponent(self.current_player)
            # If this player also has no valid moves, the game is over
            if not self.get_valid_moves():
                return "Game Over"
        
        return True
    
    def is_game_over(self):
        """Check if the game is over"""
        # Game is over if board is full
        if np.count_nonzero(self.board) == 64:
            return True
        
        # Game is over if neither player can make a valid move
        player = self.current_player
        if not self.get_valid_moves():
            self.current_player = self.get_opponent(player)
            if not self.get_valid_moves():
                self.current_player = player  # Restore original player
                return True
            self.current_player = player  # Restore original player
        
        return False
    
    def get_winner(self):
        """Get the winner of the game"""
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == 2)
        
        if black_count > white_count:
            return "Black wins!"
        elif white_count > black_count:
            return "White wins!"
        else:
            return "It's a tie!"

# Example game with player input
def play_game():
    game = Reversi()
    
    print("Welcome to Reversi!")
    print("Corner 2x2 squares are restricted and can't be played on.")
    print("Black (●) plays first.")
    
    while not game.is_game_over():
        game.print_board()
        
        player_name = "Black" if game.current_player == 1 else "White"
        symbol = "●" if game.current_player == 1 else "○"
        valid_moves = game.get_valid_moves()
        
        if not valid_moves:
            print(f"{player_name} ({symbol}) has no valid moves. Turn passes.")
            game.current_player = game.get_opponent(game.current_player)
            continue
        
        print(f"{player_name} ({symbol})'s turn")
        print(f"Valid moves: {valid_moves}")
        
        try:
            row = int(input("Enter row (0-7): "))
            col = int(input("Enter column (0-7): "))
            
            if game.make_move(row, col) == "Game Over":
                print("Neither player can move. Game over!")
                break
            elif not game.make_move(row, col):
                print("Invalid move! Try again.")
        except ValueError:
            print("Please enter valid numbers.")
    
    # Game over
    game.print_board()
    print("Game over!")
    print(game.get_winner())

if __name__ == "__main__":
    play_game()
