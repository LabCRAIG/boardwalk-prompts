class QuartzGame:
    def __init__(self):
        # Initialize 8x8 board with None for empty spaces
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Set up initial board configuration with A and V pieces in the center
        self.board[3][3] = 'A'
        self.board[4][4] = 'A'
        self.board[3][4] = 'V'
        self.board[4][3] = 'V'
        
        # Player 1 uses 'A', Player 2 uses 'V'
        self.current_player = 1
        self.player_pieces = {1: 'A', 2: 'V'}
        
        # Game status
        self.game_over = False
        self.winner = None
    
    def print_board(self):
        """Print the current state of the board."""
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row_str = f"{i} "
            for j in range(8):
                if self.board[i][j] is None:
                    row_str += ". "
                else:
                    row_str += f"{self.board[i][j]} "
            print(row_str)
        print()
    
    def count_pieces(self):
        """Count the number of pieces for each player."""
        count_a = sum(row.count('A') for row in self.board)
        count_v = sum(row.count('V') for row in self.board)
        return {'A': count_a, 'V': count_v}
    
    def get_valid_moves(self):
        """Get all valid moves for the current player."""
        valid_moves = []
        player_piece = self.player_pieces[self.current_player]
        opponent_piece = self.player_pieces[3 - self.current_player]  # 3-1=2, 3-2=1
        
        # Search for valid moves in all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:
                    continue  # Skip occupied spaces
                
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    if not (0 <= r < 8 and 0 <= c < 8) or self.board[r][c] != opponent_piece:
                        continue  # Need at least one opponent piece adjacent
                    
                    # Continue in this direction looking for our own piece
                    pieces_to_flip = [(r, c)]
                    r += dr
                    c += dc
                    while 0 <= r < 8 and 0 <= c < 8:
                        if self.board[r][c] is None:
                            break  # Empty space, not valid
                        if self.board[r][c] == player_piece:
                            # Found our piece, this is a valid move
                            if pieces_to_flip:
                                if (row, col) not in valid_moves:
                                    valid_moves.append((row, col))
                            break
                        # Otherwise it's an opponent piece, keep going
                        pieces_to_flip.append((r, c))
                        r += dr
                        c += dc
        
        return valid_moves
    
    def make_move(self, row, col):
        """Make a move at the specified position if valid."""
        valid_moves = self.get_valid_moves()
        if (row, col) not in valid_moves:
            return False
        
        player_piece = self.player_pieces[self.current_player]
        opponent_piece = self.player_pieces[3 - self.current_player]
        
        # Place the piece
        self.board[row][col] = player_piece
        
        # Flip opponent pieces in all directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            pieces_to_flip = []
            r, c = row + dr, col + dc
            
            # Collect opponent pieces to flip
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent_piece:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            
            # Check if we found our own piece at the end
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player_piece:
                # Flip all the collected pieces
                for flip_r, flip_c in pieces_to_flip:
                    self.board[flip_r][flip_c] = player_piece
        
        # Switch to the other player
        self.current_player = 3 - self.current_player
        
        # Check if the next player has any valid moves
        if not self.get_valid_moves():
            # If not, switch back to the current player
            self.current_player = 3 - self.current_player
            # If current player also has no moves, game is over
            if not self.get_valid_moves():
                self.end_game()
        
        return True
    
    def end_game(self):
        """End the game and determine the winner."""
        self.game_over = True
        counts = self.count_pieces()
        if counts['A'] > counts['V']:
            self.winner = 1
        elif counts['V'] > counts['A']:
            self.winner = 2
        else:
            self.winner = 0  # Draw
    
    def is_board_full(self):
        """Check if the board is full."""
        for row in self.board:
            if None in row:
                return False
        return True
    
    def play_game(self):
        """Play the game with console input."""
        while not self.game_over:
            self.print_board()
            counts = self.count_pieces()
            print(f"Player 1 (A): {counts['A']} pieces")
            print(f"Player 2 (V): {counts['V']} pieces")
            print(f"Player {self.current_player}'s turn ({self.player_pieces[self.current_player]})")
            
            valid_moves = self.get_valid_moves()
            if not valid_moves:
                print(f"No valid moves for Player {self.current_player}. Passing turn.")
                self.current_player = 3 - self.current_player
                valid_moves = self.get_valid_moves()
                if not valid_moves:
                    print("No valid moves for either player. Game over.")
                    self.end_game()
                continue
            
            print("Valid moves:", valid_moves)
            
            move_made = False
            while not move_made:
                try:
                    row = int(input("Enter row (0-7): "))
                    col = int(input("Enter column (0-7): "))
                    if 0 <= row < 8 and 0 <= col < 8:
                        move_made = self.make_move(row, col)
                        if not move_made:
                            print("Invalid move. Try again.")
                    else:
                        print("Invalid coordinates. Try again.")
                except ValueError:
                    print("Please enter valid numbers.")
            
            # Check if board is full after move
            if self.is_board_full():
                self.end_game()
        
        # Game is over, show final result
        self.print_board()
        counts = self.count_pieces()
        print(f"Final score - Player 1 (A): {counts['A']}, Player 2 (V): {counts['V']}")
        
        if self.winner == 0:
            print("Game ended in a draw!")
        else:
            print(f"Player {self.winner} wins!")


# Example usage to play the game
if __name__ == "__main__":
    game = QuartzGame()
    game.play_game()