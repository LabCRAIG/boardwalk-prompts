from game import Game, Board, is_movement, get_move_elements
import numpy as np

class Violet(Game):
    class Player:
        PLAYER_1 = 1  # Controls A's
        PLAYER_2 = 2  # Controls V's

    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = self.initial_player()

    def initial_player(self):
        return self.Player.PLAYER_1  # Player 1 starts

    def next_player(self):
        return self.Player.PLAYER_2 if self.current_player == self.Player.PLAYER_1 else self.Player.PLAYER_1

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        # Check if move is a valid movement
        if not is_movement(move):
            return False

        origin, destination = get_move_elements(move)
        piece = self.board.layout[origin[0], origin[1]]

        # Check if the piece belongs to the current player
        if self.current_player == self.Player.PLAYER_1 and piece != 'A':
            return False
        if self.current_player == self.Player.PLAYER_2 and piece != 'V':
            return False

        # Check if the destination is valid
        if not self.is_line_of_sight_clear(origin, destination):
            return False

        return True

    def perform_move(self, move: str):
        # Move the piece
        origin, destination = get_move_elements(move)
        piece = self.board.layout[origin[0], origin[1]]
        self.board.move_piece(move)

        # Prompt the player to shoot an X
        while True:
            shoot_move = input(f"Player {self.current_player}, place an X from {destination}: ")
            if self.validate_shoot_move(shoot_move, destination):
                self.perform_shoot_move(shoot_move)
                break
            else:
                print("Invalid X placement. Try again.")

    def validate_shoot_move(self, move: str, shooter_position: tuple[int, int]) -> bool:
        if not is_movement(move):
            return False

        _, target = get_move_elements(move)

        # Check that the target is within the shooter's line of sight
        if not self.is_line_of_sight_clear(shooter_position, target, allow_blank_only=True):
            return False

        return True

    def perform_shoot_move(self, move: str):
        _, target = get_move_elements(move)
        self.board.place_piece(f"X {target[0]},{target[1]}")

    def is_line_of_sight_clear(self, origin: tuple[int, int], destination: tuple[int, int], allow_blank_only=False) -> bool:
        dy = destination[0] - origin[0]
        dx = destination[1] - origin[1]

        # Ensure the movement is along a straight line or diagonal
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False

        # Normalize direction
        step_y = dy // abs(dy) if dy != 0 else 0
        step_x = dx // abs(dx) if dx != 0 else 0

        # Check all spaces between origin and destination
        y, x = origin
        while (y, x) != destination:
            y += step_y
            x += step_x
            if (y, x) == destination:
                break
            if self.board.layout[y, x] != '_':
                return False

        # Check the destination space
        if allow_blank_only and self.board.layout[destination[0], destination[1]] != '_':
            return False

        return True

    def game_finished(self) -> bool:
        # Check if the current player can make any valid moves
        for y, x in np.ndindex(self.board.layout.shape):
            piece = self.board.layout[y, x]
            if self.current_player == self.Player.PLAYER_1 and piece == 'A':
                if self.has_valid_moves((y, x)):
                    return False
            elif self.current_player == self.Player.PLAYER_2 and piece == 'V':
                if self.has_valid_moves((y, x)):
                    return False

        return True

    def has_valid_moves(self, position: tuple[int, int]) -> bool:
        # Check all possible directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dy, dx in directions:
            y, x = position
            while 0 <= y + dy < self.board.layout.shape[0] and 0 <= x + dx < self.board.layout.shape[1]:
                y += dy
                x += dx
                if self.board.layout[y, x] == '_':
                    return True
                else:
                    break
        return False

    def get_winner(self) -> int:
        # The current player cannot move, so the other player wins
        return self.next_player()

    def finish_message(self, winner):
        print(f"Player {winner} wins!")

if __name__ == '__main__':
    # Define the initial board layout
    layout = (
        "___V__V___\n"
        "__________\n"
        "__________\n"
        "V________V\n"
        "__________\n"
        "__________\n"
        "A________A\n"
        "__________\n"
        "__________\n"
        "___A__A___"
    )
    board = Board((10, 10), layout)
    game = Violet(board)
    game.game_loop()