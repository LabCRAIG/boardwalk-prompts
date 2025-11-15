
class CheckersGame:
    def __init__(self):
        # Initialize the board: 0=empty, 1=black, 2=red, 3=black king, 4=red king
        self.board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]
        self.current_player = 1  # Black goes first
        self.black_pieces = 12
        self.red_pieces = 12
        self.selected_piece = None
        self.available_moves = []
        self.jump_available = False
        self.mandatory_piece = None

    def display_board(self):
        """Display the current board state."""
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(f"{i} ", end="")
            for cell in row:
                if cell == 0:
                    print("· ", end="")
                elif cell == 1:
                    print("b ", end="")
                elif cell == 2:
                    print("r ", end="")
                elif cell == 3:
                    print("B ", end="")
                elif cell == 4:
                    print("R ", end="")
            print()
        print()

    def is_valid_position(self, row, col):
        """Check if a position is within the board boundaries."""
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece_moves(self, row, col, check_jumps_only=False):
        """Get all valid moves for a piece at the given position."""
        moves = []
        jumps = []
        piece = self.board[row][col]
        
        # Check if the piece belongs to the current player
        if (piece == 1 or piece == 3) and self.current_player == 1:  # Black pieces
            piece_player = 1
        elif (piece == 2 or piece == 4) and self.current_player == 2:  # Red pieces
            piece_player = 2
        else:
            return []
        
        # Determine move directions based on piece type
        directions = []
        if piece == 1:  # Black regular
            directions = [(1, -1), (1, 1)]
        elif piece == 2:  # Red regular
            directions = [(-1, -1), (-1, 1)]
        elif piece == 3 or piece == 4:  # Kings
            directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        
        # Check for regular moves and jumps
        for dr, dc in directions:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col) and self.board[new_row][new_col] == 0:
                if not check_jumps_only:
                    moves.append(((row, col), (new_row, new_col)))
            
            # Jump move
            jump_row, jump_col = new_row + dr, new_col + dc
            if (self.is_valid_position(new_row, new_col) and 
                self.is_valid_position(jump_row, jump_col) and 
                self.board[jump_row][jump_col] == 0 and
                (self.board[new_row][new_col] in [3-piece_player, 4-piece_player+2])):
                jumps.append(((row, col), (jump_row, jump_col)))
        
        return jumps if jumps else moves if not check_jumps_only else []

    def get_all_possible_moves(self):
        """Get all possible moves for the current player."""
        all_moves = []
        all_jumps = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if ((piece == 1 or piece == 3) and self.current_player == 1) or \
                   ((piece == 2 or piece == 4) and self.current_player == 2):
                    jumps = self.get_piece_moves(row, col, check_jumps_only=True)
                    if jumps:
                        all_jumps.extend(jumps)
                    else:
                        all_moves.extend(self.get_piece_moves(row, col))
        
        # If jumps are available, they are mandatory
        return all_jumps if all_jumps else all_moves

    def make_move(self, start, end):
        """Move a piece from start to end position."""
        start_row, start_col = start
        end_row, end_col = end
        
        # Check if the move is a jump
        is_jump = abs(start_row - end_row) == 2
        
        # Move the piece
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        self.board[end_row][end_col] = piece
        
        # Check if it should be kinged
        if (piece == 1 and end_row == 7) or (piece == 2 and end_row == 0):
            self.board[end_row][end_col] = piece + 2  # Promote to king
        
        # Remove jumped piece if it's a jump
        if is_jump:
            middle_row, middle_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            jumped_piece = self.board[middle_row][middle_col]
            self.board[middle_row][middle_col] = 0
            
            # Update piece count
            if jumped_piece in [1, 3]:  # Black piece
                self.black_pieces -= 1
            else:  # Red piece
                self.red_pieces -= 1
            
            # Check for additional jumps
            additional_jumps = self.get_piece_moves(end_row, end_col, check_jumps_only=True)
            if additional_jumps:
                self.mandatory_piece = (end_row, end_col)
                return False  # Don't switch turn yet, additional jumps available
        
        # Switch turn
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        self.mandatory_piece = None
        return True

    def check_winner(self):
        """Check if there's a winner."""
        if self.black_pieces == 0:
            return 2  # Red wins
        if self.red_pieces == 0:
            return 1  # Black wins
        
        # Check if current player has no valid moves
        if not self.get_all_possible_moves():
            return 3 - self.current_player  # Opponent wins
        
        return 0  # No winner yet

    def play_game(self):
        """Main game loop."""
        print("Welcome to Checkers!")
        print("Enter moves as 'row_from col_from row_to col_to' (e.g., '2 1 3 0')")
        print("Black (b/B) moves first, then Red (r/R).")
        
        while True:
            self.display_board()
            
            winner = self.check_winner()
            if winner:
                if winner == 1:
                    print("Black wins!")
                else:
                    print("Red wins!")
                break
            
            print(f"{'Black' if self.current_player == 1 else 'Red'}'s turn")
            
            valid_moves = self.get_all_possible_moves()
            if not valid_moves:
                print(f"No valid moves for {'Black' if self.current_player == 1 else 'Red'}.")
                print(f"{'Red' if self.current_player == 1 else 'Black'} wins!")
                break
            
            # Check if there's a mandatory piece to move
            if self.mandatory_piece:
                print(f"You must continue jumping with piece at {self.mandatory_piece}")
                valid_moves = self.get_piece_moves(self.mandatory_piece[0], self.mandatory_piece[1], 
                                                check_jumps_only=True)
            
            # Get player input
            while True:
                try:
                    move_input = input("Enter your move: ")
                    if move_input.lower() == 'quit':
                        print("Thanks for playing!")
                        return
                    
                    coords = list(map(int, move_input.split()))
                    if len(coords) != 4:
                        print("Invalid input format. Please use 'row_from col_from row_to col_to'.")
                        continue
                    
                    start = (coords[0], coords[1])
                    end = (coords[2], coords[3])
                    move = (start, end)
                    
                    if move in valid_moves:
                        turn_complete = self.make_move(start, end)
                        if not turn_complete:
                            self.display_board()
                            print("Additional jump available!")
                        break
                    else:
                        print("Invalid move. Try again.")
                        
                except ValueError:
                    print("Invalid input. Please enter numbers.")
                except IndexError:
                    print("Invalid coordinates. Please enter values between 0 and 7.")


if __name__ == "__main__":
    game = CheckersGame()
    game.play_game()
