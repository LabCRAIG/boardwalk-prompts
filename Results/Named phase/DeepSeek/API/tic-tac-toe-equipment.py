from game import Game, Board, is_movement, is_placement, get_move_elements

class TicTacToe5x5(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 0 uses 'X', Player 1 uses 'O'
        self.players = {0: 'X', 1: 'O'}
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            # Check if position is blank and piece belongs to current player
            if (self.board.layout[row, col] != '_' or 
                piece != self.players[self.current_player]):
                return False
            return True
            
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            # Check if origin has current player's piece and destination is blank
            if (self.board.layout[from_row, from_col] != self.players[self.current_player] or 
                self.board.layout[to_row, to_col] != '_'):
                return False
            return True
            
        return False
    
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            self.board.move_piece(move)
    
    def game_finished(self):
        # Check all possible 5-in-a-row lines
        board = self.board.layout
        
        # Check rows
        for row in range(5):
            for start_col in range(1):  # Only need to check starting at col 0
                if (board[row, start_col] != '_' and
                    board[row, start_col] == board[row, start_col+1] == 
                    board[row, start_col+2] == board[row, start_col+3] == 
                    board[row, start_col+4]):
                    return True
        
        # Check columns
        for col in range(5):
            for start_row in range(1):  # Only need to check starting at row 0
                if (board[start_row, col] != '_' and
                    board[start_row, col] == board[start_row+1, col] == 
                    board[start_row+2, col] == board[start_row+3, col] == 
                    board[start_row+4, col]):
                    return True
        
        # Check diagonals (top-left to bottom-right)
        for row in range(1):
            for col in range(1):
                if (board[row, col] != '_' and
                    board[row, col] == board[row+1, col+1] == 
                    board[row+2, col+2] == board[row+3, col+3] == 
                    board[row+4, col+4]):
                    return True
        
        # Check diagonals (top-right to bottom-left)
        for row in range(1):
            for col in range(4, 5):
                if (board[row, col] != '_' and
                    board[row, col] == board[row+1, col-1] == 
                    board[row+2, col-2] == board[row+3, col-3] == 
                    board[row+4, col-4]):
                    return True
        
        # Check if board is full (draw)
        return '_' not in board
    
    def get_winner(self):
        board = self.board.layout
        players = {'X': 0, 'O': 1}
        
        # Check rows
        for row in range(5):
            for start_col in range(1):
                if (board[row, start_col] != '_' and
                    board[row, start_col] == board[row, start_col+1] == 
                    board[row, start_col+2] == board[row, start_col+3] == 
                    board[row, start_col+4]):
                    return players[board[row, start_col]]
        
        # Check columns
        for col in range(5):
            for start_row in range(1):
                if (board[start_row, col] != '_' and
                    board[start_row, col] == board[start_row+1, col] == 
                    board[start_row+2, col] == board[start_row+3, col] == 
                    board[start_row+4, col]):
                    return players[board[start_row, col]]
        
        # Check diagonals
        for row in range(1):
            for col in range(1):
                if (board[row, col] != '_' and
                    board[row, col] == board[row+1, col+1] == 
                    board[row+2, col+2] == board[row+3, col+3] == 
                    board[row+4, col+4]):
                    return players[board[row, col]]
        
        for row in range(1):
            for col in range(4, 5):
                if (board[row, col] != '_' and
                    board[row, col] == board[row+1, col-1] == 
                    board[row+2, col-2] == board[row+3, col-3] == 
                    board[row+4, col-4]):
                    return players[board[row, col]]
        
        return None  # Draw
    
    def next_player(self):
        return 1 if self.current_player == 0 else 0
    
    def initial_player(self):
        return 0
    
    def prompt_current_player(self):
        player_char = self.players[self.current_player]
        return input(f"Player {self.current_player} ({player_char}), enter your move: ")
    
    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} ({self.players[winner]}) wins!")

if __name__ == '__main__':
    board = Board((5, 5))
    mygame = TicTacToe5x5(board)
    mygame.game_loop()