import sys

class AmethystGame:
    def __init__(self):
        # Initialize 8x8 board
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.current_player = 1  # Player 1 starts
        self.capture_in_progress = False
        self.capturing_piece_pos = None
        self.player1_pieces = set()  # Track player 1's pieces (A and Â)
        self.player2_pieces = set()  # Track player 2's pieces (O and Ô)
        
        # Set up initial board
        self.setup_board()
        
    def setup_board(self):
        # Initialize the board with alternating pieces as described in the rules
        # Player 1 pieces (A) at the bottom
        for row in range(5, 8):
            start_col = 0 if row % 2 == 0 else 1
            for col in range(start_col, 8, 2):
                self.board[row][col] = 'A'
                self.player1_pieces.add((row, col))
        
        # Player 2 pieces (O) at the top
        for row in range(0, 3):
            start_col = 0 if row % 2 == 0 else 1
            for col in range(start_col, 8, 2):
                self.board[row][col] = 'O'
                self.player2_pieces.add((row, col))
        
        # Set blank spaces in the middle rows
        for row in range(3, 5):
            start_col = 0 if row % 2 == 0 else 1
            for col in range(start_col, 8, 2):
                self.board[row][col] = '_'
                
    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(f"{i} {' '.join(row)}")
        print()
        
    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_blank_space(self, row, col):
        return self.is_valid_position(row, col) and self.board[row][col] == '_'
    
    def is_player_piece(self, row, col, player):
        if not self.is_valid_position(row, col):
            return False
        piece = self.board[row][col]
        if player == 1:
            return piece in {'A', 'Â'}
        else:  # player == 2
            return piece in {'O', 'Ô'}
    
    def is_opponent_piece(self, row, col, player):
        if not self.is_valid_position(row, col):
            return False
        piece = self.board[row][col]
        if player == 1:
            return piece in {'O', 'Ô'}
        else:  # player == 2
            return piece in {'A', 'Â'}
    
    def get_valid_moves(self, row, col):
        moves = []
        if not self.is_valid_position(row, col):
            return moves
        
        piece = self.board[row][col]
        player = 1 if piece in {'A', 'Â'} else 2
        
        # Regular moves (1 step diagonally)
        directions = []
        if piece in {'A', 'Â', 'Ô'}:  # These pieces can move up
            directions.extend([(-1, -1), (-1, 1)])
        if piece in {'O', 'Â', 'Ô'}:  # These pieces can move down
            directions.extend([(1, -1), (1, 1)])
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_blank_space(new_row, new_col):
                moves.append((new_row, new_col, False))  # False indicates not a capture
        
        # Captures (2 steps diagonally, jumping over opponent)
        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            if self.is_opponent_piece(mid_row, mid_col, player):
                end_row, end_col = mid_row + dr, mid_col + dc
                if self.is_blank_space(end_row, end_col):
                    moves.append((end_row, end_col, True))  # True indicates a capture
        
        return moves
    
    def get_all_valid_moves(self, player):
        all_moves = {}
        pieces = self.player1_pieces if player == 1 else self.player2_pieces
        
        for row, col in pieces:
            moves = self.get_valid_moves(row, col)
            if moves:
                all_moves[(row, col)] = moves
                
        return all_moves
    
    def get_all_capture_moves(self, player):
        all_captures = {}
        all_moves = self.get_all_valid_moves(player)
        
        for piece_pos, moves in all_moves.items():
            capture_moves = [move for move in moves if move[2]]  # Filter captures
            if capture_moves:
                all_captures[piece_pos] = capture_moves
                
        return all_captures
    
    def execute_move(self, start_row, start_col, end_row, end_col, is_capture):
        piece = self.board[start_row][start_col]
        player = 1 if piece in {'A', 'Â'} else 2
        
        # Remove piece from old position
        self.board[start_row][start_col] = '_'
        if player == 1:
            self.player1_pieces.remove((start_row, start_col))
        else:
            self.player2_pieces.remove((start_row, start_col))
        
        # Handle capture if applicable
        if is_capture:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            
            # Remove captured piece
            self.board[mid_row][mid_col] = '_'
            if captured_piece in {'A', 'Â'}:
                self.player1_pieces.remove((mid_row, mid_col))
            else:
                self.player2_pieces.remove((mid_row, mid_col))
        
        # Promote pieces if they reach the opposite end
        if piece == 'A' and end_row == 0:
            piece = 'Â'  # Promote A to Â
        elif piece == 'O' and end_row == 7:
            piece = 'Ô'  # Promote O to Ô
        
        # Place piece in new position
        self.board[end_row][end_col] = piece
        if player == 1:
            self.player1_pieces.add((end_row, end_col))
        else:
            self.player2_pieces.add((end_row, end_col))
        
        # Check for additional captures
        additional_captures = False
        if is_capture:
            moves = self.get_valid_moves(end_row, end_col)
            capture_moves = [move for move in moves if move[2]]
            if capture_moves:
                additional_captures = True
                self.capture_in_progress = True
                self.capturing_piece_pos = (end_row, end_col)
            else:
                self.capture_in_progress = False
                self.capturing_piece_pos = None
                self.current_player = 3 - self.current_player  # Switch players
        else:
            self.current_player = 3 - self.current_player  # Switch players
        
        return additional_captures
    
    def check_game_over(self):
        # Check if any player has no pieces left
        if not self.player1_pieces:
            return 2  # Player 2 wins
        if not self.player2_pieces:
            return 1  # Player 1 wins
        
        # Check if current player has no valid moves
        all_moves = self.get_all_valid_moves(self.current_player)
        if not all_moves:
            return 3 - self.current_player  # Other player wins
        
        return 0  # Game not over
    
    def play_game(self):
        game_over = False
        winner = 0
        
        print("Welcome to Amethyst!")
        print("Player 1: A, Â (move upward)")
        print("Player 2: O, Ô (move downward)")
        print("Â and Ô can move both up and down")
        
        while not game_over:
            self.print_board()
            
            # Check if game is over
            winner = self.check_game_over()
            if winner != 0:
                game_over = True
                break
            
            # Handle forced captures
            if self.capture_in_progress:
                print(f"Player {self.current_player} must continue capturing with piece at "
                      f"{self.capturing_piece_pos[0]}, {self.capturing_piece_pos[1]}")
                row, col = self.capturing_piece_pos
                moves = self.get_valid_moves(row, col)
                capture_moves = [move for move in moves if move[2]]
                
                print("Available capture moves:")
                for i, (r, c, _) in enumerate(capture_moves):
                    print(f"{i+1}: {r}, {c}")
                
                choice = int(input("Choose a move (enter the number): ")) - 1
                while choice < 0 or choice >= len(capture_moves):
                    choice = int(input("Invalid choice. Try again: ")) - 1
                
                end_row, end_col, is_capture = capture_moves[choice]
                additional_captures = self.execute_move(row, col, end_row, end_col, is_capture)
                
                if not additional_captures:
                    print(f"Player {3 - self.current_player}'s turn")
            else:
                # Regular turn
                print(f"Player {self.current_player}'s turn")
                
                # Check for forced captures
                capture_moves = self.get_all_capture_moves(self.current_player)
                if capture_moves:
                    print("You must make a capture.")
                    
                    # List pieces that can capture
                    print("Pieces that can capture:")
                    piece_positions = list(capture_moves.keys())
                    for i, (r, c) in enumerate(piece_positions):
                        print(f"{i+1}: {r}, {c} ({self.board[r][c]})")
                    
                    piece_choice = int(input("Choose a piece (enter the number): ")) - 1
                    while piece_choice < 0 or piece_choice >= len(piece_positions):
                        piece_choice = int(input("Invalid choice. Try again: ")) - 1
                    
                    row, col = piece_positions[piece_choice]
                    
                    # List capture moves for chosen piece
                    moves = capture_moves[(row, col)]
                    print("Available capture moves:")
                    for i, (r, c, _) in enumerate(moves):
                        print(f"{i+1}: {r}, {c}")
                    
                    move_choice = int(input("Choose a move (enter the number): ")) - 1
                    while move_choice < 0 or move_choice >= len(moves):
                        move_choice = int(input("Invalid choice. Try again: ")) - 1
                    
                    end_row, end_col, is_capture = moves[move_choice]
                    self.execute_move(row, col, end_row, end_col, is_capture)
                else:
                    # Regular moves
                    all_moves = self.get_all_valid_moves(self.current_player)
                    
                    # List pieces that can move
                    print("Pieces that can move:")
                    piece_positions = list(all_moves.keys())
                    for i, (r, c) in enumerate(piece_positions):
                        print(f"{i+1}: {r}, {c} ({self.board[r][c]})")
                    
                    piece_choice = int(input("Choose a piece (enter the number): ")) - 1
                    while piece_choice < 0 or piece_choice >= len(piece_positions):
                        piece_choice = int(input("Invalid choice. Try again: ")) - 1
                    
                    row, col = piece_positions[piece_choice]
                    
                    # List moves for chosen piece
                    moves = all_moves[(row, col)]
                    print("Available moves:")
                    for i, (r, c, is_cap) in enumerate(moves):
                        move_type = "capture" if is_cap else "move"
                        print(f"{i+1}: {r}, {c} ({move_type})")
                    
                    move_choice = int(input("Choose a move (enter the number): ")) - 1
                    while move_choice < 0 or move_choice >= len(moves):
                        move_choice = int(input("Invalid choice. Try again: ")) - 1
                    
                    end_row, end_col, is_capture = moves[move_choice]
                    self.execute_move(row, col, end_row, end_col, is_capture)
        
        # Game over
        self.print_board()
        print(f"Game over! Player {winner} wins!")

if __name__ == "__main__":
    game = AmethystGame()
    game.play_game()