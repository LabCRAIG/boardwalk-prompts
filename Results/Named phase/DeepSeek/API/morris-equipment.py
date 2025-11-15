from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    WHITE = 0
    BLACK = 1

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.initial_player()
        self.white_pieces = 9
        self.black_pieces = 9
        self.white_on_board = 0
        self.black_on_board = 0
        self.phase = "placement"  # placement, movement, flying
        self.mill_formed = False

    def initial_player(self):
        return Player.WHITE.value

    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"Player {player_name}, enter your move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        try:
            if is_placement(move):
                if self.phase != "placement":
                    return False
                
                piece, (row, col) = get_move_elements(move)
                if piece != self._get_piece_char():
                    return False
                
                if self.board.layout[row, col] != '_':
                    return False
                
                return True

            elif is_movement(move):
                if self.phase == "placement":
                    return False
                
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                
                if self.board.layout[from_row, from_col] != self._get_piece_char():
                    return False
                
                if self.board.layout[to_row, to_col] != '_':
                    return False
                
                if self.phase == "movement" and not self._are_adjacent((from_row, from_col), (to_row, to_col)):
                    return False
                
                return True

        except (ValueError, IndexError):
            return False
        
        return False

    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            if self.current_player == Player.WHITE.value:
                self.white_pieces -= 1
                self.white_on_board += 1
            else:
                self.black_pieces -= 1
                self.black_on_board += 1
            
            if self._forms_mill(row, col):
                self.mill_formed = True
                return
            
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            self.board.move_piece(move)
            
            if self._forms_mill(to_row, to_col):
                self.mill_formed = True
                return
        
        self.mill_formed = False
        self._update_phase()

    def _update_phase(self):
        if self.phase == "placement" and self.white_pieces == 0 and self.black_pieces == 0:
            self.phase = "movement"
        
        if self.phase == "movement":
            if self.white_on_board <= 3:
                self.phase = "flying"
            elif self.black_on_board <= 3:
                self.phase = "flying"

    def _get_piece_char(self):
        return 'W' if self.current_player == Player.WHITE.value else 'B'

    def _are_adjacent(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            return True
        
        if (r1 == 3 and c1 == 3) or (r2 == 3 and c2 == 3):
            return True
        
        return False

    def _forms_mill(self, row, col):
        piece = self._get_piece_char()
        
        if row == 3 and col == 3:
            return False
        
        if row % 2 == 1 and col % 2 == 1:
            if row == 1 and col == 1:
                return (self.board.layout[1, 0] == piece and self.board.layout[1, 2] == piece) or \
                       (self.board.layout[0, 1] == piece and self.board.layout[2, 1] == piece)
            elif row == 1 and col == 5:
                return (self.board.layout[1, 4] == piece and self.board.layout[1, 6] == piece) or \
                       (self.board.layout[0, 5] == piece and self.board.layout[2, 5] == piece)
            elif row == 5 and col == 1:
                return (self.board.layout[5, 0] == piece and self.board.layout[5, 2] == piece) or \
                       (self.board.layout[4, 1] == piece and self.board.layout[6, 1] == piece)
            elif row == 5 and col == 5:
                return (self.board.layout[5, 4] == piece and self.board.layout[5, 6] == piece) or \
                       (self.board.layout[4, 5] == piece and self.board.layout[6, 5] == piece)
        
        return False

    def game_finished(self):
        if self.white_on_board < 3 or self.black_on_board < 3:
            return True
        return False

    def get_winner(self):
        if self.white_on_board < 3:
            return Player.BLACK.value
        elif self.black_on_board < 3:
            return Player.WHITE.value
        return None

    def next_player(self):
        if self.mill_formed:
            return self.current_player
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value

    def round_counter(self):
        if self.mill_formed:
            return self.round
        return self.round + 1

    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    board_layout = """\
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _"""
    board = Board((7, 7), board_layout)
    mygame = NineMensMorris(board)
    mygame.game_loop()