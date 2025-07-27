class VioletGame:
    def __init__(self):
        self.board_size = 10
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
        # Initialize pieces
        self.initialize_pieces()
        
    def initialize_pieces(self):
        # Player 2's V pieces
        v_positions = [(0, 3), (0, 6), (3, 0), (3, 9)]
        for pos in v_positions:
            self.board[pos[0]][pos[1]] = ('V', 2)
            
        # Player 1's A pieces
        a_positions = [(6, 0), (6, 9), (9, 3), (9, 6)]
        for pos in a_positions:
            self.board[pos[0]][pos[1]] = ('A', 1)
    
    def get_player_pieces(self, player):
        pieces = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] and self.board[i][j][1] == player:
                    pieces.append((i, j))
        return pieces
    
    def is_valid_move(self, start, end, player):
        # Check if start position has player's piece
        if not (0 <= start[0] < self.board_size and 0 <= start[1] < self.board_size):
            return False
            
        piece = self.board[start[0]][start[1]]
        if not piece or piece[1] != player:
            return False
            
        # Check if end position is empty and within bounds
        if not (0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size):
            return False
        if self.board[end[0]][end[1]] is not None:
            return False
            
        # Check if path is clear
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # Normalize direction (either -1, 0, or 1)
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        # Check all positions along the path except start and end
        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] or y != end[1]:
            if self.board[x][y] is not None:
                return False
            x += step_x
            y += step_y
            
        return True
    
    def is_valid_shot(self, shooter_pos, shot_pos):
        # Check if shot position is in line of sight from shooter
        if not (0 <= shot_pos[0] < self.board_size and 0 <= shot_pos[1] < self.board_size):
            return False
        if self.board[shot_pos[0]][shot_pos[1]] is not None:
            return False
            
        dx = shot_pos[0] - shooter_pos[0]
        dy = shot_pos[1] - shooter_pos[1]
        
        # Must be in same row, column, or diagonal
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
            
        # Check if path is clear
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        x, y = shooter_pos[0] + step_x, shooter_pos[1] + step_y
        while x != shot_pos[0] or y != shot_pos[1]:
            if self.board[x][y] is not None:
                return False
            x += step_x
            y += step_y
            
        return True
    
    def has_valid_moves(self, player):
        pieces = self.get_player_pieces(player)
        for piece_pos in pieces:
            # Check all possible moves for this piece
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip no movement
                        
                    # Check in this direction until we hit something
                    x, y = piece_pos[0] + dx, piece_pos[1] + dy
                    while 0 <= x < self.board_size and 0 <= y < self.board_size:
                        if self.board[x][y] is None:
                            # Found a valid move
                            return True
                        else:
                            break  # Path blocked
                        x += dx
                        y += dy
        return False
    
    def make_move(self, start_pos, end_pos, shot_pos):
        player = self.current_player
        piece_type = 'A' if player == 1 else 'V'
        
        # Validate move
        if not self.is_valid_move(start_pos, end_pos, player):
            return False, "Invalid move"
            
        # Validate shot
        if not self.is_valid_shot(end_pos, shot_pos):
            return False, "Invalid shot position"
            
        # Execute move
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = None
        self.board[end_pos[0]][end_pos[1]] = piece
        
        # Place X
        self.board[shot_pos[0]][shot_pos[1]] = ('X', 0)
        
        # Check if opponent has moves left
        opponent = 3 - player  # 1 -> 2, 2 -> 1
        if not self.has_valid_moves(opponent):
            self.game_over = True
            self.winner = player
            
        # Switch player if game isn't over
        if not self.game_over:
            self.current_player = opponent
            
        return True, "Move successful"
    
    def print_board(self):
        print("   " + " ".join(str(i) for i in range(self.board_size)))
        for i in range(self.board_size):
            row = [str(i) + " "]
            for j in range(self.board_size):
                if self.board[i][j] is None:
                    row.append("·")
                else:
                    piece, player = self.board[i][j]
                    if player == 0:  # X
                        row.append("X")
                    else:
                        row.append(f"{piece}{player}")
            print(" ".join(row))
        print()


# Example usage:
if __name__ == "__main__":
    game = VioletGame()
    print("Initial board:")
    game.print_board()
    
    # Example moves
    print("Player 1 moves A from (6,0) to (5,1) and shoots X to (4,2)")
    success, message = game.make_move((6, 0), (5, 1), (4, 2))
    print(message)
    game.print_board()
    
    if not game.game_over:
        print("Player 2 moves V from (0,3) to (1,2) and shoots X to (2,1)")
        success, message = game.make_move((0, 3), (1, 2), (2, 1))
        print(message)
        game.print_board()
