
import numpy as np

class Checkers:
    def __init__(self):
        # 0 = empty, 1 = player 1 piece, 2 = player 2 piece
        # 3 = player 1 king, 4 = player 2 king
        self.board = np.zeros((8, 8), dtype=int)
        self.current_player = 1
        self.initialize_board()
        
    def initialize_board(self):
        # Player 1 pieces (bottom rows)
        for row in range(6, 8):
            for col in range(8):
                self.board[row][col] = 1
                
        # Player 2 pieces (top rows)
        for row in range(0, 2):
            for col in range(8):
                self.board[row][col] = 2
    
    def print_board(self):
        symbols = {0: '.', 1: 'o', 2: 'x', 3: 'O', 4: 'X'}
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row_str = f"{i} "
            for j in range(8):
                row_str += symbols[self.board[i][j]] + " "
            print(row_str)
        print()
    
    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if piece == 0 or (piece == 1 and self.current_player == 2) or (piece == 2 and self.current_player == 1):
            return []
        
        moves = []
        jumps = []
        
        # Define directions based on piece type
        directions = []
        if piece == 1:  # Player 1 regular piece (moves up)
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:  # Player 2 regular piece (moves down)
            directions = [(1, -1), (1, 1)]
        elif piece in [3, 4]:  # Kings (move any direction)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Check each direction for moves and jumps
        for dr, dc in directions:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] == 0:
                moves.append((new_row, new_col))
                
            # Jump move
            jump_row, jump_col = row + 2*dr, col + 2*dc
            if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board[jump_row][jump_col] == 0:
                captured_row, captured_col = row + dr, col + dc
                captured = self.board[captured_row][captured_col]
                
                # Check if there's an opponent's piece to capture
                if (piece in [1, 3] and captured in [2, 4]) or (piece in [2, 4] and captured in [1, 3]):
                    jumps.append((jump_row, jump_col))
        
        # Prioritize jumps if available
        return jumps if jumps else moves
    
    def get_all_valid_moves(self):
        all_moves = {}
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (piece == 1 or piece == 3) and self.current_player == 1:
                    moves = self.get_valid_moves(row, col)
                    if moves:
                        all_moves[(row, col)] = moves
                elif (piece == 2 or piece == 4) and self.current_player == 2:
                    moves = self.get_valid_moves(row, col)
                    if moves:
                        all_moves[(row, col)] = moves
        return all_moves
    
    def make_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Move the piece
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = 0
        self.board[to_row][to_col] = piece
        
        # Check if it was a jump (capture)
        if abs(from_row - to_row) == 2:
            captured_row = (from_row + to_row) // 2
            captured_col = (from_col + to_col) // 2
            self.board[captured_row][captured_col] = 0
            
            # Check for additional jumps
            additional_jumps = self.get_valid_moves(to_row, to_col)
            # Only consider jumps, not regular moves
            additional_jumps = [move for move in additional_jumps if abs(move[0] - to_row) == 2]
            if additional_jumps:
                return False  # Player must continue jumping
        
        # Check for promotion to king
        if piece == 1 and to_row == 0:  # Player 1 piece reaches top row
            self.board[to_row][to_col] = 3  # Promote to king
        elif piece == 2 and to_row == 7:  # Player 2 piece reaches bottom row
            self.board[to_row][to_col] = 4  # Promote to king
            
        # Switch players
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        return True
    
    def is_game_over(self):
        # Check if a player has no pieces left or no valid moves
        player1_pieces = np.isin(self.board, [1, 3]).any()
        player2_pieces = np.isin(self.board, [2, 4]).any()
        
        if not player1_pieces:
            return True, "Player 2 wins!"
        if not player2_pieces:
            return True, "Player 1 wins!"
        
        # Check if current player has no valid moves
        all_moves = self.get_all_valid_moves()
        if not all_moves:
            return True, f"Player {3 - self.current_player} wins! Player {self.current_player} has no valid moves."
        
        return False, ""


def play_game():
    game = Checkers()
    game_over, message = False, ""
    
    while not game_over:
        game.print_board()
        print(f"Player {game.current_player}'s turn")
        
        all_valid_moves = game.get_all_valid_moves()
        if not all_valid_moves:
            print(f"Player {game.current_player} has no valid moves!")
            game_over = True
            continue
        
        # Display available pieces to move
        print("Pieces that can move:")
        for i, (row, col) in enumerate(all_valid_moves.keys()):
            print(f"{i+1}: ({row}, {col})")
        
        # Get piece selection
        valid_selection = False
        while not valid_selection:
            try:
                choice = int(input("Select a piece to move (number): ")) - 1
                if 0 <= choice < len(all_valid_moves):
                    from_pos = list(all_valid_moves.keys())[choice]
                    valid_selection = True
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Display available moves
        moves = all_valid_moves[from_pos]
        print(f"Available moves for piece at {from_pos}:")
        for i, move in enumerate(moves):
            print(f"{i+1}: {move}")
        
        # Get move selection
        valid_move = False
        while not valid_move:
            try:
                move_choice = int(input("Select a move (number): ")) - 1
                if 0 <= move_choice < len(moves):
                    to_pos = moves[move_choice]
                    valid_move = True
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Make the move
        turn_complete = game.make_move(from_pos, to_pos)
        
        # Check for multi-jumps
        current_pos = to_pos
        while not turn_complete:
            game.print_board()
            print(f"Player {game.current_player} must continue jumping with piece at {current_pos}")
            
            additional_jumps = game.get_valid_moves(*current_pos)
            # Filter for only jumps
            additional_jumps = [move for move in additional_jumps if abs(move[0] - current_pos[0]) == 2]
            
            for i, move in enumerate(additional_jumps):
                print(f"{i+1}: {move}")
            
            valid_jump = False
            while not valid_jump:
                try:
                    jump_choice = int(input("Select your next jump (number): ")) - 1
                    if 0 <= jump_choice < len(additional_jumps):
                        to_pos = additional_jumps[jump_choice]
                        valid_jump = True
                    else:
                        print("Invalid selection. Try again.")
                except ValueError:
                    print("Please enter a number.")
            
            turn_complete = game.make_move(current_pos, to_pos)
            current_pos = to_pos
            
        # Check if game is over
        game_over, message = game.is_game_over()
    
    game.print_board()
    print(message)


if __name__ == "__main__":
    play_game()
