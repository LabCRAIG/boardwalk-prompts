
from game import Game, Board, is_movement, is_placement, get_move_elements

# Game subclass definition
class PegSolitaire(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = [0]  # Single-player game

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if not is_movement(move):
            return False
        
        origin, destination = get_move_elements(move)
        mid_row = (origin[0] + destination[0]) // 2
        mid_col = (origin[1] + destination[1]) // 2
        mid_pos = (mid_row, mid_col)

        # Ensure the origin contains a peg, the middle has a peg, and the destination is blank
        return (
            self.board.layout[origin[0], origin[1]] == 'P' and
            self.board.layout[mid_row, mid_col] == 'P' and
            self.board.layout[destination[0], destination[1]] == '_'
        )

    def perform_move(self, move: str):
        origin, destination = get_move_elements(move)
        mid_row = (origin[0] + destination[0]) // 2
        mid_col = (origin[1] + destination[1]) // 2
        mid_pos = (mid_row, mid_col)

        # Perform the standard movement
        super().perform_move(move)

        # Remove the jumped peg
        self.board.place_piece(f"_ {mid_pos[0]},{mid_pos[1]}")

    def game_finished(self) -> bool:
        # Check if there are exactly two pegs left
        peg_positions = [
            (row, col)
            for row in range(self.board.height)
            for col in range(self.board.width)
            if self.board.layout[row, col] == 'P'
        ]

        if len(peg_positions) != 2:
            return False

        # Check if one peg cannot capture the other
        peg1, peg2 = peg_positions
        diff_row = abs(peg1[0] - peg2[0])
        diff_col = abs(peg1[1] - peg2[1])

        # Pegs are too far apart to jump over each other
        if diff_row > 2 or diff_col > 2:
            return True

        # Check if the middle position is blank
        mid_row = (peg1[0] + peg2[0]) // 2
        mid_col = (peg1[1] + peg2[1]) // 2
        return self.board.layout[mid_row, mid_col] != 'P'

    def get_winner(self):
        # Single-player game, so we return the only player as the winner
        return self.players[0]

    def next_player(self):
        # Single-player game, so the same player always plays
        return self.players[0]

if __name__ == '__main__':
    # Define the initial layout of the Peg Solitaire board
    initial_layout = (
        "  P P P  \n"
        "  P P P  \n"
        "P P P P P\n"
        "P P _ P P\n"
        "P P P P P\n"
        "  P P P  \n"
        "  P P P  "
    )
    board = Board((7, 7), initial_layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()
