from game import Game, Board, is_placement, is_movement, get_move_elements

class DaisyGame(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player reserves
        self.reserve_p1 = {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9}
        self.reserve_p2 = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        # Track whether "A" or "a" are on the board
        self.A_on_board = False
        self.a_on_board = False

        self.game_over = False

    def initial_player(self):
        return 1  # Player 1 starts

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        board = self.board.layout
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            reserve = self.get_current_reserve()
            return (
                reserve.get(piece, 0) > 0 and  # Piece must be in reserve
                board[x][y] == "_"  # Target space must be blank
            )
        elif is_movement(move):
            (start_x, start_y), (end_x, end_y) = get_move_elements(move)
            piece = board[start_x][start_y]
            target = board[end_x][end_y]

            # Validate piece ownership and target space
            if self.current_player == 1 and piece.islower():
                return False
            if self.current_player == 2 and piece.isupper():
                return False
            if target != "_" and (
                (self.current_player == 1 and target.isupper()) or
                (self.current_player == 2 and target.islower())
            ):
                return False

            # Check capture rules
            if target != "_" and (
                (self.current_player == 1 and not self.A_on_board) or
                (self.current_player == 2 and not self.a_on_board)
            ):
                return False

            # Validate piece movement
            dx, dy = end_x - start_x, end_y - start_y
            return self.is_valid_piece_move(piece, dx, dy)
        return False

    def perform_move(self, move):
        board = self.board
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            board.place_piece(move)  # Place the piece
            self.update_reserve(piece, -1)
            # Track A/a placement
            if piece == "A":
                self.A_on_board = True
            elif piece == "a":
                self.a_on_board = True
        elif is_movement(move):
            (start_x, start_y), (end_x, end_y) = get_move_elements(move)
            piece = board.layout[start_x][start_y]
            target = board.layout[end_x][end_y]

            # Handle captures
            if target != "_":
                captured_piece = target.upper() if self.current_player == 1 else target.lower()
                self.update_reserve(captured_piece, 1)

            # Move the piece
            board.move_piece(move)

            # Check win conditions
            if target == "a" and self.current_player == 1:
                self.game_over = True
            elif target == "A" and self.current_player == 2:
                self.game_over = True

    def next_player(self):
        return 2 if self.current_player == 1 else 1

    def game_finished(self):
        return self.game_over

    def get_winner(self):
        if self.game_over:
            return self.current_player
        return None

    def finish_message(self, winner):
        if winner:
            print(f"Player {winner} wins by capturing the opponent's A/a!")
        else:
            print("Game over with no winner.")

    def get_current_reserve(self):
        return self.reserve_p1 if self.current_player == 1 else self.reserve_p2

    def update_reserve(self, piece, count):
        reserve = self.get_current_reserve()
        if piece in reserve:
            reserve[piece] += count

    def is_valid_piece_move(self, piece, dx, dy):
        # Check movement rules for each piece type
        piece_type = piece.upper()
        if piece_type == "A":
            return abs(dx) <= 1 and abs(dy) <= 1
        elif piece_type == "B":
            return dx == 0 or dy == 0
        elif piece_type == "C":
            return abs(dx) == abs(dy)
        elif piece_type == "D":
            return abs(dx) <= 1 and (dy == 0 or dx == dy)
        elif piece_type == "E":
            return abs(dx) == abs(dy) or (dx == 1 and dy == 0)
        elif piece_type == "F":
            return dx == 2 and abs(dy) == 1
        elif piece_type == "G":
            return dx > 0 and dy == 0
        elif piece_type == "H":
            return dx == 1 and dy == 0
        return False

if __name__ == "__main__":
    # Create a 9x9 board with default (empty) layout
    board = Board((9, 9))
    game = DaisyGame(board)
    game.game_loop()