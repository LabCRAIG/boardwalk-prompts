
import chess

class CustomChessGame:
    def __init__(self):
        self.board = chess.Board()

    def display_board(self):
        print(self.board)

    def play_turn(self, move):
        """
        Play a move, or invoke custom rules if applicable.
        """
        if self.board.is_game_over():
            print(f"Game over: {self.board.result()}")
            return

        if self.is_bishop_conversion(move):
            self.bishop_conversion(move)
        elif self.is_queen_rook_swap(move):
            self.queen_rook_swap(move)
        else:
            try:
                self.board.push_uci(move)
            except ValueError:
                print("Invalid move. Try again.")

    def is_bishop_conversion(self, move):
        """
        Check if the move is a bishop conversion action.
        Format: bishop_position-convert. Example: 'c1-convert'
        """
        if "-convert" in move:
            bishop_square = chess.parse_square(move.split("-")[0])
            piece = self.board.piece_at(bishop_square)
            return piece and piece.piece_type == chess.BISHOP
        return False

    def bishop_conversion(self, move):
        """
        Perform the bishop conversion of adjacent pawns.
        """
        bishop_square = chess.parse_square(move.split("-")[0])
        bishop_color = self.board.piece_at(bishop_square).color

        # Get horizontal adjacent squares
        adjacent_squares = []
        file_index = bishop_square % 8
        if file_index > 0:  # Not on the 'a' file
            adjacent_squares.append(bishop_square - 1)
        if file_index < 7:  # Not on the 'h' file
            adjacent_squares.append(bishop_square + 1)

        # Convert enemy pawns
        for square in adjacent_squares:
            piece = self.board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN and piece.color != bishop_color:
                self.board.remove_piece_at(square)
                self.board.set_piece_at(square, chess.Piece(chess.PAWN, bishop_color))

        print("Bishop conversion performed.")
        self.display_board()

    def is_queen_rook_swap(self, move):
        """
        Check if the move is a queen-rook swap action.
        Format: queen_position-swap. Example: 'd1-swap'
        """
        if "-swap" in move:
            queen_square = chess.parse_square(move.split("-")[0])
            piece = self.board.piece_at(queen_square)
            return piece and piece.piece_type == chess.QUEEN
        return False

    def queen_rook_swap(self, move):
        """
        Perform the queen-rook swap if both pieces occupy squares of the same color.
        """
        queen_square = chess.parse_square(move.split("-")[0])
        queen_color = self.board.piece_at(queen_square).color

        # Locate rooks of the same color
        rooks = [square for square in self.board.pieces(chess.ROOK, queen_color)]
        for rook_square in rooks:
            if (queen_square + rook_square) % 2 == 0:  # Same color square
                # Swap queen and rook
                self.board.set_piece_at(queen_square, chess.Piece(chess.ROOK, queen_color))
                self.board.set_piece_at(rook_square, chess.Piece(chess.QUEEN, queen_color))
                print("Queen and rook swapped.")
                self.display_board()
                return

        print("No valid rook found for swapping.")

    def start(self):
        """
        Start the interactive game loop.
        """
        print("Welcome to Custom Chess!")
        self.display_board()

        while not self.board.is_game_over():
            print(f"{'White' if self.board.turn else 'Black'}'s turn.")
            move = input("Enter your move (or custom action): ")
            self.play_turn(move)

        print(f"Game over: {self.board.result()}")


if __name__ == "__main__":
    game = CustomChessGame()
    game.start()
