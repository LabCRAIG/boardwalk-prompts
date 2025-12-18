
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum

class PegSolitaire(Game):
    class Players(Enum):
        PLAYER = 0

    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = self.initial_player()

    def initial_player(self):
        return PegSolitaire.Players.PLAYER.value

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if is_movement(move):
            origin, destination = get_move_elements(move)
            x1, y1 = origin
            x2, y2 = destination

            # Ensure the move is orthogonal and jumps over a piece
            if abs(x1 - x2) + abs(y1 - y2) != 2:  # Must jump exactly two spaces
                return False

            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

            # Valid if origin has a peg, destination is empty, and there's a peg to jump over
            return (
                self.board.layout[x1, y1] == 'P' and
                self.board.layout[x2, y2] == '_' and
                self.board.layout[mid_x, mid_y] == 'P'
            )

        return False

    def perform_move(self, move: str):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            x1, y1 = origin
            x2, y2 = destination
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

            # Move the peg
            self.board.move_piece(move)

            # Remove the jumped peg
            self.board.place_piece(f"_ {mid_x},{mid_y}")

    def game_finished(self) -> bool:
        # Game ends when no valid moves are available
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == 'P':
                    # Check all possible moves from this position
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        x2, y2 = x + dx, y + dy
                        mid_x, mid_y = x + dx // 2, y + dy // 2
                        if 0 <= x2 < self.board.height and 0 <= y2 < self.board.width:
                            if (
                                self.board.layout[x2, y2] == '_' and
                                self.board.layout[mid_x, mid_y] == 'P'
                            ):
                                return False
        return True

    def get_winner(self):
        # Player wins if there's exactly one peg remaining
        peg_count = sum(row.count('P') for row in self.board.layout)
        return PegSolitaire.Players.PLAYER.value if peg_count == 1 else None

    def finish_message(self, winner):
        if winner is not None:
            print("Congratulations! You solved the puzzle!")
        else:
            print("No more moves available. Better luck next time!")

if __name__ == '__main__':
    # Define the diamond-shaped board layout
    diamond_layout = (
        "     _     \n"
        "    PPP    \n"
        "   PPPPP   \n"
        "  PPPPPPP  \n"
        " PPPPPPPPP \n"
        "  PPPPPPP  \n"
        "   PPPPP   \n"
        "    PPP    \n"
        "     _     "
    )
    board = Board((9, 9), diamond_layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()
