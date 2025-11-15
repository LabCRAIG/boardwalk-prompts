import numpy as np
import os
import time

class ReversiWithKing:
    def __init__(self):
        # Initialize 8x8 board: 0 = empty, 1 = black, 2 = white
        self.board = np.zeros((8, 8), dtype=int)
        
        # Set up the initial board state
        self.board[3, 3] = 2  # White
        self.board[3, 4] = 1  # Black
        self.board[4, 3] = 1  # Black
        self.board[4, 4] = 2  # White
        
        # Player 1 is black, Player 2 is white
        self.current_player = 1
        
        # Kings (special pieces) for each player
        self.black_king_played = False
        self.white_king_played = False
        
        # Kings' positions (None until played)
        self.black_king_pos = None
        self.white_king_pos = None
        
        # Game state
        self.game_over = False
        self.winner = None

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_board(self):
        """Display the current board state."""
        self.clear_screen()
        print("  0 1 2 3 4 5 6 7")
        print(" +-+-+-+-+-+-+-+-+")
        
        for i in range(8):
            row = f"{i}|"
            for j in range(8):
                if self.board[i, j] == 0:
                    row += " |"
                elif self.board[i, j] == 1:
                    if (i, j) == self.black_king_pos:
                        row += "B|"
                    else:
                        row += "●|"
                elif self.board[i, j] == 2:
                    if (i, j) == self.white_king_pos:
                        row += "W|"
                    else:
                        row += "○|"
            print(row)
            print(" +-+-+-+-+-+-+-+-+")
            
        print(f"Black (●): {np.sum(self.board == 1)}")
        print(f"White (○): {np.sum(self.board == 2)}")
        print(f"Black king played: {self.black_king_played}")
        print(f"White king played: {self.white_king_played}")
        
    def is_valid_move(self, row, col, is_king=False):
        """Check if a move is valid."""
        # Check if the position is on the board
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
            
        # Check if the position is already occupied
        if self.board[row, col] != 0:
            return False
            
        opponent = 3 - self.current_player  # 1 -> 2, 2 -> 1
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        # For each direction, check if we can capture opponent's pieces
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8) or self.board[r, c] != opponent:
                continue
                
            # Check for king in the line if we're not placing a king
            king_in_line = False
            if not is_king:
                # Check if the opponent's king is in this line
                if opponent == 1 and self.black_king_played:  # Check for black king
                    test_r, test_c = r, c
                    while 0 <= test_r < 8 and 0 <= test_c < 8:
                        if (test_r, test_c) == self.black_king_pos:
                            king_in_line = True
                            break
                        test_r += dr
                        test_c += dc
                elif opponent == 2 and self.white_king_played:  # Check for white king
                    test_r, test_c = r, c
                    while 0 <= test_r < 8 and 0 <= test_c < 8:
                        if (test_r, test_c) == self.white_king_pos:
                            king_in_line = True
                            break
                        test_r += dr
                        test_c += dc
            
            # If the opponent's king is in this line, we can't capture
            if king_in_line:
                continue
                
            # Continue in the direction to see if we can sandwich opponent pieces
            r += dr
            c += dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r, c] == 0:
                    break
                if self.board[r, c] == self.current_player:
                    return True  # Valid move found
                r += dr
                c += dc
                
        return False
        
    def get_valid_moves(self, is_king=False):
        """Get all valid moves for the current player."""
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, is_king):
                    valid_moves.append((i, j))
        return valid_moves
        
    def make_move(self, row, col, is_king=False):
        """Make a move and update the board."""
        if not self.is_valid_move(row, col, is_king):
            return False
            
        # Place the piece
        self.board[row, col] = self.current_player
        
        # If it's a king, update the king's status and position
        if is_king:
            if self.current_player == 1:
                self.black_king_played = True
                self.black_king_pos = (row, col)
            else:
                self.white_king_played = True
                self.white_king_pos = (row, col)
        
        # Capture opponent pieces
        opponent = 3 - self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            # Check if we can capture in this direction
            r, c = row + dr, col + dc
            to_flip = []
            
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
                
            if to_flip and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.current_player:
                # Check if king is in this line
                king_in_line = False
                if opponent == 1 and self.black_king_played:
                    for flip_r, flip_c in to_flip:
                        if (flip_r, flip_c) == self.black_king_pos:
                            king_in_line = True
                            break
                elif opponent == 2 and self.white_king_played:
                    for flip_r, flip_c in to_flip:
                        if (flip_r, flip_c) == self.white_king_pos:
                            king_in_line = True
                            break
                
                # If the opponent's king isn't in this line, flip the pieces
                if not king_in_line:
                    for flip_r, flip_c in to_flip:
                        self.board[flip_r, flip_c] = self.current_player
                        
                        # If we flipped a king position, update it
                        if (flip_r, flip_c) == self.black_king_pos:
                            self.black_king_pos = None
                        elif (flip_r, flip_c) == self.white_king_pos:
                            self.white_king_pos = None
                            
        # Switch to the other player
        self.current_player = opponent
        return True
        
    def check_game_over(self):
        """Check if the game is over."""
        # Check if either player has valid moves
        black_moves = self.current_player == 1 and (len(self.get_valid_moves()) > 0 or (not self.black_king_played))
        white_moves = self.current_player == 2 and (len(self.get_valid_moves()) > 0 or (not self.white_king_played))
        
        if not black_moves and not white_moves:
            self.game_over = True
            black_count = np.sum(self.board == 1)
            white_count = np.sum(self.board == 2)
            
            if black_count > white_count:
                self.winner = 1
            elif white_count > black_count:
                self.winner = 2
            else:
                self.winner = 0  # Draw
                
        return self.game_over
    
    def switch_player_if_no_moves(self):
        """Switch player if they have no valid moves."""
        valid_moves = self.get_valid_moves()
        king_available = (self.current_player == 1 and not self.black_king_played) or \
                         (self.current_player == 2 and not self.white_king_played)
                         
        if not valid_moves and not king_available:
            self.current_player = 3 - self.current_player
            return True
        return False
        
    def play_game(self):
        """Main game loop."""
        while not self.game_over:
            self.print_board()
            
            # Check if the current player has any valid moves
            if self.switch_player_if_no_moves():
                print(f"Player {self.current_player} has no valid moves. Switching players.")
                time.sleep(2)
                continue
                
            # Current player info
            player_name = "Black" if self.current_player == 1 else "White"
            piece_symbol = "●" if self.current_player == 1 else "○"
            
            print(f"{player_name}'s turn ({piece_symbol})")
            
            # Ask if the player wants to play the king
            king_available = (self.current_player == 1 and not self.black_king_played) or \
                             (self.current_player == 2 and not self.white_king_played)
                             
            is_king = False
            if king_available:
                while True:
                    play_king = input("Do you want to play your king piece? (y/n): ").lower()
                    if play_king in ['y', 'n']:
                        is_king = (play_king == 'y')
                        break
                    print("Invalid input. Please enter 'y' or 'n'.")
            
            # Get valid moves for the current player
            valid_moves = self.get_valid_moves(is_king)
            
            if not valid_moves and not is_king:
                print("No valid moves available.")
                time.sleep(2)
                self.current_player = 3 - self.current_player
                continue
                
            # Display valid moves
            print("Valid moves:", valid_moves)
            
            # Get player's move
            while True:
                try:
                    move_input = input("Enter your move (row,col): ")
                    row, col = map(int, move_input.split(','))
                    
                    if (row, col) in valid_moves or (is_king and self.board[row, col] == 0):
                        if self.make_move(row, col, is_king):
                            break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter row,col (e.g. 3,4)")
                except IndexError:
                    print("Position out of bounds. Please enter valid coordinates.")
            
            # Check if the game is over
            if self.check_game_over():
                self.print_board()
                if self.winner == 0:
                    print("Game over! It's a draw!")
                else:
                    winner_name = "Black" if self.winner == 1 else "White"
                    print(f"Game over! {winner_name} wins!")
                break

if __name__ == "__main__":
    game = ReversiWithKing()
    game.play_game()