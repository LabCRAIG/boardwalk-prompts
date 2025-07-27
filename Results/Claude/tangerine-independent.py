class TangerineGame:
    def __init__(self):
        # Initialize a 6x6 board with empty spaces
        self.board = [[' ' for _ in range(6)] for _ in range(6)]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        """Display the current state of the board."""
        print("  0 1 2 3 4 5")
        print("  -----------")
        for i, row in enumerate(self.board):
            print(f"{i}|{' '.join(row)}|")
        print("  -----------")
    
    def is_valid_move(self, row, col, player):
        """Check if a move is valid for the current player."""
        # Check if the coordinates are within bounds
        if not (0 <= row < 6 and 0 <= col < 6):
            return False
        
        # Player 1 places H pieces (horizontally)
        if player == 1:
            # Check if there's space for an H piece (needs two horizontal spaces)
            if col + 1 < 6 and self.board[row][col] == ' ' and self.board[row][col + 1] == ' ':
                return True
            
        # Player 2 places V pieces (vertically)
        elif player == 2:
            # Check if there's space for a V piece (needs two vertical spaces)
            if row + 1 < 6 and self.board[row][col] == ' ' and self.board[row + 1][col] == ' ':
                return True
            
        return False
    
    def make_move(self, row, col):
        """Attempt to make a move at the specified position."""
        if self.game_over:
            print("Game is already over!")
            return False
        
        if not self.is_valid_move(row, col, self.current_player):
            print("Invalid move!")
            return False
        
        # Make the move based on the current player
        if self.current_player == 1:
            # Player 1 places an H piece (horizontally)
            self.board[row][col] = 'H'
            self.board[row][col + 1] = 'H'
        else:
            # Player 2 places a V piece (vertically)
            self.board[row][col] = 'V'
            self.board[row + 1][col] = 'V'
        
        # Check if the game is over
        if self.check_game_over():
            self.game_over = True
            self.winner = 3 - self.current_player  # The other player wins
            return True
        
        # Switch to the other player
        self.current_player = 3 - self.current_player
        return True
    
    def check_game_over(self):
        """Check if the current player has any valid moves left."""
        for row in range(6):
            for col in range(6):
                if self.is_valid_move(row, col, self.current_player):
                    return False
        return True
    
    def has_valid_moves(self, player):
        """Check if the specified player has any valid moves."""
        for row in range(6):
            for col in range(6):
                if self.is_valid_move(row, col, player):
                    return True
        return False

    def get_all_valid_moves(self, player):
        """Get a list of all valid moves for the specified player."""
        valid_moves = []
        for row in range(6):
            for col in range(6):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def play_game(self):
        """Interactive game loop for two human players."""
        print("Welcome to Tangerine!")
        print("Player 1 places H pieces horizontally, Player 2 places V pieces vertically.")
        
        while not self.game_over:
            print(f"\nPlayer {self.current_player}'s turn")
            self.display_board()
            
            valid_moves = self.get_all_valid_moves(self.current_player)
            if not valid_moves:
                print(f"Player {self.current_player} has no valid moves!")
                self.game_over = True
                self.winner = 3 - self.current_player
                break
            
            print(f"Valid moves: {valid_moves}")
            
            try:
                row = int(input("Enter row (0-5): "))
                col = int(input("Enter column (0-5): "))
                
                if self.make_move(row, col):
                    pass  # Move was successful
                else:
                    print("Try again.")
            except ValueError:
                print("Please enter valid numbers.")
        
        # Game is over
        self.display_board()
        if self.winner:
            print(f"Game over! Player {self.winner} wins!")
        else:
            print("Game over! It's a tie!")


# Simple AI player implementation using Minimax algorithm
def minimax(game, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    player = 1 if maximizing_player else 2
    
    # Check if game is over or reached max depth
    if depth == 0 or game.game_over:
        # Simple heuristic: difference in number of valid moves
        p1_moves = len(game.get_all_valid_moves(1))
        p2_moves = len(game.get_all_valid_moves(2))
        return p1_moves - p2_moves if maximizing_player else p2_moves - p1_moves
    
    valid_moves = game.get_all_valid_moves(player)
    
    if maximizing_player:
        value = float('-inf')
        for move in valid_moves:
            row, col = move
            # Create a copy of the game
            new_game = TangerineGame()
            new_game.board = [row[:] for row in game.board]
            new_game.current_player = player
            
            new_game.make_move(row, col)
            eval = minimax(new_game, depth - 1, False, alpha, beta)
            value = max(value, eval)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = float('inf')
        for move in valid_moves:
            row, col = move
            # Create a copy of the game
            new_game = TangerineGame()
            new_game.board = [row[:] for row in game.board]
            new_game.current_player = player
            
            new_game.make_move(row, col)
            eval = minimax(new_game, depth - 1, True, alpha, beta)
            value = min(value, eval)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def get_best_move(game, depth=3):
    player = game.current_player
    valid_moves = game.get_all_valid_moves(player)
    best_move = None
    
    if player == 1:  # Maximizing player
        best_value = float('-inf')
        for move in valid_moves:
            row, col = move
            # Create a copy of the game
            new_game = TangerineGame()
            new_game.board = [row[:] for row in game.board]
            new_game.current_player = player
            
            new_game.make_move(row, col)
            move_value = minimax(new_game, depth - 1, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
    else:  # Minimizing player
        best_value = float('inf')
        for move in valid_moves:
            row, col = move
            # Create a copy of the game
            new_game = TangerineGame()
            new_game.board = [row[:] for row in game.board]
            new_game.current_player = player
            
            new_game.make_move(row, col)
            move_value = minimax(new_game, depth - 1, True)
            if move_value < best_value:
                best_value = move_value
                best_move = move
    
    return best_move

def play_against_ai():
    game = TangerineGame()
    human_player = int(input("Which player do you want to be? (1 or 2): "))
    ai_player = 3 - human_player
    
    print("You are player", human_player)
    print("Player 1 uses 'H' pieces, Player 2 uses 'V' pieces")
    
    while not game.game_over:
        game.display_board()
        current = game.current_player
        
        if current == human_player:
            print(f"Your turn (Player {human_player})")
            valid_moves = game.get_all_valid_moves(current)
            
            if not valid_moves:
                print("You have no valid moves!")
                game.game_over = True
                game.winner = ai_player
                break
            
            print(f"Valid moves: {valid_moves}")
            
            try:
                row = int(input("Enter row (0-5): "))
                col = int(input("Enter column (0-5): "))
                
                if not game.make_move(row, col):
                    print("Invalid move, try again.")
                    continue
            except ValueError:
                print("Please enter valid numbers.")
                continue
                
        else:  # AI's turn
            print(f"AI's turn (Player {ai_player})")
            valid_moves = game.get_all_valid_moves(current)
            
            if not valid_moves:
                print("AI has no valid moves!")
                game.game_over = True
                game.winner = human_player
                break
            
            # Get the best move for the AI
            best_move = get_best_move(game)
            if best_move:
                row, col = best_move
                print(f"AI places at ({row}, {col})")
                game.make_move(row, col)
            else:
                # Fallback to first valid move if minimax fails
                row, col = valid_moves[0]
                print(f"AI places at ({row}, {col})")
                game.make_move(row, col)
    
    # Game is over
    game.display_board()
    if game.winner == human_player:
        print("Congratulations! You win!")
    elif game.winner == ai_player:
        print("AI wins! Better luck next time.")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    print("Welcome to Tangerine!")
    print("1. Play against another human")
    print("2. Play against AI")
    choice = input("Choose an option: ")
    
    if choice == "1":
        game = TangerineGame()
        game.play_game()
    elif choice == "2":
        play_against_ai()
    else:
        print("Invalid choice!")