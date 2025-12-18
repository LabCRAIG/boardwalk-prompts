class TopazGame:
    def __init__(self):
        # Initialize the board with null spaces (whitespace) and free spaces (_)
        self.board = [
            [' ', ' ', '_', ' ', ' ', '_', ' ', ' ', '_'],
            [' ', '_', ' ', '_', ' ', '_', ' '],
            [' ', ' ', '_', '_', '_', ' ', ' '],
            ['_', '_', '_', ' ', '_', '_', '_'],
            [' ', ' ', '_', '_', '_', ' ', ' '],
            [' ', '_', ' ', '_', ' ', '_', ' '],
            [' ', ' ', '_', ' ', ' ', '_', ' ', ' ', '_']
        ]
        self.players = ['A', 'B']
        self.current_player = 0  # Player 1 (A) starts
        self.phase = 'placement'  # 'placement' or 'movement'
        self.pieces_placed = {'A': 0, 'B': 0}
        self.total_pieces = 9  # per player

    def print_board(self):
        """Print the board with row and column indices for clarity."""
        print("   " + " ".join(str(i) for i in range(7)))
        for i, row in enumerate(self.board):
            print(f"{i}  " + " ".join(cell if cell != ' ' else ' ' for cell in row))

    def is_valid_position(self, row, col):
        """Check if (row, col) is a valid position on the board (not null)."""
        if row < 0 or row >= 7 or col < 0 or col >= len(self.board[row]):
            return False
        return self.board[row][col] != ' '  # Not a null space

    def is_free_space(self, row, col):
        """Check if (row, col) is a free space (underscore)."""
        if not self.is_valid_position(row, col):
            return False
        return self.board[row][col] == '_'

    def get_adjacent_spaces(self, row, col):
        """Return list of adjacent free spaces (orthogonal only)."""
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_free_space(new_row, new_col):
                adjacent.append((new_row, new_col))
        return adjacent

    def place_piece(self, row, col):
        """Place a piece during the placement phase."""
        if self.phase != 'placement':
            return False, "Not in placement phase"
        if not self.is_free_space(row, col):
            return False, "Invalid position"
        
        player = self.players[self.current_player]
        self.board[row][col] = player
        self.pieces_placed[player] += 1

        # Check if all pieces are placed
        if all(placed == self.total_pieces for placed in self.pieces_placed.values()):
            self.phase = 'movement'

        # Check for captures
        capture_possible = self.check_capture(row, col)
        self.switch_player()
        return True, "Placement successful" + (" (Capture possible!)" if capture_possible else "")

    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece during the movement phase."""
        if self.phase != 'movement':
            return False, "Not in movement phase"
        player = self.players[self.current_player]
        if self.board[from_row][from_col] != player:
            return False, "Not your piece"
        if (to_row, to_col) not in self.get_adjacent_spaces(from_row, from_col):
            return False, "Invalid move"

        # Perform the move
        self.board[from_row][from_col] = '_'
        self.board[to_row][to_col] = player

        # Check for captures
        capture_possible = self.check_capture(to_row, to_col)
        self.switch_player()
        return True, "Move successful" + (" (Capture possible!)" if capture_possible else "")

    def check_capture(self, row, col):
        """Check if the last action created a 3-in-a-row/column. Returns True if capture possible."""
        player = self.players[self.current_player]
        directions = [
            [(0, -1), (0, 1)],  # Horizontal
            [(-1, 0), (1, 0)]    # Vertical
        ]

        for axis in directions:
            count = 1  # The current piece
            for dr, dc in axis[0]:  # Check one direction
                r, c = row + dr, col + dc
                while self.is_valid_position(r, c) and self.board[r][c] == player:
                    count += 1
                    r += dr
                    c += dc
            for dr, dc in axis[1]:  # Check the opposite direction
                r, c = row + dr, col + dc
                while self.is_valid_position(r, c) and self.board[r][c] == player:
                    count += 1
                    r += dr
                    c += dc
            if count >= 3:
                return True
        return False

    def perform_capture(self, row, col):
        """Remove an opponent's piece after a capture condition is met."""
        opponent = self.players[1 - self.current_player]
        if not self.is_valid_position(row, col) or self.board[row][col] != opponent:
            return False, "Invalid capture target"
        
        self.board[row][col] = '_'
        return True, "Capture successful"

    def switch_player(self):
        """Switch to the other player's turn."""
        self.current_player = 1 - self.current_player

    def check_win_condition(self):
        """Check if the current player has won (only during movement phase)."""
        if self.phase != 'movement':
            return None
        
        opponent = self.players[1 - self.current_player]
        opponent_pieces = sum(row.count(opponent) for row in self.board)
        
        # Win if opponent has <= 2 pieces
        if opponent_pieces <= 2:
            return f"Player {self.players[self.current_player]} wins! Opponent has ≤2 pieces."
        
        # Win if opponent cannot move
        can_move = False
        for r in range(7):
            for c in range(len(self.board[r])):
                if self.board[r][c] == opponent:
                    if self.get_adjacent_spaces(r, c):
                        can_move = True
                        break
            if can_move:
                break
        if not can_move:
            return f"Player {self.players[self.current_player]} wins! Opponent cannot move."
        
        return None

    def play(self):
        """Main game loop for CLI play."""
        print("Welcome to Topaz!")
        while True:
            self.print_board()
            player = self.players[self.current_player]
            print(f"\nPlayer {player}'s turn ({self.phase} phase)")

            if self.phase == 'placement':
                try:
                    row, col = map(int, input("Enter row and column to place (e.g., '2 3'): ").split())
                    success, msg = self.place_piece(row, col)
                    print(msg)
                except ValueError:
                    print("Invalid input. Try again.")
            else:  # movement phase
                try:
                    from_row, from_col = map(int, input("Move from (row col): ").split())
                    to_row, to_col = map(int, input("Move to (row col): ").split())
                    success, msg = self.move_piece(from_row, from_col, to_row, to_col)
                    print(msg)
                except ValueError:
                    print("Invalid input. Try again.")

            # Check for captures
            if success and "Capture possible!" in msg:
                self.print_board()
                try:
                    cap_row, cap_col = map(int, input(f"Player {player}, capture opponent's piece (row col): ").split())
                    cap_success, cap_msg = self.perform_capture(cap_row, cap_col)
                    print(cap_msg)
                except ValueError:
                    print("Invalid capture. Skipping.")

            # Check win condition
            result = self.check_win_condition()
            if result:
                self.print_board()
                print(result)
                break

if __name__ == "__main__":
    game = TopazGame()
    game.play()