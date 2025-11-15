class OrchidGame:
    def __init__(self):
        # Initialize the board and game state
        self.board = [[" " for _ in range(5)] for _ in range(5)]  # 5x5 board
        self.players = {"Player 1": "A", "Player 2": "B"}
        self.current_player = "Player 1"
        self.phase = 1  # Phase 1: Placement, Phase 2: Movement
        self.pieces_left = {"A": 12, "B": 12}
        self.middle_position = (2, 2)  # Middle of the board

    def display_board(self):
        # Display the board
        print("\n  0 1 2 3 4")
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()

    def switch_player(self):
        # Switch the current player
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

    def is_valid_position(self, x, y):
        # Check if a position is valid
        return 0 <= x < 5 and 0 <= y < 5 and self.board[x][y] == " "

    def place_piece(self, x, y):
        # Place a piece on the board during Phase 1
        if not self.is_valid_position(x, y) or (x, y) == self.middle_position:
            print("Invalid position. Try again.")
            return False
        piece = self.players[self.current_player]
        self.board[x][y] = piece
        self.pieces_left[piece] -= 1
        return True

    def move_piece(self, x, y, target_x, target_y):
        # Move a piece during Phase 2
        piece = self.players[self.current_player]
        if not (0 <= target_x < 5 and 0 <= target_y < 5):
            print("Target out of bounds. Try again.")
            return False
        if self.board[x][y] != piece:
            print("You can only move your own piece. Try again.")
            return False
        if self.board[target_x][target_y] != " ":
            print("Target position is not empty. Try again.")
            return False
        if x != target_x and y != target_y:
            print("You can only move orthogonally. Try again.")
            return False
        if x == target_x:
            # Horizontal movement
            step = 1 if target_y > y else -1
            for col in range(y + step, target_y, step):
                if self.board[x][col] != " ":
                    print("Path is blocked. Try again.")
                    return False
        else:
            # Vertical movement
            step = 1 if target_x > x else -1
            for row in range(x + step, target_x, step):
                if self.board[row][y] != " ":
                    print("Path is blocked. Try again.")
                    return False
        # Move the piece
        self.board[x][y] = " "
        self.board[target_x][target_y] = piece
        self.check_captures(target_x, target_y)
        return True

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
                    self.board[nx][ny] == opponent_piece and
                    self.board[ex][ey] == piece):
                # Capture the opponent's piece
                self.board[nx][ny] = " "
                self.pieces_left[opponent_piece] -= 1
                print(f"{self.current_player} captured a piece!")

    def check_win(self):
        # Check for win conditions
        if self.pieces_left["A"] == 0:
            print("Player 2 (B) wins!")
            return True
        if self.pieces_left["B"] == 0:
            print("Player 1 (A) wins!")
            return True
        return False

    def play(self):
        # Main game loop
        while True:
            self.display_board()
            if self.check_win():
                break
            print(f"{self.current_player}'s turn.")
            piece = self.players[self.current_player]
            if self.phase == 1:
                # Phase 1: Placement
                print(f"Place two pieces. Pieces left: {self.pieces_left[piece]}")
                for _ in range(2):
                    if self.pieces_left[piece] == 0:
                        print("No pieces left to place.")
                        break
                    try:
                        x, y = map(int, input("Enter position to place (x y): ").split())
                        if self.place_piece(x, y):
                            self.display_board()
                        else:
                            break
                # Check if Phase 2 should start
                if self.pieces_left["A"] == 0 and self.pieces_left["B"] == 0:
                    self.phase = 2
                    print("All pieces placed. Phase 2 begins!")
            elif self.phase == 2:
                # Phase 2: Movement
                try:
                    x, y, target_x, target_y = map(int, input("Enter move (x y target_x target_y): ").split())
                    if self.move_piece(x, y, target_x, target_y):
                        pass
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
            self.switch_player()


# Start the game
if __name__ == "__main__":
    game = OrchidGame()
    game.play()