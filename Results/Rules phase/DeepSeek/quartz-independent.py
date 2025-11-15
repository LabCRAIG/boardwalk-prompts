import numpy as np

class QuartzGame:
    def __init__(self):
        self.board_size = 8
        self.reset_game()
        
    def reset_game(self):
        """Initialize the game board and state"""
        self.board = np.full((self.board_size, self.board_size), ' ', dtype=str)
        # Set up the initial 2x2 center pieces
        self.board[3:5, 3:5] = [['A', 'V'], ['V', 'A']]
        self.current_player = 'A'  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def is_valid_move(self, row, col):
        """Check if placing a piece at (row, col) is valid for current player"""
        if self.board[row, col] != ' ':
            return False
            
        # Check all 8 directions for a valid line
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                        (0,-1),          (0,1),
                        (1,-1),  (1,0),  (1,1)]:
            if self._check_direction(row, col, dr, dc):
                return True
        return False
    
    def _check_direction(self, row, col, dr, dc):
        """Check if there's a valid line in a specific direction"""
        opponent = 'V' if self.current_player == 'A' else 'A'
        r, c = row + dr, col + dc
        found_opponent = False
        
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if self.board[r, c] == opponent:
                found_opponent = True
                r += dr
                c += dc
            elif self.board[r, c] == self.current_player and found_opponent:
                return True
            else:
                break
        return False
    
    def make_move(self, row, col):
        """Place a piece and flip opponent's pieces if valid"""
        if self.game_over or not self.is_valid_move(row, col):
            return False
            
        self.board[row, col] = self.current_player
        
        # Flip opponent's pieces in all valid directions
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                        (0,-1),          (0,1),
                        (1,-1),  (1,0),  (1,1)]:
            self._flip_direction(row, col, dr, dc)
            
        # Switch player and check if next player has valid moves
        self._switch_player()
        
        # Check if game is over
        self._check_game_over()
        return True
    
    def _flip_direction(self, row, col, dr, dc):
        """Flip opponent's pieces in a valid direction"""
        opponent = 'V' if self.current_player == 'A' else 'A'
        to_flip = []
        r, c = row + dr, col + dc
        
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if self.board[r, c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            elif self.board[r, c] == self.current_player:
                for flip_r, flip_c in to_flip:
                    self.board[flip_r, flip_c] = self.current_player
                break
            else:
                break
    
    def _switch_player(self):
        """Switch to the other player if they have valid moves, otherwise keep current player"""
        self.current_player = 'V' if self.current_player == 'A' else 'A'
        
        # If no valid moves for next player, switch back
        if not self._has_valid_moves():
            self.current_player = 'V' if self.current_player == 'A' else 'A'
            # If original player also has no moves, game will end in _check_game_over
    
    def _has_valid_moves(self):
        """Check if current player has any valid moves"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row, col] == ' ' and self.is_valid_move(row, col):
                    return True
        return False
    
    def _check_game_over(self):
        """Check if the game should end"""
        # Game ends if board is full or neither player can move
        empty_spaces = np.sum(self.board == ' ')
        a_can_move = self._player_can_move('A')
        v_can_move = self._player_can_move('V')
        
        if empty_spaces == 0 or (not a_can_move and not v_can_move):
            self.game_over = True
            self._determine_winner()
    
    def _player_can_move(self, player):
        """Check if a specific player has any valid moves"""
        original_player = self.current_player
        self.current_player = player
        has_moves = self._has_valid_moves()
        self.current_player = original_player
        return has_moves
    
    def _determine_winner(self):
        """Count pieces and determine the winner"""
        a_count = np.sum(self.board == 'A')
        v_count = np.sum(self.board == 'V')
        
        if a_count > v_count:
            self.winner = 'A'
        elif v_count > a_count:
            self.winner = 'V'
        else:
            self.winner = 'Tie'
    
    def display_board(self):
        """Print the current game board"""
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print(f"Current player: {self.current_player}")
        if self.game_over:
            print(f"Game over! Winner: {self.winner}")

def play_quartz():
    """Play the Quartz game in the console"""
    game = QuartzGame()
    
    while not game.game_over:
        game.display_board()
        
        # Get player input
        while True:
            try:
                move = input(f"Player {game.current_player}, enter your move as 'row col': ")
                if move.lower() == 'quit':
                    print("Game ended by player.")
                    return
                
                row, col = map(int, move.split())
                if game.make_move(row, col):
                    break
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Please enter two numbers separated by a space (e.g., '3 4')")
    
    game.display_board()

if __name__ == "__main__":
    print("Welcome to Quartz!")
    print("Players take turns placing their pieces (A or V) on the board.")
    print("To place a piece, enter the row and column numbers (0-7) separated by a space.")
    print("Type 'quit' to end the game early.\n")
    
    play_quartz()