from game import Game, Board, is_placement, get_move_elements

class Peridot(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 1 starts (represented as 0 to match API's integer expectation)
        self.current_player = 0  
        
    def validate_move(self, move: str) -> bool:
        # First, verify basic formatting and board bounds
        if not super().validate_move(move):
            return False
            
        if not is_placement(move):
            return False
            
        # Extract piece and position
        piece, (row, col) = get_move_elements(move)
        
        # Verify correct piece for current player
        if (self.current_player == 0 and piece != 'A') or \
           (self.current_player == 1 and piece != 'V'):
            return False
            
        # Verify space is blank
        return self.board.layout[row][col] == '_'
        
    def perform_move(self, move: str):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)
        
    def game_finished(self) -> bool:
        layout = self.board.layout
        
        # Check rows
        for row in layout:
            if row[0] in ('A', 'V') and all(cell == row[0] for cell in row):
                return True
                
        # Check columns
        for col in range(3):
            if layout[0][col] in ('A', 'V') and all(layout[row][col] == layout[0][col] for row in range(3)):
                return True
                
        # Check diagonals
        if layout[1][1] in ('A', 'V'):
            if (layout[0][0] == layout[1][1] == layout[2][2]) or \
               (layout[0][2] == layout[1][1] == layout[2][0]):
                return True
                
        # Check for tie (board full)
        return not any('_' in row for row in layout)
        
    def get_winner(self) -> int:
        layout = self.board.layout
        
        # Check rows
        for row in layout:
            if row[0] == 'A' and all(cell == 'A' for cell in row):
                return 0
            if row[0] == 'V' and all(cell == 'V' for cell in row):
                return 1
                
        # Check columns
        for col in range(3):
            if layout[0][col] == 'A' and all(layout[row][col] == 'A' for row in range(3)):
                return 0
            if layout[0][col] == 'V' and all(layout[row][col] == 'V' for row in range(3)):
                return 1
                
        # Check diagonals
        if layout[1][1] == 'A':
            if (layout[0][0] == layout[1][1] == layout[2][2]) or \
               (layout[0][2] == layout[1][1] == layout[2][0]):
                return 0
        elif layout[1][1] == 'V':
            if (layout[0][0] == layout[1][1] == layout[2][2]) or \
               (layout[0][2] == layout[1][1] == layout[2][0]):
                return 1
                
        return None  # No winner yet or tie
        
    def prompt_current_player(self) -> str:
        piece = 'A' if self.current_player == 0 else 'V'
        while True:
            move = input(f"Player {self.current_player + 1} ({piece}), enter your move (e.g., 'A 1,1'): ")
            move = move.strip().upper()
            if is_placement(move):
                return move
            print("Invalid format. Please use 'P row,col' (e.g., 'A 1,1')")
            
    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a tie!")

if __name__ == '__main__':
    # Initialize 3x3 blank board (underscores represent empty spaces)
    board = Board((3, 3), layout="___\n___\n___")
    game = Peridot(board)
    game.game_loop()
