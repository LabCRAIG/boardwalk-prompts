
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    BLACK = 0
    WHITE = 1

class Reversi(Game):
    def __init__(self, board):
        super().__init__(board)
        self.directions = [(-1, -1), (-1, 0), (-1, 1), 
                          (0, -1),           (0, 1), 
                          (1, -1),  (1, 0),  (1, 1)]
        self.pieces = {Player.BLACK: 'B', Player.WHITE: 'W'}
        
        # Initialize the starting board
        self.board.place_piece("B 3,4")
        self.board.place_piece("W 3,3")
        self.board.place_piece("B 4,3")
        self.board.place_piece("W 4,4")

    def initial_player(self):
        return Player.BLACK.value

    def next_player(self):
        return (self.current_player + 1) % 2

    def get_state(self):
        board_layout = deepcopy(self.board.layout)
        return (board_layout, self.current_player, [])

    def prompt_current_player(self):
        player_piece = self.pieces[Player(self.current_player)]
        prompt = f"Player {player_piece}'s move: "
        move_input = input(prompt)
        # Format the move as placement
        if len(move_input.split()) == 1:
            row, col = map(int, move_input.split(','))
            return f"{player_piece} {row},{col}"
        return move_input

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Reversi only allows placements
        if not is_placement(move):
            return False
            
        piece, (row, col) = get_move_elements(move)
        
        # Check if the piece belongs to the current player
        if piece != self.pieces[Player(self.current_player)]:
            return False
            
        # Check if the position is blank
        if self.board.layout[row, col] != '_':
            return False
            
        # Check if the move would flip at least one opponent's piece
        opponent_piece = self.pieces[Player((self.current_player + 1) % 2)]
        
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.board.height and 
                0 <= c < self.board.width and 
                self.board.layout[r, c] == opponent_piece):
                
                # There's an opponent's piece adjacent in this direction
                # Continue in this direction to see if we can flip
                pieces_to_flip = []
                while 0 <= r < self.board.height and 0 <= c < self.board.width:
                    if self.board.layout[r, c] == '_' or self.board.layout[r, c] == ' ':
                        break
                    if self.board.layout[r, c] == piece:
                        # Found our own piece, can flip everything in between
                        return True
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
                    
        return False
                
    def perform_move(self, move):
        super().perform_move(move)
        
        piece, (row, col) = get_move_elements(move)
        opponent_piece = self.pieces[Player((self.current_player + 1) % 2)]
        
        # Find and flip opponent's pieces
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            # Follow direction until we hit our own piece or the edge
            while (0 <= r < self.board.height and 
                  0 <= c < self.board.width):
                if self.board.layout[r, c] == '_' or self.board.layout[r, c] == ' ':
                    break
                if self.board.layout[r, c] == piece:
                    # Flip all opponent's pieces in between
                    for flip_r, flip_c in pieces_to_flip:
                        self.board.place_piece(f"{piece} {flip_r},{flip_c}")
                    break
                pieces_to_flip.append((r, c))
                r += dr
                c += dc

    def has_valid_moves(self, player_enum):
        player_piece = self.pieces[Player(player_enum)]
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] != '_':
                    continue
                
                move = f"{player_piece} {row},{col}"
                if self.validate_move(move):
                    return True
        return False

    def game_finished(self):
        # Game is over if neither player has valid moves
        return not self.has_valid_moves(0) and not self.has_valid_moves(1)

    def get_winner(self):
        # Count pieces
        black_count = 0
        white_count = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == 'B':
                    black_count += 1
                elif self.board.layout[row, col] == 'W':
                    white_count += 1
        
        if black_count > white_count:
            return Player.BLACK.value
        elif white_count > black_count:
            return Player.WHITE.value
        else:
            return None  # Draw
            
    def finish_message(self, winner):
        black_count = 0
        white_count = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == 'B':
                    black_count += 1
                elif self.board.layout[row, col] == 'W':
                    white_count += 1
        
        print(f"Game over! Final score: Black (B): {black_count}, White (W): {white_count}")
        
        if winner is None:
            print("It's a tie!")
        else:
            winner_piece = self.pieces[Player(winner)]
            print(f"Player {winner_piece} wins!")

if __name__ == '__main__':
    board = Board((8, 8))
    mygame = Reversi(board)
    mygame.game_loop()
