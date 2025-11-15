
from game import Game, Board, is_placement, get_move_elements

class TicTacToe5x5(Game):
    def __init__(self, board):
        super().__init__(board)
        self.players = {0: 'X', 1: 'O'}  # Two players, represented by 'X' and 'O'

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_placement(move):
            return False
        
        _, (row, col) = get_move_elements(move)
        return self.board.layout[row, col] == '_'  # Ensure the space is blank

    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)  # Place the piece on the board

    def game_finished(self):
        # Check rows, columns, and diagonals for a winning line
        layout = self.board.layout
        for i in range(self.board.height):
            for j in range(self.board.width):
                if layout[i, j] == '_':
                    continue
                if self.check_winning_line(i, j):
                    return True
        return '_' not in layout  # Game finishes if the board is full without a winner

    def get_winner(self):
        layout = self.board.layout
        for i in range(self.board.height):
            for j in range(self.board.width):
                if layout[i, j] != '_' and self.check_winning_line(i, j):
                    return 0 if layout[i, j] == 'X' else 1
        return None  # Return None if it's a draw

    def next_player(self):
        return (self.current_player + 1) % len(self.players)

    def initial_player(self):
        return 0  # Player 0 starts

    def finish_message(self, winner):
        if winner is None:
            print("It's a draw!")
        else:
            print(f"Player {winner} ({self.players[winner]}) wins!")

    def check_winning_line(self, row, col):
        piece = self.board.layout[row, col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Down, Right, Diagonal Right-Down, Diagonal Left-Down
        for dr, dc in directions:
            count = 1
            for step in range(1, 5):
                r, c = row + dr * step, col + dc * step
                if 0 <= r < self.board.height and 0 <= c < self.board.width and self.board.layout[r, c] == piece:
                    count += 1
                else:
                    break
            if count == 5:  # Winning line of 5 pieces
                return True
        return False

if __name__ == '__main__':
    board = Board((5, 5))  # Create a 5x5 board
    game = TicTacToe5x5(board)
    game.game_loop()
