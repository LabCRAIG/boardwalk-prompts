from game import Game, Board, is_movement, get_move_elements

class SaffronGame(Game):
    def __init__(self, board: Board):
        # Initialize the parent class
        super().__init__(board)
        # Track the positions of Player 1's and Player 2's pieces
        self.positions = {'A': (3, 3), 'B': (4, 4)}
        # Enum for players
        self.players = {1: 'A', 2: 'B'}
        self.current_player = 1

    def validate_move(self, move: str) -> bool:
        # Check if the move is a valid movement
        if not is_movement(move):
            return False

        # Extract origin and destination from the move
        origin, destination = get_move_elements(move)

        # Ensure the origin matches the current player's piece
        piece = self.players[self.current_player]
        if self.board.layout[origin[0], origin[1]] != piece:
            return False

        # Ensure the destination is within bounds and not occupied by the opponent's piece
        dest_x, dest_y = destination
        if not (0 <= dest_x < 8 and 0 <= dest_y < 8):
            return False
        if self.board.layout[dest_x, dest_y] not in ['_', 'a', 'b']:
            return False  # Invalid if destination is not empty or a marker

        return True

    def perform_move(self, move: str):
        # Extract origin and destination from the move
        origin, destination = get_move_elements(move)
        piece = self.players[self.current_player]

        # Check if the player loses by moving onto a marker
        dest_x, dest_y = destination
        if self.board.layout[dest_x, dest_y] in ['a', 'b']:
            # Mark the game as finished
            self.board.layout[dest_x, dest_y] = piece  # Update the board
            raise Exception(f"Player {self.current_player} loses! Moved onto a marker.")

        # Place a marker on the origin position
        marker = 'a' if piece == 'A' else 'b'
        self.board.layout[origin[0], origin[1]] = marker

        # Move the piece to the destination
        self.board.layout[dest_x, dest_y] = piece
        self.positions[piece] = destination  # Update piece position

    def game_finished(self) -> bool:
        # Check if any player has lost
        try:
            # If the game raises an exception, it means a player loses
            self.get_winner()
            return False
        except Exception:
            return True

    def get_winner(self) -> int:
        # Determine the winner of the game
        # If an exception was raised (player lost), the other player wins
        piece = self.players[self.current_player]
        if self.board.layout[self.positions[piece][0], self.positions[piece][1]] in ['a', 'b']:
            return 3 - self.current_player
        return None  # Game is not finished

    def next_player(self) -> int:
        # Alternate between Player 1 and Player 2
        return 2 if self.current_player == 1 else 1

    def finish_message(self, winner):
        print(f"Player {winner} wins!")


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
    saffron_game = SaffronGame(board)
    saffron_game.game_loop()