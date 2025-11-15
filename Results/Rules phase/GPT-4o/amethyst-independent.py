class AmethystGame:
    def __init__(self):
        self.board = [
            ['_', 'O', '_', 'O', '_', 'O', '_', 'O'],
            ['O', '_', 'O', '_', 'O', '_', 'O', '_'],
            ['_', 'O', '_', 'O', '_', 'O', '_', 'O'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['A', '_', 'A', '_', 'A', '_', 'A', '_'],
            ['_', 'A', '_', 'A', '_', 'A', '_', 'A'],
            ['A', '_', 'A', '_', 'A', '_', 'A', '_']
        ]
        self.current_player = 1  # Player 1 starts
        self.pieces = {1: ['A', 'Â'], 2: ['O', 'Ô']}
        self.directions = {
            'A': [(-1, -1), (-1, 1)],
            'O': [(1, -1), (1, 1)],
            'Â': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'Ô': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        }
    
    def print_board(self):
        print("  " + " ".join(str(i) for i in range(8)))  # Column indices
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()

    def is_in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if piece not in self.pieces[self.current_player]:
            return []

        moves = []
        for dr, dc in self.directions[piece]:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if self.is_in_bounds(new_row, new_col) and self.board[new_row][new_col] == '_':
                moves.append((new_row, new_col))
            
            # Capture move
            capture_row, capture_col = row + 2 * dr, col + 2 * dc
            middle_row, middle_col = row + dr, col + dc
            if (
                self.is_in_bounds(capture_row, capture_col) and
                self.board[capture_row][capture_col] == '_' and
                self.board[middle_row][middle_col] in self.pieces[3 - self.current_player]
            ):
                moves.append((capture_row, capture_col))
        
        return moves

    def make_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = '_'
        self.board[end_row][end_col] = piece

        # Check if a capture was made
        if abs(end_row - start_row) == 2:
            capture_row, capture_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            self.board[capture_row][capture_col] = '_'

        # Check for promotion
        if piece == 'A' and end_row == 0:
            self.board[end_row][end_col] = 'Â'
        elif piece == 'O' and end_row == 7:
            self.board[end_row][end_col] = 'Ô'

    def has_valid_moves(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] in self.pieces[self.current_player]:
                    if self.get_valid_moves(row, col):
                        return True
        return False

    def play(self):
        while True:
            self.print_board()
            if not self.has_valid_moves():
                print(f"Player {3 - self.current_player} wins! Player {self.current_player} has no valid moves.")
                break

            print(f"Player {self.current_player}'s turn.")
            try:
                start_row, start_col = map(int, input("Enter the piece to move (row col): ").split())
                end_row, end_col = map(int, input("Enter the target position (row col): ").split())

                if (
                    self.is_in_bounds(start_row, start_col) and
                    self.is_in_bounds(end_row, end_col) and
                    self.board[start_row][start_col] in self.pieces[self.current_player] and
                    (end_row, end_col) in self.get_valid_moves(start_row, start_col)
                ):
                    self.make_move(start_row, start_col, end_row, end_col)

                    # Check if another capture is possible
                    while abs(end_row - start_row) == 2:  # A capture was made
                        start_row, start_col = end_row, end_col
                        valid_moves = self.get_valid_moves(start_row, start_col)
                        capture_moves = [
                            move for move in valid_moves if abs(move[0] - start_row) == 2
                        ]
                        if capture_moves:
                            self.print_board()
                            print(f"Player {self.current_player} must continue capturing.")
                            end_row, end_col = map(int, input("Enter the target position (row col): ").split())
                            if (end_row, end_col) in capture_moves:
                                self.make_move(start_row, start_col, end_row, end_col)
                            else:
                                print("Invalid move. Try again.")
                                break
                        else:
                            break

                    # Switch turn if no more captures are possible
                    self.current_player = 3 - self.current_player
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter row and column as numbers.")

game = AmethystGame()
game.play()