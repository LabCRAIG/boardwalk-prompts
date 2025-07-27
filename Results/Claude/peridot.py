from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum

class Player(Enum):
    ONE = 0
    TWO = 1

class Peridot(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pieces = {Player.ONE: 'A', Player.TWO: 'V'}
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Only placements are allowed
        if not is_placement(move):
            return False
        
        piece, position = get_move_elements(move)
        
        # Check if the piece belongs to the current player
        if piece != self.pieces[Player.ONE if self.current_player == Player.ONE.value else Player.TWO]:
            return False
        
        # Check if the position is empty
        i, j = position
        return self.board.layout[i][j] == '_'
    
    def game_finished(self):
        # Check rows
        for i in range(3):
            if all(self.board.layout[i][j] == 'A' for j in range(3)) or \
               all(self.board.layout[i][j] == 'V' for j in range(3)):
                return True
        
        # Check columns
        for j in range(3):
            if all(self.board.layout[i][j] == 'A' for i in range(3)) or \
               all(self.board.layout[i][j] == 'V' for i in range(3)):
                return True
        
        # Check diagonals
        if all(self.board.layout[i][i] == 'A' for i in range(3)) or \
           all(self.board.layout[i][i] == 'V' for i in range(3)):
            return True
        
        if all(self.board.layout[i][2-i] == 'A' for i in range(3)) or \
           all(self.board.layout[i][2-i] == 'V' for i in range(3)):
            return True
        
        # Check if board is full (tie)
        for i in range(3):
            for j in range(3):
                if self.board.layout[i][j] == '_':
                    return False
        
        return True
    
    def get_winner(self):
        # Check rows
        for i in range(3):
            if all(self.board.layout[i][j] == 'A' for j in range(3)):
                return Player.ONE.value
            if all(self.board.layout[i][j] == 'V' for j in range(3)):
                return Player.TWO.value
        
        # Check columns
        for j in range(3):
            if all(self.board.layout[i][j] == 'A' for i in range(3)):
                return Player.ONE.value
            if all(self.board.layout[i][j] == 'V' for i in range(3)):
                return Player.TWO.value
        
        # Check diagonals
        if all(self.board.layout[i][i] == 'A' for i in range(3)):
            return Player.ONE.value
        if all(self.board.layout[i][i] == 'V' for i in range(3)):
            return Player.TWO.value
        
        if all(self.board.layout[i][2-i] == 'A' for i in range(3)):
            return Player.ONE.value
        if all(self.board.layout[i][2-i] == 'V' for i in range(3)):
            return Player.TWO.value
        
        # If the game is finished but no winner, it's a tie
        return None
    
    def next_player(self):
        return Player.TWO.value if self.current_player == Player.ONE.value else Player.ONE.value
    
    def prompt_current_player(self):
        player_char = self.pieces[Player.ONE if self.current_player == Player.ONE.value else Player.TWO]
        player_num = 1 if self.current_player == Player.ONE.value else 2
        
        move = input(f"Player {player_num}'s turn (piece {player_char}). Enter your move (format: '{player_char} row,col'): ")
        
        # If the player only enters coordinates, add the piece character
        if not is_placement(move) and not is_movement(move):
            if ',' in move:
                move = f"{player_char} {move}"
        
        return move
    
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a tie!")
        else:
            player_num = 1 if winner == Player.ONE.value else 2
            print(f"Player {player_num} wins!")

if __name__ == '__main__':
    board = Board((3, 3))
    mygame = Peridot(board)
    mygame.game_loop()