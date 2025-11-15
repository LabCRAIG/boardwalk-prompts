
from game import Game, Board, is_movement, is_placement, get_move_elements

class Chess(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        # Initialize player as 0 (white) and 1 (black)
        self.current_player = self.initial_player()
        # Map player to piece case: 0 -> uppercase, 1 -> lowercase
        self.player_piece_case = {0: str.isupper, 1: str.islower}
        # Direction for pawns based on player
        self.pawn_direction = {0: -1, 1: 1}
        # Define piece movement rules
        self.piece_rules = {
            'P': self._pawn_moves,
            'R': self._rook_moves,
            'N': self._knight_moves,
            'B': self._bishop_moves,
            'Q': self._queen_moves,
            'K': self._king_moves
        }

    def initial_player(self) -> int:
        return 0  # White starts

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False
        
        if is_movement(move):
            origin, destination = get_move_elements(move)
            x1, y1 = origin
            x2, y2 = destination

            # Check if origin contains a piece belonging to the current player
            piece = self.board.layout[x1, y1]
            if piece == '_' or not self.player_piece_case[self.current_player](piece):
                return False

            # Ensure the destination is valid for the piece
            valid_moves = self.piece_rules[piece.upper()](origin)
            if destination not in valid_moves:
                return False

        return True

    def perform_move(self, move: str):
        super().perform_move(move)

        if is_movement(move):
            origin, destination = get_move_elements(move)
            x1, y1 = origin
            x2, y2 = destination

            # Handle pawn promotion
            piece = self.board.layout[x2, y2]
            if piece.upper() == 'P' and (x2 == 0 or x2 == 7):
                self.board.layout[x2, y2] = 'Q' if self.current_player == 0 else 'q'

    def game_finished(self) -> bool:
        # Check if either king is missing (game over)
        layout = self.board.layout
        return 'K' not in layout or 'k' not in layout

    def get_winner(self) -> int:
        # Determine winner: if black king is missing, white wins, and vice versa
        layout = self.board.layout
        if 'K' not in layout:
            return 1  # Black wins
        elif 'k' not in layout:
            return 0  # White wins
        return None  # Draw (shouldn't happen in chess)

    def next_player(self) -> int:
        return (self.current_player + 1) % 2

    def _pawn_moves(self, origin):
        x, y = origin
        direction = self.pawn_direction[self.current_player]
        moves = []

        # Single forward move
        if self._is_on_board(x + direction, y) and self.board.layout[x + direction, y] == '_':
            moves.append((x + direction, y))

        # Double forward move from initial position
        if (self.current_player == 0 and x == 6) or (self.current_player == 1 and x == 1):
            if self.board.layout[x + direction, y] == '_' and \
               self.board.layout[x + 2 * direction, y] == '_':
                moves.append((x + 2 * direction, y))

        # Diagonal captures
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if self._is_on_board(nx, ny) and \
               self.board.layout[nx, ny] != '_' and \
               not self.player_piece_case[self.current_player](self.board.layout[nx, ny]):
                moves.append((nx, ny))

        return moves

    def _rook_moves(self, origin):
        return self._linear_moves(origin, [(1, 0), (0, 1), (-1, 0), (0, -1)])  # Orthogonal directions

    def _bishop_moves(self, origin):
        return self._linear_moves(origin, [(1, 1), (1, -1), (-1, 1), (-1, -1)])  # Diagonal directions

    def _queen_moves(self, origin):
        return self._linear_moves(origin, [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])  # All directions

    def _king_moves(self, origin):
        x, y = origin
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self._is_on_board(nx, ny) and \
               (self.board.layout[nx, ny] == '_' or not self.player_piece_case[self.current_player](self.board.layout[nx, ny])):
                moves.append((nx, ny))
        return moves

    def _knight_moves(self, origin):
        x, y = origin
        moves = []
        jumps = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if self._is_on_board(nx, ny) and \
               (self.board.layout[nx, ny] == '_' or not self.player_piece_case[self.current_player](self.board.layout[nx, ny])):
                moves.append((nx, ny))
        return moves

    def _linear_moves(self, origin, directions):
        x, y = origin
        moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while self._is_on_board(nx, ny):
                if self.board.layout[nx, ny] == '_':
                    moves.append((nx, ny))
                elif not self.player_piece_case[self.current_player](self.board.layout[nx, ny]):
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return moves

    def _is_on_board(self, x, y):
        return 0 <= x < self.board.height and 0 <= y < self.board.width


if __name__ == '__main__':
    initial_layout = (
        "rnbqkbnr\n"
        "pppppppp\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "PPPPPPPP\n"
        "RNBQKBNR"
    )
    board = Board((8, 8), initial_layout)
    chess = Chess(board)
    chess.game_loop()
