from game import Game, Board, is_placement, is_movement, get_move_elements

class Amethyst(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.pieces = {0: ['A', 'Â'], 1: ['O', 'Ô']}  # Player 1 (0) and Player 2 (1)
        self.directions = {
            'A': [(-1, -1), (-1, 1)],
            'O': [(1, -1), (1, 1)],
            'Â': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'Ô': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        }

    def initial_player(self):
        return 0  # Player 1 starts

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        # Parse the move
        if is_movement(move):
            (start, end) = get_move_elements(move)
            start_row, start_col = start
            end_row, end_col = end
        else:
            return False

        # Validate origin square
        piece = self.board.layout[start_row][start_col]
        if piece not in self.pieces[self.current_player]:
            return False

        # Validate destination square
        if self.board.layout[end_row][end_col] != '_':
            return False

        # Check if the movement is valid
        dr, dc = end_row - start_row, end_col - start_col
        if (dr, dc) in self.directions[piece]:
            return True

        # Check if the capture move is valid
        if abs(dr) == 2 and abs(dc) == 2:
            middle_row, middle_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            middle_piece = self.board.layout[middle_row][middle_col]
            if middle_piece in self.pieces[1 - self.current_player]:  # Opponent's piece
                return True

        return False

    def perform_move(self, move: str):
        if is_movement(move):
            (start, end) = get_move_elements(move)
            start_row, start_col = start
            end_row, end_col = end

            # Move the piece
            piece = self.board.layout[start_row][start_col]
            self.board.move_piece(move)

            # Handle captures
            if abs(end_row - start_row) == 2:  # A capture was made
                capture_row, capture_col = (start_row + end_row) // 2, (start_col + end_col) // 2
                self.board.layout[capture_row][capture_col] = '_'

            # Handle promotions
            if piece == 'A' and end_row == 0:
                self.board.layout[end_row][end_col] = 'Â'
            elif piece == 'O' and end_row == 7:
                self.board.layout[end_row][end_col] = 'Ô'

    def game_finished(self) -> bool:
        # Check if either player has no pieces left or no valid moves
        for player in [0, 1]:
            has_pieces = False
            for row in range(self.board.height):
                for col in range(self.board.width):
                    piece = self.board.layout[row][col]
                    if piece in self.pieces[player]:
                        has_pieces = True
                        if self.get_valid_moves(row, col):
                            return False  # Player has valid moves
            if not has_pieces:
                return True  # Player has no pieces left
        return True

    def get_winner(self) -> int:
        # Determine the winner based on the remaining valid moves or pieces
        for player in [0, 1]:
            for row in range(self.board.height):
                for col in range(self.board.width):
                    piece = self.board.layout[row][col]
                    if piece in self.pieces[player] and self.get_valid_moves(row, col):
                        return player
        return 1 - self.current_player  # Opponent wins if no moves are left

    def next_player(self) -> int:
        # Determine the next player
        return 1 - self.current_player

    def get_valid_moves(self, row: int, col: int):
        # Get all valid moves for a piece at (row, col)
        piece = self.board.layout[row][col]
        if piece not in self.pieces[self.current_player]:
            return []

        moves = []
        for dr, dc in self.directions[piece]:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if self.is_in_bounds(new_row, new_col) and self.board.layout[new_row][new_col] == '_':
                moves.append((new_row, new_col))

            # Capture move
            capture_row, capture_col = row + 2 * dr, col + 2 * dc
            middle_row, middle_col = row + dr, col + dc
            if (
                self.is_in_bounds(capture_row, capture_col) and
                self.board.layout[capture_row][capture_col] == '_' and
                self.board.layout[middle_row][middle_col] in self.pieces[1 - self.current_player]
            ):
                moves.append((capture_row, capture_col))

        return moves

    def is_in_bounds(self, row, col):
        return 0 <= row < self.board.height and 0 <= col < self.board.width

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a draw!")


if __name__ == '__main__':
    # Define the initial board layout
    layout = (
        "_O_O_O_O\n"
        "O_O_O_O_\n"
        "_O_O_O_O\n"
        "________\n"
        "________\n"
        "A_A_A_A_\n"
        "_A_A_A_A\n"
        "A_A_A_A_\n"
    )
    board = Board((8, 8), layout)
    game = Amethyst(board)
    game.game_loop()