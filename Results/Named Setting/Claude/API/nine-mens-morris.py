
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 0
    TWO = 1

class NineMensMorris(Game):
    def __init__(self, board):
        super().__init__(board)
        # Number of pieces each player has to place initially
        self.pieces_to_place = {Player.ONE: 9, Player.TWO: 9}
        # Number of pieces each player has on the board
        self.pieces_on_board = {Player.ONE: 0, Player.TWO: 0}
        # Flag to track if a mill was formed in the last move
        self.mill_formed = False
        # Player pieces
        self.player_pieces = {Player.ONE: 'X', Player.TWO: 'O'}
        # Valid positions on the board (coordinates where pieces can be placed)
        self.valid_positions = [
            (0, 0), (0, 3), (0, 6),
            (1, 1), (1, 3), (1, 5),
            (2, 2), (2, 3), (2, 4),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
            (4, 2), (4, 3), (4, 4),
            (5, 1), (5, 3), (5, 5),
            (6, 0), (6, 3), (6, 6)
        ]
        # Map of adjacent positions
        self.adjacent_positions = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4), (3, 3)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 0): [(0, 0), (3, 1), (6, 0)],
            (3, 1): [(1, 1), (3, 0), (3, 2), (5, 1)],
            (3, 2): [(2, 2), (3, 1), (3, 3), (4, 2)],
            (3, 3): [(2, 3), (3, 2), (3, 4), (4, 3)],
            (3, 4): [(2, 4), (3, 3), (3, 5), (4, 4)],
            (3, 5): [(1, 5), (3, 4), (3, 6), (5, 5)],
            (3, 6): [(0, 6), (3, 5), (6, 6)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(3, 3), (4, 2), (4, 4), (5, 3)],
            (4, 4): [(3, 4), (4, 3)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(4, 3), (5, 1), (5, 5), (6, 3)],
            (5, 5): [(3, 5), (5, 3)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(5, 3), (6, 0), (6, 6)],
            (6, 6): [(3, 6), (6, 3)]
        }

    def initial_player(self):
        return Player.ONE.value
    
    def prompt_current_player(self):
        player = Player(self.current_player)
        player_piece = self.player_pieces[player]
        
        # Phase 1: Placing pieces
        if self.pieces_to_place[player] > 0:
            if self.mill_formed:
                return input(f"Player {player.value + 1} ({player_piece}), remove opponent's piece: ")
            else:
                return input(f"Player {player.value + 1} ({player_piece}), place a piece (remaining: {self.pieces_to_place[player]}): ")
        # Phase 2 & 3: Moving pieces
        else:
            if self.mill_formed:
                return input(f"Player {player.value + 1} ({player_piece}), remove opponent's piece: ")
            else:
                return input(f"Player {player.value + 1} ({player_piece}), move a piece: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            print("Invalid coordinates.")
            return False
        
        player = Player(self.current_player)
        opponent = Player(1 - self.current_player)
        player_piece = self.player_pieces[player]
        opponent_piece = self.player_pieces[opponent]
        
        # Handling mill removal
        if self.mill_formed:
            if not is_placement(move):
                print("To remove a piece, use format: '_ row,col'")
                return False
                
            piece, coords = get_move_elements(move)
            if piece != '_':
                print("Use '_ row,col' to remove a piece.")
                return False
                
            if self.board.layout[coords] != opponent_piece:
                print("You can only remove opponent's pieces.")
                return False
                
            # Check if the piece is part of a mill
            if self.is_in_mill(coords, opponent_piece):
                # Only allow removing from mill if all opponent pieces are in mills
                all_in_mills = True
                for pos in self.valid_positions:
                    if self.board.layout[pos] == opponent_piece and not self.is_in_mill(pos, opponent_piece):
                        all_in_mills = False
                        break
                
                if not all_in_mills:
                    print("You cannot remove a piece that is part of a mill unless all opponent pieces are in mills.")
                    return False
            
            return True
            
        # Phase 1: Placing pieces
        if self.pieces_to_place[player] > 0:
            if not is_placement(move):
                print("During the placement phase, use format: 'X row,col'")
                return False
                
            piece, coords = get_move_elements(move)
            
            if piece != player_piece:
                print(f"You must place your own piece ('{player_piece}').")
                return False
                
            if coords not in self.valid_positions:
                print("Invalid position on the board.")
                return False
                
            if self.board.layout[coords] != '_':
                print("This position is already occupied.")
                return False
                
            return True
            
        # Phase 2 & 3: Moving pieces
        else:
            if not is_movement(move):
                print("During the movement phase, use format: 'row1,col1 row2,col2'")
                return False
                
            origin, dest = get_move_elements(move)
            
            if origin not in self.valid_positions or dest not in self.valid_positions:
                print("Invalid position on the board.")
                return False
                
            if self.board.layout[origin] != player_piece:
                print("You can only move your own pieces.")
                return False
                
            if self.board.layout[dest] != '_':
                print("Destination position must be empty.")
                return False
                
            # Phase 3: Flying (when player has only 3 pieces)
            if self.pieces_on_board[player] <= 3:
                return True
                
            # Phase 2: Regular movement
            if dest not in self.adjacent_positions[origin]:
                print("You can only move to adjacent positions.")
                return False
                
            return True

    def perform_move(self, move):
        player = Player(self.current_player)
        opponent = Player(1 - self.current_player)
        
        # Handling mill removal
        if self.mill_formed:
            _, coords = get_move_elements(move)
            self.board.place_piece(f"_ {coords[0]},{coords[1]}")
            self.pieces_on_board[opponent] -= 1
            self.mill_formed = False
            return
        
        # Phase 1: Placing pieces
        if self.pieces_to_place[player] > 0:
            super().perform_move(move)
            self.pieces_to_place[player] -= 1
            self.pieces_on_board[player] += 1
            
            # Check if a mill is formed
            piece, coords = get_move_elements(move)
            if self.check_mills(coords, piece):
                self.mill_formed = True
        
        # Phase 2 & 3: Moving pieces
        else:
            origin, dest = get_move_elements(move)
            player_piece = self.player_pieces[player]
            super().perform_move(move)
            
            # Check if a mill is formed
            if self.check_mills(dest, player_piece):
                self.mill_formed = True

    def get_state(self):
        state = super().get_state()
        additional_params = [
            self.pieces_to_place[Player.ONE],
            self.pieces_to_place[Player.TWO],
            self.pieces_on_board[Player.ONE],
            self.pieces_on_board[Player.TWO],
            self.mill_formed
        ]
        return (state[0], state[1], additional_params)

    def game_finished(self):
        player_one = Player.ONE
        player_two = Player.TWO
        
        # Game is finished if both players have placed all their pieces
        if self.pieces_to_place[player_one] == 0 and self.pieces_to_place[player_two] == 0:
            # Check if a player has fewer than 3 pieces
            if self.pieces_on_board[player_one] < 3 or self.pieces_on_board[player_two] < 3:
                return True
                
            # Check if the current player has no valid moves
            player = Player(self.current_player)
            if self.no_valid_moves(player):
                return True
        
        return False
    
    def no_valid_moves(self, player):
        # If the player is in the flying phase (3 pieces), they always have moves
        if self.pieces_on_board[player] <= 3:
            return False
            
        # Check if any piece can move
        player_piece = self.player_pieces[player]
        for pos in self.valid_positions:
            if self.board.layout[pos] == player_piece:
                for adj_pos in self.adjacent_positions[pos]:
                    if self.board.layout[adj_pos] == '_':
                        return False
        
        return True

    def get_winner(self):
        player_one = Player.ONE
        player_two = Player.TWO
        
        if self.pieces_on_board[player_one] < 3:
            return player_two.value
        elif self.pieces_on_board[player_two] < 3:
            return player_one.value
        
        # If current player has no valid moves, opponent wins
        player = Player(self.current_player)
        if self.no_valid_moves(player):
            return (1 - self.current_player)
            
        return None  # Should not reach here

    def next_player(self):
        # If a mill was formed, the same player goes again to remove an opponent's piece
        if self.mill_formed:
            return self.current_player
        # Otherwise, alternate players
        return 1 - self.current_player

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("The game ended in a draw.")

    def is_in_mill(self, pos, piece):
        """Check if a position is part of a mill"""
        return any(all(self.board.layout[p] == piece for p in mill) 
                  for mill in self.get_possible_mills(pos))
    
    def check_mills(self, pos, piece):
        """Check if a mill is formed at the given position"""
        for mill in self.get_possible_mills(pos):
            if all(self.board.layout[p] == piece for p in mill):
                return True
        return False
    
    def get_possible_mills(self, pos):
        """Get all possible mills that include the given position"""
        mills = []
        # Horizontal mills
        if pos[0] == 0:
            if pos[1] == 0: mills.append([(0, 0), (0, 3), (0, 6)])
            elif pos[1] == 3: mills.append([(0, 0), (0, 3), (0, 6)])
            elif pos[1] == 6: mills.append([(0, 0), (0, 3), (0, 6)])
        elif pos[0] == 1:
            if pos[1] == 1: mills.append([(1, 1), (1, 3), (1, 5)])
            elif pos[1] == 3: mills.append([(1, 1), (1, 3), (1, 5)])
            elif pos[1] == 5: mills.append([(1, 1), (1, 3), (1, 5)])
        elif pos[0] == 2:
            if pos[1] == 2: mills.append([(2, 2), (2, 3), (2, 4)])
            elif pos[1] == 3: mills.append([(2, 2), (2, 3), (2, 4)])
            elif pos[1] == 4: mills.append([(2, 2), (2, 3), (2, 4)])
        elif pos[0] == 3:
            if pos[1] == 0: mills.append([(3, 0), (3, 1), (3, 2)])
            elif pos[1] == 1: mills.append([(3, 0), (3, 1), (3, 2)])
            elif pos[1] == 2: mills.append([(3, 0), (3, 1), (3, 2)])
            elif pos[1] == 4: mills.append([(3, 4), (3, 5), (3, 6)])
            elif pos[1] == 5: mills.append([(3, 4), (3, 5), (3, 6)])
            elif pos[1] == 6: mills.append([(3, 4), (3, 5), (3, 6)])
        elif pos[0] == 4:
            if pos[1] == 2: mills.append([(4, 2), (4, 3), (4, 4)])
            elif pos[1] == 3: mills.append([(4, 2), (4, 3), (4, 4)])
            elif pos[1] == 4: mills.append([(4, 2), (4, 3), (4, 4)])
        elif pos[0] == 5:
            if pos[1] == 1: mills.append([(5, 1), (5, 3), (5, 5)])
            elif pos[1] == 3: mills.append([(5, 1), (5, 3), (5, 5)])
            elif pos[1] == 5: mills.append([(5, 1), (5, 3), (5, 5)])
        elif pos[0] == 6:
            if pos[1] == 0: mills.append([(6, 0), (6, 3), (6, 6)])
            elif pos[1] == 3: mills.append([(6, 0), (6, 3), (6, 6)])
            elif pos[1] == 6: mills.append([(6, 0), (6, 3), (6, 6)])
            
        # Vertical mills
        if pos[1] == 0:
            if pos[0] == 0: mills.append([(0, 0), (3, 0), (6, 0)])
            elif pos[0] == 3: mills.append([(0, 0), (3, 0), (6, 0)])
            elif pos[0] == 6: mills.append([(0, 0), (3, 0), (6, 0)])
        elif pos[1] == 1:
            if pos[0] == 1: mills.append([(1, 1), (3, 1), (5, 1)])
            elif pos[0] == 3: mills.append([(1, 1), (3, 1), (5, 1)])
            elif pos[0] == 5: mills.append([(1, 1), (3, 1), (5, 1)])
        elif pos[1] == 2:
            if pos[0] == 2: mills.append([(2, 2), (3, 2), (4, 2)])
            elif pos[0] == 3: mills.append([(2, 2), (3, 2), (4, 2)])
            elif pos[0] == 4: mills.append([(2, 2), (3, 2), (4, 2)])
        elif pos[1] == 3:
            if pos[0] == 0: mills.append([(0, 3), (1, 3), (2, 3)])
            elif pos[0] == 1: mills.append([(0, 3), (1, 3), (2, 3)])
            elif pos[0] == 2: mills.append([(0, 3), (1, 3), (2, 3)])
            elif pos[0] == 4: mills.append([(4, 3), (5, 3), (6, 3)])
            elif pos[0] == 5: mills.append([(4, 3), (5, 3), (6, 3)])
            elif pos[0] == 6: mills.append([(4, 3), (5, 3), (6, 3)])
        elif pos[1] == 4:
            if pos[0] == 2: mills.append([(2, 4), (3, 4), (4, 4)])
            elif pos[0] == 3: mills.append([(2, 4), (3, 4), (4, 4)])
            elif pos[0] == 4: mills.append([(2, 4), (3, 4), (4, 4)])
        elif pos[1] == 5:
            if pos[0] == 1: mills.append([(1, 5), (3, 5), (5, 5)])
            elif pos[0] == 3: mills.append([(1, 5), (3, 5), (5, 5)])
            elif pos[0] == 5: mills.append([(1, 5), (3, 5), (5, 5)])
        elif pos[1] == 6:
            if pos[0] == 0: mills.append([(0, 6), (3, 6), (6, 6)])
            elif pos[0] == 3: mills.append([(0, 6), (3, 6), (6, 6)])
            elif pos[0] == 6: mills.append([(0, 6), (3, 6), (6, 6)])
            
        return mills

if __name__ == '__main__':
    # Nine Men's Morris board layout
    layout = (
        "_ _ _ _ _ _ _\n"
        "  _ _ _ _ _  \n"
        "    _ _ _    \n"
        "_ _ _   _ _ _\n"
        "    _ _ _    \n"
        "  _ _ _ _ _  \n"
        "_ _ _ _ _ _ _"
    )
    board = Board((7, 7), layout)
    game = NineMensMorris(board)
    game.game_loop()
