
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pieces_to_place = {Player.ONE.value: 9, Player.TWO.value: 9}
        self.pieces_on_board = {Player.ONE.value: 0, Player.TWO.value: 0}
        self.in_mill = set()  # Tracks positions that are part of a mill
        self.previous_mills = set()  # Tracks mills from previous turn
        self.phase = "placement"  # "placement", "movement", or "flying"
        self.pieces = {Player.ONE.value: 'X', Player.TWO.value: 'O'}
        self.last_mill_formed = False

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        current_player_piece = self.pieces[self.current_player]
        opponent_player_piece = self.pieces[1 - self.current_player]
        
        # Check if it's a placement move
        if is_placement(move):
            if self.phase != "placement":
                print("You can no longer place pieces!")
                return False
                
            piece, pos = get_move_elements(move)
            
            # Check if the piece is the current player's
            if piece != current_player_piece:
                print("You must place your own pieces!")
                return False
                
            # Check if the position is empty
            if self.board.layout[pos[0]][pos[1]] != '_':
                print("That position is already occupied!")
                return False
                
            return True
            
        # Check if it's a movement move
        elif is_movement(move):
            if self.phase == "placement":
                print("You must place all your pieces first!")
                return False
                
            origin, dest = get_move_elements(move)
            
            # Check if origin contains player's piece
            if self.board.layout[origin[0]][origin[1]] != current_player_piece:
                print("You must move your own piece!")
                return False
                
            # Check if destination is empty
            if self.board.layout[dest[0]][dest[1]] != '_':
                print("Destination is already occupied!")
                return False
                
            # Check if the move is valid (adjacent in normal phase or any empty in flying phase)
            if self.phase == "movement":
                if not self.is_adjacent(origin, dest):
                    print("You can only move to adjacent positions!")
                    return False
            # Flying phase - can move anywhere
            
            return True
            
        # It's a capture move
        else:
            if not self.last_mill_formed:
                print("You can only capture after forming a mill!")
                return False
                
            try:
                pos = tuple(map(int, move.split(',')))
                
                # Check if there's an opponent's piece at the position
                if self.board.layout[pos[0]][pos[1]] != opponent_player_piece:
                    print("You can only capture your opponent's pieces!")
                    return False
                    
                # Check if the piece is part of a mill - can only capture if all pieces are in mills
                all_opponent_in_mills = True
                for i in range(self.board.height):
                    for j in range(self.board.width):
                        if self.board.layout[i][j] == opponent_player_piece:
                            if (i, j) not in self.in_mill:
                                all_opponent_in_mills = False
                                break
                    if not all_opponent_in_mills:
                        break
                        
                if (pos[0], pos[1]) in self.in_mill and not all_opponent_in_mills:
                    print("You cannot capture pieces in a mill unless all pieces are in mills!")
                    return False
                    
                return True
                
            except:
                print("Invalid capture format! Use row,col")
                return False
    
    def perform_move(self, move):
        if is_placement(move):
            super().perform_move(move)
            piece, pos = get_move_elements(move)
            
            self.pieces_to_place[self.current_player] -= 1
            self.pieces_on_board[self.current_player] += 1
            
            # Check if a mill was formed
            self.check_mills()
            
            # Update phase if needed
            if self.pieces_to_place[Player.ONE.value] == 0 and self.pieces_to_place[Player.TWO.value] == 0:
                self.phase = "movement"
                
        elif is_movement(move):
            super().perform_move(move)
            
            # Check if a mill was formed
            self.check_mills()
            
        else:  # Capture move
            pos = tuple(map(int, move.split(',')))
            self.board.layout[pos[0]][pos[1]] = '_'
            self.pieces_on_board[1 - self.current_player] -= 1
            
            # Remove the captured piece from any mills
            if pos in self.in_mill:
                self.in_mill.remove(pos)
                
            self.last_mill_formed = False
            
            # Check if opponent should enter flying phase
            if self.pieces_on_board[1 - self.current_player] == 3 and self.phase == "movement":
                # Player with only 3 pieces can fly
                self.phase = "flying"
    
    def check_mills(self):
        # Save current mills to previous_mills
        self.previous_mills = deepcopy(self.in_mill)
        self.in_mill = set()
        
        # Check horizontal mills
        for i in range(7):
            for j in range(5):
                if j+2 < 7:  # Ensure we don't go out of bounds
                    if (self.board.layout[i][j] == self.board.layout[i][j+1] == self.board.layout[i][j+2] and 
                        self.board.layout[i][j] != '_' and self.board.layout[i][j] != ' '):
                        self.in_mill.add((i, j))
                        self.in_mill.add((i, j+1))
                        self.in_mill.add((i, j+2))
        
        # Check vertical mills
        for i in range(5):
            for j in range(7):
                if i+2 < 7:  # Ensure we don't go out of bounds
                    if (self.board.layout[i][j] == self.board.layout[i+1][j] == self.board.layout[i+2][j] and 
                        self.board.layout[i][j] != '_' and self.board.layout[i][j] != ' '):
                        self.in_mill.add((i, j))
                        self.in_mill.add((i+1, j))
                        self.in_mill.add((i+2, j))
        
        # Check if a new mill was formed
        new_mill_formed = False
        for pos in self.in_mill:
            if pos not in self.previous_mills and self.board.layout[pos[0]][pos[1]] == self.pieces[self.current_player]:
                new_mill_formed = True
                break
                
        self.last_mill_formed = new_mill_formed
    
    def is_adjacent(self, pos1, pos2):
        # Define adjacency for Nine Men's Morris
        adjacency = {
            # Outer square
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (3, 0): [(0, 0), (6, 0), (3, 1)],
            (3, 6): [(0, 6), (6, 6), (3, 5)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(6, 0), (6, 6), (5, 3)],
            (6, 6): [(6, 3), (3, 6)],
            
            # Middle square
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (3, 1): [(3, 0), (1, 1), (5, 1), (3, 2)],
            (3, 5): [(3, 6), (1, 5), (5, 5), (3, 4)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(5, 1), (5, 5), (6, 3), (4, 3)],
            (5, 5): [(5, 3), (3, 5)],
            
            # Inner square
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4), (3, 3)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 2): [(3, 1), (2, 2), (4, 2), (3, 3)],
            (3, 4): [(3, 5), (2, 4), (4, 4), (3, 3)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (5, 3), (3, 3)],
            (4, 4): [(4, 3), (3, 4)],
            
            # Center (added per rule change)
            (3, 3): [(2, 3), (3, 2), (4, 3), (3, 4)]
        }
        
        if pos1 in adjacency and pos2 in adjacency[pos1]:
            return True
        return False
    
    def prompt_current_player(self):
        player_name = "X" if self.current_player == Player.ONE.value else "O"
        
        if self.last_mill_formed:
            print(f"Player {player_name}, you formed a mill! Capture an opponent's piece.")
            return input("Capture (row,col): ")
        
        if self.phase == "placement":
            pieces_left = self.pieces_to_place[self.current_player]
            print(f"Player {player_name}'s turn (Placement phase - {pieces_left} pieces left to place)")
            return f"{self.pieces[self.current_player]} " + input("Place at (row,col): ")
        
        if self.phase == "movement":
            print(f"Player {player_name}'s turn (Movement phase)")
            origin = input("Select piece at (row,col): ")
            dest = input("Move to (row,col): ")
            return f"{origin} {dest}"
        
        if self.phase == "flying":
            flying_player = "X" if self.pieces_on_board[Player.ONE.value] == 3 else "O"
            if player_name == flying_player:
                print(f"Player {player_name}'s turn (Flying phase)")
            else:
                print(f"Player {player_name}'s turn (Movement phase)")
            origin = input("Select piece at (row,col): ")
            dest = input("Move to (row,col): ")
            return f"{origin} {dest}"
    
    def game_finished(self):
        # Game ends if a player has less than 3 pieces after the placement phase
        if self.phase != "placement":
            if self.pieces_on_board[Player.ONE.value] < 3:
                return True
            if self.pieces_on_board[Player.TWO.value] < 3:
                return True
                
        # Game ends if a player has no legal moves
        if self.phase != "placement" and not self.last_mill_formed:
            # Check if current player can move
            current_piece = self.pieces[self.current_player]
            has_moves = False
            
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if self.board.layout[i][j] == current_piece:
                        pos = (i, j)
                        # In flying phase, just need one piece and one empty space
                        if self.phase == "flying" and self.pieces_on_board[self.current_player] == 3:
                            for x in range(self.board.height):
                                for y in range(self.board.width):
                                    if self.board.layout[x][y] == '_':
                                        has_moves = True
                                        break
                                if has_moves:
                                    break
                        else:
                            # In regular movement, check adjacent positions
                            for adj in self.get_adjacent_positions(pos):
                                if self.board.layout[adj[0]][adj[1]] == '_':
                                    has_moves = True
                                    break
                        if has_moves:
                            break
                if has_moves:
                    break
                    
            if not has_moves:
                return True
                
        return False
    
    def get_adjacent_positions(self, pos):
        adjacency = {
            # Outer square
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (3, 0): [(0, 0), (6, 0), (3, 1)],
            (3, 6): [(0, 6), (6, 6), (3, 5)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(6, 0), (6, 6), (5, 3)],
            (6, 6): [(6, 3), (3, 6)],
            
            # Middle square
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (3, 1): [(3, 0), (1, 1), (5, 1), (3, 2)],
            (3, 5): [(3, 6), (1, 5), (5, 5), (3, 4)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(5, 1), (5, 5), (6, 3), (4, 3)],
            (5, 5): [(5, 3), (3, 5)],
            
            # Inner square
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4), (3, 3)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 2): [(3, 1), (2, 2), (4, 2), (3, 3)],
            (3, 4): [(3, 5), (2, 4), (4, 4), (3, 3)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (5, 3), (3, 3)],
            (4, 4): [(4, 3), (3, 4)],
            
            # Center (added per rule change)
            (3, 3): [(2, 3), (3, 2), (4, 3), (3, 4)]
        }
        
        if pos in adjacency:
            return adjacency[pos]
        return []
    
    def get_winner(self):
        if self.pieces_on_board[Player.ONE.value] < 3 and self.phase != "placement":
            return Player.TWO.value
        if self.pieces_on_board[Player.TWO.value] < 3 and self.phase != "placement":
            return Player.ONE.value
            
        # If current player has no legal moves, they lose
        current_piece = self.pieces[self.current_player]
        has_moves = False
        
        if self.phase != "placement" and not self.last_mill_formed:
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if self.board.layout[i][j] == current_piece:
                        pos = (i, j)
                        # In flying phase, just need one piece and one empty space
                        if self.phase == "flying" and self.pieces_on_board[self.current_player] == 3:
                            for x in range(self.board.height):
                                for y in range(self.board.width):
                                    if self.board.layout[x][y] == '_':
                                        has_moves = True
                                        break
                                if has_moves:
                                    break
                        else:
                            # In regular movement, check adjacent positions
                            for adj in self.get_adjacent_positions(pos):
                                if self.board.layout[adj[0]][adj[1]] == '_':
                                    has_moves = True
                                    break
                        if has_moves:
                            break
                if has_moves:
                    break
                    
            if not has_moves:
                return 1 - self.current_player
        
        return None
    
    def next_player(self):
        # If a mill was formed, the same player gets another turn (to capture)
        if self.last_mill_formed:
            return self.current_player
        return 1 - self.current_player
    
    def finish_message(self, winner):
        if winner == Player.ONE.value:
            print("Player X wins the game!")
        elif winner == Player.TWO.value:
            print("Player O wins the game!")
        else:
            print("The game ends in a draw!")

if __name__ == '__main__':
    # Nine Men's Morris board with a valid center position
    morris_layout = (
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _"
    )
    
    # Create the board with a 7x7 grid
    board = Board((7, 7), morris_layout)
    
    # Initialize the game with the board
    game = NineMensMorris(board)
    
    # Start the game
    game.game_loop()
