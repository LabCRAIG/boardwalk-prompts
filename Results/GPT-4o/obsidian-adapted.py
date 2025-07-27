from game import Game, Board, is_placement, is_movement, get_move_elements

class Obsidian(Game):
    def __init__(self, board):
        super().__init__(board)
        self.has_moved = set()  # Tracks pieces that have moved (for F and f)

    def initial_player(self):
        return 1  # Player 1 starts
    
    def next_player(self):
        return 3 - self.current_player  # Switch player
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        # Parse move
        if is_movement(move):
            (start, end) = get_move_elements(move)
            start_x, start_y = start
            end_x, end_y = end
            piece = self.board.layout[start_x][start_y]

            # Ensure the piece belongs to the current player
            if (self.current_player == 1 and not piece.islower()) or (self.current_player == 2 and not piece.isupper()):
                return False
            
            # Get valid moves for the piece
            valid_moves = self.get_valid_moves(start_x, start_y)
            return (end_x, end_y) in valid_moves
        return False

    def perform_move(self, move):
        if is_movement(move):
            (start, end) = get_move_elements(move)
            start_x, start_y = start
            end_x, end_y = end
            piece = self.board.layout[start_x][start_y]
            
            # Update the board
            self.board.move_piece(move)

            # Handle promotion
            if piece == "f" and end_x == 0:
                self.board.place_piece(f"e {end_x},{end_y}")
            elif piece == "F" and end_x == 7:
                self.board.place_piece(f"E {end_x},{end_y}")

            # Mark piece as having moved
            if piece in {"f", "F"}:
                self.has_moved.add((end_x, end_y))

    def game_finished(self):
        # Check if D or d is captured
        d_exists = any("d" in row for row in self.board.layout)
        D_exists = any("D" in row for row in self.board.layout)
        return not d_exists or not D_exists

    def get_winner(self):
        d_exists = any("d" in row for row in self.board.layout)
        D_exists = any("D" in row for row in self.board.layout)
        if not d_exists:
            return 2  # Player 2 wins
        if not D_exists:
            return 1  # Player 1 wins
        return None  # No winner yet

    def get_valid_moves(self, x, y):
        piece = self.board.layout[x][y]
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

if __name__ == '__main__':
    # Define the initial board layout
    layout = (
        "ABCDECBA\n"
        "FFFFFFFF\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "ffffffff\n"
        "abcdecba"
    )
    board = Board((8, 8), layout)
    game = Obsidian(board)
    game.game_loop()