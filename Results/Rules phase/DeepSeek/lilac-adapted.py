from game import Game, Board, is_movement, is_placement, get_move_elements

class Lilac(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def initial_player(self):
        return 1  # Player 1 starts
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_movement(move):
            return False  # Lilac only allows movements
            
        (from_pos, to_pos) = get_move_elements(move)
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Check piece ownership
        piece = self.board.layout[from_x][from_y]
        if self.current_player == 1 and piece != 'V':
            return False
        if self.current_player == 2 and piece not in ('A', 'Â'):
            return False
            
        # Check orthogonal movement
        if not (abs(from_x - to_x) == 1 and from_y == to_y) or (abs(from_y - to_y) == 1 and from_x == to_x):
            return False
            
        # Check destination is empty
        if self.board.layout[to_x][to_y] != '_':
            return False
            
        # Special case for center (only Â can be there)
        if to_x == 3 and to_y == 3 and piece != 'Â':
            return False
            
        return True
    
    def perform_move(self, move):
        (from_pos, to_pos) = get_move_elements(move)
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        piece = self.board.layout[from_x][from_y]
        
        # Perform the move
        self.board.move_piece(move)
        
        # Check for captures
        self._check_captures(to_x, to_y)
        
        # Check win conditions
        self._check_win_conditions()
        
    def _check_captures(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        opponent = 'A' if self.current_player == 1 else 'V'
        
        for dx, dy in directions:
            nx1, ny1 = x + dx, y + dy
            nx2, ny2 = x - dx, y - dy
            
            if (0 <= nx1 < 7 and 0 <= ny1 < 7 and 
                0 <= nx2 < 7 and 0 <= ny2 < 7):
                piece1 = self.board.layout[nx1][ny1]
                piece2 = self.board.layout[nx2][ny2]
                
                if piece1 == opponent and piece2 == opponent:
                    captured_piece = self.board.layout[x][y]
                    if captured_piece in ['V', 'A', 'Â']:
                        self.board.place_piece(f'_ {x},{y}')
    
    def _check_win_conditions(self):
        # Find Â position
        â_pos = None
        for i in range(7):
            for j in range(7):
                if self.board.layout[i][j] == 'Â':
                    â_pos = (i, j)
                    break
            if â_pos:
                break
        
        # Player 1 wins if Â is captured
        if not â_pos:
            self.game_over = True
            self.winner = 1
            return
            
        # Player 2 wins if Â reaches border
        if â_pos[0] in (0, 6) or â_pos[1] in (0, 6):
            self.game_over = True
            self.winner = 2
            return
    
    def game_finished(self):
        return self.game_over
        
    def get_winner(self):
        return self.winner
        
    def next_player(self):
        return 3 - self.current_player if not self.game_over else self.current_player
        
    def prompt_current_player(self):
        self.print_board()
        player_pieces = "V's" if self.current_player == 1 else "A's and Â"
        print(f"Player {self.current_player}'s turn ({player_pieces})")
        while True:
            try:
                from_x, from_y = map(int, input("Enter piece to move (row col, 0-6): ").split())
                to_x, to_y = map(int, input("Enter destination (row col, 0-6): ").split())
                return f"{from_x},{from_y} {to_x},{to_y}"
            except ValueError:
                print("Please enter two numbers separated by a space.")
    
    def print_board(self):
        print("\nCurrent Board:")
        for row in self.board.layout:
            print(" ".join(piece if piece != '_' else '_' for piece in row))
        print()

if __name__ == '__main__':
    initial_layout = (
        "_VVV___\n"
        "___V___\n"
        "V_AAA_V\n"
        "VVAÂAVV\n"
        "V_AAA_V\n"
        "___V___\n"
        "_VVV___"
    )
    board = Board((7, 7), initial_layout)
    game = Lilac(board)
    game.game_loop()