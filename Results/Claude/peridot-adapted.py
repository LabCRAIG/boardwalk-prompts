from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Peridot(Game):
    def __init__(self, board):
        super().__init__(board)
        # Define player pieces
        self.PLAYER_PIECES = {0: 'A', 1: 'V'}
    
    def validate_move(self, move):
        # First check if move is valid according to board dimensions
        if not super().validate_move(move):
            return False
        
        # Check if move is a placement (not a movement)
        if not is_placement(move):
            print("Invalid move format. Use 'X row,col' to place a piece.")
            return False
        
        # Extract the piece and position from the move
        piece, (row, col) = get_move_elements(move)
        
        # Check if the player is using their correct piece
        if piece != self.PLAYER_PIECES[self.current_player]:
            print(f"Player {self.current_player + 1} must use '{self.PLAYER_PIECES[self.current_player]}' pieces.")
            return False
        
        # Check if the target position is empty (blank)
        if self.board.layout[row, col] != '_':
            print("That space is already occupied.")
            return False
            
        return True
    
    def prompt_current_player(self):
        print(f"Player {self.current_player + 1}'s turn ({self.PLAYER_PIECES[self.current_player]})")
        user_input = input("Enter row and column (0-2) separated by a space: ")
        
        try:
            # Convert user input to standard move format
            row, col = map(int, user_input.split())
            if not (0 <= row < 3 and 0 <= col < 3):
                print("Invalid coordinates. Must be between 0 and 2.")
                return self.prompt_current_player()
                
            # Format the move in standard format: "X row,col"
            return f"{self.PLAYER_PIECES[self.current_player]} {row},{col}"
        except ValueError:
            print("Please enter two numbers separated by a space.")
            return self.prompt_current_player()
    
    def perform_move(self, move):
        # The default implementation is sufficient as we're just placing pieces
        super().perform_move(move)
    
    def game_finished(self):
        # Check if a player has won
        for player in [0, 1]:
            piece = self.PLAYER_PIECES[player]
            # Check rows
            for row in range(3):
                if all(self.board.layout[row, col] == piece for col in range(3)):
                    return True
            
            # Check columns
            for col in range(3):
                if all(self.board.layout[row, col] == piece for row in range(3)):
                    return True
            
            # Check main diagonal
            if all(self.board.layout[i, i] == piece for i in range(3)):
                return True
            
            # Check other diagonal
            if all(self.board.layout[i, 2-i] == piece for i in range(3)):
                return True
        
        # Check if the board is full (tie)
        if all(self.board.layout[row, col] != '_' for row in range(3) for col in range(3)):
            return True
            
        return False
    
    def get_winner(self):
        # Check if a player has won
        for player in [0, 1]:
            piece = self.PLAYER_PIECES[player]
            # Check rows
            for row in range(3):
                if all(self.board.layout[row, col] == piece for col in range(3)):
                    return player
            
            # Check columns
            for col in range(3):
                if all(self.board.layout[row, col] == piece for row in range(3)):
                    return player
            
            # Check main diagonal
            if all(self.board.layout[i, i] == piece for i in range(3)):
                return player
            
            # Check other diagonal
            if all(self.board.layout[i, 2-i] == piece for i in range(3)):
                return player
        
        # If no winner but game is finished, it's a tie
        return None
    
    def next_player(self):
        # Switch between player 0 and player 1
        return 1 - self.current_player
    
    def initial_player(self):
        # Player 1 starts (represented as 0 in our implementation)
        return 0
    
    def finish_message(self, winner):
        if winner is None:
            print("It's a tie!")
        else:
            print(f"Player {winner + 1} wins!")


if __name__ == '__main__':
    # Create a 3x3 board
    board = Board((3, 3))
    
    # Initialize game
    game = Peridot(board)
    
    # Display welcome message
    print("Welcome to Peridot!")
    print("Player 1 uses 'A', Player 2 uses 'V'")
    
    # Start the game
    game.game_loop()