from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import IntEnum

class Player(IntEnum):
    ONE = 0  # Player 1 - uses H pieces
    TWO = 1  # Player 2 - uses V pieces

class Tangerine(Game):
    def __init__(self, board):
        super().__init__(board)
        # No additional attributes needed - the game state is fully captured by
        # the board layout and current player
    
    def validate_move(self, move):
        # First check if the move is valid in terms of board boundaries
        if not super().validate_move(move):
            return False
        
        # Only placement moves are valid in Tangerine
        if not is_placement(move):
            return False
        
        piece, (row, col) = get_move_elements(move)
        
        # Check if the piece corresponds to the current player
        if (self.current_player == Player.ONE and piece != 'H') or \
           (self.current_player == Player.TWO and piece != 'V'):
            return False
        
        # For H pieces (Player 1), check if there's space horizontally
        if piece == 'H':
            if col + 1 >= self.board.width or self.board.layout[row][col] != '_' or self.board.layout[row][col + 1] != '_':
                return False
        
        # For V pieces (Player 2), check if there's space vertically
        elif piece == 'V':
            if row + 1 >= self.board.height or self.board.layout[row][col] != '_' or self.board.layout[row + 1][col] != '_':
                return False
        
        return True
    
    def perform_move(self, move):
        # First perform the standard placement action
        super().perform_move(move)
        
        # Then place the second part of the piece
        piece, (row, col) = get_move_elements(move)
        
        if piece == 'H':
            # Place another H to the right
            self.board.place_piece(f"H {row},{col+1}")
        elif piece == 'V':
            # Place another V above
            self.board.place_piece(f"V {row+1},{col}")
    
    def game_finished(self):
        # Check if the current player has any valid moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                # Check for Player 1 (H pieces)
                if self.current_player == Player.ONE and \
                   col + 1 < self.board.width and \
                   self.board.layout[row][col] == '_' and \
                   self.board.layout[row][col + 1] == '_':
                    return False
                
                # Check for Player 2 (V pieces)
                if self.current_player == Player.TWO and \
                   row + 1 < self.board.height and \
                   self.board.layout[row][col] == '_' and \
                   self.board.layout[row + 1][col] == '_':
                    return False
        
        # If we get here, no valid moves were found
        return True
    
    def get_winner(self):
        # The player who can't make a move loses, so the winner is the other player
        return (self.current_player + 1) % 2
    
    def next_player(self):
        # Alternate between players
        return (self.current_player + 1) % 2
    
    def initial_player(self):
        # Player 1 (using H pieces) starts the game
        return Player.ONE
    
    def prompt_current_player(self):
        player_piece = 'H' if self.current_player == Player.ONE else 'V'
        player_num = self.current_player + 1  # Display as 1-indexed
        print(f"Player {player_num}'s turn (using {player_piece} pieces)")
        
        while True:
            try:
                row = int(input("Enter row (0-5): "))
                col = int(input("Enter column (0-5): "))
                
                # Format the move in the standard format
                return f"{player_piece} {row},{col}"
            except ValueError:
                print("Please enter valid numbers.")
    
    def finish_message(self, winner):
        winner_num = winner + 1  # Display as 1-indexed
        print(f"Game over! Player {winner_num} wins!")


if __name__ == '__main__':
    # Initialize a 6x6 board with all blank spaces
    board = Board((6, 6))
    
    # Create the game instance
    game = Tangerine(board)
    
    # Start the game loop
    game.game_loop()
