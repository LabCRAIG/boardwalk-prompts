import numpy as np
import random
import os

class Reversi:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        # Initial setup
        self.board[3, 3] = self.board[4, 4] = 1  # White
        self.board[3, 4] = self.board[4, 3] = 2  # Black
        self.current_player = 2  # Black starts
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),           (0, 1),
                          (1, -1),  (1, 0),   (1, 1)]
    
    def print_board(self):
        """Print the current board state"""
        print("  a b c d e f g h")
        for i in range(8):
            print(f"{i+1} ", end="")
            for j in range(8):
                if self.board[i, j] == 0:
                    print(". ", end="")
                elif self.board[i, j] == 1:
                    print("O ", end="")  # White
                else:
                    print("X ", end="")  # Black
            print()
    
    def is_valid_move(self, row, col, player):
        """Check if a move is valid for the given player"""
        if self.board[row, col] != 0:
            return False
        
        opponent = 3 - player  # 1->2, 2->1
        valid = False
        
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                # Continue in this direction
                r += dr
                c += dc
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == player:
                    valid = True
                    break
        
        return valid
    
    def get_valid_moves(self, player):
        """Get all valid moves for the given player"""
        moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, player):
                    moves.append((i, j))
        return moves
    
    def make_move(self, row, col, player):
        """Make a move and flip the appropriate pieces"""
        if not self.is_valid_move(row, col, player):
            return False
        
        self.board[row, col] = player
        opponent = 3 - player
        
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                # Continue in this direction
                r += dr
                c += dc
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == player:
                    # Flip pieces along this direction
                    r, c = row + dr, col + dc
                    while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                        self.board[r, c] = player
                        r += dr
                        c += dc
        
        return True
    
    def get_score(self):
        """Get the current score (white, black)"""
        white_count = np.sum(self.board == 1)
        black_count = np.sum(self.board == 2)
        return white_count, black_count
    
    def is_game_over(self):
        """Check if the game is over"""
        # Game is over if neither player can make a move
        return len(self.get_valid_moves(1)) == 0 and len(self.get_valid_moves(2)) == 0
    
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 3 - self.current_player
    
    def get_ai_move(self, player):
        """Simple AI that chooses a random valid move"""
        valid_moves = self.get_valid_moves(player)
        if valid_moves:
            return random.choice(valid_moves)
        return None
    
    def play(self):
        """Main game loop"""
        print("Welcome to Reversi!")
        print("You are playing as X (Black)")
        print("Enter moves in the format 'a1', 'b2', etc.")
        print("Type 'quit' to exit the game.")
        
        while not self.is_game_over():
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_board()
            
            white_score, black_score = self.get_score()
            print(f"Score: X (You): {black_score}, O (AI): {white_score}")
            
            if self.current_player == 2:  # Human player (Black)
                valid_moves = self.get_valid_moves(2)
                if not valid_moves:
                    print("No valid moves for you. Passing turn to AI.")
                    self.switch_player()
                    continue
                
                move = input("Your move: ").lower()
                if move == 'quit':
                    break
                
                # Parse input
                if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
                    print("Invalid input. Please use format like 'a1', 'b2', etc.")
                    input("Press Enter to continue...")
                    continue
                
                col = ord(move[0]) - ord('a')
                row = int(move[1]) - 1
                
                if not (0 <= row < 8 and 0 <= col < 8):
                    print("Invalid position. Please choose between a1 and h8.")
                    input("Press Enter to continue...")
                    continue
                
                if not self.make_move(row, col, 2):
                    print("Invalid move. Please choose a valid position.")
                    input("Press Enter to continue...")
                    continue
                
                self.switch_player()
            
            else:  # AI player (White)
                print("AI is thinking...")
                move = self.get_ai_move(1)
                if move:
                    row, col = move
                    print(f"AI plays {chr(ord('a') + col)}{row + 1}")
                    self.make_move(row, col, 1)
                else:
                    print("AI has no valid moves. Passing turn to you.")
                
                self.switch_player()
                input("Press Enter to continue...")
        
        # Game over
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_board()
        white_score, black_score = self.get_score()
        print(f"Game Over! Final Score: X (You): {black_score}, O (AI): {white_score}")
        
        if black_score > white_score:
            print("Congratulations! You win!")
        elif white_score > black_score:
            print("AI wins! Better luck next time.")
        else:
            print("It's a tie!")

# Start the game
if __name__ == "__main__":
    game = Reversi()
    game.play()