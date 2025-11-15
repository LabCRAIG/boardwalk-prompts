import numpy as np
import sys

class ReversiWithKing:
    def __init__(self):
        self.board_size = 8
        self.reset_game()
        
    def reset_game(self):
        # Initialize the board
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Set up initial pieces
        mid = self.board_size // 2
        self.board[mid-1][mid-1] = 2  # White
        self.board[mid][mid] = 2      # White
        self.board[mid-1][mid] = 1    # Black
        self.board[mid][mid-1] = 1    # Black
        
        # Track kings
        self.black_king_used = False
        self.white_king_used = False
        
        # Game state
        self.current_player = 1  # Black starts
        self.game_over = False
        
    def is_valid_position(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size
        
    def is_valid_move(self, row, col, player, is_king=False):
        # Check if position is empty and on board
        if not self.is_valid_position(row, col) or self.board[row][col] != 0:
            return False
            
        opponent = 3 - player  # 1->2, 2->1
        
        # Check all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        
        valid = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if not self.is_valid_position(r, c) or self.board[r][c] != opponent:
                continue
                
            # Continue in this direction
            r += dr
            c += dc
            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                r += dr
                c += dc
                
            # If we found a player's piece at the end, it's a valid move
            if self.is_valid_position(r, c) and self.board[r][c] == player:
                # Special case: if this is a king move, check if the line contains opponent's king
                if is_king:
                    # Check if there's an opponent king in the line we would flip
                    temp_r, temp_c = row + dr, col + dc
                    king_found = False
                    while temp_r != r or temp_c != c:
                        if self.board[temp_r][temp_c] == 4 if player == 1 else 3:
                            king_found = True
                            break
                        temp_r += dr
                        temp_c += dc
                    
                    # If king found in the line, this move is invalid for king placement
                    if king_found:
                        continue
                
                valid = True
                break
                
        return valid
        
    def get_valid_moves(self, player, include_king=False):
        moves = []
        king_moves = []
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
                
                # Check if king can be placed here
                if include_king and not (self.black_king_used if player == 1 else self.white_king_used):
                    if self.is_valid_move(row, col, player, is_king=True):
                        king_moves.append((row, col, True))
        
        return moves, king_moves
        
    def make_move(self, row, col, is_king=False):
        player = self.current_player
        opponent = 3 - player
        
        if is_king:
            if (player == 1 and self.black_king_used) or (player == 2 and self.white_king_used):
                return False, "King already used"
                
            if not self.is_valid_move(row, col, player, is_king=True):
                return False, "Invalid king move"
                
            # Place the king (coded as 3 for black king, 4 for white king)
            self.board[row][col] = 3 if player == 1 else 4
            
            # Mark king as used
            if player == 1:
                self.black_king_used = True
            else:
                self.white_king_used = True
                
        else:
            if not self.is_valid_move(row, col, player):
                return False, "Invalid move"
                
            # Place normal piece
            self.board[row][col] = player
            
        # Flip opponent's pieces in all valid directions
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        
        flipped = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if not self.is_valid_position(r, c) or self.board[r][c] != opponent:
                continue
                
            # Continue in this direction to find a player's piece
            path = []
            r, c = row + dr, col + dc
            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                path.append((r, c))
                r += dr
                c += dc
                
            # If we found a player's piece at the end, flip all opponent pieces in between
            if self.is_valid_position(r, c) and (self.board[r][c] == player or 
                                               (player == 1 and self.board[r][c] == 3) or 
                                               (player == 2 and self.board[r][c] == 4)):
                # Special case: if this is a king move, don't flip if there's a king in the path
                if is_king:
                    king_in_path = False
                    for pr, pc in path:
                        if self.board[pr][pc] == 3 or self.board[pr][pc] == 4:
                            king_in_path = True
                            break
                    
                    if king_in_path:
                        continue
                
                # Flip the pieces
                for pr, pc in path:
                    self.board[pr][pc] = player
                flipped = True
                
        if not flipped and not is_king:
            return False, "Move doesn't flip any pieces"
            
        # Switch player
        self.current_player = opponent
        
        # Check if game is over
        black_moves, black_king_moves = self.get_valid_moves(1, include_king=not self.black_king_used)
        white_moves, white_king_moves = self.get_valid_moves(2, include_king=not self.white_king_used)
        
        if (not black_moves and not black_king_moves and 
            not white_moves and not white_king_moves):
            self.game_over = True
            
        return True, "Move successful"
        
    def get_score(self):
        black_count = np.sum((self.board == 1) | (self.board == 3))
        white_count = np.sum((self.board == 2) | (self.board == 4))
        return black_count, white_count
        
    def print_board(self):
        symbols = {0: '.', 1: 'B', 2: 'W', 3: 'K', 4: 'Q'}  # K for black king, Q for white queen
        
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for row in range(self.board_size):
            print(f"{row} ", end="")
            for col in range(self.board_size):
                print(symbols[self.board[row][col]] + " ", end="")
            print()
            
        black_score, white_score = self.get_score()
        print(f"Score: Black {black_score} - White {white_score}")
        print(f"Kings available: Black {'No' if self.black_king_used else 'Yes'}, White {'No' if self.white_king_used else 'Yes'}")
        print(f"Current player: {'Black' if self.current_player == 1 else 'White'}")
        
    def play(self):
        print("Welcome to Reversi with Kings!")
        print("Black moves first. Enter your moves as 'row col' or 'row col king' to use your king.")
        print("For example: '3 4' for a normal move or '3 4 king' to use your king piece.")
        
        while not self.game_over:
            self.print_board()
            
            player = self.current_player
            moves, king_moves = self.get_valid_moves(player, include_king=not (self.black_king_used if player == 1 else self.white_king_used))
            
            if not moves and not king_moves:
                print(f"{'Black' if player == 1 else 'White'} has no valid moves. Passing turn.")
                self.current_player = 3 - player
                continue
                
            # Get player input
            while True:
                try:
                    inp = input("Enter your move: ").strip().split()
                    if not inp:
                        continue
                        
                    if inp[0].lower() == 'quit':
                        print("Thanks for playing!")
                        return
                        
                    row = int(inp[0])
                    col = int(inp[1])
                    is_king = len(inp) > 2 and inp[2].lower() == 'king'
                    
                    success, message = self.make_move(row, col, is_king)
                    if success:
                        break
                    else:
                        print(f"Invalid move: {message}")
                except (ValueError, IndexError):
                    print("Please enter your move as 'row col' or 'row col king'")
                except KeyboardInterrupt:
                    print("\nThanks for playing!")
                    return
                    
        # Game over
        self.print_board()
        black_score, white_score = self.get_score()
        
        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("It's a tie!")
            
        print("Game over!")

if __name__ == "__main__":
    game = ReversiWithKing()
    game.play()