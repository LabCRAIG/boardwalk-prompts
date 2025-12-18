
from game import Game, Board, is_movement, is_placement, get_move_elements

class NineMensMorris(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.pieces = {0: 'X', 1: 'O'}  # Player pieces
        self.pieces_in_hand = {0: 9, 1: 9}  # Number of pieces each player can still place
        self.pieces_on_board = {0: set(), 1: set()}  # Tracks player pieces on the board
        self.removal_phase = False  # Indicates if a player can remove an opponent's piece
        self.mill_formed_by = None  # Tracks which player formed a mill

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False
        
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            if self.board.layout[x, y] != '_':  # Space must be blank for placement
                return False
            if piece != self.pieces[self.current_player]:  # Must play their own piece
                return False
            if self.pieces_in_hand[self.current_player] <= 0:  # No pieces left to place
                return False
            return True

        elif is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            if self.board.layout[x1, y1] != self.pieces[self.current_player]:  # Must move own piece
                return False
            if self.board.layout[x2, y2] != '_':  # Destination must be blank
                return False
            if not self.is_adjacent((x1, y1), (x2, y2)):  # Must move to an adjacent position
                return False
            return True

        return False

    def perform_move(self, move: str):
        if is_placement(move):
            piece, (x, y) = get_move_elements(move)
            self.board.place_piece(move)
            self.pieces_in_hand[self.current_player] -= 1
            self.pieces_on_board[self.current_player].add((x, y))
            if self.check_mill((x, y), self.current_player):
                self.removal_phase = True
                self.mill_formed_by = self.current_player
        elif is_movement(move):
            (x1, y1), (x2, y2) = get_move_elements(move)
            self.board.move_piece(move)
            self.pieces_on_board[self.current_player].remove((x1, y1))
            self.pieces_on_board[self.current_player].add((x2, y2))
            if self.check_mill((x2, y2), self.current_player):
                self.removal_phase = True
                self.mill_formed_by = self.current_player

        elif self.removal_phase:
            piece, (x, y) = get_move_elements(move)
            opponent = 1 - self.current_player
            if self.board.layout[x, y] == self.pieces[opponent] and self.is_on_same_square((x, y)):
                self.board.place_piece(f"_ {x},{y}")
                self.pieces_on_board[opponent].remove((x, y))
                self.removal_phase = False
                self.mill_formed_by = None

    def is_adjacent(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
        # Define adjacency rules specific to the Nine Men's Morris board
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def check_mill(self, position: tuple[int, int], player: int) -> bool:
        # Check if a mill is formed by the piece at the given position
        x, y = position
        piece = self.pieces[player]

        # Horizontal mill check
        row = self.board.layout[x, :]
        if all(cell == piece for cell in row):
            return True
        
        # Vertical mill check
        col = self.board.layout[:, y]
        if all(cell == piece for cell in col):
            return True
        
        return False

    def is_on_same_square(self, position: tuple[int, int]) -> bool:
        x, y = position
        square = min(x, y)  # Simplistic logic for determining square; adapt as needed
        return all(
            (x1, y1) in self.pieces_on_board[1 - self.mill_formed_by]
            for x1, y1 in self.pieces_on_board[1 - self.mill_formed_by]
            if min(x1, y1) == square
        )

    def game_finished(self) -> bool:
        # Game ends when a player has less than 3 pieces on the board
        return any(len(pieces) < 3 for pieces in self.pieces_on_board.values())

    def get_winner(self) -> int:
        # Winner is the player with 3 or more pieces on the board
        if len(self.pieces_on_board[0]) < 3:
            return 1
        elif len(self.pieces_on_board[1]) < 3:
            return 0
        return None

    def next_player(self) -> int:
        return 1 - self.current_player

if __name__ == '__main__':
    layout = (
        "X X X X X\n"
        "X _ _ _ X\n"
        "X _ _ _ X\n"
        "X _ _ _ X\n"
        "X X X X X"
    )
    board = Board((5, 5), layout)
    mygame = NineMensMorris(board)
    mygame.game_loop()
