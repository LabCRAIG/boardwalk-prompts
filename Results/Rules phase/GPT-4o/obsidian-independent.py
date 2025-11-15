class ObsidianGame:
    def __init__(self):
        # Initial board setup
        self.board = [
            ["A", "B", "C", "D", "E", "C", "B", "A"],
            ["F", "F", "F", "F", "F", "F", "F", "F"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["f", "f", "f", "f", "f", "f", "f", "f"],
            ["a", "b", "c", "d", "e", "c", "b", "a"],
        ]
        self.current_player = 1  # Player 1 starts
        self.has_moved = set()  # Tracks pieces that have moved (for F and f)

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def is_within_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def is_enemy_piece(self, x, y, player):
        piece = self.board[x][y]
        if player == 1:
            return piece.isupper()
        else:
            return piece.islower()

    def is_ally_piece(self, x, y, player):
        piece = self.board[x][y]
        if player == 1:
            return piece.islower()
        else:
            return piece.isupper()

    def is_empty(self, x, y):
        return self.board[x][y] == "."

    def move_piece(self, start_x, start_y, end_x, end_y):
        piece = self.board[start_x][start_y]
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = "."
        # Handle promotion
        if piece == "f" and end_x == 0:
            self.board[end_x][end_y] = "e"
        elif piece == "F" and end_x == 7:
            self.board[end_x][end_y] = "E"
        # Mark piece as having moved (relevant for f/F)
        if piece in {"f", "F"}:
            self.has_moved.add((end_x, end_y))

    def get_valid_moves(self, x, y):
        piece = self.board[x][y]
        player = 1 if piece.islower() else 2
        valid_moves = []

        if piece.lower() == "f":
            direction = -1 if player == 1 else 1
            start_pos = (x, y) not in self.has_moved
            # Normal move
            if self.is_within_bounds(x + direction, y) and self.is_empty(x + direction, y):
                valid_moves.append((x + direction, y))
            # Double move (only if not moved)
            if start_pos and self.is_within_bounds(x + 2 * direction, y) and self.is_empty(x + direction, y) and self.is_empty(x + 2 * direction, y):
                valid_moves.append((x + 2 * direction, y))
            # Captures
            for dy in [-1, 1]:
                if self.is_within_bounds(x + direction, y + dy) and self.is_enemy_piece(x + direction, y + dy, player):
                    valid_moves.append((x + direction, y + dy))

        elif piece.lower() == "a":
            # Orthogonal moves
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                while self.is_within_bounds(nx, ny) and self.is_empty(nx, ny):
                    valid_moves.append((nx, ny))
                    nx, ny += dx, dy
                if self.is_within_bounds(nx, ny) and self.is_enemy_piece(nx, ny, player):
                    valid_moves.append((nx, ny))

        elif piece.lower() == "c":
            # Diagonal moves
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                while self.is_within_bounds(nx, ny) and self.is_empty(nx, ny):
                    valid_moves.append((nx, ny))
                    nx, ny += dx, dy
                if self.is_within_bounds(nx, ny) and self.is_enemy_piece(nx, ny, player):
                    valid_moves.append((nx, ny))

        elif piece.lower() == "b":
            # Knight-like moves (2 in one direction, 1 in the other)
            for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                nx, ny = x + dx, y + dy
                if self.is_within_bounds(nx, ny) and (self.is_empty(nx, ny) or self.is_enemy_piece(nx, ny, player)):
                    valid_moves.append((nx, ny))

        elif piece.lower() == "e":
            # Queen-like moves (orthogonal and diagonal)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                while self.is_within_bounds(nx, ny) and self.is_empty(nx, ny):
                    valid_moves.append((nx, ny))
                    nx, ny += dx, dy
                if self.is_within_bounds(nx, ny) and self.is_enemy_piece(nx, ny, player):
                    valid_moves.append((nx, ny))

        elif piece.lower() == "d":
            # King-like moves (one space in any direction)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                if self.is_within_bounds(nx, ny) and (self.is_empty(nx, ny) or self.is_enemy_piece(nx, ny, player)):
                    valid_moves.append((nx, ny))

        return valid_moves

    def check_win(self):
        # Check if D or d is captured
        d_exists = any("d" in row for row in self.board)
        D_exists = any("D" in row for row in self.board)
        if not d_exists:
            return 2  # Player 2 wins
        if not D_exists:
            return 1  # Player 1 wins
        return 0  # No winner yet

    def play_turn(self, start_x, start_y, end_x, end_y):
        if self.is_within_bounds(start_x, start_y) and self.is_within_bounds(end_x, end_y):
            piece = self.board[start_x][start_y]
            if (self.current_player == 1 and piece.islower()) or (self.current_player == 2 and piece.isupper()):
                valid_moves = self.get_valid_moves(start_x, start_y)
                if (end_x, end_y) in valid_moves:
                    self.move_piece(start_x, start_y, end_x, end_y)
                    winner = self.check_win()
                    if winner:
                        print(f"Player {winner} wins!")
                        return True
                    self.current_player = 3 - self.current_player  # Switch player
                    return False
        print("Invalid move. Try again.")
        return False


# Game loop
game = ObsidianGame()
game.display_board()

while True:
    print(f"Player {game.current_player}'s turn")
    start_pos = input("Enter the starting position (e.g., 6 0): ")
    end_pos = input("Enter the ending position (e.g., 4 0): ")
    start_x, start_y = map(int, start_pos.split())
    end_x, end_y = map(int, end_pos.split())
    if game.play_turn(start_x, start_y, end_x, end_y):
        break
    game.display_board()