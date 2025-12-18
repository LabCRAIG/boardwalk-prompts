
from game import Game, Board, is_movement, get_move_elements

class CheckersGame(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: 'X', 1: 'O'}  # Player 0: X, Player 1: O
        self.directions = {0: 1, 1: -1}  # Direction of movement for each player

    def prompt_current_player(self) -> str:
        return input(f"Player {self.current_player}'s move ({self.players[self.current_player]}): ")

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if not is_movement(move):
            return False

        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Ensure the origin square contains the current player's piece
        if self.board.layout[ox, oy] != self.players[self.current_player]:
            return False

        # Ensure the destination square is blank
        if self.board.layout[dx, dy] != '_':
            return False

        # Check if the move is a simple diagonal move or a capture move
        direction = self.directions[self.current_player]
        if (dx, dy) == (ox + direction, oy + 1) or (dx, dy) == (ox + direction, oy - 1):
            return True  # Simple diagonal move
        elif (dx, dy) == (ox + 2 * direction, oy + 2) or (dx, dy) == (ox + 2 * direction, oy - 2):
            mx, my = (ox + dx) // 2, (oy + dy) // 2  # Middle position
            opponent = self.players[1 - self.current_player]
            if self.board.layout[mx, my] == opponent:  # Capture move
                return True

        return False

    def perform_move(self, move: str):
        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Move the piece
        self.board.move_piece(move)

        # Check if it's a capture move
        if abs(dx - ox) == 2:  # Jumped two squares
            mx, my = (ox + dx) // 2, (oy + dy) // 2  # Middle position
            self.board.place_piece(f'_ {mx},{my}')  # Remove captured piece

        # Check for promotion
        if dx == 0 and self.current_player == 1 or dx == self.board.height - 1 and self.current_player == 0:
            self.board.place_piece(f'K {dx},{dy}')  # Promote to king

    def game_finished(self) -> bool:
        # Game is finished if one player has no pieces left or no valid moves
        for player, piece in self.players.items():
            if any(piece in row for row in self.board.layout):
                if any(self.validate_move(f"{x},{y} {x+dx},{y+dy}")
                       for x, row in enumerate(self.board.layout)
                       for y, cell in enumerate(row)
                       for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]):
                    return False  # Player has valid moves
        return True

    def get_winner(self) -> int:
        # Determine the winner
        player_pieces = {player: 0 for player in self.players}
        for row in self.board.layout:
            for cell in row:
                if cell in self.players.values():
                    player_pieces[self.players.values().index(cell)] += 1

        if player_pieces[0] > player_pieces[1]:
            return 0
        elif player_pieces[1] > player_pieces[0]:
            return 1
        else:
            return None  # Draw

    def next_player(self) -> int:
        return 1 - self.current_player

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner} ({self.players[winner]}) wins!")
        else:
            print("The game is a draw!")

if __name__ == '__main__':
    # Initial Checkers board setup
    layout = (
        " O O O O\n"
        "O O O O \n"
        " O O O O\n"
        "_ _ _ _ \n"
        " _ _ _ _\n"
        "X X X X \n"
        " X X X X\n"
        "X X X X \n"
    )
    board = Board((8, 8), layout)
    checkers = CheckersGame(board)
    checkers.game_loop()
