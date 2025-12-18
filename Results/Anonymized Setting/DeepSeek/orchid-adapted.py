from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Orchid(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 'A'  # Player 1 is 'A', Player 2 is 'B'
        self.phase = 1  # 1: placement, 2: movement
        self.pieces_to_place = {'A': 12, 'B': 12}
        self.placements_this_turn = 0
        
    def prompt_current_player(self):
        if self.phase == 1:
            pieces_left = self.pieces_to_place[self.current_player]
            placements = min(2, pieces_left)
            print(f"Player {self.current_player}'s turn (Placement Phase)")
            print(f"Place {placements} piece(s) (format: 'X row,col')")
            print(f"Pieces left: A: {self.pieces_to_place['A']}, B: {self.pieces_to_place['B']}")
        else:
            print(f"Player {self.current_player}'s turn (Movement Phase)")
            print("Enter move (format: 'from_row,col to_row,col')")
        return input("Your move: ").strip()
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if self.phase == 1:
            if not is_placement(move):
                return False
            piece, (row, col) = get_move_elements(move)
            if piece != self.current_player:
                return False
            if not (0 <= row < 5 and 0 <= col < 5):
                return False
            if self.board.layout[row, col] != '_':
                return False
            if row == 2 and col == 2:  # Center is forbidden
                return False
            if self.pieces_to_place[self.current_player] <= 0:
                return False
            return True
        else:
            if not is_movement(move):
                return False
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            if not (0 <= from_row < 5 and 0 <= from_col < 5):
                return False
            if not (0 <= to_row < 5 and 0 <= to_col < 5):
                return False
            if self.board.layout[from_row, from_col] != self.current_player:
                return False
            if self.board.layout[to_row, to_col] != '_':
                return False
            if from_row != to_row and from_col != to_col:  # Must move orthogonally
                return False
            
            # Check path is clear
            if from_row == to_row:  # Horizontal move
                step = 1 if to_col > from_col else -1
                for col in range(from_col + step, to_col, step):
                    if self.board.layout[from_row, col] != '_':
                        return False
            else:  # Vertical move
                step = 1 if to_row > from_row else -1
                for row in range(from_row + step, to_row, step):
                    if self.board.layout[row, from_col] != '_':
                        return False
            return True
    
    def perform_move(self, move):
        if self.phase == 1:
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_to_place[self.current_player] -= 1
            self.placements_this_turn += 1
            
            # Check if all pieces are placed
            if all(count == 0 for count in self.pieces_to_place.values()):
                self.phase = 2
        else:
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            self.board.move_piece(move)
            self.check_captures(to_row, to_col)
    
    def check_captures(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        opponent = 'B' if self.current_player == 'A' else 'A'
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_capture = []
            
            while 0 <= r < 5 and 0 <= c < 5:
                if self.board.layout[r, c] == opponent:
                    to_capture.append((r, c))
                    r += dr
                    c += dc
                elif self.board.layout[r, c] == self.current_player:
                    # Capture all pieces in to_capture
                    for cap_r, cap_c in to_capture:
                        self.board.layout[cap_r, cap_c] = '_'
                    break
                else:
                    break
    
    def game_finished(self):
        a_count = np.count_nonzero(self.board.layout == 'A')
        b_count = np.count_nonzero(self.board.layout == 'B')
        return a_count == 0 or b_count == 0 or not self.has_valid_moves()
    
    def get_winner(self):
        a_count = np.count_nonzero(self.board.layout == 'A')
        b_count = np.count_nonzero(self.board.layout == 'B')
        
        if a_count == 0:
            return 'B'
        if b_count == 0:
            return 'A'
        return None
    
    def has_valid_moves(self):
        if self.phase == 1:
            return self.pieces_to_place[self.current_player] > 0
        
        # Check if current player has any valid moves
        player_positions = np.argwhere(self.board.layout == self.current_player)
        for (row, col) in player_positions:
            # Check all four directions
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                distance = 1
                while True:
                    new_row, new_col = row + dr * distance, col + dc * distance
                    if not (0 <= new_row < 5 and 0 <= new_col < 5):
                        break
                    if self.board.layout[new_row, new_col] != '_':
                        break
                    return True  # Found at least one valid move
                    distance += 1
        return False
    
    def next_player(self):
        if self.phase == 1:
            if self.placements_this_turn >= min(2, self.pieces_to_place[self.current_player]):
                self.placements_this_turn = 0
                return 'B' if self.current_player == 'A' else 'A'
            return self.current_player
        else:
            if self.has_valid_moves():
                return 'B' if self.current_player == 'A' else 'A'
            return self.current_player  # Player gets another turn if opponent has no moves
    
    def finish_message(self, winner):
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("The game ended in a draw!")

if __name__ == '__main__':
    # Initialize 5x5 board with all blank spaces
    board = Board((5, 5))
    game = Orchid(board)
    print("Welcome to Orchid!")
    print("Player 1: A")
    print("Player 2: B")
    print("Phase 1: Placement phase - place two pieces per turn (except center)")
    print("Phase 2: Movement phase - move one piece orthogonally to capture opponent's pieces")
    print()
    game.game_loop()
