from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Topaz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = ['A', 'B']
        self.current_player = 0  # Player 1 (A) starts
        self.phase = 'placement'
        self.pieces_placed = {'A': 0, 'B': 0}
        self.total_pieces = 9
        self.last_move_position = None  # Track position for capture checks

    def initial_player(self):
        return 0  # Player A starts

    def prompt_current_player(self):
        player = self.players[self.current_player]
        if self.phase == 'placement':
            return input(f"Player {player}, enter placement (e.g., 'A 2,3'): ")
        else:
            return input(f"Player {player}, enter movement (e.g., '2,3 3,3'): ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        player = self.players[self.current_player]
        try:
            if self.phase == 'placement':
                if not is_placement(move):
                    return False
                piece, (row, col) = get_move_elements(move)
                if piece != player:
                    return False
                if not self._is_free_space(row, col):
                    return False
            else:  # movement phase
                if not is_movement(move):
                    return False
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                if self.board.layout[from_row][from_col] != player:
                    return False
                if not self._is_adjacent_move(from_row, from_col, to_row, to_col):
                    return False
                if not self._is_free_space(to_row, to_col):
                    return False
            return True
        except (ValueError, IndexError):
            return False

    def perform_move(self, move):
        player = self.players[self.current_player]
        if self.phase == 'placement':
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_placed[player] += 1
            self.last_move_position = (row, col)
            
            # Check if all pieces are placed
            if all(placed == self.total_pieces for placed in self.pieces_placed.values()):
                self.phase = 'movement'
        else:  # movement phase
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            self.board.move_piece(move)
            self.last_move_position = (to_row, to_col)

    def _is_free_space(self, row, col):
        """Check if position is valid and free (underscore)"""
        try:
            return self.board.layout[row][col] == '_'
        except IndexError:
            return False

    def _is_adjacent_move(self, from_row, from_col, to_row, to_col):
        """Check if move is to an adjacent orthogonal space"""
        return (abs(from_row - to_row) == 1 and from_col == to_col) or \
               (abs(from_col - to_col) == 1 and from_row == to_row)

    def game_finished(self):
        if self.phase != 'movement':
            return False
        
        opponent = self.players[1 - self.current_player]
        opponent_pieces = np.count_nonzero(self.board.layout == opponent)
        
        # Win if opponent has <= 2 pieces
        if opponent_pieces <= 2:
            return True
        
        # Win if opponent cannot move
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.layout[r][c] == opponent:
                    # Check adjacent spaces
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.board.height and 0 <= nc < self.board.width:
                            if self.board.layout[nr][nc] == '_':
                                return False
        return True

    def get_winner(self):
        if not self.game_finished():
            return None
            
        opponent_idx = 1 - self.current_player
        return self.current_player  # Current player wins

    def next_player(self):
        # Check if capture is possible before switching players
        if self.last_move_position and self._check_capture(*self.last_move_position):
            self._handle_capture()
            return self.current_player  # Same player gets another turn
        return 1 - self.current_player

    def _check_capture(self, row, col):
        """Check if the last move created a 3-in-a-row/column"""
        player = self.players[self.current_player]
        directions = [
            [(0, -1), (0, 1)],  # Horizontal
            [(-1, 0), (1, 0)]    # Vertical
        ]

        for axis in directions:
            count = 1  # Current piece
            for dr, dc in axis[0]:  # Check one direction
                r, c = row + dr, col + dc
                while self._is_player_piece(r, c, player):
                    count += 1
                    r += dr
                    c += dc
            for dr, dc in axis[1]:  # Check opposite direction
                r, c = row + dr, col + dc
                while self._is_player_piece(r, c, player):
                    count += 1
                    r += dr
                    c += dc
            if count >= 3:
                return True
        return False

    def _is_player_piece(self, row, col, player):
        """Helper to check if position contains player's piece"""
        try:
            return self.board.layout[row][col] == player
        except IndexError:
            return False

    def _handle_capture(self):
        """Prompt player to capture an opponent piece"""
        opponent = self.players[1 - self.current_player]
        print(self.board)
        print(f"Player {self.players[self.current_player]}, you can capture an opponent piece!")
        
        while True:
            try:
                move = input(f"Enter position to capture (e.g., '2,3'): ")
                if ',' in move:
                    row, col = map(int, move.split(','))
                    if self._is_player_piece(row, col, opponent):
                        self.board.place_piece(f'_ {row},{col}')  # Replace with blank
                        print("Capture successful!")
                        break
                print("Invalid capture. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Try again.")

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {self.players[winner]} wins!")
        else:
            print("Game ended in a draw.")

if __name__ == '__main__':
    # Create initial board layout
    layout_str = """   _  _  _
     _ _ _ 
      ___  
    ___ ___
      ___  
     _ _ _ 
    _  _  _"""
    
    # Convert to proper layout string for Board class
    layout_lines = [line.strip() for line in layout_str.split('\n')]
    layout = '\n'.join(line.ljust(7) for line in layout_lines)
    
    board = Board((7,7), layout)
    game = Topaz(board)
    game.game_loop()
