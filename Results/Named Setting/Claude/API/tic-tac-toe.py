from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum

class TicTacToePlayer(Enum):
    X = 0
    O = 1

class TicTacToe(Game):
    def __init__(self, board):
        super().__init__(board)
        # Initialize any game-specific attributes
        self.player_symbols = {
            TicTacToePlayer.X: 'X',
            TicTacToePlayer.O: 'O'
        }
    
    def prompt_current_player(self) -> str:
        player_symbol = self.player_symbols[TicTacToePlayer(self.current_player)]
        return input(f"Player {player_symbol}'s turn. Enter position (row,col): ")
    
    def validate_move(self, move: str) -> bool:
        # First check if the move format is valid using parent method
        if not super().validate_move(move):
            print("Invalid move format. Use 'X row,col' format.")
            return False
        
        # Tic-tac-toe only uses placements
        if not is_placement(move):
            print("Only piece placement is allowed. Use 'X row,col' format.")
            return False
        
        # Extract the piece and position from the move
        piece, position = get_move_elements(move)
        row, col = position
        
        # Check if the piece matches the current player's symbol
        if piece != self.player_symbols[TicTacToePlayer(self.current_player)]:
            print(f"You must place your own piece ({self.player_symbols[TicTacToePlayer(self.current_player)]}).")
            return False
        
        # Check if the position is already occupied
        if self.board.layout[row, col] != '_':
            print("That position is already occupied. Choose another position.")
            return False
        
        return True
    
    def game_finished(self) -> bool:
        # Check rows
        for i in range(3):
            if self.board.layout[i, 0] != '_' and \
               self.board.layout[i, 0] == self.board.layout[i, 1] == self.board.layout[i, 2]:
                return True
        
        # Check columns
        for i in range(3):
            if self.board.layout[0, i] != '_' and \
               self.board.layout[0, i] == self.board.layout[1, i] == self.board.layout[2, i]:
                return True
        
        # Check diagonals
        if self.board.layout[0, 0] != '_' and \
           self.board.layout[0, 0] == self.board.layout[1, 1] == self.board.layout[2, 2]:
            return True
        
        if self.board.layout[0, 2] != '_' and \
           self.board.layout[0, 2] == self.board.layout[1, 1] == self.board.layout[2, 0]:
            return True
        
        # Check if the board is full (draw)
        for i in range(3):
            for j in range(3):
                if self.board.layout[i, j] == '_':
                    return False
        
        # If we reach here, the board is full with no winner (draw)
        return True
    
    def get_winner(self) -> int:
        # Check rows
        for i in range(3):
            if self.board.layout[i, 0] != '_' and \
               self.board.layout[i, 0] == self.board.layout[i, 1] == self.board.layout[i, 2]:
                return TicTacToePlayer.X.value if self.board.layout[i, 0] == 'X' else TicTacToePlayer.O.value
        
        # Check columns
        for i in range(3):
            if self.board.layout[0, i] != '_' and \
               self.board.layout[0, i] == self.board.layout[1, i] == self.board.layout[2, i]:
                return TicTacToePlayer.X.value if self.board.layout[0, i] == 'X' else TicTacToePlayer.O.value
        
        # Check diagonals
        if self.board.layout[0, 0] != '_' and \
           self.board.layout[0, 0] == self.board.layout[1, 1] == self.board.layout[2, 2]:
            return TicTacToePlayer.X.value if self.board.layout[0, 0] == 'X' else TicTacToePlayer.O.value
        
        if self.board.layout[0, 2] != '_' and \
           self.board.layout[0, 2] == self.board.layout[1, 1] == self.board.layout[2, 0]:
            return TicTacToePlayer.X.value if self.board.layout[0, 2] == 'X' else TicTacToePlayer.O.value
        
        # If there's no winner but the game is finished, it's a draw
        return None
    
    def next_player(self) -> int:
        # Toggle between X and O
        return TicTacToePlayer.O.value if self.current_player == TicTacToePlayer.X.value else TicTacToePlayer.X.value
    
    def initial_player(self) -> int:
        # X goes first
        return TicTacToePlayer.X.value
    
    def finish_message(self, winner):
        if winner is None:
            print("Game over! It's a draw!")
        else:
            winner_symbol = self.player_symbols[TicTacToePlayer(winner)]
            print(f"Game over! Player {winner_symbol} wins!")

if __name__ == '__main__':
    board = Board((3, 3))  # Create a 3x3 board
    game = TicTacToe(board)
    game.game_loop()