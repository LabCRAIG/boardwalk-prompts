from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

# Game subclass definition
class Orchid(Game):
    class Player:
        PLAYER_1 = 0
        PLAYER_2 = 1

    def __init__(self, board):
        super().__init__(board)
        self.phase = 1  # Phase 1: Placement, Phase 2: Movement
        self.pieces_per_player = 12
        self.remaining_pieces = {self.Player.PLAYER_1: self.pieces_per_player,
                                 self.Player.PLAYER_2: self.pieces_per_player}

    def initial_player(self):
        return self.Player.PLAYER_1

    def prompt_current_player(self):
        player = "A" if self.current_player == self.Player.PLAYER_1 else "B"
        action = "place two pieces" if self.phase == 1 else "move a piece"
        return input(f"Player {player}, it's your turn to {action}: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if self.phase == 1:  # Placement phase
            if not is_placement(move):
                return False
            piece, (x, y) = get_move_elements(move)
            if self.remaining_pieces[self.current_player] < 2:
                return False
            if piece not in ["A", "B"]:
                return False
            if self.board.layout[x, y] != "_" or (x == 2 and y == 2):  # Middle is restricted
                return False
            return True
        elif self.phase == 2:  # Movement phase
            if not is_movement(move):
                return False
            (x1, y1), (x2, y2) = get_move_elements(move)
            if self.board.layout[x1, y1] != ("A" if self.current_player == self.Player.PLAYER_1 else "B"):
                return False
            if self.board.layout[x2, y2] != "_":
                return False
            if x1 != x2 and y1 != y2:  # Must move orthogonally
                return False
            return True
        return False

    def perform_move(self, move):
        if self.phase == 1:  # Placement phase
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            self.remaining_pieces[self.current_player] -= 1
            if all(p == 0 for p in self.remaining_pieces.values()):  # Transition to Phase 2
                self.phase = 2
        elif self.phase == 2:  # Movement phase
            (x1, y1), (x2, y2) = get_move_elements(move)
            self.board.move_piece(move)
            self.capture_pieces(x2, y2)

    def capture_pieces(self, x, y):
        current_piece = self.board.layout[x, y]
        opponent_piece = "B" if current_piece == "A" else "A"

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
                if self.board.layout[nx, ny] == opponent_piece:
                    # Check if there's a current player's piece in the direction
                    cx, cy = nx + dx, ny + dy
                    if (0 <= cx < self.board.height and 0 <= cy < self.board.width and
                            self.board.layout[cx, cy] == current_piece):
                        self.board.layout[nx, ny] = "_"  # Capture the piece
                    break
                elif self.board.layout[nx, ny] == "_":
                    break
                nx, ny = nx + dx, ny + dy

    def next_player(self):
        return (self.current_player + 1) % 2

    def game_finished(self):
        return (np.count_nonzero(self.board.layout == "A") == 0 or
                np.count_nonzero(self.board.layout == "B") == 0)

    def get_winner(self):
        count_a = np.count_nonzero(self.board.layout == "A")
        count_b = np.count_nonzero(self.board.layout == "B")
        if count_a > count_b:
            return self.Player.PLAYER_1
        elif count_b > count_a:
            return self.Player.PLAYER_2
        return None

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {'A' if winner == self.Player.PLAYER_1 else 'B'} wins!")

if __name__ == '__main__':
    board = Board((5, 5))
    mygame = Orchid(board)
    mygame.game_loop()