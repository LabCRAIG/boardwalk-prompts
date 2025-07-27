from game import Game, Board, is_movement, is_placement, get_move_elements

class OrchidGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.phase = 1  # Phase 1: Placement, Phase 2: Movement
        self.pieces_left = {"A": 12, "B": 12}
        self.middle_position = (2, 2)
        self.players = {0: "A", 1: "B"}  # Player 0 -> A, Player 1 -> B

    def initial_player(self):
        return 0  # Player 1 starts (represented as 0)
    
    def next_player(self):
        return 1- self.current_player

    def validate_move(self, move):
        if self.phase == 1:
            # Placement phase validation
            if not is_placement(move):
                return False
            piece, (x, y) = get_move_elements(move)
            if piece != self.players[self.current_player]:
                return False  # Can only place your own piece
            if (x, y) == self.middle_position:
                return False  # Cannot place in the middle
            return self.board.layout[x, y] == "_"  # Must be a blank space
        elif self.phase == 2:
            # Movement phase validation
            if not is_movement(move):
                return False
            (x, y), (target_x, target_y) = get_move_elements(move)
            if self.board.layout[x, y] != self.players[self.current_player]:
                return False  # Can only move your own piece
            if self.board.layout[target_x, target_y] != "_":
                return False  # Target must be empty
            if x != target_x and y != target_y:
                return False  # Must move orthogonally
            # Check for path obstruction
            if x == target_x:  # Horizontal move
                step = 1 if target_y > y else -1
                for col in range(y + step, target_y, step):
                    if self.board.layout[x, col] != "_":
                        return False  # Path is blocked
            else:  # Vertical move
                step = 1 if target_x > x else -1
                for row in range(x + step, target_x, step):
                    if self.board.layout[row, y] != "_":
                        return False  # Path is blocked
            return True
        return False

    def perform_move(self, move):
        if self.phase == 1:
            # Placement phase
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_left[piece] -= 1
            # Check if Phase 2 should start
            if self.pieces_left["A"] == 0 and self.pieces_left["B"] == 0:
                print("All pieces placed. Phase 2 begins!")
                self.phase = 2
        elif self.phase == 2:
            # Movement phase
            (x, y), (target_x, target_y) = get_move_elements(move)
            self.board.move_piece(move)
            self.check_captures(target_x, target_y)

    def check_captures(self, x, y):
        # Check for captures in all 4 orthogonal directions
        piece = self.players[self.current_player]
        opponent_piece = "A" if piece == "B" else "B"
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            ex, ey = x + 2 * dx, y + 2 * dy
            if (0 <= nx < 5 and 0 <= ny < 5 and
                    0 <= ex < 5 and 0 <= ey < 5 and
                    self.board.layout[nx, ny] == opponent_piece and
                    self.board.layout[ex][ey] == piece):
                # Capture the opponent's piece
                self.board.layout[nx, ny] = "_"
                self.pieces_left[opponent_piece] -= 1
                print(f"Player {self.current_player + 1} captured a piece!")

    def game_finished(self):
        # Check if either player has no pieces left
        return self.pieces_left["A"] == 0 or self.pieces_left["B"] == 0

    def get_winner(self):
        if self.pieces_left["A"] == 0:
            return 1  # Player 2 wins
        if self.pieces_left["B"] == 0:
            return 0  # Player 1 wins
        return None  # Game is not yet finished

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a draw!")

    def prompt_current_player(self):
        if self.phase == 1:
            print(f"Player {self.current_player + 1}'s turn (Placement Phase). Pieces left: {self.pieces_left[self.players[self.current_player]]}")
            return input("Enter your move (e.g., 'A 1,1'): ")
        elif self.phase == 2:
            print(f"Player {self.current_player + 1}'s turn (Movement Phase).")
            return input("Enter your move (e.g., '1,1 1,3'): ")

if __name__ == '__main__':
    # Initialize a 5x5 board with all blank spaces
    board = Board((5, 5))
    orchid_game = OrchidGame(board)
    orchid_game.game_loop()