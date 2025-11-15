class DaisyGame:
    def __init__(self):
        # Initialize the board (9x9 empty board)
        self.board = [['.' for _ in range(9)] for _ in range(9)]
        
        # Player 1 piece reserves
        self.reserve_p1 = {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9}
        # Player 2 piece reserves
        self.reserve_p2 = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        
        # Turn order: Player 1 starts
        self.current_player = 1
        # Track if A and a are on the board (required for captures)
        self.A_on_board = False
        self.a_on_board = False
        # Game state
        self.game_over = False

    def print_board(self):
        # Print the current state of the board
        print("  " + " ".join(map(str, range(9))))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()

    def get_reserve(self):
        # Get the current player's reserve
        return self.reserve_p1 if self.current_player == 1 else self.reserve_p2

    def opposite_player_reserve(self):
        # Get the opposite player's reserve
        return self.reserve_p2 if self.current_player == 1 else self.reserve_p1

    def is_valid_position(self, x, y):
        # Check if a position is within the board bounds and free
        return 0 <= x < 9 and 0 <= y < 9

    def place_piece(self, piece, x, y):
        # Place a piece from the reserve onto the board
        reserve = self.get_reserve()
        if reserve.get(piece, 0) > 0 and self.board[x][y] == '.':
            self.board[x][y] = piece
            reserve[piece] -= 1
            if piece == 'A':
                self.A_on_board = True
            elif piece == 'a':
                self.a_on_board = True
            return True
        return False

    def move_piece(self, start_x, start_y, end_x, end_y):
        # Move a piece from one position to another
        if not self.is_valid_position(start_x, start_y) or not self.is_valid_position(end_x, end_y):
            return False

        piece = self.board[start_x][start_y]
        target = self.board[end_x][end_y]
        if piece == '.' or (self.current_player == 1 and piece.islower()) or (self.current_player == 2 and piece.isupper()):
            return False

        # Check capture rules
        if target != '.':
            if (self.current_player == 1 and target.isupper()) or (self.current_player == 2 and target.islower()):
                return False
            if (self.current_player == 1 and not self.A_on_board) or (self.current_player == 2 and not self.a_on_board):
                return False
            # Add captured piece to reserve
            reserve = self.get_reserve()
            reserve[target.upper() if self.current_player == 1 else target.lower()] += 1

        # Validate move based on piece type
        dx, dy = end_x - start_x, end_y - start_y
        if not self.is_valid_move(piece, dx, dy):
            return False

        # Perform the move
        self.board[start_x][start_y] = '.'
        self.board[end_x][end_y] = piece

        # Check win conditions
        if target == 'a' and self.current_player == 1:
            self.game_over = True
            print("Player 1 wins by capturing a!")
        elif target == 'A' and self.current_player == 2:
            self.game_over = True
            print("Player 2 wins by capturing A!")
        return True

    def is_valid_move(self, piece, dx, dy):
        # Validate move based on piece type
        if piece.upper() == 'A':
            return abs(dx) <= 1 and abs(dy) <= 1
        elif piece.upper() == 'B':
            return dx == 0 or dy == 0
        elif piece.upper() == 'C':
            return abs(dx) == abs(dy)
        elif piece.upper() == 'D':
            return abs(dx) <= 1 and (dy == 0 or dy == dx)
        elif piece.upper() == 'E':
            return abs(dx) == abs(dy) or (dx == 1 and dy == 0)
        elif piece.upper() == 'F':
            return dx == 2 and abs(dy) == 1
        elif piece.upper() == 'G':
            return dx > 0 and dy == 0
        elif piece.upper() == 'H':
            return dx == 1 and dy == 0
        return False

    def play_turn(self):
        # Play a single turn
        self.print_board()
        print(f"Player {self.current_player}'s turn.")
        
        # Display reserves
        reserve = self.get_reserve()
        print("Your reserve:", reserve)
        
        # Get action from player
        action = input("Enter action (place/move): ").strip().lower()
        if action == "place":
            piece = input("Enter piece to place: ").strip()
            x, y = map(int, input("Enter position (x y): ").split())
            if not self.place_piece(piece, x, y):
                print("Invalid placement.")
                return
        elif action == "move":
            start_x, start_y = map(int, input("Enter start position (x y): ").split())
            end_x, end_y = map(int, input("Enter end position (x y): ").split())
            if not self.move_piece(start_x, start_y, end_x, end_y):
                print("Invalid move.")
                return
        else:
            print("Invalid action.")
            return

        # Switch player
        self.current_player = 3 - self.current_player

    def start_game(self):
        # Start the game loop
        while not self.game_over:
            self.play_turn()


# Run the game
game = DaisyGame()
game.start_game()