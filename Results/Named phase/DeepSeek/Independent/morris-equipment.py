import numpy as np
import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 600
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (240, 217, 181)
PLAYER1_COLOR = (0, 0, 0)  # Black
PLAYER2_COLOR = (255, 255, 255)  # White
HIGHLIGHT_COLOR = (255, 0, 0)
MILL_COLOR = (0, 255, 0)
DOT_RADIUS = 10

# Board representation
# The board has 25 positions (24 standard + 1 center)
# Positions are numbered 0-23 for the standard positions, and 24 for the center

# Adjacency list for movement (including center connections)
ADJACENT = {
    0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
    6: [7, 11], 7: [4, 6, 8], 8: [7, 12], 9: [0, 10, 21], 10: [3, 9, 11, 18], 
    11: [6, 10, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23], 
    15: [11, 16], 16: [15, 17, 19], 17: [12, 16], 18: [10, 19], 19: [16, 18, 20, 22], 
    20: [13, 19], 21: [9, 22], 22: [19, 21, 23], 23: [14, 22],
    # Center connections (position 24)
    24: [4, 7, 10, 13, 16, 19]  # Center connects to all inner ring positions
}

# Mill combinations (including mills that involve the center)
MILLS = [
    # Horizontal mills
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [9, 10, 11], [12, 13, 14], [15, 16, 17],
    [18, 19, 20], [21, 22, 23],
    # Vertical mills
    [0, 9, 21], [3, 10, 18], [6, 11, 15],
    [1, 4, 7], [16, 19, 22], [8, 12, 17],
    [5, 13, 20], [2, 14, 23],
    # Mills involving the center
    [4, 24, 7], [10, 24, 13], [16, 24, 19],
    [1, 4, 24], [7, 4, 24], [10, 24, 13],
    [13, 24, 10], [16, 24, 19], [19, 24, 16]
]

# Game state
class GameState:
    def __init__(self):
        self.board = [None] * 25  # 24 standard positions + 1 center
        self.player = 0  # 0 for player 1 (black), 1 for player 2 (white)
        self.phase = 0  # 0: placement, 1: movement, 2: flying
        self.pieces_to_place = [9, 9]  # Pieces left to place for each player
        self.pieces_on_board = [0, 0]  # Pieces on board for each player
        self.selected = None
        self.mill_formed = False
        self.game_over = False
        self.winner = None
        
    def place_piece(self, pos):
        if self.board[pos] is None and self.pieces_to_place[self.player] > 0:
            self.board[pos] = self.player
            self.pieces_to_place[self.player] -= 1
            self.pieces_on_board[self.player] += 1
            
            # Check for mill
            if self.check_mill(pos):
                self.mill_formed = True
            else:
                self.next_turn()
            
            # Check if we should move to movement phase
            if self.pieces_to_place[0] == 0 and self.pieces_to_place[1] == 0:
                self.phase = 1
                
            return True
        return False
    
    def move_piece(self, from_pos, to_pos):
        if (self.board[from_pos] == self.player and self.board[to_pos] is None and
            (self.phase == 2 or to_pos in ADJACENT[from_pos])):
            self.board[from_pos] = None
            self.board[to_pos] = self.player
            
            # Check for mill
            if self.check_mill(to_pos):
                self.mill_formed = True
            else:
                self.next_turn()
                
            return True
        return False
    
    def remove_piece(self, pos):
        if self.board[pos] == 1 - self.player and not self.check_mill(pos) or self.all_in_mills(1 - self.player):
            self.board[pos] = None
            self.pieces_on_board[1 - self.player] -= 1
            
            # Check if game is over
            if self.pieces_on_board[1 - self.player] < 3:
                self.game_over = True
                self.winner = self.player
                
            # Check if opponent can fly
            if self.pieces_on_board[1 - self.player] == 3 and self.phase == 1:
                self.phase = 2  # Opponent can now fly
                
            self.mill_formed = False
            self.next_turn()
            return True
        return False
    
    def check_mill(self, pos):
        player = self.board[pos]
        if player is None:
            return False
            
        for mill in MILLS:
            if pos in mill:
                if all(self.board[p] == player for p in mill):
                    return True
        return False
    
    def all_in_mills(self, player):
        # Check if all of player's pieces are in mills
        for pos in range(25):
            if self.board[pos] == player and not self.check_mill(pos):
                return False
        return True
    
    def next_turn(self):
        self.player = 1 - self.player
        self.selected = None
        
    def get_valid_moves(self, pos):
        if self.board[pos] != self.player:
            return []
            
        if self.phase == 0:  # Placement phase
            return [i for i in range(25) if self.board[i] is None]
        elif self.phase == 1:  # Movement phase
            return [adj for adj in ADJACENT[pos] if self.board[adj] is None]
        else:  # Flying phase
            return [i for i in range(25) if self.board[i] is None]

# Board coordinates for drawing
def get_board_coordinates():
    # Standard coordinates for the 24 positions
    coordinates = []
    
    # Outer ring
    ring_size = BOARD_SIZE // 2
    for i in range(8):
        angle = i * np.pi / 4
        x = WIDTH // 2 + int(ring_size * np.cos(angle))
        y = HEIGHT // 2 + int(ring_size * np.sin(angle))
        coordinates.append((x, y))
    
    # Middle ring
    ring_size = BOARD_SIZE // 3
    for i in range(8):
        angle = i * np.pi / 4
        x = WIDTH // 2 + int(ring_size * np.cos(angle))
        y = HEIGHT // 2 + int(ring_size * np.sin(angle))
        coordinates.append((x, y))
    
    # Inner ring
    ring_size = BOARD_SIZE // 6
    for i in range(8):
        angle = i * np.pi / 4
        x = WIDTH // 2 + int(ring_size * np.cos(angle))
        y = HEIGHT // 2 + int(ring_size * np.sin(angle))
        coordinates.append((x, y))
    
    # Center position
    coordinates.append((WIDTH // 2, HEIGHT // 2))
    
    return coordinates

# Draw the board
def draw_board(screen, game_state, coordinates):
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the board lines
    for i in range(0, 8, 2):
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, coordinates[i], coordinates[(i+4)%8], 2)
        pygame.draw.line(screen, LINE_COLOR, coordinates[i+8], coordinates[(i+4)%8+8], 2)
        pygame.draw.line(screen, LINE_COLOR, coordinates[i+16], coordinates[(i+4)%8+16], 2)
        
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, coordinates[(i+2)%8], coordinates[(i+6)%8], 2)
        pygame.draw.line(screen, LINE_COLOR, coordinates[(i+2)%8+8], coordinates[(i+6)%8+8], 2)
        pygame.draw.line(screen, LINE_COLOR, coordinates[(i+2)%8+16], coordinates[(i+6)%8+16], 2)
    
    # Draw connections to center
    center_pos = 24
    for adj in ADJACENT[center_pos]:
        pygame.draw.line(screen, LINE_COLOR, coordinates[center_pos], coordinates[adj], 2)
    
    # Draw positions
    for i, (x, y) in enumerate(coordinates):
        color = LINE_COLOR
        if game_state.board[i] == 0:
            color = PLAYER1_COLOR
        elif game_state.board[i] == 1:
            color = PLAYER2_COLOR
            
        pygame.draw.circle(screen, color, (x, y), DOT_RADIUS)
        
        # Highlight selected piece
        if i == game_state.selected:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (x, y), DOT_RADIUS + 3, 2)
            
        # Highlight mills
        for mill in MILLS:
            if i in mill and all(game_state.board[pos] == game_state.board[i] for pos in mill if game_state.board[i] is not None):
                pygame.draw.circle(screen, MILL_COLOR, (x, y), DOT_RADIUS + 5, 2)
    
    # Draw game info
    font = pygame.font.SysFont(None, 36)
    player_text = f"Player {'Black' if game_state.player == 0 else 'White'}'s turn"
    phase_text = f"Phase: {'Placement' if game_state.phase == 0 else 'Movement' if game_state.phase == 1 else 'Flying'}"
    pieces_text = f"Pieces to place: {game_state.pieces_to_place[game_state.player]}"
    
    screen.blit(font.render(player_text, True, LINE_COLOR), (20, 20))
    screen.blit(font.render(phase_text, True, LINE_COLOR), (20, 60))
    screen.blit(font.render(pieces_text, True, LINE_COLOR), (20, 100))
    
    if game_state.game_over:
        winner_text = f"Game Over! {'Black' if game_state.winner == 0 else 'White'} wins!"
        screen.blit(font.render(winner_text, True, (255, 0, 0)), (WIDTH // 2 - 150, HEIGHT - 50))

# Find which position was clicked
def find_clicked_position(mouse_pos, coordinates):
    x, y = mouse_pos
    for i, (pos_x, pos_y) in enumerate(coordinates):
        if (pos_x - x)**2 + (pos_y - y)**2 <= DOT_RADIUS**2 * 4:
            return i
    return None

# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nine Men's Morris with Center")
    clock = pygame.time.Clock()
    
    game_state = GameState()
    coordinates = get_board_coordinates()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN and not game_state.game_over:
                pos = find_clicked_position(event.pos, coordinates)
                if pos is not None:
                    if game_state.mill_formed:
                        # Try to remove opponent's piece
                        if game_state.remove_piece(pos):
                            pass
                    elif game_state.phase == 0:  # Placement phase
                        if game_state.place_piece(pos):
                            pass
                    else:  # Movement or flying phase
                        if game_state.selected is None:
                            if game_state.board[pos] == game_state.player:
                                game_state.selected = pos
                        else:
                            if game_state.move_piece(game_state.selected, pos):
                                game_state.selected = None
                            elif game_state.board[pos] == game_state.player:
                                game_state.selected = pos
        
        draw_board(screen, game_state, coordinates)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()