from game import Game, Board, is_placement, get_move_elements
from copy import deepcopy

class QuartzGame(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = 0  # Player 1 starts (0 represents 'A', 1 represents 'V')
        self.player_symbols = ['A', 'V']  # Player 1 = 'A', Player 2 = 'V'

    def initial_player(self):
        return 0  # Player 1 ('A') starts

    def validate_move(self, move: str) -> bool:
        if not is_placement(move):
            return False  # Only placement moves are valid

        piece, (row, col) = get_move_elements(move)
        if piece != self.player_symbols[self.current_player]:
            return False  # The piece must belong to the current player

        if self.board.layout[row, col] != '_':
            return False  # The space must be blank

        opponent_symbol = self.player_symbols[1 - self.current_player]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False

            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] == opponent_symbol:
                    found_opponent = True
                elif self.board.layout[r, c] == piece:
                    if found_opponent:
                        return True  # Valid move, captures opponent pieces
                    else:
                        break
                else:
                    break
                r += dr
                c += dc

        return False  # No valid capture lines

    def perform_move(self, move: str):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)  # Place the piece on the board

        opponent_symbol = self.player_symbols[1 - self.current_player]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []

            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] == opponent_symbol:
                    pieces_to_flip.append((r, c))
                elif self.board.layout[r, c] == piece:
                    for rr, cc in pieces_to_flip:
                        self.board.layout[rr, cc] = piece  # Flip opponent pieces
                    break
                else:
                    break
                r += dr
                c += dc

    def game_finished(self) -> bool:
        # The game is over if the board is full or if neither player has valid moves
        if '_' not in self.board.layout:
            return True  # No blank spaces left

        for player in range(2):
            if self.has_valid_moves(player):
                return False  # At least one player can still move

        return True  # No valid moves for either player

    def has_valid_moves(self, player: int) -> bool:
        piece = self.player_symbols[player]
        for row in range(self.board.height):
            for col in range(self.board.width):
                move = f"{piece} {row},{col}"
                if self.validate_move(move):
                    return True
        return False

    def get_winner(self):
        count_a = (self.board.layout == 'A').sum()
        count_v = (self.board.layout == 'V').sum()

        if count_a > count_v:
            return 0  # Player 1 ('A') wins
        elif count_v > count_a:
            return 1  # Player 2 ('V') wins
        else:
            return None  # It's a tie

    def next_player(self):
        return 1 - self.current_player  # Alternate between 0 and 1

    def finish_message(self, winner):
        if winner is None:
            print("It's a tie!")
        else:
            print(f"Player {self.player_symbols[winner]} wins!")


if __name__ == '__main__':
    # Define the 8x8 board with the initial layout
    initial_layout = (
        "________\n"
        "________\n"
        "________\n"
        "___AV___\n"
        "___VA___\n"
        "________\n"
        "________\n"
        "________"
    )
    board = Board((8, 8), initial_layout)
    game = QuartzGame(board)
    game.game_loop()