
from game import Game, Board, is_movement, get_move_elements


class PegSolitaire(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = 0  # Only one player in Peg Solitaire

    def validate_move(self, move: str) -> bool:
        if not is_movement(move):
            return False

        # Extract the move elements
        (origin, destination) = get_move_elements(move)
        x1, y1 = origin
        x2, y2 = destination

        # Ensure the origin and destination are valid
        if not (0 <= x1 < self.board.height and 0 <= y1 < self.board.width):
            return False
        if not (0 <= x2 < self.board.height and 0 <= y2 < self.board.width):
            return False

        # Ensure the origin has a peg and the destination is blank
        if self.board.layout[x1, y1] != 'P' or self.board.layout[x2, y2] != '_':
            return False

        # Ensure the move is orthogonal and exactly two spaces
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) == 2 and dy == 0:  # Vertical move
            mid_x, mid_y = x1 + dx // 2, y1
        elif abs(dy) == 2 and dx == 0:  # Horizontal move
            mid_x, mid_y = x1, y1 + dy // 2
        else:
            return False

        # Ensure there's a peg in the middle space to jump over
        if self.board.layout[mid_x, mid_y] != 'P':
            return False

        return True

    def perform_move(self, move: str):
        (origin, destination) = get_move_elements(move)
        x1, y1 = origin
        x2, y2 = destination

        # Perform the move: move the peg and clear the origin and middle spaces
        dx, dy = x2 - x1, y2 - y1
        mid_x, mid_y = x1 + dx // 2, y1 + dy // 2

        super().perform_move(move)  # Moves the peg
        self.board.place_piece(f"_ {mid_x},{mid_y}")  # Remove the jumped peg

    def game_finished(self) -> bool:
        # The game is finished when no valid moves are left
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == 'P':
                    # Check all possible moves from this peg
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        new_x, new_y = x + dx, y + dy
                        middle_x, middle_y = x + dx // 2, y + dy // 2
                        if (
                            0 <= new_x < self.board.height and
                            0 <= new_y < self.board.width and
                            self.board.layout[new_x, new_y] == '_' and
                            self.board.layout[middle_x, middle_y] == 'P'
                        ):
                            return False
        return True

    def get_winner(self):
        # The fewer pegs left, the better the player's score.
        remaining_pegs = sum(row.count('P') for row in self.board.layout)
        return remaining_pegs

    def finish_message(self, winner):
        print(f"Game over! Pegs remaining: {winner}. Aim for fewer pegs!")


if __name__ == '__main__':
    # The standard Peg Solitaire board layout
    layout = (
        "  PPP  \n"
        "  PPP  \n"
        "PPPPPPP\n"
        "PPP_PPP\n"
        "PPPPPPP\n"
        "  PPP  \n"
        "  PPP  "
    )
    board = Board((7, 7), layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()
