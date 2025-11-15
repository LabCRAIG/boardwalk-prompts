class Piece:
    def __init__(self, piece_type, player):
        self.type = piece_type
        self.player = player
        self.upper = piece_type.isupper()
    
    def __str__(self):
        return self.type
    
    def get_moves(self, board, x, y):
        moves = []
        if self.type.lower() == 'a':
            # A/a: moves one space in any direction
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 9 and 0 <= ny < 9:
                        moves.append((nx, ny))
        elif self.type.lower() == 'b':
            # B/b: moves any number orthogonally (rook-like)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 9 and 0 <= ny < 9:
                    if board[nx][ny] is None:
                        moves.append((nx, ny))
                    else:
                        break
                    nx += dx
                    ny += dy
        elif self.type.lower() == 'c':
            # C/c: moves any number diagonally (bishop-like)
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 9 and 0 <= ny < 9:
                    if board[nx][ny] is None:
                        moves.append((nx, ny))
                    else:
                        break
                    nx += dx
                    ny += dy
        elif self.type.lower() == 'd':
            # D/d: moves one square in any direction except diagonally backward
            forward = -1 if self.upper else 1  # uppercase moves up, lowercase moves down
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    # Check if move is diagonally backward
                    if (dx != 0 and dy != 0) and (dy == forward):
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 9 and 0 <= ny < 9:
                        moves.append((nx, ny))
        elif self.type.lower() == 'e':
            # E/e: moves one square diagonally or one square forward orthogonally
            forward = -1 if self.upper else 1
            # Diagonal moves
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 9 and 0 <= ny < 9:
                        moves.append((nx, ny))
            # Forward orthogonal move
            nx, ny = x, y + forward
            if 0 <= ny < 9:
                moves.append((nx, ny))
        elif self.type.lower() == 'f':
            # F/f: moves two forward, then one left/right (knight-like but restricted)
            forward = -1 if self.upper else 1
            # Two forward, one left/right
            for side in [-1, 1]:
                nx, ny = x + side, y + 2 * forward
                if 0 <= nx < 9 and 0 <= ny < 9:
                    moves.append((nx, ny))
        elif self.type.lower() == 'g':
            # G/g: moves any number orthogonally forward (forward-only rook)
            forward = -1 if self.upper else 1
            # Forward/backward
            ny = y + forward
            while 0 <= ny < 9:
                if board[x][ny] is None:
                    moves.append((x, ny))
                else:
                    break
                ny += forward
            # Left/right
            for dx in [-1, 1]:
                nx = x + dx
                while 0 <= nx < 9:
                    if board[nx][y] is None:
                        moves.append((nx, y))
                    else:
                        break
                    nx += dx
        elif self.type.lower() == 'h':
            # H/h: moves one space forward orthogonally (pawn-like)
            forward = -1 if self.upper else 1
            nx, ny = x, y + forward
            if 0 <= ny < 9:
                moves.append((nx, ny))
        return moves

class DaisyGame:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.players = {
            1: {'reserve': {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9}, 'has_placed_a': False},
            2: {'reserve': {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}, 'has_placed_a': False}
        }
        self.current_player = 1
        self.winner = None
    
    def print_board(self):
        print("   " + " ".join(str(i) for i in range(9)))
        for y in range(9):
            row = []
            for x in range(9):
                piece = self.board[x][y]
                row.append(str(piece) if piece else '.')
            print(f"{y}  " + " ".join(row))
        print()
    
    def is_valid_place(self, piece_type, x, y):
        if not (0 <= x < 9 and 0 <= y < 9):
            return False
        if self.board[x][y] is not None:
            return False
        player_reserve = self.players[self.current_player]['reserve']
        if piece_type not in player_reserve or player_reserve[piece_type] <= 0:
            return False
        # Check if placing A/a (special rule)
        if piece_type.lower() == 'a':
            self.players[self.current_player]['has_placed_a'] = True
        return True
    
    def is_valid_move(self, x, y, new_x, new_y):
        if not (0 <= new_x < 9 and 0 <= new_y < 9):
            return False
        piece = self.board[x][y]
        if piece is None or piece.player != self.current_player:
            return False
        # Check if player has placed their A/a before capturing
        target_piece = self.board[new_x][new_y]
        if target_piece is not None and target_piece.player != self.current_player:
            if not self.players[self.current_player]['has_placed_a']:
                return False
        # Check movement rules
        moves = piece.get_moves(self.board, x, y)
        return (new_x, new_y) in moves
    
    def place_piece(self, piece_type, x, y):
        if not self.is_valid_place(piece_type, x, y):
            return False
        player_reserve = self.players[self.current_player]['reserve']
        player_reserve[piece_type] -= 1
        self.board[x][y] = Piece(piece_type, self.current_player)
        return True
    
    def move_piece(self, x, y, new_x, new_y):
        if not self.is_valid_move(x, y, new_x, new_y):
            return False
        piece = self.board[x][y]
        target_piece = self.board[new_x][new_y]
        
        # Capture logic
        if target_piece is not None:
            captured_type = target_piece.type
            # Add to reserve (convert to current player's case)
            if self.current_player == 1:
                reserve_type = captured_type.upper()
            else:
                reserve_type = captured_type.lower()
            self.players[self.current_player]['reserve'][reserve_type] += 1
            
            # Check win condition
            if (self.current_player == 1 and captured_type == 'a') or (self.current_player == 2 and captured_type == 'A'):
                self.winner = self.current_player
        
        # Move the piece
        self.board[x][y] = None
        self.board[new_x][new_y] = piece
        return True
    
    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
    
    def play(self):
        print("Welcome to Daisy!")
        print("Player 1: Uppercase (A-H)")
        print("Player 2: Lowercase (a-h)")
        print("Place pieces with 'place X Y', move with 'move X1 Y1 X2 Y2'")
        
        while self.winner is None:
            self.print_board()
            player = self.current_player
            print(f"Player {player}'s turn. Reserve: {self.players[player]['reserve']}")
            
            while True:
                cmd = input("> ").strip().split()
                if not cmd:
                    continue
                
                if cmd[0] == 'place' and len(cmd) == 3:
                    piece_type = cmd[1]
                    try:
                        x, y = map(int, cmd[2:])
                        if self.place_piece(piece_type, x, y):
                            break
                        else:
                            print("Invalid placement!")
                    except:
                        print("Invalid input!")
                
                elif cmd[0] == 'move' and len(cmd) == 5:
                    try:
                        x1, y1, x2, y2 = map(int, cmd[1:])
                        if self.move_piece(x1, y1, x2, y2):
                            break
                        else:
                            print("Invalid move!")
                    except:
                        print("Invalid input!")
                
                else:
                    print("Unknown command. Use 'place X Y' or 'move X1 Y1 X2 Y2'")
            
            self.switch_player()
        
        print(f"Player {self.winner} wins!")

if __name__ == "__main__":
    game = DaisyGame()
    game.play()
