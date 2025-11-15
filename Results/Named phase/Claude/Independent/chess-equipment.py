import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)

# Piece class to represent chess pieces
class Piece:
    def __init__(self, color, piece_type, row, col):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type  # 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king'
        self.row = row
        self.col = col
        self.has_moved = False
        self.image = None
        self.load_image()
        
    def load_image(self):
        # Generate images programmatically using pygame
        size = SQUARE_SIZE - 10
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Basic piece shapes
        if self.piece_type == 'pawn':
            color = WHITE if self.color == 'white' else BLACK
            pygame.draw.circle(self.image, color, (size//2, size//3), size//5)
            pygame.draw.polygon(self.image, color, [
                (size//4, size//3), 
                (3*size//4, size//3),
                (3*size//4, 2*size//3),
                (size//4, 2*size//3)
            ])
        elif self.piece_type == 'knight':
            color = WHITE if self.color == 'white' else BLACK
            # Horse head shape
            points = [
                (size//5, 4*size//5),
                (size//3, size//3),
                (size//2, size//5),
                (2*size//3, size//4),
                (3*size//4, size//3),
                (4*size//5, size//2),
                (4*size//5, 3*size//4),
                (3*size//4, 4*size//5)
            ]
            pygame.draw.polygon(self.image, color, points)
            # Eye
            eye_color = BLACK if self.color == 'white' else WHITE
            pygame.draw.circle(self.image, eye_color, (3*size//5, 2*size//5), size//15)
        elif self.piece_type == 'bishop':
            color = WHITE if self.color == 'white' else BLACK
            pygame.draw.circle(self.image, color, (size//2, size//4), size//6)
            pygame.draw.polygon(self.image, color, [
                (size//3, size//4),
                (2*size//3, size//4),
                (3*size//4, 4*size//5),
                (size//4, 4*size//5)
            ])
        elif self.piece_type == 'rook':
            color = WHITE if self.color == 'white' else BLACK
            pygame.draw.polygon(self.image, color, [
                (size//4, size//5),
                (size//4, size//3),
                (3*size//4, size//3),
                (3*size//4, size//5)
            ])
            pygame.draw.rect(self.image, color, (size//4, size//3, size//2, size//2))
        elif self.piece_type == 'queen':
            color = WHITE if self.color == 'white' else BLACK
            # Crown base
            pygame.draw.rect(self.image, color, (size//4, 2*size//3, size//2, size//5))
            # Crown points
            for i in range(5):
                x = size//4 + i*size//10
                pygame.draw.polygon(self.image, color, [
                    (x, 2*size//3),
                    (x + size//20, size//3),
                    (x + size//10, 2*size//3)
                ])
        elif self.piece_type == 'king':
            color = WHITE if self.color == 'white' else BLACK
            # Crown base
            pygame.draw.rect(self.image, color, (size//4, 2*size//3, size//2, size//5))
            # Crown
            pygame.draw.rect(self.image, color, (3*size//8, size//3, size//4, size//3))
            # Cross
            pygame.draw.rect(self.image, color, (7*size//16, size//5, size//8, size//3))
            pygame.draw.rect(self.image, color, (3*size//8, size//4, size//4, size//8))

        # Add outline
        outline_color = BLACK if self.color == 'white' else WHITE
        pygame.draw.rect(self.image, outline_color, (0, 0, size, size), 2)
        
    def move(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True

# Chess game class
class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game with Modified Knight Positions")
        self.clock = pygame.time.Clock()
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.turn = 'white'  # White starts
        self.valid_moves = []
        self.init_board()

    def init_board(self):
        # Set up pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = Piece('black', 'pawn', 1, col)
            self.board[6][col] = Piece('white', 'pawn', 6, col)

        # Set up other pieces except knights
        # Black pieces on top row
        self.board[0][0] = Piece('black', 'rook', 0, 0)
        self.board[0][7] = Piece('black', 'rook', 0, 7)
        self.board[0][2] = Piece('black', 'bishop', 0, 2)
        self.board[0][5] = Piece('black', 'bishop', 0, 5)
        self.board[0][3] = Piece('black', 'queen', 0, 3)
        self.board[0][4] = Piece('black', 'king', 0, 4)
        # Note: Knights (0,1) and (0,6) are left empty

        # White pieces on bottom row
        self.board[7][0] = Piece('white', 'rook', 7, 0)
        self.board[7][7] = Piece('white', 'rook', 7, 7)
        self.board[7][2] = Piece('white', 'bishop', 7, 2)
        self.board[7][5] = Piece('white', 'bishop', 7, 5)
        self.board[7][3] = Piece('white', 'queen', 7, 3)
        self.board[7][4] = Piece('white', 'king', 7, 4)
        # Note: Knights (7,1) and (7,6) are left empty

        # Place knights in the center four squares
        # White knights
        self.board[3][3] = Piece('white', 'knight', 3, 3)  # d5
        self.board[4][4] = Piece('white', 'knight', 4, 4)  # e4
        
        # Black knights
        self.board[3][4] = Piece('black', 'knight', 3, 4)  # e5
        self.board[4][3] = Piece('black', 'knight', 4, 3)  # d4

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Draw square
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )
                
                # Highlight selected piece's square
                if (self.selected_piece and 
                    self.selected_piece.row == row and 
                    self.selected_piece.col == col):
                    pygame.draw.rect(
                        self.screen,
                        HIGHLIGHT,
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    pygame.draw.circle(
                        self.screen,
                        HIGHLIGHT,
                        (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 8
                    )
                
                # Draw piece if exists
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(
                        piece.image, 
                        (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5)
                    )

    def get_valid_moves(self, piece):
        moves = []
        row, col = piece.row, piece.col
        
        if piece.piece_type == 'pawn':
            # Movement direction depends on color
            direction = 1 if piece.color == 'black' else -1
            
            # Move forward one square
            if 0 <= row + direction < BOARD_SIZE:
                if self.board[row + direction][col] is None:
                    moves.append((row + direction, col))
                    
                    # Move forward two squares on first move
                    if not piece.has_moved:
                        if 0 <= row + 2*direction < BOARD_SIZE:
                            if self.board[row + 2*direction][col] is None:
                                moves.append((row + 2*direction, col))
            
            # Capture diagonally
            for dcol in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + dcol < BOARD_SIZE:
                    if (self.board[row + direction][col + dcol] and 
                        self.board[row + direction][col + dcol].color != piece.color):
                        moves.append((row + direction, col + dcol))
        
        elif piece.piece_type == 'knight':
            # Knight moves in L-shape: 2 in one direction, 1 in perpendicular direction
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            
            for drow, dcol in knight_moves:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if not self.board[new_row][new_col] or self.board[new_row][new_col].color != piece.color:
                        moves.append((new_row, new_col))
        
        elif piece.piece_type == 'bishop' or piece.piece_type == 'queen':
            # Diagonal moves
            for drow, dcol in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for dist in range(1, BOARD_SIZE):
                    new_row, new_col = row + drow * dist, col + dcol * dist
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))
                        elif self.board[new_row][new_col].color != piece.color:
                            moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
        
        if piece.piece_type == 'rook' or piece.piece_type == 'queen':
            # Horizontal and vertical moves
            for drow, dcol in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                for dist in range(1, BOARD_SIZE):
                    new_row, new_col = row + drow * dist, col + dcol * dist
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))
                        elif self.board[new_row][new_col].color != piece.color:
                            moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
        
        elif piece.piece_type == 'king':
            # King moves one square in any direction
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if drow == 0 and dcol == 0:
                        continue
                    new_row, new_col = row + drow, col + dcol
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        if not self.board[new_row][new_col] or self.board[new_row][new_col].color != piece.color:
                            moves.append((new_row, new_col))
        
        return moves

    def handle_click(self, row, col):
        # If a piece is already selected
        if self.selected_piece:
            # Check if the clicked position is a valid move
            if (row, col) in self.valid_moves:
                # Make the move
                prev_row, prev_col = self.selected_piece.row, self.selected_piece.col
                self.board[prev_row][prev_col] = None
                
                # If capturing, remove the opponent piece
                if self.board[row][col]:
                    if self.board[row][col].piece_type == 'king':
                        print(f"{self.selected_piece.color.capitalize()} wins!")
                        pygame.time.delay(3000)  # Delay for 3 seconds
                        self.init_board()  # Reset the board
                        self.turn = 'white'
                        self.selected_piece = None
                        self.valid_moves = []
                        return
                
                # Move the piece
                self.selected_piece.move(row, col)
                self.board[row][col] = self.selected_piece
                
                # Switch turns
                self.turn = 'black' if self.turn == 'white' else 'white'
                self.selected_piece = None
                self.valid_moves = []
            
            # If clicking on another piece of the same color, select that piece instead
            elif self.board[row][col] and self.board[row][col].color == self.turn:
                self.selected_piece = self.board[row][col]
                self.valid_moves = self.get_valid_moves(self.selected_piece)
            
            # If clicking elsewhere, deselect
            else:
                self.selected_piece = None
                self.valid_moves = []
        
        # If no piece is selected, select a piece of the current turn
        elif self.board[row][col] and self.board[row][col].color == self.turn:
            self.selected_piece = self.board[row][col]
            self.valid_moves = self.get_valid_moves(self.selected_piece)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // SQUARE_SIZE
                        row = pos[1] // SQUARE_SIZE
                        self.handle_click(row, col)
            
            self.screen.fill(BLACK)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Main function
def main():
    game = ChessGame()
    game.run()

if __name__ == "__main__":
    main()