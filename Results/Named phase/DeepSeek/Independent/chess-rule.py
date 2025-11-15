import numpy as np

class ChessGame:
    def __init__(self):
        # Initialize the board
        self.board = np.array([
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ])
        
        self.current_player = 'white'
        self.game_over = False
        self.castling_rights = {
            'white': {'king_side': True, 'queen_side': True},
            'black': {'king_side': True, 'queen_side': True}
        }
        
    def print_board(self):
        print("  a b c d e f g h")
        print("  ----------------")
        for i in range(8):
            print(f"{8-i}|{' '.join(self.board[i])}|{8-i}")
        print("  ----------------")
        print("  a b c d e f g h")
    
    def get_piece_color(self, piece):
        if piece == ' ':
            return None
        return 'white' if piece.isupper() else 'black'
    
    def is_same_color(self, pos1, pos2):
        # Check if two positions are the same color on the chessboard
        row1, col1 = pos1
        row2, col2 = pos2
        return (row1 + col1) % 2 == (row2 + col2) % 2
    
    def get_adjacent_positions(self, row, col):
        # Get horizontally adjacent positions
        adjacent = []
        if col > 0:
            adjacent.append((row, col-1))  # Left
        if col < 7:
            adjacent.append((row, col+1))  # Right
        return adjacent
    
    def convert_notation(self, notation):
        # Convert algebraic notation to board coordinates
        if len(notation) != 2:
            return None
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None
    
    def is_valid_move(self, start, end):
        # Basic move validation (simplified for this example)
        start_row, start_col = start
        end_row, end_col = end
        
        # Can't move to a square with your own piece
        if self.get_piece_color(self.board[start_row][start_col]) == self.get_piece_color(self.board[end_row][end_col]):
            return False
        
        # Add more standard chess rules here in a real implementation
        return True
    
    def bishop_convert(self, bishop_pos):
        row, col = bishop_pos
        bishop_color = self.get_piece_color(self.board[row][col])
        
        if bishop_color != self.current_player:
            return False
        
        adjacent = self.get_adjacent_positions(row, col)
        converted = False
        
        for pos in adjacent:
            r, c = pos
            piece = self.board[r][c]
            piece_color = self.get_piece_color(piece)
            
            # Convert opposing pawns
            if piece_color and piece_color != bishop_color and piece.lower() == 'p':
                # Convert the pawn to the bishop's color
                self.board[r][c] = 'P' if bishop_color == 'white' else 'p'
                converted = True
        
        return converted
    
    def queen_swap_rook(self, queen_pos):
        queen_row, queen_col = queen_pos
        queen = self.board[queen_row][queen_col]
        queen_color = self.get_piece_color(queen)
        
        if queen_color != self.current_player or queen.lower() != 'q':
            return False
        
        # Find rooks of the same color
        rooks = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if (piece.lower() == 'r' and 
                    self.get_piece_color(piece) == queen_color and
                    self.is_same_color(queen_pos, (r, c))):
                    rooks.append((r, c))
        
        if not rooks:
            return False
        
        # For simplicity, let's just swap with the first available rook
        rook_pos = rooks[0]
        rook_row, rook_col = rook_pos
        
        # Swap queen and rook
        self.board[queen_row][queen_col], self.board[rook_row][rook_col] = \
        self.board[rook_row][rook_col], self.board[queen_row][queen_col]
        
        return True
    
    def make_move(self, start, end):
        start_pos = self.convert_notation(start)
        end_pos = self.convert_notation(end)
        
        if not start_pos or not end_pos:
            print("Invalid coordinates")
            return False
        
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        if not self.is_valid_move(start_pos, end_pos):
            print("Invalid move")
            return False
        
        # Make the move
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '
        
        # Check for special moves
        piece_moved = self.board[end_row][end_col].lower()
        
        # Bishop conversion ability
        if piece_moved == 'b':
            if self.bishop_convert((end_row, end_col)):
                print("Bishop converted adjacent pawns!")
        
        # Queen-rook swap ability
        if piece_moved == 'q':
            if self.queen_swap_rook((end_row, end_col)):
                print("Queen swapped with rook!")
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def play(self):
        print("Welcome to Chess with Special Rules!")
        print("1. Bishops can convert opposing pawns horizontally adjacent to them")
        print("2. Queens can swap places with rooks on same-colored squares")
        print("Enter moves in algebraic notation (e.g., e2 e4)")
        
        while not self.game_over:
            self.print_board()
            print(f"{self.current_player.capitalize()}'s turn")
            
            move = input("Enter your move (or 'quit' to end): ").strip()
            if move.lower() == 'quit':
                break
            
            try:
                start, end = move.split()
                if not self.make_move(start, end):
                    print("Try again")
            except:
                print("Invalid input. Please use format: e2 e4")
        
        print("Game over!")

# Start the game
if __name__ == "__main__":
    game = ChessGame()
    game.play()