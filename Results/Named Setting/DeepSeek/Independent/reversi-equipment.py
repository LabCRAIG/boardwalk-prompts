import numpy as np
import sys

class Reversi:
    def __init__(self):
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        # Set up initial pieces
        self.board[3][3] = self.board[4][4] = 1  # White
        self.board[3][4] = self.board[4][3] = 2  # Black
        
        # Define restricted 2x2 corner areas
        self.restricted_areas = [
            (0, 0, 1, 1),   # Top-left
            (0, 6, 1, 7),   # Top-right
            (6, 0, 7, 1),   # Bottom-left
            (6, 6, 7, 7)    # Bottom-right
        ]
        
        self.current_player = 1  # White starts

    def is_valid_move(self, row, col):
        # Check if position is on the board
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False
        
        # Check if position is empty
        if self.board[row][col] != 0:
            return False
            
        # Check if position is in a restricted corner 2x2 area
        for area in self.restricted_areas:
            if area[0] <= row <= area[2] and area[1] <= col <= area[3]:
                return False
                
        # Check if the move would flip at least one opponent's piece
        opponent = 3 - self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == opponent:
                r, c = r + dr, c + dc
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == opponent:
                    r, c = r + dr, c + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    return True
                    
        return False

    def get_valid_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col):
                    moves.append((row, col))
        return moves

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
            
        self.board[row][col] = self.current_player
        opponent = 3 - self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == opponent:
                pieces_to_flip = []
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                    r, c = r + dr, c + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    for flip_row, flip_col in pieces_to_flip:
                        self.board[flip_row][flip_col] = self.current_player
        
        self.current_player = 3 - self.current_player
        return True

    def is_game_over(self):
        # Game is over if neither player can make a move
        return len(self.get_valid_moves()) == 0 and len(self.get_valid_moves_for_player(3 - self.current_player)) == 0

    def get_valid_moves_for_player(self, player):
        original_player = self.current_player
        self.current_player = player
        moves = self.get_valid_moves()
        self.current_player = original_player
        return moves

    def get_score(self):
        white_count = np.count_nonzero(self.board == 1)
        black_count = np.count_nonzero(self.board == 2)
        return white_count, black_count

    def print_board(self):
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for row in range(self.board_size):
            print(f"{row} ", end="")
            for col in range(self.board_size):
                # Check if this cell is in a restricted area
                is_restricted = False
                for area in self.restricted_areas:
                    if area[0] <= row <= area[2] and area[1] <= col <= area[3]:
                        is_restricted = True
                        break
                
                if is_restricted:
                    print("X ", end="")
                else:
                    if self.board[row][col] == 0:
                        print(". ", end="")
                    elif self.board[row][col] == 1:
                        print("W ", end="")
                    else:
                        print("B ", end="")
            print()
        print()

def main():
    game = Reversi()
    
    while not game.is_game_over():
        game.print_board()
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            print(f"Player {game.current_player} has no valid moves. Passing turn.")
            game.current_player = 3 - game.current_player
            continue
            
        print(f"Player {game.current_player}'s turn. Valid moves: {valid_moves}")
        
        if game.current_player == 1:  # Human player (White)
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                if not game.make_move(row, col):
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter valid numbers.")
        else:  # Simple AI (Black)
            print("AI is thinking...")
            # Simple AI: choose the first valid move
            row, col = valid_moves[0]
            print(f"AI chooses: ({row}, {col})")
            game.make_move(row, col)
    
    game.print_board()
    white_score, black_score = game.get_score()
    print(f"Game over! White: {white_score}, Black: {black_score}")
    if white_score > black_score:
        print("White wins!")
    elif black_score > white_score:
        print("Black wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()