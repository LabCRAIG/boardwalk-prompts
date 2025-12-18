
from game import Game, Board, is_movement, is_placement, get_move_elements

class Checkers(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: 'w', 1: 'b'}  # White and black players
        self.kings = {'W', 'B'}         # King pieces
        self.pieces = {'w', 'b', 'W', 'B'}  # All pieces
        self.initial_pieces = {'w': 12, 'b': 12}  # Initial piece counts
        self.captured_pieces = {'w': 0, 'b': 0}  # Tracks captures

    def initial_player(self) -> int:
        return 0  # White starts

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False
        if is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination
            piece = self.board.layout[ox, oy]

            if piece not in self.pieces or piece.lower() != self.players[self.current_player]:
                return False  # Not the player's piece

            if self.board.layout[dx, dy] != '_':
                return False  # Destination must be empty

            dx_diff, dy_diff = abs(dx - ox), abs(dy - oy)
            if piece in self.kings:
                return dx_diff == dy_diff == 1 or (dx_diff == dy_diff == 2 and self.is_capture(origin, destination))
            else:
                direction = 1 if self.current_player == 0 else -1
                return (dx - ox == direction and dx_diff == dy_diff == 1) or self.is_capture(origin, destination)

        return False  # Invalid format

    def is_capture(self, origin, destination):
        ox, oy = origin
        dx, dy = destination
        mx, my = (ox + dx) // 2, (oy + dy) // 2  # Midpoint
        middle_piece = self.board.layout[mx, my]
        return middle_piece.lower() == self.players[(self.current_player + 1) % 2]  # Opponent's piece

    def perform_move(self, move: str):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination
            piece = self.board.layout[ox, oy]

            if abs(dx - ox) == 2:  # Capture
                mx, my = (ox + dx) // 2, (oy + dy) // 2
                captured_piece = self.board.layout[mx, my]
                self.board.place_piece(f'_ {mx},{my}')
                self.captured_pieces[captured_piece.lower()] += 1

                # Remove both kings if applicable
                if piece in self.kings and captured_piece in self.kings:
                    self.board.place_piece(f'_ {ox},{oy}')
                    self.board.place_piece(f'_ {dx},{dy}')
                    return

            self.board.move_piece(move)

            # Promote to king if reaching the opponent's end
            if (piece == 'w' and dx == self.board.height - 1) or (piece == 'b' and dx == 0):
                self.board.place_piece(f'{piece.upper()} {dx},{dy}')
        else:
            super().perform_move(move)

    def game_finished(self) -> bool:
        # Game ends when a player has no pieces left or no valid moves
        for player, piece in self.players.items():
            if self.captured_pieces[piece] == self.initial_pieces[piece]:
                return True

            if any(self.validate_move(f"{x},{y} {nx},{ny}")
                   for x in range(self.board.height)
                   for y in range(self.board.width)
                   for nx in range(self.board.height)
                   for ny in range(self.board.width)
                   if self.board.layout[x, y].lower() == piece):
                return False

        return True

    def get_winner(self):
        # Determine winner based on remaining pieces
        if self.captured_pieces['w'] == self.initial_pieces['w']:
            return 1  # Black wins
        elif self.captured_pieces['b'] == self.initial_pieces['b']:
            return 0  # White wins
        return None  # Draw

    def next_player(self) -> int:
        return (self.current_player + 1) % 2  # Alternate turns

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {self.players[winner]} wins!")
        else:
            print("It's a draw!")

if __name__ == '__main__':
    initial_layout = (
        " b b b b\n"
        "b b b b \n"
        " b b b b\n"
        "_ _ _ _ \n"
        "_ _ _ _ \n"
        "w w w w \n"
        " w w w w\n"
        "w w w w \n"
    )
    board = Board((8, 8), initial_layout)
    mygame = Checkers(board)
    mygame.game_loop()
