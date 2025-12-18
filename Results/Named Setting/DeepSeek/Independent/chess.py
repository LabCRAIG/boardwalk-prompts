import pygame
import sys
from pygame.locals import *

class ChessGame:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WINDOW_SIZE = 640
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = self.WINDOW_SIZE // self.BOARD_SIZE
        self.FPS = 60
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.HIGHLIGHT = (247, 247, 105, 150)
        self.MOVE_HIGHLIGHT = (106, 168, 79, 150)
        
        # Setup display
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption('Python Chess')
        self.clock = pygame.time.Clock()
        
        # Load piece images
        self.piece_images = self.load_piece_images()
        
        # Game state
        self.board = self.create_starting_board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'white'
        self.game_over = False
        self.winner = None
        
    def load_piece_images(self):
        """Load and scale chess piece images"""
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        images = {}
        
        for color in colors:
            for piece in pieces:
                try:
                    # You'll need to have these images in a 'pieces' folder
                    # or replace with your own image loading logic
                    img = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    # For a real implementation, load actual piece images here
                    # This is a placeholder - in practice you'd load PNG images
                    pygame.draw.rect(img, (100, 100, 100, 100), 
                                   (5, 5, self.SQUARE_SIZE-10, self.SQUARE_SIZE-10))
                    images[f'{color}_{piece}'] = img
                except:
                    # Fallback: draw text representation
                    img = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    font = pygame.font.Font(None, 36)
                    text = font.render(piece[0].upper(), True, 
                                     (255, 255, 255) if color == 'white' else (0, 0, 0))
                    img.fill((150, 150, 150) if color == 'white' else (50, 50, 50))
                    img.blit(text, (self.SQUARE_SIZE//2 - 10, self.SQUARE_SIZE//2 - 10))
                    images[f'{color}_{piece}'] = img
        
        return images
    
    def create_starting_board(self):
        """Create the initial chess board setup"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Set up pawns
        for col in range(8):
            board[1][col] = {'type': 'pawn', 'color': 'black'}
            board[6][col] = {'type': 'pawn', 'color': 'white'}
        
        # Set up other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        
        for col in range(8):
            board[0][col] = {'type': back_row[col], 'color': 'black'}
            board[7][col] = {'type': back_row[col], 'color': 'white'}
        
        return board
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                # Draw square
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, color, 
                               (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                self.SQUARE_SIZE, self.SQUARE_SIZE))
                
                # Draw piece if exists
                piece = self.board[row][col]
                if piece:
                    piece_img = self.piece_images[f"{piece['color']}_{piece['type']}"]
                    self.screen.blit(piece_img, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
        
        # Highlight selected piece
        if self.selected_piece:
            row, col = self.selected_piece
            highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(self.HIGHLIGHT)
            self.screen.blit(highlight, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
        
        # Highlight valid moves
        for move_row, move_col in self.valid_moves:
            highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(self.MOVE_HIGHLIGHT)
            self.screen.blit(highlight, (move_col * self.SQUARE_SIZE, move_row * self.SQUARE_SIZE))
    
    def get_valid_moves(self, row, col):
        """Get valid moves for a piece at given position"""
        piece = self.board[row][col]
        if not piece or piece['color'] != self.turn:
            return []
        
        moves = []
        piece_type = piece['type']
        
        # Basic movement patterns (simplified - real chess has more complex rules)
        if piece_type == 'pawn':
            direction = -1 if piece['color'] == 'white' else 1
            # Move forward
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                moves.append((row + direction, col))
                # Double move from starting position
                if ((piece['color'] == 'white' and row == 6) or 
                    (piece['color'] == 'black' and row == 1)) and \
                   not self.board[row + 2 * direction][col]:
                    moves.append((row + 2 * direction, col))
            
            # Capture diagonally
            for capture_col in [col - 1, col + 1]:
                if 0 <= row + direction < 8 and 0 <= capture_col < 8:
                    target = self.board[row + direction][capture_col]
                    if target and target['color'] != piece['color']:
                        moves.append((row + direction, capture_col))
        
        elif piece_type == 'rook':
            # Horizontal and vertical movement
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                for i in range(1, 8):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != piece['color']:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'knight':
            # L-shaped movement
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), 
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if not self.board[r][c] or self.board[r][c]['color'] != piece['color']:
                        moves.append((r, c))
        
        elif piece_type == 'bishop':
            # Diagonal movement
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != piece['color']:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'queen':
            # Combination of rook and bishop movement
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), 
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != piece['color']:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'king':
            # One square in any direction
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8:
                        if not self.board[r][c] or self.board[r][c]['color'] != piece['color']:
                            moves.append((r, c))
        
        return moves
    
    def make_move(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check if move is valid
        if (to_row, to_col) not in self.valid_moves:
            return False
        
        # Move the piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Check for pawn promotion
        piece = self.board[to_row][to_col]
        if piece['type'] == 'pawn' and (to_row == 0 or to_row == 7):
            # Automatically promote to queen (simplified)
            piece['type'] = 'queen'
        
        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        # Check for game over (simplified - just check if king is captured)
        # In real chess, you'd need to check for checkmate and stalemate
        kings = {'white': False, 'black': False}
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['type'] == 'king':
                    kings[piece['color']] = True
        
        if not kings['white']:
            self.game_over = True
            self.winner = 'black'
        elif not kings['black']:
            self.game_over = True
            self.winner = 'white'
        
        return True
    
    def handle_click(self, pos):
        """Handle mouse click on the board"""
        if self.game_over:
            return
        
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        if self.selected_piece:
            # Try to move the selected piece
            if self.make_move(self.selected_piece, (row, col)):
                self.selected_piece = None
                self.valid_moves = []
            else:
                # Select a different piece
                piece = self.board[row][col]
                if piece and piece['color'] == self.turn:
                    self.selected_piece = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
                else:
                    self.selected_piece = None
                    self.valid_moves = []
        else:
            # Select a piece
            piece = self.board[row][col]
            if piece and piece['color'] == self.turn:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
    
    def draw_game_over(self):
        """Display game over message"""
        if self.game_over:
            overlay = pygame.Surface((self.WINDOW_SIZE, self.WINDOW_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            font = pygame.font.Font(None, 72)
            text = font.render(f"{self.winner.capitalize()} wins!", True, self.WHITE)
            text_rect = text.get_rect(center=(self.WINDOW_SIZE//2, self.WINDOW_SIZE//2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Click to play again", True, self.WHITE)
            restart_rect = restart_text.get_rect(center=(self.WINDOW_SIZE//2, self.WINDOW_SIZE//2 + 50))
            self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = self.create_starting_board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'white'
        self.game_over = False
        self.winner = None
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.handle_click(event.pos)
            
            # Draw everything
            self.screen.fill(self.BLACK)
            self.draw_board()
            self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()