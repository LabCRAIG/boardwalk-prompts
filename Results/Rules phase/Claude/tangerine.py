from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Tangerine(Game):
    def __init__(self, board):
        super().__init__(board)
        # Player 1 uses H pieces, Player 2 uses V pieces
        self.player_pieces = {
            Player.ONE.value: 'H',
            Player.TWO.value: 'V'
        }
    
    def validate_move(self, move):
        # First check if the move is a valid format and within board boundaries
        if not super().validate_move(move):
            return False
        
        # Ensure the move is a placement (not a movement)
        if not is_placement(move):
            print("Only piece placement is allowed.")
            return False
        
        # Extract the piece and position from the move
        piece, position = get_move_elements(move)
        row, col = position
        
        # Verify that the piece matches the current player
        expected_piece = self.player_pieces[self.current_player]
        if piece != expected_piece:
            print(f"Player {self.current_player + 1} can only place {expected_piece} pieces.")
            return False
        
        # Check if the placement respects piece characteristics
        if piece == 'H':
            # For H pieces, we need to check if the right position is within bounds and empty
            if col + 1 >= self.board.width:
                print("Invalid placement: H piece needs space to the right.")
                return False
            
            # Check if both positions are blank
            if self.board.layout[row][col] != '_' or self.board.layout[row][col + 1] != '_':
                print("Invalid placement: Both positions must be empty.")
                return False
        
        elif piece == 'V':
            # For V pieces, we need to check if the position above is within bounds and empty
            if row - 1 < 0:  # Note: row - 1 because "upward" in the matrix is decreasing row index
                print("Invalid placement: V piece needs space above.")
                return False
            
            # Check if both positions are blank
            if self.board.layout[row][col] != '_' or self.board.layout[row - 1][col] != '_':
                print("Invalid placement: Both positions must be empty.")
                return False
        
        return True
    
    def perform_move(self, move):
        # Extract the piece and position from the move
        piece, position = get_move_elements(move)
        row, col = position
        
        # Place the main piece
        super().perform_move(move)
        
        # Place the second part of the piece based on its type
        if piece == 'H':
            # Place another H to the right
            additional_move = f"H {row},{col+1}"
            self.board.place_piece(additional_move)
        
        elif piece == 'V':
            # Place another V above
            additional_move = f"V {row-1},{col}"
            self.board.place_piece(additional_move)
    
    def game_finished(self):
        # Check if the current player can make any valid moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.player_pieces[self.current_player]
                move = f"{piece} {row},{col}"
                
                # Temporarily save the current player to restore after validation
                current = self.current_player
                if self.validate_move(move):
                    self.current_player = current
                    return False
                self.current_player = current
        
        # If we get here, no valid moves were found
        return True
    
    def get_winner(self):
        # If the game is finished, the current player has no valid moves
        # So the other player is the winner
        return (self.current_player + 1) % 2
    
    def next_player(self):
        # Players alternate turns
        return (self.current_player + 1) % 2
    
    def prompt_current_player(self):
        piece = self.player_pieces[self.current_player]
        return input(f"Player {self.current_player + 1} ({piece}), enter your move (e.g. '{piece} row,col'): ")
    
    def finish_message(self, winner):
        print(f"Player {winner + 1} wins! Player {self.current_player + 1} has no valid moves left.")

if __name__ == '__main__':
    board = Board((6, 6))
    game = Tangerine(board)
    game.game_loop()