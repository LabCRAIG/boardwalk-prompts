
from game import Game, Board, is_movement, is_placement, get_move_elements
from copy import deepcopy
import numpy as np

# Game subclass definition
class ReversiWithKing(Game):
    def __init__(self, board):
        super().__init__(board)
        self.kings_played = {0: False, 1: False}  # Tracks if each player has played their king
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if is_placement(move):
            piece, position = get_move_elements(move)
            if piece not in {'X', 'O', 'K', 'Q'}:  # X and K for player 0, O and Q for player 1
                return False
            if self.board.layout[position] != '_':  # Ensure the space is blank
                return False
            if piece in {'K', 'Q'}:  # Check king placement rules
                current_player_king = 'K' if self.current_player == 0 else 'Q'
                if self.kings_played[self.current_player] or piece != current_player_king:
                    return False
        elif is_movement(move):
            origin, destination = get_move_elements(move)
            if self.board.layout[origin].upper() not in {'X', 'O', 'K', 'Q'}:
                return False
            if self.board.layout[destination] != '_':  # Ensure the destination is blank
                return False
        else:
            return False
        
        return True

    def perform_move(self, move):
        if is_placement(move):
            piece, position = get_move_elements(move)
            self.board.place_piece(move)
            if piece in {'K', 'Q'}:  # Mark king as played
                self.kings_played[self.current_player] = True
            self.flip_pieces(position)
        elif is_movement(move):
            origin, destination = get_move_elements(move)
            self.board.move_piece(move)
            self.flip_pieces(destination)

    def flip_pieces(self, position):
        current_piece = 'X' if self.current_player == 0 else 'O'
        opponent_piece = 'O' if self.current_player == 0 else 'X'
        opponent_king = 'Q' if self.current_player == 0 else 'K'

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            to_flip = []
            x, y = position
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < self.board.height and 0 <= y < self.board.width):
                    break
                cell = self.board.layout[x, y]
                if cell == current_piece:
                    for fx, fy in to_flip:
                        self.board.layout[fx, fy] = current_piece
                    break
                elif cell == opponent_piece:
                    to_flip.append((x, y))
                elif cell == opponent_king:  # Stop flipping if the line contains the opponent's king
                    break
                else:
                    break

    def game_finished(self):
        # The game ends when no valid moves are available for either player or the board is full
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == '_':  # Empty space available
                    return False
        return True

    def get_winner(self):
        # Count pieces for each player
        counts = {'X': 0, 'O': 0}
        for row in self.board.layout:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return 0 if counts['X'] > counts['O'] else 1 if counts['O'] > counts['X'] else None

    def next_player(self):
        return 1 - self.current_player  # Alternate between player 0 and 1

if __name__ == '__main__':
    initial_layout = (
        '________\n'
        '________\n'
        '________\n'
        '___OX___\n'
        '___XO___\n'
        '________\n'
        '________\n'
        '________'
    )
    board = Board((8, 8), initial_layout)
    reversi_game = ReversiWithKing(board)
    reversi_game.game_loop()
