
from game import Game, Board, is_movement, is_placement, get_move_elements

# Enum for players
PLAYER_ONE = 0
PLAYER_TWO = 1

class NineMensMorris(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.phase = "placement"  # Game phases: "placement" or "movement"
        self.pieces = {PLAYER_ONE: 9, PLAYER_TWO: 9}  # Remaining pieces to place
        self.mills = {PLAYER_ONE: 0, PLAYER_TWO: 0}  # Number of mills formed
        self.captured_pieces = {PLAYER_ONE: 0, PLAYER_TWO: 0}  # Pieces captured
        self.positions = {PLAYER_ONE: set(), PLAYER_TWO: set()}  # Player positions

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if self.phase == "placement" and is_placement(move):
            piece, (row, col) = get_move_elements(move)
            return piece == "X" and self.board.layout[row][col] == "_"
        elif self.phase == "movement" and is_movement(move):
            (start, end) = get_move_elements(move)
            start_piece = self.board.layout[start[0]][start[1]]
            end_piece = self.board.layout[end[0]][end[1]]
            return start_piece in ("1", "2") and end_piece == "_"
        return False

    def perform_move(self, move: str):
        if self.phase == "placement" and is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces[self.current_player] -= 1
            self.positions[self.current_player].add((row, col))
            if self.is_mill((row, col)):
                self.mills[self.current_player] += 1
        elif self.phase == "movement" and is_movement(move):
            (start, end) = get_move_elements(move)
            self.board.move_piece(move)
            self.positions[self.current_player].remove(start)
            self.positions[self.current_player].add(end)
            if self.is_mill(end):
                self.mills[self.current_player] += 1

        # Transition to the next phase if all pieces are placed
        if self.phase == "placement" and all(p == 0 for p in self.pieces.values()):
            self.phase = "movement"

    def is_mill(self, position) -> bool:
        """Check whether the position completes a mill."""
        row, col = position
        piece = str(self.current_player + 1)

        # Define all possible mill combinations for a given position
        mills = [
            [(row, c) for c in range(self.board.width)],  # Horizontal
            [(r, col) for r in range(self.board.height)]  # Vertical
        ]

        for mill in mills:
            if all(self.board.layout[r][c] == piece for r, c in mill if (r, c) in self.positions[self.current_player]):
                return True
        return False

    def game_finished(self) -> bool:
        """Check if the game has ended."""
        # A player wins if the opponent has less than 3 pieces or cannot move
        for player in [PLAYER_ONE, PLAYER_TWO]:
            if len(self.positions[player]) < 3 or not self.has_valid_moves(player):
                return True
        return False

    def has_valid_moves(self, player: int) -> bool:
        """Check if the player has valid moves."""
        for pos in self.positions[player]:
            row, col = pos
            neighbors = self.get_neighbors(row, col)
            if any(self.board.layout[n[0]][n[1]] == "_" for n in neighbors):
                return True
        return False

    def get_neighbors(self, row: int, col: int):
        """Return valid neighbor positions for a given position."""
        neighbors = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)
        ]
        return [(r, c) for r, c in neighbors if 0 <= r < self.board.height and 0 <= c < self.board.width]

    def get_winner(self) -> int:
        """Determine the winner."""
        if len(self.positions[PLAYER_ONE]) < 3 or not self.has_valid_moves(PLAYER_ONE):
            return PLAYER_TWO
        elif len(self.positions[PLAYER_TWO]) < 3 or not self.has_valid_moves(PLAYER_TWO):
            return PLAYER_ONE
        return None

    def next_player(self) -> int:
        """Switch to the next player."""
        return PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a draw!")

if __name__ == '__main__':
    # Define a 7x7 Nine Men's Morris board with null spaces
    layout = (
        "X_____X\n"
        "_X___X_\n"
        "__X_X__\n"
        "XXX_XXX\n"
        "__X_X__\n"
        "_X___X_\n"
        "X_____X"
    )
    board = Board((7, 7), layout)
    game = NineMensMorris(board)
    game.game_loop()
