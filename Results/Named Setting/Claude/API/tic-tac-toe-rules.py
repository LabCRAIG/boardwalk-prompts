from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    X = 0
    O = 1

class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = ['X', 'O']
    
    def prompt_current_player(self) -> str:
        player_symbol = self.players[self.current_player]
        return input(f"Player {player_symbol}, enter your move (e.g. 'X 0,0'): ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Check if it's a placement move
        if is_placement(move):
            piece, position = get_move_elements(move)
            row, col = position
            
            # Check if the piece belongs to the current player
            if piece != self.players[self.current_player]:
                return False
            
            # Check if the space is empty
            if self.board.layout[row, col] != '_':
                return False
            
            return True
        
        return False
    
    def game_finished(self) -> bool:
        # Check if board is full
        if '_' not in self.board.layout:
            return True
        
        # Check if any player has won
        return self.get_winner() is not None
    
    def get_winner(self) -> int:
        layout = self.board.layout
        height, width = layout.shape
        
        # Check for horizontal wins
        for row in range(height):
            for col in range(width - 2):
                if layout[row, col] == layout[row, col+1] == layout[row, col+2] != '_':
                    if layout[row, col] == 'X':
                        return Player.X.value
                    else:
                        return Player.O.value
        
        # Check for vertical wins
        for col in range(width):
            for row in range(height - 2):
                if layout[row, col] == layout[row+1, col] == layout[row+2, col] != '_':
                    if layout[row, col] == 'X':
                        return Player.X.value
                    else:
                        return Player.O.value
        
        # Check for 2x2 square wins
        for row in range(height - 1):
            for col in range(width - 1):
                if layout[row, col] == layout[row, col+1] == layout[row+1, col] == layout[row+1, col+1] != '_':
                    if layout[row, col] == 'X':
                        return Player.X.value
                    else:
                        return Player.O.value
        
        return None
    
    def next_player(self) -> int:
        # Switch between players (0 and 1)
        return (self.current_player + 1) % 2
    
    def initial_player(self) -> int:
        return Player.X.value
    
    def finish_message(self, winner):
        if winner is None:
            print("Game ended in a draw!")
        else:
            winner_symbol = self.players[winner]
            print(f"Player {winner_symbol} wins!")
    
    def get_state(self) -> tuple:
        return (deepcopy(self.board.layout), self.current_player, [])

if __name__ == '__main__':
    board = Board((3, 3))
    mygame = TicTacToe(board)
    mygame.game_loop()