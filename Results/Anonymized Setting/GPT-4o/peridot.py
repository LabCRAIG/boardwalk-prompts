from game import Game, Board, is_placement, get_move_elements

class Peridot(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = {0: 'A', 1: 'V'}  # Player 1 -> 'A', Player 2 -> 'V'

    def validate_move(self, move: str) -> bool:
        # Check if the move is a valid placement
        if not is_placement(move):
            return False
        
        # Parse the move
        piece, (row, col) = get_move_elements(move)
        
        # Check if the piece belongs to the current player
        if piece != self.players[self.current_player]:
            return False

        # Check if the target space is empty
        if self.board.layout[row, col] != '_':
            return False

        return True

    def perform_move(self, move: str):
        # Parse the move
        piece, (row, col) = get_move_elements(move)
        
        # Place the piece on the board
        self.board.place_piece(move)

    def game_finished(self) -> bool:
        layout = self.board.layout

        # Check rows and columns
        for i in range(3):
            if all(layout[i, j] == 'A' for j in range(3)) or all(layout[i, j] == 'V' for j in range(3)):
                return True
            if all(layout[j, i] == 'A' for j in range(3)) or all(layout[j, i] == 'V' for j in range(3)):
                return True

        # Check diagonals
        if all(layout[i, i] == 'A' for i in range(3)) or all(layout[i, i] == 'V' for i in range(3)):
            return True
        if all(layout[i, 2 - i] == 'A' for i in range(3)) or all(layout[i, 2 - i] == 'V' for i in range(3)):
            return True

        # Check if the board is full (tie case)
        if all(layout[i, j] != '_' for i in range(3) for j in range(3)):
            return True

        return False

    def get_winner(self):
        layout = self.board.layout

        # Check rows and columns
        for i in range(3):
            if all(layout[i, j] == 'A' for j in range(3)):
                return 0  # Player 1 wins
            if all(layout[i, j] == 'V' for j in range(3)):
                return 1  # Player 2 wins
            if all(layout[j, i] == 'A' for j in range(3)):
                return 0  # Player 1 wins
            if all(layout[j, i] == 'V' for j in range(3)):
                return 1  # Player 2 wins

        # Check diagonals
        if all(layout[i, i] == 'A' for i in range(3)):
            return 0  # Player 1 wins
        if all(layout[i, i] == 'V' for i in range(3)):
            return 1  # Player 2 wins
        if all(layout[i, 2 - i] == 'A' for i in range(3)):
            return 0  # Player 1 wins
        if all(layout[i, 2 - i] == 'V' for i in range(3)):
            return 1  # Player 2 wins

        # Check for a tie (no winner)
        if all(layout[i, j] != '_' for i in range(3) for j in range(3)):
            return None

        return None

    def next_player(self) -> int:
        # Alternate turns between players
        return (self.current_player + 1) % 2

    def finish_message(self, winner):
        if winner is None:
            print("It's a tie!")
        else:
            print(f"Player {winner + 1} wins!")

if __name__ == '__main__':
    # Create a 3x3 board
    board = Board((3, 3))
    
    # Initialize and start the game
    mygame = Peridot(board)
    mygame.game_loop()