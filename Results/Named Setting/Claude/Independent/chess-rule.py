
import copy

class ChessPiece:
    def __init__(self, color, position):
        self.color = color  # "white" or "black"
        self.position = position  # (row, col)
        self.has_moved = False

    def get_valid_moves(self, board):
        return []

    def __str__(self):
        return f"{self.color[0].upper()}{self.__class__.__name__[0]}"


class Pawn(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}P"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == "white" else 1
        
        # Forward move
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Double move from starting position
            if not self.has_moved:
                if 0 <= row + 2*direction < 8 and board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))
        
        # Captures
        for dc in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + dc < 8:
                target = board[row + direction][col + dc]
                if target and target.color != self.color:
                    moves.append((row + direction, col + dc))
        
        return moves


class Rook(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}R"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Check in all four directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        
        return moves


class Knight(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}N"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Knight's possible moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        
        return moves


class Bishop(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}B"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Check in all four diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        
        return moves
    
    def get_convertible_pawns(self, board):
        """Get horizontally adjacent enemy pawns that can be converted"""
        convertible = []
        row, col = self.position
        
        # Check left and right
        for dc in [-1, 1]:
            if 0 <= col + dc < 8:
                piece = board[row][col + dc]
                if piece and isinstance(piece, Pawn) and piece.color != self.color:
                    convertible.append((row, col + dc))
        
        return convertible


class Queen(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}Q"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Combine rook and bishop movements
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Rook directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Bishop directions
        ]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        
        return moves
    
    def get_swappable_rooks(self, board):
        """Get rooks of same color that can be swapped with the queen"""
        swappable = []
        queen_row, queen_col = self.position
        queen_square_color = (queen_row + queen_col) % 2  # 0 for black, 1 for white square
        
        # Find rooks of the same color on squares of the same color
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and isinstance(piece, Rook) and piece.color == self.color:
                    square_color = (row + col) % 2
                    if square_color == queen_square_color:
                        swappable.append((row, col))
        
        return swappable


class King(ChessPiece):
    def __str__(self):
        return f"{self.color[0].upper()}K"
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Check all 8 surrounding squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the current position
                
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))
        
        # Castling would be implemented here, but it's complex and requires checking
        # for pieces between king and rook, whether king or rook has moved,
        # and whether king passes through or ends up in check
        
        return moves


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.setup_board()
    
    def setup_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Pawn("black", (1, col))
            self.board[6][col] = Pawn("white", (6, col))
        
        # Set up other pieces
        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.board[0][col] = back_row[col]("black", (0, col))
            self.board[7][col] = back_row[col]("white", (7, col))
    
    def display_board(self):
        print("  a b c d e f g h")
        print(" +-----------------+")
        for row in range(8):
            print(f"{8-row}|", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(piece, end=" ")
                else:
                    print(".", end=" ")
            print(f"|{8-row}")
        print(" +-----------------+")
        print("  a b c d e f g h")
    
    def get_piece_at(self, position):
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def is_valid_move(self, from_pos, to_pos):
        piece = self.get_piece_at(from_pos)
        
        # Basic checks
        if not piece:
            return False
        if piece.color != self.current_turn:
            return False
        
        # Check if the move is in the piece's valid moves
        valid_moves = piece.get_valid_moves(self.board)
        return to_pos in valid_moves
    
    def make_move(self, from_pos, to_pos):
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        piece = self.get_piece_at(from_pos)
        
        # Execute the move
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        piece.position = to_pos
        piece.has_moved = True
        
        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"
        return True
    
    def convert_pawn(self, bishop_pos, pawn_pos):
        bishop = self.get_piece_at(bishop_pos)
        pawn = self.get_piece_at(pawn_pos)
        
        # Validate conversion
        if not bishop or not isinstance(bishop, Bishop) or bishop.color != self.current_turn:
            return False
        if not pawn or not isinstance(pawn, Pawn) or pawn.color == self.current_turn:
            return False
        
        # Check if pawn is horizontally adjacent
        if bishop_pos[0] != pawn_pos[0] or abs(bishop_pos[1] - pawn_pos[1]) != 1:
            return False
        
        # Perform conversion
        pawn.color = bishop.color
        
        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"
        return True
    
    def swap_queen_rook(self, queen_pos, rook_pos):
        queen = self.get_piece_at(queen_pos)
        rook = self.get_piece_at(rook_pos)
        
        # Validate swap
        if not queen or not isinstance(queen, Queen) or queen.color != self.current_turn:
            return False
        if not rook or not isinstance(rook, Rook) or rook.color != self.current_turn:
            return False
        
        # Check if both pieces are on squares of the same color
        queen_square_color = (queen_pos[0] + queen_pos[1]) % 2
        rook_square_color = (rook_pos[0] + rook_pos[1]) % 2
        if queen_square_color != rook_square_color:
            return False
        
        # Perform swap
        self.board[queen_pos[0]][queen_pos[1]] = rook
        self.board[rook_pos[0]][rook_pos[1]] = queen
        rook.position = queen_pos
        queen.position = rook_pos
        
        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"
        return True
    
    def is_in_check(self, color):
        # Find the king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        # Check if any opponent piece can capture the king
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    valid_moves = piece.get_valid_moves(self.board)
                    if king_pos in valid_moves:
                        return True
        
        return False
    
    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        
        # Try all possible moves for each piece of the given color
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self.board)
                    
                    for move in valid_moves:
                        # Make temporary move
                        temp_board = copy.deepcopy(self)
                        temp_board.make_move((row, col), move)
                        
                        # If after the move, the king is not in check, it's not checkmate
                        if not temp_board.is_in_check(color):
                            return False
        
        # Also check special moves
        # Bishop conversion
        for row in range(8):
            for col in range(8):
                bishop = self.board[row][col]
                if bishop and isinstance(bishop, Bishop) and bishop.color == color:
                    convertible = bishop.get_convertible_pawns(self.board)
                    
                    for pawn_pos in convertible:
                        # Make temporary conversion
                        temp_board = copy.deepcopy(self)
                        temp_board.convert_pawn((row, col), pawn_pos)
                        
                        # If after the conversion, the king is not in check, it's not checkmate
                        if not temp_board.is_in_check(color):
                            return False
        
        # Queen-Rook swap
        for row in range(8):
            for col in range(8):
                queen = self.board[row][col]
                if queen and isinstance(queen, Queen) and queen.color == color:
                    swappable = queen.get_swappable_rooks(self.board)
                    
                    for rook_pos in swappable:
                        # Make temporary swap
                        temp_board = copy.deepcopy(self)
                        temp_board.swap_queen_rook((row, col), rook_pos)
                        
                        # If after the swap, the king is not in check, it's not checkmate
                        if not temp_board.is_in_check(color):
                            return False
        
        # If no move gets the king out of check, it's checkmate
        return True


def algebraic_to_coords(notation):
    """Convert algebraic notation (e.g., 'e4') to (row, col) coordinates"""
    col = ord(notation[0].lower()) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)

def coords_to_algebraic(coords):
    """Convert (row, col) coordinates to algebraic notation"""
    row, col = coords
    return f"{chr(col + ord('a'))}{8 - row}"

def play_game():
    board = ChessBoard()
    
    while True:
        board.display_board()
        print(f"{board.current_turn.capitalize()}'s turn")
        
        if board.is_in_check(board.current_turn):
            print("CHECK!")
            if board.is_checkmate(board.current_turn):
                print("CHECKMATE!")
                print(f"{('White' if board.current_turn == 'black' else 'Black')} wins!")
                break
        
        action = input("Enter action (move/convert/swap): ").strip().lower()
        
        if action == "move":
            from_square = input("Move from (e.g. e2): ").strip().lower()
            to_square = input("Move to (e.g. e4): ").strip().lower()
            
            try:
                from_pos = algebraic_to_coords(from_square)
                to_pos = algebraic_to_coords(to_square)
                
                if board.make_move(from_pos, to_pos):
                    print("Move successful")
                else:
                    print("Invalid move. Try again.")
            except:
                print("Invalid input. Use algebraic notation (e.g., e2).")
        
        elif action == "convert":
            bishop_square = input("Bishop position (e.g. c4): ").strip().lower()
            pawn_square = input("Pawn to convert (e.g. c5): ").strip().lower()
            
            try:
                bishop_pos = algebraic_to_coords(bishop_square)
                pawn_pos = algebraic_to_coords(pawn_square)
                
                if board.convert_pawn(bishop_pos, pawn_pos):
                    print("Conversion successful")
                else:
                    print("Invalid conversion. Try again.")
            except:
                print("Invalid input. Use algebraic notation (e.g., e2).")
        
        elif action == "swap":
            queen_square = input("Queen position (e.g. d1): ").strip().lower()
            rook_square = input("Rook position (e.g. a1): ").strip().lower()
            
            try:
                queen_pos = algebraic_to_coords(queen_square)
                rook_pos = algebraic_to_coords(rook_square)
                
                if board.swap_queen_rook(queen_pos, rook_pos):
                    print("Swap successful")
                else:
                    print("Invalid swap. Try again.")
            except:
                print("Invalid input. Use algebraic notation (e.g., e2).")
        
        elif action == "quit":
            print("Game ended.")
            break
        
        else:
            print("Unknown action. Use 'move', 'convert', 'swap', or 'quit'.")


if __name__ == "__main__":
    print("Welcome to Chess with Special Rules!")
    print("Special Rules:")
    print("1. Bishops can convert enemy pawns that are horizontally adjacent to them")
    print("2. Queens can swap places with friendly rooks if both are on squares of the same color")
    play_game()
