from game import Game, Board, is_movement, is_placement, get_move_elements

class Topaz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = {0: 'A', 1: 'B'}  # Player enums: 0 for Player 1 and 1 for Player 2
        self.pieces_left = {0: 9, 1: 9}  # Pieces left for each player
        self.phase = 1  # Phase 1: Placement, Phase 2: Movement

    def validate_move(self, move):
        if self.phase == 1 and is_placement(move):
            piece, (x, y) = get_move_elements(move)
            if piece != self.players[self.current_player]:
                return False  # Can only place your own piece
            return self.board.layout[x, y] == '_'  # Must place on a blank space
        elif self.phase == 2 and is_movement(move):
            (x, y), (new_x, new_y) = get_move_elements(move)
            if self.board.layout[x, y] != self.players[self.current_player]:
                return False  # Must move your own piece
            if self.board.layout[new_x, new_y] != '_':
                return False  # Must move to a blank space
            # Must move to an adjacent, orthogonal space
            return abs(x - new_x) + abs(y - new_y) == 1
        return False

    def perform_move(self, move):
        if self.phase == 1 and is_placement(move):
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_left[self.current_player] -= 1
            self.check_capture(x, y)
            self.check_phase_transition()
        elif self.phase == 2 and is_movement(move):
            (x, y), (new_x, new_y) = get_move_elements(move)
            self.board.move_piece(move)
            self.check_capture(new_x, new_y)
            self.check_loss_condition()

    def game_finished(self):
        return False
        # Game ends if a player has 2 or fewer pieces or cannot move
        return self.get_winner() is not None

    def get_winner(self):
        # Check if a player has lost
        for player in [0, 1]:
            if self.pieces_left[player] <= 2:
                return 1 - player  # The other player wins
        # Check if a player cannot move
        for player in [0, 1]:
            for x in range(self.board.height):
                for y in range(self.board.width):
                    if self.board.layout[x, y] == self.players[player]:
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.board.height and 0 <= ny < self.board.width:
                                if self.board.layout[nx, ny] == '_':
                                    return None  # Player can still move
        return 1 - self.current_player  # The other player wins

    def next_player(self):
        return 1 - self.current_player  # Alternate players

    def initial_player(self):
        return 0  # Player 1 starts

    def round_counter(self):
        return self.round + 1

    def finish_message(self, winner):
        print(f"Player {winner + 1} wins!")

    def check_capture(self, x, y):
        piece = self.board.layout[x, y]
        for direction in [(0, 1), (1, 0)]:  # Check rows and columns
            count = 1
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
                    if self.board.layout[nx, ny] == piece:
                        count += 1
                        nx += dx
                        ny += dy
                    else:
                        break
            if count >= 3:  # Capture condition met
                self.capture_piece()
                break

    def capture_piece(self):
        opponent = self.players[1 - self.current_player]
        print(f"Player {self.current_player + 1} captured! Choose an opponent piece to remove.")
        while True:
            try:
                move = input(f"Enter the position (row, column) of {opponent} to remove: ")
                x, y = map(int, move.split(','))
                if self.board.layout[x, y] == opponent:
                    self.board.layout[x, y] = '_'
                    self.pieces_left[1 - self.current_player] -= 1
                    break
                else:
                    print("Invalid position. Try again.")
            except ValueError:
                print("Invalid input. Enter two integers separated by a comma.")

    def check_phase_transition(self):
        if self.pieces_left[0] == 0 and self.pieces_left[1] == 0:
            self.phase = 2
            print("All pieces placed. Transitioning to Phase 2: Movement phase.")

# Main function
if __name__ == '__main__':
    layout = (
        "_ _ _\n"
        " _ _ _\n"
        "  ___\n"
        "___ ___\n"
        "  ___\n"
        " _ _ _\n"
        "_ _ _"
    )
    board = Board((7, 7), layout)
    game = Topaz(board)
    game.game_loop()