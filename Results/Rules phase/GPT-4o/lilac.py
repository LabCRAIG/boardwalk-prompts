from game import Game, Board, is_movement, get_move_elements
import numpy as np

class Lilac(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = {1: 'V', 2: 'A'}  # Player 1 controls 'V', Player 2 controls 'A' and 'Â'
        self.center = (3, 3)  # Center of the board
        self.Â = 'Â'  # Special piece
        self.border_positions = self.get_border_positions()  # Border spaces of the board
    
    def get_border_positions(self):
        """Returns all border positions on the board."""
        height, width = self.board.height, self.board.width
        borders = set()
        for i in range(height):
            borders.add((i, 0))
            borders.add((i, width - 1))
        for j in range(width):
            borders.add((0, j))
            borders.add((height - 1, j))
        return borders

    def validate_move(self, move):
        """Validates a player's move."""
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
        
        origin, destination = get_move_elements(move)
        piece = self.board.layout[origin]

        # Ensure the piece belongs to the current player
        if (self.current_player == 1 and piece != 'V') or (self.current_player == 2 and piece not in ['A', 'Â']):
            return False

        # Ensure the move is orthogonal and within one space
        if abs(origin[0] - destination[0]) + abs(origin[1] - destination[1]) != 1:
            return False

        # Ensure the destination is blank
        if self.board.layout[destination] != '_':
            return False

        # Ensure Â can only occupy the center
        if piece == 'Â' and destination != self.center:
            return False

        return True

    def perform_move(self, move):
        """Performs the move and resolves any captures."""
        origin, destination = get_move_elements(move)
        piece = self.board.layout[origin]

        # Move the piece
        self.board.move_piece(move)

        # Check for captures
        self.resolve_captures(destination)

    def resolve_captures(self, position):
        """Checks and removes any pieces captured around a given position."""
        x, y = position
        adjacent_positions = [
            (x - 1, y), (x + 1, y),  # Vertical neighbors
            (x, y - 1), (x, y + 1)   # Horizontal neighbors
        ]

        for dx, dy in adjacent_positions:
            if 0 <= dx < self.board.height and 0 <= dy < self.board.width:
                piece = self.board.layout[(dx, dy)]
                if piece not in ['_', ' ']:  # Check if there's a piece to capture
                    # Check if the piece is sandwiched
                    opposite = (2 * dx - x, 2 * dy - y)
                    if (0 <= opposite[0] < self.board.height and
                        0 <= opposite[1] < self.board.width and
                        self.board.layout[opposite] == self.players[self.current_player]):
                        # Capture the piece
                        self.board.place_piece(f"_ {dx},{dy}")

    def game_finished(self):
        """Checks if the game is finished."""
        # Check if Â is captured
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[(x, y)] == 'Â':
                    # Check if Â is on the border
                    if (x, y) in self.border_positions:
                        return True
                    return False
        return True  # Â is captured

    def get_winner(self):
        """Determines the winner."""
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[(x, y)] == 'Â':
                    # If Â reaches the border, Player 2 wins
                    if (x, y) in self.border_positions:
                        return 2
                    return None  # Game not finished
        return 1  # If Â is captured, Player 1 wins

    def next_player(self):
        """Returns the next player."""
        return 2 if self.current_player == 1 else 1

if __name__ == '__main__':
    initial_layout = (
        "__VVV__\n"
        "___V___\n"
        "V_AAA_V\n"
        "VVAÂAVV\n"
        "V_AAA_V\n"
        "___V___\n"
        "__VVV__"
    )
    board = Board((7, 7), initial_layout)
    lilac = Lilac(board)
    lilac.game_loop()