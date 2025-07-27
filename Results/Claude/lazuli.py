from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    PLAYER = 0

class Lazuli(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = Player.PLAYER.value
    
    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
        
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Check if origin has a piece
        if self.board.layout[origin_row][origin_col] != 'X':
            return False
        
        # Check if destination is blank
        if self.board.layout[dest_row][dest_col] != '_':
            return False
        
        # Check if the move is horizontal or vertical
        is_horizontal = origin_row == dest_row
        is_vertical = origin_col == dest_col
        
        if not (is_horizontal or is_vertical):
            return False
        
        # Check if the move is exactly 2 spaces away
        if is_horizontal:
            if abs(dest_col - origin_col) != 2:
                return False
            # Check if there's a piece to jump over
            middle_col = (origin_col + dest_col) // 2
            if self.board.layout[origin_row][middle_col] != 'X':
                return False
        elif is_vertical:
            if abs(dest_row - origin_row) != 2:
                return False
            # Check if there's a piece to jump over
            middle_row = (origin_row + dest_row) // 2
            if self.board.layout[middle_row][origin_col] != 'X':
                return False
        
        return True
    
    def perform_move(self, move: str):
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Move the piece
        super().perform_move(move)
        
        # Remove the jumped-over piece
        if origin_row == dest_row:  # Horizontal move
            middle_col = (origin_col + dest_col) // 2
            middle_move = f"_ {origin_row},{middle_col}"
            self.board.place_piece(middle_move)
        else:  # Vertical move
            middle_row = (origin_row + dest_row) // 2
            middle_move = f"_ {middle_row},{origin_col}"
            self.board.place_piece(middle_move)
    
    def game_finished(self) -> bool:
        # Count the pieces
        piece_count = 0
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'X':
                    piece_count += 1
        
        # Check if there's only one piece left in the center
        center_row, center_col = self.board.height // 2, self.board.width // 2
        if piece_count == 1 and self.board.layout[center_row][center_col] == 'X':
            return True
        
        # Check if there are valid moves left
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'X':
                    # Check each direction (up, down, left, right)
                    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        # Check if the destination is within bounds
                        if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                            # Check if the destination is blank
                            if self.board.layout[new_row][new_col] == '_':
                                # Check if there's a piece to jump over
                                middle_row, middle_col = row + dr//2, col + dc//2
                                if self.board.layout[middle_row][middle_col] == 'X':
                                    return False  # Valid move found
        
        # No valid moves left
        return True
    
    def get_winner(self) -> int:
        # Player wins if only one piece remains and it's in the center
        center_row, center_col = self.board.height // 2, self.board.width // 2
        
        piece_count = 0
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'X':
                    piece_count += 1
        
        if piece_count == 1 and self.board.layout[center_row][center_col] == 'X':
            return Player.PLAYER.value
        
        return None  # No winner (player lost)
    
    def next_player(self) -> int:
        return Player.PLAYER.value
    
    def prompt_current_player(self) -> str:
        return input("Enter your move (origin_row,origin_col dest_row,dest_col): ")
    
    def finish_message(self, winner):
        if winner is not None:
            print("Congratulations! You won the game!")
        else:
            print("Game over! You lost.")

if __name__ == '__main__':
    # Create initial board layout
    layout = ""
    for i in range(7):
        for j in range(7):
            # Null spaces in corners (2x2 squares)
            if (i < 2 and j < 2) or (i < 2 and j > 4) or (i > 4 and j < 2) or (i > 4 and j > 4):
                layout += " "
            # Center is blank
            elif i == 3 and j == 3:
                layout += "_"
            # Everything else is X
            else:
                layout += "X"
        if i < 6:  # Don't add newline after the last row
            layout += "\n"
    
    board = Board((7, 7), layout)
    game = Lazuli(board)
    game.game_loop()