import numpy as np
import os

class Checkers:
    def __init__(self):
        # Board representation:
        # 0: empty square
        # 1: red piece
        # 2: red king
        # -1: black piece
        # -2: black king
        self.board = np.zeros((8, 8), dtype=int)
        self.current_player = 1  # 1 for red, -1 for black
        self.game_over = False
        self.winner = None
        self.setup_board()
    
    def setup_board(self):
        # Set up the initial board configuration
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Only dark squares can have pieces
                    if row < 3:
                        self.board[row, col] = -1  # Black pieces
                    elif row > 4:
                        self.board[row, col] = 1   # Red pieces
    
    def print_board(self):
        """Print the current board state with ASCII characters"""
        print("  " + " ".join(str(i) for i in range(8)))
        for row in range(8):
            print(f"{row} ", end="")
            for col in range(8):
                piece = self.board[row, col]
                if piece == 0:
                    print(". ", end="")
                elif piece == 1:
                    print("r ", end="")
                elif piece == 2:
                    print("R ", end="")
                elif piece == -1:
                    print("b ", end="")
                elif piece == -2:
                    print("B ", end="")
            print()
        print(f"Current player: {'Red' if self.current_player == 1 else 'Black'}")
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        if not self.is_valid_position(row, col) or self.board[row, col] == 0:
            return []
        
        piece = self.board[row, col]
        moves = []
        captures = []
        
        # Determine movement direction based on piece type
        if piece > 0:  # Red piece or king
            directions = [(1, -1), (1, 1)]  # Down-left, down-right
            if piece == 2:  # Red king can also move up
                directions.extend([(-1, -1), (-1, 1)])
        else:  # Black piece or king
            directions = [(-1, -1), (-1, 1)]  # Up-left, up-right
            if piece == -2:  # Black king can also move down
                directions.extend([(1, -1), (1, 1)])
        
        # Check for regular moves and captures
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            jump_row, jump_col = row + 2*dr, col + 2*dc
            
            # Regular move
            if (self.is_valid_position(new_row, new_col) and 
                self.board[new_row, new_col] == 0):
                moves.append((new_row, new_col, False))
            
            # Capture move
            if (self.is_valid_position(jump_row, jump_col) and
                self.is_valid_position(new_row, new_col) and
                self.board[new_row, new_col] * piece < 0 and  # Opponent piece
                self.board[jump_row, jump_col] == 0):
                captures.append((jump_row, jump_col, True, new_row, new_col))
        
        # If captures are available, they are mandatory
        return captures if captures else moves
    
    def get_all_valid_moves(self):
        """Get all valid moves for the current player"""
        all_moves = {}
        has_captures = False
        
        for row in range(8):
            for col in range(8):
                if self.board[row, col] * self.current_player > 0:
                    moves = self.get_valid_moves(row, col)
                    if moves:
                        # Check if any moves are captures
                        if any(move[2] for move in moves):
                            has_captures = True
                        all_moves[(row, col)] = moves
        
        # If captures are available, filter out non-capture moves
        if has_captures:
            filtered_moves = {}
            for pos, moves in all_moves.items():
                capture_moves = [move for move in moves if move[2]]
                if capture_moves:
                    filtered_moves[pos] = capture_moves
            return filtered_moves
        
        return all_moves
    
    def make_move(self, from_pos, to_pos):
        """Make a move from from_pos to to_pos"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Get all valid moves for the piece
        valid_moves = self.get_valid_moves(from_row, from_col)
        move_info = None
        
        # Find the specific move
        for move in valid_moves:
            if move[0] == to_row and move[1] == to_col:
                move_info = move
                break
        
        if move_info is None:
            return False  # Invalid move
        
        # Move the piece
        piece = self.board[from_row, from_col]
        self.board[to_row, to_col] = piece
        self.board[from_row, from_col] = 0
        
        # Handle capture
        if move_info[2]:  # If it's a capture
            capture_row, capture_col = move_info[3], move_info[4]
            self.board[capture_row, capture_col] = 0
        
        # Check for promotion to king
        if (piece == 1 and to_row == 0) or (piece == -1 and to_row == 7):
            self.board[to_row, to_col] = 2 if piece == 1 else -2
        
        # Check for multiple captures
        if move_info[2]:  # If we just made a capture
            # Check if more captures are possible from the new position
            further_captures = [move for move in self.get_valid_moves(to_row, to_col) 
                              if move[2]]
            if further_captures:
                return "continue"  # Player gets another turn
        
        # Switch player if no further captures
        self.current_player *= -1
        return True
    
    def check_game_over(self):
        """Check if the game is over and determine the winner"""
        # Check if current player has any moves
        moves = self.get_all_valid_moves()
        if not moves:
            self.game_over = True
            self.winner = -self.current_player
            return True
        
        # Check if any pieces remain
        red_pieces = np.sum(self.board > 0)
        black_pieces = np.sum(self.board < 0)
        
        if red_pieces == 0:
            self.game_over = True
            self.winner = -1  # Black wins
            return True
        elif black_pieces == 0:
            self.game_over = True
            self.winner = 1   # Red wins
            return True
        
        return False
    
    def play(self):
        """Main game loop"""
        print("Welcome to Checkers!")
        print("Red pieces: r (regular), R (king)")
        print("Black pieces: b (regular), B (king)")
        print("Enter moves as 'row col to row col' (e.g., '5 2 to 4 3')")
        
        while not self.game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_board()
            
            moves = self.get_all_valid_moves()
            if not moves:
                break
            
            print("\nAvailable moves:")
            for (row, col), move_list in moves.items():
                for move in move_list:
                    print(f"  ({row}, {col}) -> ({move[0]}, {move[1]}){' [CAPTURE]' if move[2] else ''}")
            
            try:
                move_input = input("\nEnter your move: ").strip()
                if move_input.lower() in ['quit', 'exit']:
                    break
                
                # Parse input like "5 2 to 4 3"
                if 'to' in move_input:
                    parts = move_input.split('to')
                    from_part = parts[0].strip().split()
                    to_part = parts[1].strip().split()
                    
                    if len(from_part) == 2 and len(to_part) == 2:
                        from_row, from_col = int(from_part[0]), int(from_part[1])
                        to_row, to_col = int(to_part[0]), int(to_part[1])
                        
                        result = self.make_move((from_row, from_col), (to_row, to_col))
                        
                        if result == "continue":
                            print("Capture made! You get another turn.")
                            input("Press Enter to continue...")
                            continue
                        elif result:
                            # Check if game is over
                            self.check_game_over()
                        else:
                            print("Invalid move! Try again.")
                            input("Press Enter to continue...")
                    else:
                        print("Invalid input format! Use 'row col to row col'")
                        input("Press Enter to continue...")
                else:
                    print("Please include 'to' in your move input")
                    input("Press Enter to continue...")
                    
            except (ValueError, IndexError):
                print("Invalid input! Please enter numbers for row and column.")
                input("Press Enter to continue...")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_board()
        if self.winner:
            winner_name = "Red" if self.winner == 1 else "Black"
            print(f"\nGame over! {winner_name} wins!")
        else:
            print("\nGame ended!")

# Simple AI opponent for demonstration
class CheckersAI:
    def __init__(self, game, player=-1):
        self.game = game
        self.player = player
    
    def get_move(self):
        """Get a move for the AI player"""
        moves = self.game.get_all_valid_moves()
        if not moves:
            return None
        
        # Convert moves to a list of (from_pos, to_pos) tuples
        all_possible_moves = []
        for from_pos, move_list in moves.items():
            for move in move_list:
                all_possible_moves.append((from_pos, (move[0], move[1])))
        
        # Simple strategy: prefer captures, then random move
        capture_moves = []
        regular_moves = []
        
        for from_pos, to_pos in all_possible_moves:
            # Check if this is a capture (we'd need to check the specific move info)
            # For simplicity, we'll assume any move that jumps 2 squares is a capture
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            if abs(to_row - from_row) == 2:  # Capture move
                capture_moves.append((from_pos, to_pos))
            else:
                regular_moves.append((from_pos, to_pos))
        
        if capture_moves:
            return capture_moves[0]  # Return first capture
        elif regular_moves:
            return regular_moves[0]  # Return first regular move
        
        return None

def play_against_ai():
    """Play a game against a simple AI"""
    game = Checkers()
    ai = CheckersAI(game)
    
    print("Welcome to Checkers vs AI!")
    print("You are Red (r, R), AI is Black (b, B)")
    
    while not game.game_over:
        if game.current_player == 1:  # Human player's turn
            os.system('cls' if os.name == 'nt' else 'clear')
            game.print_board()
            
            moves = game.get_all_valid_moves()
            if not moves:
                break
            
            try:
                move_input = input("\nEnter your move (row col to row col): ").strip()
                if 'to' in move_input:
                    parts = move_input.split('to')
                    from_part = parts[0].strip().split()
                    to_part = parts[1].strip().split()
                    
                    if len(from_part) == 2 and len(to_part) == 2:
                        from_row, from_col = int(from_part[0]), int(from_part[1])
                        to_row, to_col = int(to_part[0]), int(to_part[1])
                        
                        result = game.make_move((from_row, from_col), (to_row, to_col))
                        
                        if result == "continue":
                            print("Capture made! You get another turn.")
                        elif not result:
                            print("Invalid move! Try again.")
                            input("Press Enter to continue...")
                        else:
                            game.check_game_over()
                    else:
                        print("Invalid input format!")
                        input("Press Enter to continue...")
                else:
                    print("Please include 'to' in your move input")
                    input("Press Enter to continue...")
                    
            except (ValueError, IndexError):
                print("Invalid input! Please enter numbers for row and column.")
                input("Press Enter to continue...")
        
        else:  # AI's turn
            move = ai.get_move()
            if move:
                from_pos, to_pos = move
                print(f"\nAI moves: {from_pos} -> {to_pos}")
                result = game.make_move(from_pos, to_pos)
                if result == "continue":
                    print("AI made a capture and gets another turn!")
                game.check_game_over()
            else:
                break
            
            input("Press Enter to continue...")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    game.print_board()
    if game.winner:
        winner_name = "Red" if game.winner == 1 else "Black"
        print(f"\nGame over! {winner_name} wins!")
    else:
        print("\nGame ended!")

if __name__ == "__main__":
    # Choose game mode
    print("Choose game mode:")
    print("1. Two players")
    print("2. Play against AI")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        game = Checkers()
        game.play()
    elif choice == "2":
        play_against_ai()
    else:
        print("Invalid choice. Starting two-player game.")
        game = Checkers()
        game.play()