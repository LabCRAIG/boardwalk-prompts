class ObsidianGame:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        self.initialize_board()
        self.piece_moved = {
            'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False,
            'a': False, 'b': False, 'c': False, 'd': False, 'e': False, 'f': False
        }

    def initialize_board(self):
        # Set up Player 2's pieces (uppercase)
        self.board[0] = ['A', 'B', 'C', 'D', 'E', 'C', 'B', 'A']
        self.board[1] = ['F'] * 8
        
        # Set up Player 1's pieces (lowercase)
        self.board[6] = ['f'] * 8
        self.board[7] = ['a', 'b', 'c', 'd', 'e', 'c', 'b', 'a']

    def print_board(self):
        print("  " + " ".join([str(i) for i in range(8)]))
        for i, row in enumerate(self.board):
            print(str(i) + " " + " ".join(piece if piece != ' ' else '.' for piece in row))
        print()

    def is_valid_position(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def is_own_piece(self, piece):
        if self.current_player == 1:
            return piece.islower()
        else:
            return piece.isupper()

    def is_opponent_piece(self, piece):
        if piece == ' ':
            return False
        if self.current_player == 1:
            return piece.isupper()
        else:
            return piece.islower()

    def get_valid_moves(self, x, y):
        piece = self.board[x][y]
        if piece == ' ' or not self.is_own_piece(piece):
            return []
        
        moves = []
        piece_type = piece.lower()
        
        if piece_type == 'f':
            # Pawn movement
            direction = -1 if self.current_player == 1 else 1
            # Forward move
            if self.is_valid_position(x + direction, y) and self.board[x + direction][y] == ' ':
                moves.append((x + direction, y))
                # Initial double move
                if not self.piece_moved[piece] and self.is_valid_position(x + 2*direction, y) and self.board[x + 2*direction][y] == ' ':
                    moves.append((x + 2*direction, y))
            # Captures
            for dy in [-1, 1]:
                if self.is_valid_position(x + direction, y + dy):
                    target = self.board[x + direction][y + dy]
                    if self.is_opponent_piece(target):
                        moves.append((x + direction, y + dy))
        
        elif piece_type == 'a':
            # Rook movement (orthogonal)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                for step in range(1, 8):
                    nx, ny = x + dx*step, y + dy*step
                    if not self.is_valid_position(nx, ny):
                        break
                    if self.board[nx][ny] == ' ':
                        moves.append((nx, ny))
                    elif self.is_opponent_piece(self.board[nx][ny]):
                        moves.append((nx, ny))
                        break
                    else:
                        break
        
        elif piece_type == 'c':
            # Bishop movement (diagonal)
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                for step in range(1, 8):
                    nx, ny = x + dx*step, y + dy*step
                    if not self.is_valid_position(nx, ny):
                        break
                    if self.board[nx][ny] == ' ':
                        moves.append((nx, ny))
                    elif self.is_opponent_piece(self.board[nx][ny]):
                        moves.append((nx, ny))
                        break
                    else:
                        break
        
        elif piece_type == 'b':
            # Knight movement (L-shaped)
            moves = [
                (x+2, y+1), (x+2, y-1),
                (x-2, y+1), (x-2, y-1),
                (x+1, y+2), (x+1, y-2),
                (x-1, y+2), (x-1, y-2)
            ]
            moves = [(nx, ny) for nx, ny in moves if self.is_valid_position(nx, ny) and 
                     (self.board[nx][ny] == ' ' or self.is_opponent_piece(self.board[nx][ny]))]
        
        elif piece_type == 'e':
            # Queen movement (any direction)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                for step in range(1, 8):
                    nx, ny = x + dx*step, y + dy*step
                    if not self.is_valid_position(nx, ny):
                        break
                    if self.board[nx][ny] == ' ':
                        moves.append((nx, ny))
                    elif self.is_opponent_piece(self.board[nx][ny]):
                        moves.append((nx, ny))
                        break
                    else:
                        break
        
        elif piece_type == 'd':
            # King movement (one space any direction)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.is_valid_position(nx, ny) and (self.board[nx][ny] == ' ' or self.is_opponent_piece(self.board[nx][ny])):
                    moves.append((nx, ny))
        
        return moves

    def make_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        
        # Validate move
        if not self.is_valid_position(*start) or not self.is_valid_position(*end):
            return False
        
        piece = self.board[start_x][start_y]
        if piece == ' ' or not self.is_own_piece(piece):
            return False
        
        valid_moves = self.get_valid_moves(start_x, start_y)
        if (end_x, end_y) not in valid_moves:
            return False
        
        # Check for promotion
        target_piece = self.board[end_x][end_y]
        if self.is_opponent_piece(target_piece):
            # Check if capturing opponent's D/d
            if target_piece.lower() == 'd':
                self.game_over = True
                self.winner = self.current_player
        
        # Move the piece
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = ' '
        self.piece_moved[piece] = True
        
        # Check for pawn promotion
        if piece.lower() == 'f':
            if (self.current_player == 1 and end_x == 0) or (self.current_player == 2 and end_x == 7):
                promoted_piece = 'e' if self.current_player == 1 else 'E'
                self.board[end_x][end_y] = promoted_piece
                self.piece_moved[promoted_piece] = True
        
        # Switch player
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
        return True

    def play(self):
        print("Welcome to Obsidian!")
        print("Player 1 controls lowercase pieces (a, b, c, d, e, f)")
        print("Player 2 controls uppercase pieces (A, B, C, D, E, F)")
        print("To make a move, enter coordinates in the format 'start_x start_y end_x end_y'")
        print("Example: '6 0 5 0' would move the piece at row 6, column 0 to row 5, column 0")
        print()
        
        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            
            while True:
                try:
                    move = input("Enter your move: ").split()
                    if len(move) != 4:
                        print("Please enter exactly 4 numbers separated by spaces")
                        continue
                    
                    start_x, start_y, end_x, end_y = map(int, move)
                    if self.make_move((start_x, start_y), (end_x, end_y)):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter numbers only")
        
        self.print_board()
        print(f"Game over! Player {self.winner} wins!")

# Start the game
if __name__ == "__main__":
    game = ObsidianGame()
    game.play()