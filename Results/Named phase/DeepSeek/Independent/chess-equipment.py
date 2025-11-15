import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)  # With transparency

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess with Modified Knight Placement')
clock = pygame.time.Clock()

# Load piece images
def load_pieces():
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            img = pygame.image.load(f'chess_pieces/{color}{piece}.png')
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            pieces[f'{color}{piece}'] = img
    return pieces

# Create a simple representation of pieces for testing
# In a real implementation, you would use actual images
pieces = load_pieces()

class ChessBoard:
    def __init__(self):
        self.reset_board()
        
    def reset_board(self):
        # Initialize empty board
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Set up pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = {'type': 'p', 'color': 'b'}
            self.board[6][col] = {'type': 'p', 'color': 'w'}
        
        # Set up rooks
        self.board[0][0] = {'type': 'r', 'color': 'b'}
        self.board[0][7] = {'type': 'r', 'color': 'b'}
        self.board[7][0] = {'type': 'r', 'color': 'w'}
        self.board[7][7] = {'type': 'r', 'color': 'w'}
        
        # Set up bishops
        self.board[0][2] = {'type': 'b', 'color': 'b'}
        self.board[0][5] = {'type': 'b', 'color': 'b'}
        self.board[7][2] = {'type': 'b', 'color': 'w'}
        self.board[7][5] = {'type': 'b', 'color': 'w'}
        
        # Set up queens
        self.board[0][3] = {'type': 'q', 'color': 'b'}
        self.board[7][3] = {'type': 'q', 'color': 'w'}
        
        # Set up kings
        self.board[0][4] = {'type': 'k', 'color': 'b'}
        self.board[7][4] = {'type': 'k', 'color': 'w'}
        
        # Modified knight placement - center four squares
        # White knights on d4 and e5, black knights on d5 and e4
        self.board[3][3] = {'type': 'n', 'color': 'w'}  # d4 (white)
        self.board[4][4] = {'type': 'n', 'color': 'w'}  # e5 (white)
        self.board[4][3] = {'type': 'n', 'color': 'b'}  # d5 (black)
        self.board[3][4] = {'type': 'n', 'color': 'b'}  # e4 (black)
        
        # Traditional knight positions remain empty
        # self.board[0][1] and self.board[0][6] remain empty for black
        # self.board[7][1] and self.board[7][6] remain empty for white
        
        self.current_turn = 'w'
        self.selected_piece = None
        self.valid_moves = []
        
    def draw(self, screen, pieces):
        # Draw the board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw piece if exists
                piece = self.board[row][col]
                if piece:
                    piece_img = pieces[f"{piece['color']}{piece['type']}"]
                    screen.blit(piece_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight selected piece
        if self.selected_piece:
            row, col = self.selected_piece
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(HIGHLIGHT)
            screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            
            # Highlight valid moves
            for move_row, move_col in self.valid_moves:
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((0, 255, 0, 100))  # Green with transparency
                screen.blit(highlight, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))
    
    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        # If a piece is already selected
        if self.selected_piece:
            selected_row, selected_col = self.selected_piece
            
            # Check if the click is on a valid move
            if (row, col) in self.valid_moves:
                # Move the piece
                self.board[row][col] = self.board[selected_row][selected_col]
                self.board[selected_row][selected_col] = None
                self.current_turn = 'b' if self.current_turn == 'w' else 'w'
            
            # Reset selection
            self.selected_piece = None
            self.valid_moves = []
            return
        
        # Select a piece if it's of the current player's color
        if self.board[row][col] and self.board[row][col]['color'] == self.current_turn:
            self.selected_piece = (row, col)
            self.calculate_valid_moves(row, col)
    
    def calculate_valid_moves(self, row, col):
        self.valid_moves = []
        piece = self.board[row][col]
        
        # Simplified move calculation - in a real implementation, you would need
        # to implement proper movement rules for each piece type
        if piece['type'] == 'p':  # Pawn
            direction = -1 if piece['color'] == 'w' else 1
            # Move forward one square
            if 0 <= row + direction < BOARD_SIZE and not self.board[row + direction][col]:
                self.valid_moves.append((row + direction, col))
                # Move forward two squares from starting position
                if (piece['color'] == 'w' and row == 6) or (piece['color'] == 'b' and row == 1):
                    if not self.board[row + 2 * direction][col]:
                        self.valid_moves.append((row + 2 * direction, col))
            # Capture diagonally
            for c_offset in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + c_offset < BOARD_SIZE:
                    if self.board[row + direction][col + c_offset] and \
                       self.board[row + direction][col + c_offset]['color'] != piece['color']:
                        self.valid_moves.append((row + direction, col + c_offset))
        
        elif piece['type'] == 'n':  # Knight
            knight_moves = [
                (row - 2, col - 1), (row - 2, col + 1),
                (row - 1, col - 2), (row - 1, col + 2),
                (row + 1, col - 2), (row + 1, col + 2),
                (row + 2, col - 1), (row + 2, col + 1)
            ]
            for r, c in knight_moves:
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if not self.board[r][c] or self.board[r][c]['color'] != piece['color']:
                        self.valid_moves.append((r, c))
        
        # For other pieces, you would implement their movement rules similarly

# Main game loop
def main():
    board = ChessBoard()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    board.handle_click(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_r:  # Reset the board
                    board.reset_board()
        
        screen.fill(WHITE)
        board.draw(screen, pieces)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    # Note: This code assumes you have a folder named 'chess_pieces' with images
    # named like 'wp.png', 'bn.png', etc. If you don't have these images,
    # you'll need to create them or modify the code to draw the pieces differently.
    main()