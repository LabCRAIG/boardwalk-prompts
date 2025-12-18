
class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color  # 'white' or 'black'
        self.symbol = symbol
        self.has_moved = False

    def is_valid_move(self, board, start, end):
        # Abstract method to be implemented by specific pieces
        pass

    def __str__(self):
        return self.symbol


class Pawn(ChessPiece):
    def __init__(self, color):
        symbol = '♙' if color == 'white' else '♟'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Direction of movement (different for white and black)
        direction = -1 if self.color == 'white' else 1
        
        # Simple forward move
        if start_col == end_col and board[end_row][end_col] is None:
            # One square forward
            if end_row == start_row + direction:
                return True
            # Two squares forward from starting position
            if not self.has_moved and end_row == start_row + 2 * direction and board[start_row + direction][start_col] is None:
                return True
        
        # Capture move (diagonal)
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if board[end_row][end_col] is not None and board[end_row][end_col].color != self.color:
                return True
        
        return False


class Rook(ChessPiece):
    def __init__(self, color):
        symbol = '♖' if color == 'white' else '♜'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Rook moves horizontally or vertically
        if start_row != end_row and start_col != end_col:
            return False
        
        # Check if path is clear
        row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        
        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        
        # Check if destination is empty or has an opponent piece
        return board[end_row][end_col] is None or board[end_row][end_col].color != self.color


class Knight(ChessPiece):
    def __init__(self, color):
        symbol = '♘' if color == 'white' else '♞'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Knight moves in an L-shape
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
        
        return False


class Bishop(ChessPiece):
    def __init__(self, color):
        symbol = '♗' if color == 'white' else '♝'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Bishop moves diagonally
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
        
        # Check if path is clear
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        
        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        
        # Check if destination is empty or has an opponent piece
        return board[end_row][end_col] is None or board[end_row][end_col].color != self.color


class Queen(ChessPiece):
    def __init__(self, color):
        symbol = '♕' if color == 'white' else '♛'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        # Queen combines rook and bishop movements
        start_row, start_col = start
        end_row, end_col = end
        
        # Check if move is horizontal, vertical, or diagonal
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        if (start_row == end_row or start_col == end_col) or (row_diff == col_diff):
            # Determine step direction
            row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
            col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)
            
            # Check path
            current_row, current_col = start_row + row_step, start_col + col_step
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col] is not None:
                    return False
                current_row += row_step
                current_col += col_step
            
            # Check destination
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
        
        return False


class King(ChessPiece):
    def __init__(self, color):
        symbol = '♔' if color == 'white' else '♚'
        super().__init__(color, symbol)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # King moves one square in any direction
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        if row_diff <= 1 and col_diff <= 1:
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
        
        # Castling (to be implemented)
        
        return False


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'
        self.initialize_board()

    def initialize_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
        
        # Set up rooks
        self.board[0][0] = Rook('black')
        self.board[0][7] = Rook('black')
        self.board[7][0] = Rook('white')
        self.board[7][7] = Rook('white')
        
        # Set up knights
        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        self.board[7][1] = Knight('white')
        self.board[7][6] = Knight('white')
        
        # Set up bishops
        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')
        self.board[7][2] = Bishop('white')
        self.board[7][5] = Bishop('white')
        
        # Set up queens
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')
        
        # Set up kings
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

    def display_board(self):
        print("  a b c d e f g h")
        print(" +-----------------+")
        for row in range(8):
            print(f"{8 - row}|", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(piece, end=" ")
                else:
                    print("·", end=" ")
            print(f"|{8 - row}")
        print(" +-----------------+")
        print("  a b c d e f g h")

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def make_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if not self.is_valid_position(start_row, start_col) or not self.is_valid_position(end_row, end_col):
            return False
        
        piece = self.board[start_row][start_col]
        
        if piece is None or piece.color != self.current_turn:
            return False
        
        if not piece.is_valid_move(self.board, start, end):
            return False
        
        # Check if king is in check after move
        # (This would need a more complex implementation)
        
        # Make the move
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        piece.has_moved = True
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        return True


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.game_over = False

    def parse_position(self, position):
        if len(position) != 2:
            return None
        
        col = ord(position[0].lower()) - ord('a')
        row = 8 - int(position[1])
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return None
        
        return row, col

    def play(self):
        print("Welcome to Chess! (Enter 'quit' to exit)")
        self.board.display_board()
        
        while not self.game_over:
            print(f"\n{self.board.current_turn.capitalize()}'s turn")
            
            try:
                move_input = input("Enter move (e.g., 'e2 e4'): ")
                
                if move_input.lower() == 'quit':
                    print("Thanks for playing!")
                    break
                
                start_pos, end_pos = move_input.split()
                start = self.parse_position(start_pos)
                end = self.parse_position(end_pos)
                
                if start is None or end is None:
                    print("Invalid position format. Use format like 'e2 e4'.")
                    continue
                
                if self.board.make_move(start, end):
                    self.board.display_board()
                else:
                    print("Invalid move. Try again.")
            
            except ValueError:
                print("Invalid input format. Use format like 'e2 e4'.")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    game = ChessGame()
    game.play()
