
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class PegSolitaire(Game):
    class Player(Enum):
        SINGLE = 0
    
    def __init__(self, board):
        super().__init__(board)
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Only movement is allowed in Peg Solitaire
        if not is_movement(move):
            return False
        
        origin, destination = get_move_elements(move)
        
        # Check if origin has a peg
        if self.board.layout[origin[0]][origin[1]] != 'O':
            return False
        
        # Check if destination is empty
        if self.board.layout[destination[0]][destination[1]] != '_':
            return False
        
        # Check if the move is exactly 2 spaces in one direction
        dx = destination[0] - origin[0]
        dy = destination[1] - origin[1]
        
        # Must move exactly 2 spaces in one cardinal direction
        if (abs(dx) == 2 and dy == 0) or (dx == 0 and abs(dy) == 2):
            # Calculate the position of the jumped peg
            middle_x = origin[0] + dx // 2
            middle_y = origin[1] + dy // 2
            
            # Check if there's a peg in the middle to jump over
            if self.board.layout[middle_x][middle_y] == 'O':
                return True
        
        return False
    
    def perform_move(self, move):
        origin, destination = get_move_elements(move)
        
        # Calculate the position of the jumped peg
        middle_x = origin[0] + (destination[0] - origin[0]) // 2
        middle_y = origin[1] + (destination[1] - origin[1]) // 2
        
        # Move the peg
        self.board.move_piece(move)
        
        # Remove the jumped peg
        jump_move = f"_ {middle_x},{middle_y}"
        self.board.place_piece(jump_move)
    
    def game_finished(self):
        # Count remaining pegs
        peg_count = 0
        peg_positions = []
        
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i][j] == 'O':
                    peg_count += 1
                    peg_positions.append((i, j))
        
        # If only one peg remains, game is won
        if peg_count == 1:
            return True
        
        # If two pegs remain and one cannot capture the other, game is won
        if peg_count == 2:
            # Check if either peg can capture the other
            for pos in peg_positions:
                # Check all four possible jump directions
                for direction in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    dest_x = pos[0] + direction[0]
                    dest_y = pos[1] + direction[1]
                    
                    # Check if destination is valid
                    if 0 <= dest_x < self.board.height and 0 <= dest_y < self.board.width:
                        if self.board.layout[dest_x][dest_y] == '_':
                            # Check if there's a peg in the middle
                            middle_x = pos[0] + direction[0] // 2
                            middle_y = pos[1] + direction[1] // 2
                            
                            if self.board.layout[middle_x][middle_y] == 'O':
                                # A capture is possible, game is not finished
                                return False
            
            # No captures possible with two pegs remaining
            return True
        
        # If more than two pegs remain, check if any valid moves exist
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.layout[i][j] == 'O':
                    # Check all four directions
                    for direction in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                        dest_x = i + direction[0]
                        dest_y = j + direction[1]
                        
                        # Check if destination is valid
                        if 0 <= dest_x < self.board.height and 0 <= dest_y < self.board.width:
                            if self.board.layout[dest_x][dest_y] == '_':
                                # Check if there's a peg in the middle
                                middle_x = i + direction[0] // 2
                                middle_y = j + direction[1] // 2
                                
                                if self.board.layout[middle_x][middle_y] == 'O':
                                    # A valid move exists
                                    return False
        
        # No valid moves remain, game is finished
        return True
    
    def get_winner(self):
        # Peg Solitaire is a single-player game
        if self.game_finished():
            # Count remaining pegs
            peg_count = 0
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if self.board.layout[i][j] == 'O':
                        peg_count += 1
            
            if peg_count <= 2:
                return self.Player.SINGLE.value
            else:
                return None
        return None
    
    def finish_message(self, winner):
        if winner is not None:
            print("Congratulations! You've won the game!")
        else:
            print("Game over! You didn't manage to win this time.")
    
    def next_player(self):
        # Peg Solitaire is single-player
        return self.Player.SINGLE.value

if __name__ == '__main__':
    # Standard English Peg Solitaire board (7x7 with corners removed)
    layout = "  OOO  \n" + \
             "  OOO  \n" + \
             "OOOOOOO\n" + \
             "OOO_OOO\n" + \
             "OOOOOOO\n" + \
             "  OOO  \n" + \
             "  OOO  "
    
    board = Board((7, 7), layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()
