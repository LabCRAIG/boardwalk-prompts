
from game import Game, Board, is_movement, get_move_elements
from enum import Enum


class Player(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1


class Checkers(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = self.initial_player()

    def initial_player(self):
        return Player.PLAYER_1.value

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if not is_movement(move):
            return False

        (origin, destination) = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Ensure origin and destination are on the board
        if not (0 <= ox < self.board.height and 0 <= oy < self.board.width):
            return False
        if not (0 <= dx < self.board.height and 0 <= dy < self.board.width):
            return False

        # Ensure there is a piece to move
        piece = self.board.layout[ox, oy]
        if piece != 'P' and piece != 'p':
            return False

        # Ensure destination is blank
        if self.board.layout[dx, dy] != '_':
            return False

        # Ensure the move is diagonal
        if abs(dx - ox) != abs(dy - oy):
            return False

        # Ensure the move is in the correct direction
        if self.current_player == Player.PLAYER_1.value and dx <= ox:
            return False
        if self.current_player == Player.PLAYER_2.value and dx >= ox:
            return False

        # Allow basic diagonal movement (1-space move)
        if abs(dx - ox) == 1:
            return True

        # Allow capture move (2-space move)
        if abs(dx - ox) == 2:
            mx, my = (ox + dx) // 2, (oy + dy) // 2  # Middle space
            middle_piece = self.board.layout[mx, my]
            if self.current_player == Player.PLAYER_1.value and middle_piece == 'p':
                return True
            if self.current_player == Player.PLAYER_2.value and middle_piece == 'P':
                return True

        return False

    def perform_move(self, move: str):
        (origin, destination) = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Move the piece
        self.board.move_piece(move)

        # Handle captures
        if abs(dx - ox) == 2:
            mx, my = (ox + dx) // 2, (oy + dy) // 2  # Middle space
            self.board.place_piece(f"_ {mx},{my}")

    def game_finished(self) -> bool:
        # Game finishes when one player has no pieces left
        p1_pieces = sum(row.count('P') for row in self.board.layout)
        p2_pieces = sum(row.count('p') for row in self.board.layout)
        return p1_pieces == 0 or p2_pieces == 0

    def get_winner(self) -> int:
        p1_pieces = sum(row.count('P') for row in self.board.layout)
        p2_pieces = sum(row.count('p') for row in self.board.layout)
        if p1_pieces > 0 and p2_pieces == 0:
            return Player.PLAYER_1.value
        elif p2_pieces > 0 and p1_pieces == 0:
            return Player.PLAYER_2.value
        return None

    def next_player(self) -> int:
        return Player.PLAYER_2.value if self.current_player == Player.PLAYER_1.value else Player.PLAYER_1.value


if __name__ == '__main__':
    # Initialize board with pieces for both players
    layout = (
        "pppppppp\n"
        "pppppppp\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "PPPPPPPP\n"
        "PPPPPPPP"
    )

    board = Board((8, 8), layout)
    checkers = Checkers(board)
    checkers.game_loop()
