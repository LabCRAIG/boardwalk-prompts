from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts (X)
        
    def initial_player(self):
        return 1
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            # Check if position is empty
            if self.board.layout[row, col] != '_':
                return False
            # Check if correct piece for current player
            if (self.current_player == 1 and piece != 'X') or (self.current_player == 2 and piece != 'O'):
                return False
            return True
            
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            # Check if origin has current player's piece
            if (self.current_player == 1 and self.board.layout[from_row, from_col] != 'X') or \
               (self.current_player == 2 and self.board.layout[from_row, from_col] != 'O'):
                return False
            # Check if destination is empty
            if self.board.layout[to_row, to_col] != '_':
                return False
            return True
            
        return False
        
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            # Move piece and leave blank at origin
            self.board.move_piece(move)
            
    def game_finished(self):
        # Check rows
        for row in range(3):
            if self.board.layout[row, 0] != '_' and \
               self.board.layout[row, 0] == self.board.layout[row, 1] == self.board.layout[row, 2]:
                return True
                
        # Check columns
        for col in range(3):
            if self.board.layout[0, col] != '_' and \
               self.board.layout[0, col] == self.board.layout[1, col] == self.board.layout[2, col]:
                return True
                
        # Check 2x2 squares
        for top_row in range(2):
            for left_col in range(2):
                square = self.board.layout[top_row:top_row+2, left_col:left_col+2]
                if np.all(square == 'X') or np.all(square == 'O'):
                    return True
                    
        # Check if board is full (draw)
        if np.all(self.board.layout != '_'):
            return True
            
        return False
        
    def get_winner(self):
        # Check rows
        for row in range(3):
            if self.board.layout[row, 0] != '_' and \
               self.board.layout[row, 0] == self.board.layout[row, 1] == self.board.layout[row, 2]:
                return 1 if self.board.layout[row, 0] == 'X' else 2
                
        # Check columns
        for col in range(3):
            if self.board.layout[0, col] != '_' and \
               self.board.layout[0, col] == self.board.layout[1, col] == self.board.layout[2, col]:
                return 1 if self.board.layout[0, col] == 'X' else 2
                
        # Check 2x2 squares
        for top_row in range(2):
            for left_col in range(2):
                square = self.board.layout[top_row:top_row+2, left_col:left_col+2]
                if np.all(square == 'X'):
                    return 1
                elif np.all(square == 'O'):
                    return 2
                    
        # Draw
        return None
        
    def next_player(self):
        return 2 if self.current_player == 1 else 1
        
    def prompt_current_player(self):
        player_char = 'X' if self.current_player == 1 else 'O'
        move_type = input(f"Player {self.current_player} ({player_char}), choose move type (P for placement, M for movement): ").upper()
        
        if move_type == 'P':
            pos = input("Enter position (row,col): ")
            return f"{player_char} {pos}"
        elif move_type == 'M':
            from_pos = input("Enter origin position (row,col): ")
            to_pos = input("Enter destination position (row,col): ")
            return f"{from_pos} {to_pos}"
        else:
            return ""
            
    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} wins!")

if __name__ == '__main__':
    board = Board((3, 3))
    mygame = TicTacToe(board)
    mygame.game_loop()