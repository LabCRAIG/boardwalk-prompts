from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum

class Player(Enum):
    X = 0
    O = 1

class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pieces = ['X', 'O']
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        # Only allow placements, not movements
        if not is_placement(move):
            return False
            
        # Extract the piece and position from the move
        piece, position = get_move_elements(move)
        
        # Verify that the piece belongs to the current player
        if piece != self.pieces[self.current_player]:
            return False
            
        # Check if the target position is empty
        row, col = position
        return self.board.layout[row][col] == '_'
    
    def game_finished(self):
        # Check if the game is won
        if self._check_win():
            return True
            
        # Check if the board is full (draw)
        for row in self.board.layout:
            for cell in row:
                if cell == '_':
                    return False
        return True
    
    def get_winner(self):
        # If previous player made a winning move
        if self._check_win():
            # Previous player is the winner
            return (self.current_player - 1) % 2
        # If no winner but game is finished, it's a draw
        return None
    
    def next_player(self):
        return (self.current_player + 1) % 2
    
    def _check_win(self):
        # Check for 5 in a row horizontally, vertically, and diagonally
        board = self.board.layout
        height, width = self.board.height, self.board.width
        
        # Check horizontal lines
        for row in range(height):
            for col in range(width - 4):
                if (board[row][col] != '_' and
                    board[row][col] == board[row][col+1] == board[row][col+2] == 
                    board[row][col+3] == board[row][col+4]):
                    return True
        
        # Check vertical lines
        for col in range(width):
            for row in range(height - 4):
                if (board[row][col] != '_' and
                    board[row][col] == board[row+1][col] == board[row+2][col] == 
                    board[row+3][col] == board[row+4][col]):
                    return True
        
        # Check diagonal lines (top-left to bottom-right)
        for row in range(height - 4):
            for col in range(width - 4):
                if (board[row][col] != '_' and
                    board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 
                    board[row+3][col+3] == board[row+4][col+4]):
                    return True
        
        # Check diagonal lines (bottom-left to top-right)
        for row in range(4, height):
            for col in range(width - 4):
                if (board[row][col] != '_' and
                    board[row][col] == board[row-1][col+1] == board[row-2][col+2] == 
                    board[row-3][col+3] == board[row-4][col+4]):
                    return True
        
        return False
    
    def prompt_current_player(self):
        player_symbol = self.pieces[self.current_player]
        move = input(f"Player {player_symbol}'s turn. Enter position (row,col): ")
        # Convert to standard move format
        try:
            row, col = map(int, move.split(','))
            return f"{player_symbol} {row},{col}"
        except ValueError:
            # If input doesn't match expected format, return an invalid move
            # that will fail validation
            return move
    
    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {self.pieces[winner]} wins!")
        else:
            print("Game ended in a draw!")

if __name__ == '__main__':
    board = Board((5, 5))
    game = TicTacToe(board)
    game.game_loop()