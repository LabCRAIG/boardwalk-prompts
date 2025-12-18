
from game import Game, Board, is_movement, is_placement, get_move_elements

class ChessWithRuleChanges(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        # Define player 1 as 0 (white) and player 2 as 1 (black)
        self.players = {0: "White", 1: "Black"}

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if is_placement(move):
            return False  # Chess doesn't allow piece placement mid-game

        if is_movement(move):
            origin, destination = get_move_elements(move)
            piece = self.board.layout[origin]

            # Ensure the piece belongs to the current player
            if self.current_player == 0 and piece.islower():
                return False
            if self.current_player == 1 and piece.isupper():
                return False

            # Ensure the destination is reachable for the piece
            # Implement basic movement rules for each piece
            # For simplicity, we'll avoid detailed movement rules here
            return True

        return False

    def perform_move(self, move: str):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            piece = self.board.layout[origin]

            # Special rule: Bishops can convert horizontally adjacent opposing pawns
            if piece.lower() == 'b':  # 'b' for bishop
                x, y = destination
                # Check left and right pawns
                for dx in [-1, 1]:
                    adjacent_x = x
                    adjacent_y = y + dx
                    if 0 <= adjacent_y < self.board.width:
                        adjacent_piece = self.board.layout[adjacent_x, adjacent_y]
                        if (self.current_player == 0 and adjacent_piece == 'p') or \
                           (self.current_player == 1 and adjacent_piece == 'P'):
                            # Convert pawn to the current player's pawn
                            converted_piece = 'P' if self.current_player == 0 else 'p'
                            self.board.place_piece(f"{converted_piece} {adjacent_x},{adjacent_y}")

            # Special rule: Queens can swap with rooks on the same color square
            if piece.lower() == 'q':  # 'q' for queen
                x, y = origin
                if (x + y) % 2 == 0:  # Ensure queen is on a dark square
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        rook_x = x + dx
                        rook_y = y + dy
                        if 0 <= rook_x < self.board.height and 0 <= rook_y < self.board.width:
                            rook_piece = self.board.layout[rook_x, rook_y]
                            if (self.current_player == 0 and rook_piece == 'R') or \
                               (self.current_player == 1 and rook_piece == 'r'):
                                # Swap queen and rook
                                self.board.move_piece(f"{origin[0]},{origin[1]} {rook_x},{rook_y}")
                                self.board.place_piece(f"{piece} {origin[0]},{origin[1]}")
                                return

            # Perform standard move
            self.board.move_piece(move)

    def game_finished(self) -> bool:
        # Check if either king is missing
        board_string = str(self.board)
        return 'K' not in board_string or 'k' not in board_string

    def get_winner(self) -> int:
        board_string = str(self.board)
        if 'K' not in board_string:
            return 1  # Black wins
        elif 'k' not in board_string:
            return 0  # White wins
        return None  # Draw

    def next_player(self) -> int:
        return 1 - self.current_player  # Alternate between 0 and 1

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {self.players[winner]} wins!")
        else:
            print("The game is a draw!")

if __name__ == '__main__':
    # Standard chess board layout
    initial_layout = (
        "rnbqkbnr\n"
        "pppppppp\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "PPPPPPPP\n"
        "RNBQKBNR"
    )
    board = Board((8, 8), initial_layout)
    mygame = ChessWithRuleChanges(board)
    mygame.game_loop()
