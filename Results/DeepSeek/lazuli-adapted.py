from game import Game, Board, is_movement, is_placement, get_move_elements

class Lazuli(Game):
    def __init__(self):
        # Create initial board layout
        layout = []
        for i in range(7):
            row = []
            for j in range(7):
                # Nullify the 2x2 corners
                if (i < 2 and j < 2) or (i < 2 and j > 4) or (i > 4 and j < 2) or (i > 4 and j > 4):
                    row.append(' ')
                else:
                    row.append('X')
            layout.append(''.join(row))
        # Empty the center
        layout[3] = layout[3][:3] + '_' + layout[3][4:]
        
        # Initialize board with the layout string
        board = Board((7, 7), '\n'.join(layout))
        super().__init__(board)
        
    def validate_move(self, move):
        if not is_movement(move):
            return False
            
        (x1, y1), (x2, y2) = get_move_elements(move)
        
        # Check bounds
        if not (0 <= x1 < 7 and 0 <= y1 < 7 and 0 <= x2 < 7 and 0 <= y2 < 7):
            return False
            
        # Check piece at origin and empty destination
        if self.board.layout[x1][y1] != 'X' or self.board.layout[x2][y2] != '_':
            return False
            
        # Check valid jump (2 spaces in one direction)
        if abs(x1 - x2) == 2 and y1 == y2:  # Vertical jump
            mid_x = (x1 + x2) // 2
            return self.board.layout[mid_x][y1] == 'X'
        elif abs(y1 - y2) == 2 and x1 == x2:  # Horizontal jump
            mid_y = (y1 + y2) // 2
            return self.board.layout[x1][mid_y] == 'X'
            
        return False

    def perform_move(self, move):
        (x1, y1), (x2, y2) = get_move_elements(move)
        
        # Move the piece
        self.board.move_piece(f"{x1},{y1} {x2},{y2}")
        
        # Remove the jumped piece
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        self.board.place_piece(f"_ {mid_x},{mid_y}")

    def game_finished(self):
        # Check win condition first
        if self.check_win():
            return True
        # Then check loss condition
        return self.check_loss()

    def get_winner(self):
        return 1 if self.check_win() else None

    def check_win(self):
        # Count remaining pieces
        pieces = sum(cell == 'X' for row in self.board.layout for cell in row)
        return pieces == 1 and self.board.layout[3][3] == 'X'

    def check_loss(self):
        # Check if any valid moves remain
        for i in range(7):
            for j in range(7):
                if self.board.layout[i][j] == 'X':
                    # Check all possible jumps
                    for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                        x2, y2 = i + dx, j + dy
                        if 0 <= x2 < 7 and 0 <= y2 < 7:
                            test_move = f"{i},{j} {x2},{y2}"
                            if self.validate_move(test_move):
                                return False
        return True

    def prompt_current_player(self):
        print("Enter your move (e.g., '3,1 3,3')")
        return super().prompt_current_player()

    def finish_message(self, winner):
        if winner:
            print("\nCongratulations! You won!")
        else:
            print("\nNo valid moves left. You lost!")

if __name__ == "__main__":
    game = Lazuli()
    game.game_loop()