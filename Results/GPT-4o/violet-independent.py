import numpy as np

class VioletGame:
    def __init__(self):
        # Initialize a 10x10 board
        self.board = np.full((10, 10), ".")  # "." represents empty space
        self.initialize_board()
        self.current_player = 1  # Player 1 starts
        self.game_over = False

    def initialize_board(self):
        # Place V's for Player 2
        self.board[0, 3] = "V"
        self.board[0, 6] = "V"
        self.board[3, 0] = "V"
        self.board[3, 9] = "V"
        # Place A's for Player 1
        self.board[6, 0] = "A"
        self.board[6, 9] = "A"
        self.board[9, 3] = "A"
        self.board[9, 6] = "A"

    def display_board(self):
        print("\n".join([" ".join(row) for row in self.board]))
        print()

    def is_valid_move(self, piece, start, end):
        # Check if start and end positions are valid
        if not (0 <= start[0] < 10 and 0 <= start[1] < 10):
            return False
        if not (0 <= end[0] < 10 and 0 <= end[1] < 10):
            return False
        if self.board[start] != piece:
            return False
        if self.board[end] != ".":
            return False

        # Determine movement direction
        dx = np.sign(end[0] - start[0])
        dy = np.sign(end[1] - start[1])

        # Ensure movement is in a straight line
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False

        # Check all spaces between start and end are free
        x, y = start
        while (x, y) != end:
            x += dx
            y += dy
            if (x, y) != end and self.board[x, y] != ".":
                return False

        return True

    def move_piece(self, piece, start, end):
        if self.is_valid_move(piece, start, end):
            self.board[start] = "."
            self.board[end] = piece
            return True
        return False

    def is_valid_shot(self, shooter, position, target):
        if self.board[shooter] not in ["A", "V"]:
            return False
        if not (0 <= target[0] < 10 and 0 <= target[1] < 10):
            return False
        if self.board[target] != ".":
            return False

        # Determine shooting direction
        dx = np.sign(target[0] - position[0])
        dy = np.sign(target[1] - position[1])

        # Ensure shooting is in a straight line
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False

        # Check all spaces between shooter and target are free
        x, y = position
        while (x, y) != target:
            x += dx
            y += dy
            if (x, y) != target and self.board[x, y] != ".":
                return False

        return True

    def shoot_x(self, position, target):
        if self.is_valid_shot(position, position, target):
            self.board[target] = "X"
            return True
        return False

    def has_valid_moves(self, player):
        piece = "A" if player == 1 else "V"
        for x in range(10):
            for y in range(10):
                if self.board[x, y] == piece:
                    # Check all possible moves
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            while 0 <= nx < 10 and 0 <= ny < 10:
                                if self.board[nx, ny] != ".":
                                    break
                                if self.is_valid_move(piece, (x, y), (nx, ny)):
                                    return True
                                nx += dx
                                ny += dy
        return False

    def play_turn(self, start, end, shot):
        if self.game_over:
            print("Game is already over!")
            return

        piece = "A" if self.current_player == 1 else "V"

        # Move the piece
        if not self.move_piece(piece, start, end):
            print("Invalid move! Try again.")
            return

        # Shoot an X
        if not self.shoot_x(end, shot):
            # Undo the move if the shot is invalid
            self.board[end] = "."
            self.board[start] = piece
            print("Invalid shot! Try again.")
            return

        # Check if the other player can still move
        if not self.has_valid_moves(3 - self.current_player):
            print(f"Player {self.current_player} wins!")
            self.game_over = True
        else:
            # Switch to the other player
            self.current_player = 3 - self.current_player

    def start_game(self):
        print("Welcome to Violet!")
        self.display_board()

        while not self.game_over:
            print(f"Player {self.current_player}'s turn.")
            try:
                start = tuple(map(int, input("Enter the start position (row col): ").split()))
                end = tuple(map(int, input("Enter the end position (row col): ").split()))
                shot = tuple(map(int, input("Enter the shot position (row col): ").split()))
                self.play_turn(start, end, shot)
                self.display_board()
            except ValueError:
                print("Invalid input! Please enter positions as row and col separated by spaces.")


if __name__ == "__main__":
    game = VioletGame()
    game.start_game()