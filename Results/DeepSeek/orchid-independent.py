class OrchidGame:
    def __init__(self):
        self.board_size = 5
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pieces = {'A': 12, 'B': 12}
        self.current_player = 'A'
        self.phase = 1  # 1: placement phase, 2: movement phase
        self.game_over = False
        
    def print_board(self):
        print("   " + " ".join(str(i) for i in range(self.board_size)))
        for i, row in enumerate(self.board):
            print(f"{i}  " + " ".join(row))
        print()
    
    def is_valid_placement(self, row, col):
        # Check if placement is valid during phase 1
        if self.phase != 1:
            return False
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        if self.board[row][col] != '.':
            return False
        # Center is forbidden
        if row == 2 and col == 2:
            return False
        return True
    
    def place_piece(self, row, col):
        if not self.is_valid_placement(row, col):
            return False
        
        self.board[row][col] = self.current_player
        self.pieces[self.current_player] -= 1
        
        # Check if we should switch to phase 2
        if all(count == 0 for count in self.pieces.values()):
            self.phase = 2
        
        return True
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        if self.phase != 2:
            return False
        if not (0 <= from_row < self.board_size and 0 <= from_col < self.board_size):
            return False
        if not (0 <= to_row < self.board_size and 0 <= to_col < self.board_size):
            return False
        if self.board[from_row][from_col] != self.current_player:
            return False
        if self.board[to_row][to_col] != '.':
            return False
        
        # Check orthogonal movement
        if from_row != to_row and from_col != to_col:
            return False
        
        # Check path is clear
        if from_row == to_row:  # Horizontal move
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if self.board[from_row][col] != '.':
                    return False
        else:  # Vertical move
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if self.board[row][from_col] != '.':
                    return False
        
        return True
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        # Move the piece
        self.board[from_row][from_col] = '.'
        self.board[to_row][to_col] = self.current_player
        
        # Check for captures
        self.check_captures(to_row, to_col)
        
        return True
    
    def check_captures(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        opponent = 'B' if self.current_player == 'A' else 'A'
        captured = False
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_capture = []
            
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] == opponent:
                    to_capture.append((r, c))
                    r += dr
                    c += dc
                elif self.board[r][c] == self.current_player:
                    # Capture all pieces in to_capture
                    for cap_r, cap_c in to_capture:
                        self.board[cap_r][cap_c] = '.'
                        captured = True
                    break
                else:
                    break
        
        return captured
    
    def switch_player(self):
        self.current_player = 'B' if self.current_player == 'A' else 'A'
    
    def check_win_condition(self):
        a_count = sum(row.count('A') for row in self.board)
        b_count = sum(row.count('B') for row in self.board)
        
        if a_count == 0:
            return 'B'
        if b_count == 0:
            return 'A'
        return None
    
    def has_valid_moves(self):
        if self.phase == 1:
            return True  # In placement phase, always can place (if pieces left)
        
        # Check if current player has any valid moves in movement phase
        for from_row in range(self.board_size):
            for from_col in range(self.board_size):
                if self.board[from_row][from_col] == self.current_player:
                    # Check all possible orthogonal moves
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    for dr, dc in directions:
                        distance = 1
                        while True:
                            to_row, to_col = from_row + dr * distance, from_col + dc * distance
                            if not (0 <= to_row < self.board_size and 0 <= to_col < self.board_size):
                                break
                            if self.board[to_row][to_col] != '.':
                                break
                            return True  # Found at least one valid move
                            distance += 1
        return False
    
    def play(self):
        print("Welcome to Orchid!")
        print("Player 1: A")
        print("Player 2: B")
        print("Phase 1: Placement phase - place two pieces per turn (except center)")
        print("Phase 2: Movement phase - move one piece orthogonally to capture opponent's pieces")
        print()
        
        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            
            if self.phase == 1:
                pieces_left = self.pieces[self.current_player]
                if pieces_left == 0:
                    print("No pieces left to place. Switching to next player.")
                    self.switch_player()
                    continue
                
                print(f"Pieces left: {pieces_left}")
                placements = 2 if pieces_left >= 2 else 1
                
                for i in range(placements):
                    while True:
                        try:
                            print(f"Placement {i+1} of {placements}")
                            row = int(input("Enter row (0-4): "))
                            col = int(input("Enter column (0-4): "))
                            if self.place_piece(row, col):
                                break
                            else:
                                print("Invalid placement. Try again.")
                        except ValueError:
                            print("Please enter numbers only.")
                
                # Check if all pieces are placed
                if all(count == 0 for count in self.pieces.values()):
                    print("\nAll pieces placed. Switching to movement phase.\n")
                    self.phase = 2
                
                self.switch_player()
            
            else:  # Phase 2
                if not self.has_valid_moves():
                    print(f"Player {self.current_player} has no valid moves and must pass.")
                    self.switch_player()
                    continue
                
                while True:
                    try:
                        print("Enter move from:")
                        from_row = int(input("  Row (0-4): "))
                        from_col = int(input("  Column (0-4): "))
                        print("Enter move to:")
                        to_row = int(input("  Row (0-4): "))
                        to_col = int(input("  Column (0-4): "))
                        
                        if self.move_piece(from_row, from_col, to_row, to_col):
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Please enter numbers only.")
                
                winner = self.check_win_condition()
                if winner:
                    self.game_over = True
                    self.print_board()
                    print(f"Player {winner} wins!")
                    break
                
                self.switch_player()


if __name__ == "__main__":
    game = OrchidGame()
    game.play()
