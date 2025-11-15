from game import Game, Board, is_movement, get_move_elements

class Saffron(Game):
    # Player enumeration
    PLAYER_1 = 1
    PLAYER_2 = 2

    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = self.initial_player()

    def initial_player(self):
        # Player 1 starts
        return self.PLAYER_1

    def validate_move(self, move: str) -> bool:
        # Check if the move is a valid movement
        if not is_movement(move):
            return False
        
        # Extract origin and destination from the move
        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Ensure the origin contains the correct player's piece
        origin_piece = self.board.layout[ox, oy]
        if self.current_player == self.PLAYER_1 and origin_piece != 'A':
            return False
        if self.current_player == self.PLAYER_2 and origin_piece != 'B':
            return False

        # Ensure the destination is orthogonally adjacent to the origin
        if abs(ox - dx) + abs(oy - dy) != 1:
            return False

        # Ensure the destination is not occupied by the opponent's piece
        destination_piece = self.board.layout[dx, dy]
        if destination_piece in ['A', 'B']:
            return False

        return True

    def perform_move(self, move: str):
        # Extract origin and destination from the move
        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Identify the player's piece and marker
        if self.current_player == self.PLAYER_1:
            piece = 'A'
            marker = 'a'
        else:
            piece = 'B'
            marker = 'b'

        # Move the piece to the new location
        self.board.move_piece(move)

        # Leave a marker at the origin
        self.board.place_piece(f"{marker} {ox},{oy}")

    def game_finished(self) -> bool:
        # Check if the current player has lost by moving onto a marker
        for x in range(self.board.height):
            for y in range(self.board.width):
                piece = self.board.layout[x, y]
                if piece == 'A' and self.current_player == self.PLAYER_1 and self._is_marker(x, y):
                    return True
                if piece == 'B' and self.current_player == self.PLAYER_2 and self._is_marker(x, y):
                    return True
        return False

    def get_winner(self) -> int:
        # Return the opponent as the winner if the current player loses
        return self.PLAYER_2 if self.current_player == self.PLAYER_1 else self.PLAYER_1

    def next_player(self) -> int:
        # Switch to the other player
        return self.PLAYER_2 if self.current_player == self.PLAYER_1 else self.PLAYER_1

    def finish_message(self, winner):
        print(f"Player {winner} wins!")

    def _is_marker(self, x, y) -> bool:
        # Check if a space contains a marker
        return self.board.layout[x, y] in ['a', 'b']


if __name__ == '__main__':
    # Define the initial board layout
    initial_layout = (
        "________\n"
        "________\n"
        "________\n"
        "___A____\n"
        "____B___\n"
        "________\n"
        "________\n"
        "________"
    )
    board = Board((8, 8), initial_layout)
    saffron_game = Saffron(board)
    saffron_game.game_loop()