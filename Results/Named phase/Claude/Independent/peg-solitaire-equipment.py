import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 7  # Size of the diamond (width at widest point)
CELL_SIZE = 60
PEG_RADIUS = 20
BG_COLOR = (240, 230, 220)
EMPTY_COLOR = (180, 160, 140)
PEG_COLOR = (100, 50, 20)
HIGHLIGHT_COLOR = (255, 200, 0)
SELECT_COLOR = (0, 200, 100)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diamond Peg Solitaire")
clock = pygame.time.Clock()

class DiamondPegSolitaire:
    def __init__(self):
        self.board = {}
        self.selected = None
        self.valid_moves = []
        self.initialize_board()
        
    def initialize_board(self):
        # Create a diamond-shaped board
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                # Calculate distance from center
                distance = abs(r - BOARD_SIZE // 2) + abs(c - BOARD_SIZE // 2)
                if distance <= BOARD_SIZE // 2 :
                    # All positions filled with pegs except the center
                    self.board[(r, c)] = (r != BOARD_SIZE // 2 or c != BOARD_SIZE // 2)
    
    def get_valid_positions(self):
        return [pos for pos in self.board.keys()]
    
    def get_valid_moves(self, pos):
        if pos not in self.board or not self.board[pos]:
            return []
        
        moves = []
        r, c = pos
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # Right, Left, Down, Up
        
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            middle_r, middle_c = r + dr // 2, c + dc // 2
            
            # Check if the landing position is on the board and empty
            if (new_r, new_c) in self.board and not self.board[(new_r, new_c)]:
                # Check if there's a peg in the middle position
                if (middle_r, middle_c) in self.board and self.board[(middle_r, middle_c)]:
                    moves.append((new_r, new_c))
        
        return moves
    
    def make_move(self, from_pos, to_pos):
        if to_pos not in self.get_valid_moves(from_pos):
            return False
        
        # Calculate the position of the jumped peg
        middle_r = (from_pos[0] + to_pos[0]) // 2
        middle_c = (from_pos[1] + to_pos[1]) // 2
        
        # Update the board
        self.board[from_pos] = False  # Remove peg from start
        self.board[to_pos] = True     # Place peg at destination
        self.board[(middle_r, middle_c)] = False  # Remove jumped peg
        
        return True
    
    def is_game_over(self):
        # Check if there are any valid moves left
        for pos in self.board:
            if self.board[pos] and self.get_valid_moves(pos):
                return False
        return True
    
    def count_pegs(self):
        return sum(1 for value in self.board.values() if value)
    
    def handle_click(self, mouse_pos):
        # Convert mouse position to board position
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        board_offset_x = center_x - (BOARD_SIZE * CELL_SIZE) // 2
        board_offset_y = center_y - (BOARD_SIZE * CELL_SIZE) // 2
        
        clicked_c = (mouse_pos[0] - board_offset_x) // CELL_SIZE
        clicked_r = (mouse_pos[1] - board_offset_y) // CELL_SIZE
        clicked_pos = (clicked_r, clicked_c)
        
        # Check if click is on the board
        if clicked_pos in self.board:
            if self.selected is None:
                # Selecting a peg
                if self.board[clicked_pos]:
                    self.selected = clicked_pos
                    self.valid_moves = self.get_valid_moves(clicked_pos)
            else:
                # Already selected a peg, check if this is a valid destination
                if clicked_pos in self.valid_moves:
                    self.make_move(self.selected, clicked_pos)
                    self.selected = None
                    self.valid_moves = []
                elif self.board[clicked_pos]:
                    # Selected another peg
                    self.selected = clicked_pos
                    self.valid_moves = self.get_valid_moves(clicked_pos)
                else:
                    # Clicked an invalid position, deselect
                    self.selected = None
                    self.valid_moves = []
    
    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Calculate board position to center it
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        board_offset_x = center_x - (BOARD_SIZE * CELL_SIZE) // 2
        board_offset_y = center_y - (BOARD_SIZE * CELL_SIZE) // 2
        
        # Draw board and pegs
        for pos in self.board:
            r, c = pos
            x = board_offset_x + c * CELL_SIZE + CELL_SIZE // 2
            y = board_offset_y + r * CELL_SIZE + CELL_SIZE // 2
            
            # Draw cell
            pygame.draw.rect(screen, EMPTY_COLOR, 
                            (board_offset_x + c * CELL_SIZE, 
                             board_offset_y + r * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE), 1)
            
            # Highlight selected position
            if self.selected == pos:
                pygame.draw.circle(screen, SELECT_COLOR, (x, y), PEG_RADIUS + 5)
            
            # Highlight valid moves
            if pos in self.valid_moves:
                pygame.draw.circle(screen, HIGHLIGHT_COLOR, (x, y), PEG_RADIUS - 5)
            
            # Draw peg
            if self.board[pos]:
                pygame.draw.circle(screen, PEG_COLOR, (x, y), PEG_RADIUS)
        
        # Display peg count and game status
        font = pygame.font.SysFont(None, 36)
        pegs_text = font.render(f"Pegs: {self.count_pegs()}", True, (0, 0, 0))
        screen.blit(pegs_text, (20, 20))
        
        if self.is_game_over():
            if self.count_pegs() == 1:
                status = "You won!"
            else:
                status = "Game over"
            status_text = font.render(status, True, (200, 0, 0))
            screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 20))
            
            restart_text = font.render("Press R to restart", True, (0, 0, 0))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 50))

def main():
    game = DiamondPegSolitaire()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    game = DiamondPegSolitaire()
        
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()