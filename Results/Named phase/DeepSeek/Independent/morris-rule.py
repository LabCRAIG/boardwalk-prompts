import numpy as np
import pygame
import sys
from enum import Enum

class Player(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class Phase(Enum):
    PLACING = 0
    MOVING = 1
    FLYING = 2

class NineMensMorris:
    def __init__(self):
        # Board representation: 24 points (0-23)
        # Board layout:
        # 0 - - - - - 1 - - - - - 2
        # |           |           |
        # |   3 - - - 4 - - - 5   |
        # |   |       |       |   |
        # |   |   6 - 7 - 8   |   |
        # |   |   |       |   |   |
        # 9 - 10- 11      12- 13- 14
        # |   |   |       |   |   |
        # |   |   15- 16- 17  |   |
        # |   |       |       |   |
        # |   18- - -19- - - 20   |
        # |           |           |
        # 21- - - - -22- - - - - 23
        
        self.board = [Player.NONE] * 24
        self.current_player = Player.WHITE
        self.phase = Phase.PLACING
        self.pieces_to_place = {Player.WHITE: 9, Player.BLACK: 9}
        self.pieces_on_board = {Player.WHITE: 0, Player.BLACK: 0}
        self.selected_piece = None
        self.mill_formed = False
        self.game_over = False
        self.winner = None
        
        # Adjacency list for movement
        self.adjacent_points = {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [7, 12],
            9: [0, 10, 21],
            10: [3, 9, 11, 18],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 14, 20],
            14: [2, 13, 23],
            15: [11, 16],
            16: [15, 17, 19],
            17: [12, 16],
            18: [10, 19],
            19: [16, 18, 20, 22],
            20: [13, 19],
            21: [9, 22],
            22: [19, 21, 23],
            23: [14, 22]
        }
        
        # Mill lines (groups of 3 points that form a mill)
        self.mill_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11],
            [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7],
            [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]
        
        # Square definitions for the special rule
        self.squares = {
            "outer": [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 22, 23],
            "middle": [4, 7, 10, 13, 16, 19],
            "inner": []  # No inner square in standard Nine Men's Morris
        }

    def switch_player(self):
        self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE

    def is_mill(self, point):
        """Check if placing a piece at the given point forms a mill"""
        player = self.board[point]
        if player == Player.NONE:
            return False
            
        for line in self.mill_lines:
            if point in line:
                if all(self.board[p] == player for p in line):
                    return True
        return False

    def get_square_type(self, point):
        """Determine which square a point belongs to"""
        if point in self.squares["outer"]:
            return "outer"
        elif point in self.squares["middle"]:
            return "middle"
        else:
            return "inner"

    def place_piece(self, point):
        """Place a piece on the board during the placing phase"""
        if self.board[point] != Player.NONE:
            return False
            
        self.board[point] = self.current_player
        self.pieces_to_place[self.current_player] -= 1
        self.pieces_on_board[self.current_player] += 1
        
        # Check if a mill was formed
        if self.is_mill(point):
            self.mill_formed = True
            return True
            
        self.switch_player()
        return True

    def move_piece(self, from_point, to_point):
        """Move a piece on the board during the moving phase"""
        if self.board[from_point] != self.current_player or self.board[to_point] != Player.NONE:
            return False
            
        # Check if the move is valid (adjacent points or flying)
        if (self.phase != Phase.FLYING and to_point not in self.adjacent_points[from_point]):
            return False
            
        self.board[from_point] = Player.NONE
        self.board[to_point] = self.current_player
        
        # Check if a mill was formed
        if self.is_mill(to_point):
            self.mill_formed = True
            return True
            
        self.switch_player()
        return True

    def remove_opponent_piece(self, point, mill_square_type):
        """Remove an opponent's piece according to the special rule"""
        if (self.board[point] == self.current_player or 
            self.board[point] == Player.NONE or
            self.get_square_type(point) != mill_square_type):
            return False
            
        # Check if the piece is part of a mill (can't remove unless no other pieces available)
        if self.is_mill(point):
            # Check if all opponent pieces are in mills
            opponent = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
            all_in_mills = True
            for i in range(24):
                if self.board[i] == opponent and not self.is_mill(i):
                    all_in_mills = False
                    break
                    
            if not all_in_mills:
                return False
                
        self.board[point] = Player.NONE
        self.pieces_on_board[Player.BLACK if self.current_player == Player.WHITE else Player.WHITE] -= 1
        
        # Check for game over
        opponent = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
        if self.pieces_on_board[opponent] < 3:
            self.game_over = True
            self.winner = self.current_player
        elif self.phase == Phase.MOVING and self.pieces_on_board[opponent] == 3:
            # Opponent enters flying phase
            pass
            
        self.mill_formed = False
        self.switch_player()
        return True

    def check_phase_transition(self):
        """Check if we need to transition to the next phase"""
        if self.phase == Phase.PLACING and self.pieces_to_place[self.current_player] == 0:
            self.phase = Phase.MOVING
            
        if (self.phase == Phase.MOVING and 
            self.pieces_on_board[self.current_player] == 3 and
            self.pieces_to_place[self.current_player] == 0):
            self.phase = Phase.FLYING

    def handle_click(self, point):
        """Handle a click on the board"""
        if self.game_over:
            return
            
        if self.mill_formed:
            # We're in the mill removal phase
            mill_square_type = None
            for i in range(24):
                if self.is_mill(i) and self.board[i] == self.current_player:
                    mill_square_type = self.get_square_type(i)
                    break
                    
            if mill_square_type and self.remove_opponent_piece(point, mill_square_type):
                self.check_phase_transition()
            return
            
        if self.phase == Phase.PLACING:
            if self.place_piece(point):
                self.check_phase_transition()
        else:  # MOVING or FLYING phase
            if self.selected_piece is None:
                if self.board[point] == self.current_player:
                    self.selected_piece = point
            else:
                if self.move_piece(self.selected_piece, point):
                    self.check_phase_transition()
                self.selected_piece = None

# Pygame visualization
class GameUI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Nine Men's Morris")
        
        self.clock = pygame.time.Clock()
        self.game = NineMensMorris()
        
        # Board coordinates for the 24 points
        self.point_coords = [
            (200, 200), (400, 200), (600, 200),  # 0, 1, 2
            (266, 266), (400, 266), (534, 266),  # 3, 4, 5
            (333, 333), (400, 333), (467, 333),  # 6, 7, 8
            (200, 400), (266, 400), (333, 400),  # 9, 10, 11
            (467, 400), (534, 400), (600, 400),  # 12, 13, 14
            (333, 467), (400, 467), (467, 467),  # 15, 16, 17
            (266, 534), (400, 534), (534, 534),  # 18, 19, 20
            (200, 600), (400, 600), (600, 600)   # 21, 22, 23
        ]
        
        self.point_radius = 15
        self.selected_point = None
        
    def draw_board(self):
        self.screen.fill((240, 217, 181))  # Beige background
        
        # Draw board lines
        for line in self.game.mill_lines:
            if len(line) == 3:
                start_pos = self.point_coords[line[0]]
                end_pos = self.point_coords[line[2]]
                pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 5)
        
        # Draw points
        for i, (x, y) in enumerate(self.point_coords):
            color = (150, 150, 150)  # Gray for empty points
            if self.game.board[i] == Player.WHITE:
                color = (255, 255, 255)  # White
            elif self.game.board[i] == Player.BLACK:
                color = (0, 0, 0)  # Black
                
            pygame.draw.circle(self.screen, color, (x, y), self.point_radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.point_radius, 2)
            
            # Highlight selected point
            if i == self.selected_point:
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), self.point_radius + 5, 2)
        
        # Draw game info
        font = pygame.font.SysFont(None, 36)
        player_text = f"Current Player: {'White' if self.game.current_player == Player.WHITE else 'Black'}"
        phase_text = f"Phase: {self.game.phase.name}"
        white_pieces = f"White: {self.game.pieces_on_board[Player.WHITE]} on board, {self.game.pieces_to_place[Player.WHITE]} to place"
        black_pieces = f"Black: {self.game.pieces_on_board[Player.BLACK]} on board, {self.game.pieces_to_place[Player.BLACK]} to place"
        
        texts = [player_text, phase_text, white_pieces, black_pieces]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 50 + i * 40))
            
        if self.game.mill_formed:
            mill_text = "MILL FORMED! Remove an opponent's piece from the same square."
            text_surface = font.render(mill_text, True, (255, 0, 0))
            self.screen.blit(text_surface, (50, 700))
            
        if self.game.game_over:
            winner_text = f"GAME OVER! {'White' if self.game.winner == Player.WHITE else 'Black'} wins!"
            text_surface = font.render(winner_text, True, (0, 100, 0))
            self.screen.blit(text_surface, (250, 50))
    
    def get_clicked_point(self, pos):
        x, y = pos
        for i, (px, py) in enumerate(self.point_coords):
            if (px - x)**2 + (py - y)**2 <= self.point_radius**2:
                return i
        return None
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    point = self.get_clicked_point(event.pos)
                    if point is not None:
                        self.game.handle_click(point)
                        self.selected_point = self.game.selected_piece
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.run()