from game import Game, Board, is_placement, is_movement, get_move_elements

class Amethyst(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: 'A', 1: 'O'}
        self.promoted_pieces = {'A': 'Â', 'O': 'Ô'}
        self.direction = {'A': (-1, -1), 'Â': (-1, -1), 'O': (1, 1), 'Ô': (1, 1)}
        self.current_player = self.initial_player()

    def initial_player(self):
        return 0  # Player 1 starts
    
    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination

            # Ensure origin piece belongs to the current player
            piece = self.board.layout[ox][oy]
            if piece not in self.players[self.current_player] + self.promoted_pieces[self.players[self.current_player]]:
                return False

            # Check diagonal movement
            if abs(dx - ox) != abs(dy - oy):
                return False

            # Check for regular move
            if abs(dx - ox) == 1:
                if self.board.layout[dx][dy] == '_':  # Must move to a blank space
                    return self._validate_direction(piece, ox, dx)

            # Check for capture move
            elif abs(dx - ox) == 2:
                mx, my = (ox + dx) // 2, (oy + dy) // 2  # Midpoint (captured piece)
                if (self.board.layout[dx][dy] == '_' and  # Target is blank
                        self.board.layout[mx][my] in self.players[1 - self.current_player] + self.promoted_pieces[self.players[1 - self.current_player]]):  # Captured piece belongs to opponent
                    return self._validate_direction(piece, ox, dx)

        return False

    def _validate_direction(self, piece, ox, dx):
        # Ensure movement direction is valid for the piece
        if piece in ('A', 'O'):
            return (dx - ox) == self.direction[piece][0]
        elif piece in ('Â', 'Ô'):
            return True  # Promoted pieces can move in any direction
        return False

    def perform_move(self, move: str):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination

            # Move the piece
            piece = self.board.layout[ox][oy]
            self.board.move_piece(move)

            # Check for capture
            if abs(dx - ox) == 2:
                mx, my = (ox + dx) // 2, (oy + dy) // 2  # Midpoint (captured piece)
                self.board.layout[mx][my] = '_'  # Remove captured piece

            # Check for promotion
            if piece == 'A' and dx == 0:
                self.board.place_piece(f'Â {dx},{dy}')
            elif piece == 'O' and dx == 7:
                self.board.place_piece(f'Ô {dx},{dy}')

    def next_player(self) -> int:
        return 1 - self.current_player  # Alternate between 0 and 1

    def game_finished(self) -> bool:
        # Check if either player has no pieces left or no valid moves
        player_pieces = {0: 0, 1: 0}
        player_moves = {0: False, 1: False}

        for x in range(self.board.height):
            for y in range(self.board.width):
                piece = self.board.layout[x][y]
                if piece in self.players[0] + self.promoted_pieces[self.players[0]]:
                    player_pieces[0] += 1
                    if self._has_valid_moves(piece, x, y):
                        player_moves[0] = True
                elif piece in self.players[1] + self.promoted_pieces[self.players[1]]:
                    player_pieces[1] += 1
                    if self._has_valid_moves(piece, x, y):
                        player_moves[1] = True

        return player_pieces[0] == 0 or player_pieces[1] == 0 or not player_moves[0] or not player_moves[1]

    def _has_valid_moves(self, piece: str, x: int, y: int) -> bool:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Regular move
            if 0 <= nx < self.board.height and 0 <= ny < self.board.width and self.board.layout[nx][ny] == '_':
                if self._validate_direction(piece, x, nx):
                    return True
            nx, ny = x + 2 * dx, y + 2 * dy  # Capture move
            mx, my = x + dx, y + dy  # Midpoint
            if (0 <= nx < self.board.height and 0 <= ny < self.board.width and
                    self.board.layout[nx][ny] == '_' and
                    self.board.layout[mx][my] in self.players[1 - self.current_player] + self.promoted_pieces[self.players[1 - self.current_player]]):
                if self._validate_direction(piece, x, nx):
                    return True
        return False

    def get_winner(self) -> int:
        # Determine the winner based on remaining pieces or valid moves
        player_pieces = {0: 0, 1: 0}
        player_moves = {0: False, 1: False}

        for x in range(self.board.height):
            for y in range(self.board.width):
                piece = self.board.layout[x][y]
                if piece in self.players[0] + self.promoted_pieces[self.players[0]]:
                    player_pieces[0] += 1
                    if self._has_valid_moves(piece, x, y):
                        player_moves[0] = True
                elif piece in self.players[1] + self.promoted_pieces[self.players[1]]:
                    player_pieces[1] += 1
                    if self._has_valid_moves(piece, x, y):
                        player_moves[1] = True

        if player_pieces[0] == 0 or not player_moves[0]:
            return 1  # Player 2 wins
        elif player_pieces[1] == 0 or not player_moves[1]:
            return 0  # Player 1 wins
        return None  # No winner (shouldn't reach here)

if __name__ == '__main__':
    initial_layout = (
        " O O O O\n"
        "O O O O \n"
        " O O O O\n"
        "_ _ _ _ \n"
        " _ _ _ _\n"
        "A A A A \n"
        " A A A A\n"
        "A A A A \n"
    )
    board = Board((8, 8), initial_layout)
    game = Amethyst(board)
    game.game_loop()