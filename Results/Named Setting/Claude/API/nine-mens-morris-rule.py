
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class Phase(Enum):
    PLACING = 0
    MOVING = 1

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pieces_to_place = {Player.ONE.value: 9, Player.TWO.value: 9}
        self.pieces_on_board = {Player.ONE.value: 0, Player.TWO.value: 0}
        self.phase = {Player.ONE.value: Phase.PLACING, Player.TWO.value: Phase.PLACING}
        self.player_pieces = {Player.ONE.value: 'X', Player.TWO.value: 'O'}
        self.last_move_mill = False
        self.current_square = None
        
        # Define the possible mill locations and their associated squares
        self.mills = [
            # Outer square (0)
            [(0, 0), (0, 3), (0, 6)], [(0, 6), (3, 6), (6, 6)], 
            [(6, 6), (6, 3), (6, 0)], [(6, 0), (3, 0), (0, 0)],
            
            # Middle square (1)
            [(1, 1), (1, 3), (1, 5)], [(1, 5), (3, 5), (5, 5)],
            [(5, 5), (5, 3), (5, 1)], [(5, 1), (3, 1), (1, 1)],
            
            # Inner square (2)
            [(2, 2), (2, 3), (2, 4)], [(2, 4), (3, 4), (4, 4)],
            [(4, 4), (4, 3), (4, 2)], [(4, 2), (3, 2), (2, 2)],
            
            # Radial lines
            [(0, 3), (1, 3), (2, 3)], [(3, 6), (3, 5), (3, 4)],
            [(6, 3), (5, 3), (4, 3)], [(3, 0), (3, 1), (3, 2)]
        ]
        
        # Map positions to their associated square
        self.position_to_square = {}
        for i, square_mills in enumerate([
            [(0, 0), (0, 3), (0, 6), (3, 6), (6, 6), (6, 3), (6, 0), (3, 0)],  # Outer
            [(1, 1), (1, 3), (1, 5), (3, 5), (5, 5), (5, 3), (5, 1), (3, 1)],  # Middle
            [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]   # Inner
        ]):
            for pos in square_mills:
                self.position_to_square[pos] = i

        # Define valid connections for movement
        self.connections = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (3, 6): [(0, 6), (6, 6), (3, 5)],
            (6, 6): [(3, 6), (6, 3)],
            (6, 3): [(6, 6), (6, 0), (5, 3)],
            (6, 0): [(6, 3), (3, 0)],
            (3, 0): [(6, 0), (0, 0), (3, 1)],
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (3, 5): [(1, 5), (3, 6), (3, 4), (5, 5)],
            (5, 5): [(3, 5), (5, 3)],
            (5, 3): [(5, 5), (5, 1), (6, 3), (4, 3)],
            (5, 1): [(5, 3), (3, 1)],
            (3, 1): [(5, 1), (3, 0), (3, 2), (1, 1)],
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 4): [(2, 4), (3, 5), (4, 4)],
            (4, 4): [(3, 4), (4, 3)],
            (4, 3): [(4, 4), (4, 2), (5, 3)],
            (4, 2): [(4, 3), (3, 2)],
            (3, 2): [(4, 2), (3, 1), (2, 2)]
        }

    def get_state(self):
        state = super().get_state()
        return (state[0], state[1], [
            self.pieces_to_place.copy(),
            self.pieces_on_board.copy(),
            self.phase.copy(),
            self.last_move_mill,
            self.current_square
        ])

    def prompt_current_player(self):
        player_symbol = self.player_pieces[self.current_player]
        phase = self.phase[self.current_player]
        
        if self.last_move_mill:
            square_name = ["outer", "middle", "inner"][self.current_square]
            return input(f"Player {player_symbol} formed a mill on the {square_name} square. Remove an opponent's piece from that square: ")
        
        if phase == Phase.PLACING:
            return input(f"Player {player_symbol}'s turn ({self.pieces_to_place[self.current_player]} pieces left to place). Place a piece: ")
        else:
            remaining_pieces = self.pieces_on_board[self.current_player]
            if remaining_pieces == 3:
                return input(f"Player {player_symbol}'s turn (flying mode). Move a piece: ")
            else:
                return input(f"Player {player_symbol}'s turn. Move a piece: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        opponent = 1 - self.current_player
        opponent_piece = self.player_pieces[opponent]
        player_piece = self.player_pieces[self.current_player]
        
        # Handle mill capture
        if self.last_move_mill:
            if not is_placement(move):
                print("Please specify a piece to remove in the format: '_ row,col'")
                return False
            
            piece, pos = get_move_elements(move)
            
            # Check if position is on the board
            if self.board.layout[pos[0]][pos[1]] != opponent_piece:
                print("You must remove an opponent's piece.")
                return False
                
            # Check if the piece is on the required square
            if self.position_to_square.get(pos) != self.current_square:
                square_name = ["outer", "middle", "inner"][self.current_square]
                print(f"You must remove a piece from the {square_name} square.")
                return False
            
            # Check if the piece is part of a mill when other pieces are available
            in_mill = False
            for mill in self.mills:
                if pos in mill and all(self.board.layout[r][c] == opponent_piece for r, c in mill):
                    in_mill = True
                    break
                    
            if in_mill:
                # Check if all opponent pieces are in mills
                all_in_mills = True
                for r in range(self.board.height):
                    for c in range(self.board.width):
                        if self.board.layout[r][c] == opponent_piece:
                            piece_in_mill = False
                            for mill in self.mills:
                                if (r, c) in mill and all(self.board.layout[pos_r][pos_c] == opponent_piece 
                                                         for pos_r, pos_c in mill):
                                    piece_in_mill = True
                                    break
                            if not piece_in_mill:
                                all_in_mills = False
                                break
                    if not all_in_mills:
                        break
                        
                if not all_in_mills:
                    print("You cannot remove a piece that is part of a mill when other pieces are available.")
                    return False
            
            return True
            
        # Normal moves (not after a mill)
        phase = self.phase[self.current_player]
        
        if phase == Phase.PLACING:
            # Placement phase
            if not is_placement(move):
                print("During placement phase, use format: 'X row,col'")
                return False
                
            piece, pos = get_move_elements(move)
            if piece != player_piece:
                print(f"You must place your piece ({player_piece})")
                return False
                
            if self.board.layout[pos[0]][pos[1]] != '_':
                print("You can only place pieces on empty spots")
                return False
                
            return True
        else:
            # Movement phase
            if not is_movement(move):
                print("During movement phase, use format: 'row1,col1 row2,col2'")
                return False
                
            origin, dest = get_move_elements(move)
            
            if self.board.layout[origin[0]][origin[1]] != player_piece:
                print("You must move your own piece")
                return False
                
            if self.board.layout[dest[0]][dest[1]] != '_':
                print("You can only move to empty spots")
                return False
                
            # Flying mode (when player has only 3 pieces)
            if self.pieces_on_board[self.current_player] == 3:
                return True
                
            # Normal movement: check if destination is connected to origin
            if dest not in self.connections[origin]:
                print("Invalid move. You can only move to adjacent positions.")
                return False
                
            return True

    def perform_move(self, move):
        if self.last_move_mill:
            # Handle mill capture
            _, pos = get_move_elements(move)
            self.board.layout[pos[0]][pos[1]] = '_'
            self.pieces_on_board[1 - self.current_player] -= 1
            self.last_move_mill = False
            return
        
        player = self.current_player
        phase = self.phase[player]
        
        if phase == Phase.PLACING:
            # Place a piece
            super().perform_move(move)
            self.pieces_to_place[player] -= 1
            self.pieces_on_board[player] += 1
            
            # Check if player has placed all pieces
            if self.pieces_to_place[player] == 0:
                self.phase[player] = Phase.MOVING
        else:
            # Move a piece
            origin, _ = get_move_elements(move)
            super().perform_move(move)
            
        # Check if a mill was formed
        _, pos = get_move_elements(move) if is_placement(move) else get_move_elements(move)[1], get_move_elements(move)[0]
        
        # Check if this move formed a mill
        for mill in self.mills:
            if pos in mill:
                if all(self.board.layout[r][c] == self.player_pieces[player] for r, c in mill):
                    self.last_move_mill = True
                    # Find which square the mill is on
                    self.current_square = self.position_to_square.get(pos)
                    break

    def game_finished(self):
        # Game ends if a player has fewer than 3 pieces after placement phase
        for player in [Player.ONE.value, Player.TWO.value]:
            if self.phase[player] == Phase.MOVING and self.pieces_on_board[player] < 3:
                return True
                
        # Check if current player can move (if in movement phase)
        current = self.current_player
        if self.phase[current] == Phase.MOVING and not self.last_move_mill:
            player_piece = self.player_pieces[current]
            
            # If player has only 3 pieces, they can "fly" to any empty spot
            if self.pieces_on_board[current] == 3:
                # Check if there's at least one piece and one empty spot
                has_piece = False
                has_empty = False
                
                for r in range(self.board.height):
                    for c in range(self.board.width):
                        if self.board.layout[r][c] == player_piece:
                            has_piece = True
                        elif self.board.layout[r][c] == '_':
                            has_empty = True
                            
                        if has_piece and has_empty:
                            return False
                
                return not (has_piece and has_empty)
            
            # Normal movement: check if any piece can move
            can_move = False
            for r in range(self.board.height):
                for c in range(self.board.width):
                    if self.board.layout[r][c] == player_piece:
                        pos = (r, c)
                        if pos in self.connections:
                            for adj_pos in self.connections[pos]:
                                if self.board.layout[adj_pos[0]][adj_pos[1]] == '_':
                                    can_move = True
                                    break
                    if can_move:
                        break
                if can_move:
                    break
                    
            return not can_move
            
        return False

    def get_winner(self):
        # If game is finished, the winner is the player who didn't cause it to end
        for player in [Player.ONE.value, Player.TWO.value]:
            if self.phase[player] == Phase.MOVING and self.pieces_on_board[player] < 3:
                return 1 - player  # Other player wins
                
        # If current player can't move, the other player wins
        return 1 - self.current_player

    def next_player(self):
        # If a mill was just formed, don't change player
        if self.last_move_mill:
            return self.current_player
            
        return 1 - self.current_player
    
    def initial_player(self):
        return Player.ONE.value

if __name__ == '__main__':
    # Create a custom layout for Nine Men's Morris
    layout = "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _\n" + \
             "_ _ _ _ _ _ _"
    
    # Create a board with the custom layout
    board = Board((7, 7), layout)
    
    # Create and start the game
    morris_game = NineMensMorris(board)
    morris_game.game_loop()
