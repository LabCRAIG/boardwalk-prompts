from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0  # Controls V's
    TWO = 1  # Controls A's and Â

class Lilac(Game):
    def __init__(self, board):
        super().__init__(board)
        self.center = (3, 3)  # The center position of the board

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Must be a movement, not a placement
        if not is_movement(move):
            print("Invalid move: You can only move existing pieces.")
            return False
        
        # Extract origin and destination
        origin, destination = get_move_elements(move)
        
        # Check if the origin has a piece belonging to the current player
        piece_at_origin = self.board.layout[origin]
        if self.current_player == Player.ONE.value and piece_at_origin != 'V':
            print("Invalid move: Player 1 can only move V pieces.")
            return False
        if self.current_player == Player.TWO.value and piece_at_origin not in ['A', 'Â']:
            print("Invalid move: Player 2 can only move A or Â pieces.")
            return False
        
        # Check if the destination is blank
        if self.board.layout[destination] != '_':
            print("Invalid move: Destination must be empty.")
            return False
        
        # Check if the move is orthogonal and only one space
        dx = abs(destination[0] - origin[0])
        dy = abs(destination[1] - origin[1])
        if not ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            print("Invalid move: Pieces can only move orthogonally one space at a time.")
            return False
        
        # Check if destination is the center - only Â can go there
        if destination == self.center and piece_at_origin != 'Â':
            print("Invalid move: Only the Â piece can occupy the center.")
            return False
        
        return True

    def perform_move(self, move):
        # Perform the basic move
        super().perform_move(move)
        
        # Check for captures
        origin, destination = get_move_elements(move)
        self.check_captures(destination)

    def check_captures(self, position):
        # Check for captures in all four orthogonal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for direction in directions:
            # Position of potential captured piece
            capture_pos = (position[0] + direction[0], position[1] + direction[1])
            
            # Check if capture position is within board boundaries
            if (0 <= capture_pos[0] < self.board.height and 
                0 <= capture_pos[1] < self.board.width):
                
                # Position of the other piece that forms the sandwich
                sandwich_pos = (capture_pos[0] + direction[0], capture_pos[1] + direction[1])
                
                # Check if sandwich position is within board boundaries
                if (0 <= sandwich_pos[0] < self.board.height and 
                    0 <= sandwich_pos[1] < self.board.width):
                    
                    piece_at_position = self.board.layout[position]
                    piece_at_capture = self.board.layout[capture_pos]
                    piece_at_sandwich = self.board.layout[sandwich_pos]
                    
                    # If the piece at position and sandwich belong to the same player
                    # and the piece at capture belongs to the opposing player
                    if piece_at_capture != '_' and piece_at_position != '_' and piece_at_sandwich != '_':
                        if ((piece_at_position == 'V' and piece_at_sandwich == 'V' and 
                             piece_at_capture in ['A', 'Â']) or 
                            (piece_at_position in ['A', 'Â'] and piece_at_sandwich in ['A', 'Â'] and 
                             piece_at_capture == 'V')):
                            # Perform the capture by replacing the captured piece with a blank space
                            self.board.place_piece(f"_ {capture_pos[0]},{capture_pos[1]}")

    def game_finished(self):
        # Check if Â has been captured (Player 1 wins)
        if not any('Â' in row for row in self.board.layout):
            return True
        
        # Find Â on the board
        a_hat_pos = None
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] == 'Â':
                    a_hat_pos = (i, j)
                    break
            if a_hat_pos:
                break
        
        # Check if Â has reached the border (Player 2 wins)
        if a_hat_pos and (a_hat_pos[0] == 0 or a_hat_pos[0] == self.board.height - 1 or 
                          a_hat_pos[1] == 0 or a_hat_pos[1] == self.board.width - 1):
            return True
        
        return False

    def get_winner(self):
        # Check if Â has been captured (Player 1 wins)
        if not any('Â' in row for row in self.board.layout):
            return Player.ONE.value
        
        # Find Â on the board
        a_hat_pos = None
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i, j] == 'Â':
                    a_hat_pos = (i, j)
                    break
            if a_hat_pos:
                break
        
        # Check if Â has reached the border (Player 2 wins)
        if a_hat_pos and (a_hat_pos[0] == 0 or a_hat_pos[0] == self.board.height - 1 or 
                          a_hat_pos[1] == 0 or a_hat_pos[1] == self.board.width - 1):
            return Player.TWO.value
        
        # This should never be reached if game_finished is true
        return None

    def next_player(self):
        # Simple alternating turns
        return (self.current_player + 1) % 2

    def initial_player(self):
        # Player 1 (V) starts
        return Player.ONE.value

    def prompt_current_player(self):
        player_name = "1 (V)" if self.current_player == Player.ONE.value else "2 (A/Â)"
        return input(f"Player {player_name}, enter your move (origin dest, e.g. '3,3 3,4'): ")

    def finish_message(self, winner):
        if winner == Player.ONE.value:
            print("Player 1 wins! The Â piece has been captured.")
        else:
            print("Player 2 wins! The Â piece has reached the border.")

    def get_state(self):
        # Return the current game state
        board_layout = deepcopy(self.board.layout)
        return (board_layout, self.current_player, [])

if __name__ == '__main__':
    initial_layout = """
   VVV   
   _V_   
  V_AAA_V 
  VVAÂAVV 
  V_AAA_V 
   _V_   
   VVV   
""".strip().replace(" ", "")
    
    board = Board((7, 7), initial_layout)
    lilac_game = Lilac(board)
    lilac_game.game_loop()