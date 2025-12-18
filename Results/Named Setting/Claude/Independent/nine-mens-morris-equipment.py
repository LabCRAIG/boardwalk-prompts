
class NineMensMorrisGame:
    def __init__(self):
        # Board representation: None=empty, 'W'=white, 'B'=black
        self.board = {
            'a7': None, 'd7': None, 'g7': None,
            'b6': None, 'd6': None, 'f6': None,
            'c5': None, 'd5': None, 'e5': None,
            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None,
            'c3': None, 'd3': None, 'e3': None,
            'b2': None, 'd2': None, 'f2': None,
            'a1': None, 'd1': None, 'g1': None
        }
        
        # Modified to include center position
        # List of all valid positions on the board
        self.positions = list(self.board.keys())
        
        # All possible mill combinations (three in a row)
        self.mills = [
            # Horizontal mills
            ['a7', 'd7', 'g7'], ['b6', 'd6', 'f6'], ['c5', 'd5', 'e5'],
            ['a4', 'b4', 'c4'], ['e4', 'f4', 'g4'], ['c3', 'd3', 'e3'],
            ['b2', 'd2', 'f2'], ['a1', 'd1', 'g1'],
            # Vertical mills
            ['a7', 'a4', 'a1'], ['b6', 'b4', 'b2'], ['c5', 'c4', 'c3'],
            ['d7', 'd6', 'd5'], ['d3', 'd2', 'd1'], ['e5', 'e4', 'e3'],
            ['f6', 'f4', 'f2'], ['g7', 'g4', 'g1'],
            # Mills involving the center
            ['d4', 'd5', 'd3'], ['d4', 'c4', 'e4'], ['b4', 'd4', 'f4'],
            ['a4', 'd4', 'g4']
        ]
        
        # Game state
        self.phase = "placing"  # "placing", "moving", "flying", "game_over"
        self.current_player = 'W'  # White starts
        self.pieces_to_place = {'W': 9, 'B': 9}
        self.pieces_on_board = {'W': 0, 'B': 0}
        self.captured = {'W': 0, 'B': 0}
        self.just_formed_mill = False
        
        # Define adjacent positions for each position
        self.adjacent = self._create_adjacency_map()
        
    def _create_adjacency_map(self):
        """Create a map of adjacent positions for each position on the board."""
        adjacency = {}
        
        # Define adjacency for each position
        horizontal_lines = [
            ['a7', 'd7', 'g7'], ['b6', 'd6', 'f6'], ['c5', 'd5', 'e5'],
            ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4'],
            ['c3', 'd3', 'e3'], ['b2', 'd2', 'f2'], ['a1', 'd1', 'g1']
        ]
        
        vertical_lines = [
            ['a7', 'a4', 'a1'], ['b6', 'b4', 'b2'], ['c5', 'c4', 'c3'],
            ['d7', 'd6', 'd5', 'd4', 'd3', 'd2', 'd1'],
            ['e5', 'e4', 'e3'], ['f6', 'f4', 'f2'], ['g7', 'g4', 'g1']
        ]
        
        # Initialize all adjacency lists
        for pos in self.positions:
            adjacency[pos] = []
        
        # Add horizontal adjacencies
        for line in horizontal_lines:
            for i in range(len(line) - 1):
                adjacency[line[i]].append(line[i+1])
                adjacency[line[i+1]].append(line[i])
        
        # Add vertical adjacencies
        for line in vertical_lines:
            for i in range(len(line) - 1):
                adjacency[line[i]].append(line[i+1])
                adjacency[line[i+1]].append(line[i])
        
        return adjacency
    
    def print_board(self):
        """Print the current state of the board."""
        # Convert None to space, W to ●, B to ○
        display = {None: " ", 'W': "●", 'B': "○"}
        
        board_str = [
            f"7 {display[self.board['a7']]}-----{display[self.board['d7']]}-----{display[self.board['g7']]}",
            "  |     |     |",
            f"6 | {display[self.board['b6']]}---{display[self.board['d6']]}---{display[self.board['f6']]} |",
            "  | |   |   | |",
            f"5 | | {display[self.board['c5']]}-{display[self.board['d5']]}-{display[self.board['e5']]} | |",
            "  | | |   | | |",
            f"4 {display[self.board['a4']]}-{display[self.board['b4']]}-{display[self.board['c4']]}-{display[self.board['d4']]}-{display[self.board['e4']]}-{display[self.board['f4']]}-{display[self.board['g4']]}",
            "  | | |   | | |",
            f"3 | | {display[self.board['c3']]}-{display[self.board['d3']]}-{display[self.board['e3']]} | |",
            "  | |   |   | |",
            f"2 | {display[self.board['b2']]}---{display[self.board['d2']]}---{display[self.board['f2']]} |",
            "  |     |     |",
            f"1 {display[self.board['a1']]}-----{display[self.board['d1']]}-----{display[self.board['g1']]}",
            "  a b c d e f g"
        ]
        
        print("\n".join(board_str))
        print(f"\nCurrent player: {'White' if self.current_player == 'W' else 'Black'} ({self.current_player})")
        
        if self.phase == "placing":
            print(f"Phase: Placing - Pieces left to place: {self.pieces_to_place[self.current_player]}")
        elif self.phase == "moving":
            print(f"Phase: Moving - Regular movement")
        elif self.phase == "flying":
            print(f"Phase: Moving - Flying (3 pieces remaining)")
        
        print(f"White: {self.pieces_on_board['W']} on board, {self.captured['W']} captured")
        print(f"Black: {self.pieces_on_board['B']} on board, {self.captured['B']} captured")
    
    def is_valid_position(self, position):
        """Check if a position is valid on the board."""
        return position in self.positions
    
    def is_mill(self, position, player):
        """Check if placing at position forms a mill for the player."""
        for mill in self.mills:
            if position in mill and all(self.board[pos] == player for pos in mill):
                return True
        return False
    
    def get_player_positions(self, player):
        """Get all positions occupied by a player."""
        return [pos for pos, piece in self.board.items() if piece == player]
    
    def has_valid_move(self, player):
        """Check if the player has any valid moves."""
        player_positions = self.get_player_positions(player)
        
        # In flying phase, a move is always available if there's an empty spot
        if self.pieces_on_board[player] == 3:
            return any(self.board[pos] is None for pos in self.positions)
        
        # In normal moving phase, check if any piece can move to an adjacent position
        return any(any(self.board[adj] is None for adj in self.adjacent[pos]) for pos in player_positions)
    
    def place_piece(self, position):
        """Place a piece during the placing phase."""
        if not self.is_valid_position(position):
            return False, "Invalid position."
        
        if self.board[position] is not None:
            return False, "Position already occupied."
        
        self.board[position] = self.current_player
        self.pieces_to_place[self.current_player] -= 1
        self.pieces_on_board[self.current_player] += 1
        
        # Check if a mill was formed
        if self.is_mill(position, self.current_player):
            self.just_formed_mill = True
            return True, "Mill formed! You can remove an opponent's piece."
        
        # No mill formed, switch player
        self.switch_player()
        
        # Check if placing phase is complete
        if self.pieces_to_place['W'] == 0 and self.pieces_to_place['B'] == 0:
            self.phase = "moving"
        
        return True, "Piece placed successfully."
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece during the moving/flying phase."""
        # Basic validity checks
        if not self.is_valid_position(from_pos) or not self.is_valid_position(to_pos):
            return False, "Invalid position."
        
        if self.board[from_pos] != self.current_player:
            return False, "You can only move your own pieces."
        
        if self.board[to_pos] is not None:
            return False, "Destination position is already occupied."
        
        # Check if the move is valid based on the game phase
        is_flying = self.pieces_on_board[self.current_player] == 3
        
        # In normal moving phase, ensure the move is to an adjacent position
        if not is_flying and to_pos not in self.adjacent[from_pos]:
            return False, "In the moving phase, you can only move to adjacent positions."
        
        # Perform the move
        self.board[from_pos] = None
        self.board[to_pos] = self.current_player
        
        # Check if a mill was formed
        if self.is_mill(to_pos, self.current_player):
            self.just_formed_mill = True
            return True, "Mill formed! You can remove an opponent's piece."
        
        # No mill formed, switch player
        self.switch_player()
        
        # Update phase if needed
        if self.pieces_on_board['W'] == 3:
            self.phase = "flying" if not self.has_valid_move('W') else "moving"
        if self.pieces_on_board['B'] == 3:
            self.phase = "flying" if not self.has_valid_move('B') else "moving"
        
        return True, "Piece moved successfully."
    
    def remove_piece(self, position):
        """Remove an opponent's piece after forming a mill."""
        opponent = 'B' if self.current_player == 'W' else 'W'
        
        # Check if the position is valid and contains an opponent's piece
        if not self.is_valid_position(position):
            return False, "Invalid position."
        
        if self.board[position] != opponent:
            return False, "You can only remove opponent's pieces."
        
        # Check if the piece is part of a mill (you can't remove pieces in mills unless all opponent pieces are in mills)
        is_in_mill = self.is_mill(position, opponent)
        
        if is_in_mill:
            # Check if all opponent's pieces are in mills
            all_in_mills = True
            for pos in self.get_player_positions(opponent):
                if not self.is_mill(pos, opponent):
                    all_in_mills = False
                    break
            
            if not all_in_mills:
                return False, "You cannot remove a piece that is part of a mill unless all opponent pieces are in mills."
        
        # Remove the piece
        self.board[position] = None
        self.pieces_on_board[opponent] -= 1
        self.captured[self.current_player] += 1
        
        # Reset mill formation flag and switch player
        self.just_formed_mill = False
        
        # Check win condition
        if self.pieces_on_board[opponent] < 3 and self.pieces_to_place[opponent] == 0:
            self.phase = "game_over"
            return True, f"Game over! {self.current_player} wins!"
        
        # Check if the opponent has any valid moves left
        if self.phase != "placing" and not self.has_valid_move(opponent):
            self.phase = "game_over"
            return True, f"Game over! {self.current_player} wins! Opponent has no valid moves."
        
        self.switch_player()
        
        return True, "Piece removed successfully."
    
    def switch_player(self):
        """Switch the current player."""
        self.current_player = 'B' if self.current_player == 'W' else 'W'

    def get_game_status(self):
        """Get the current status of the game."""
        return {
            'phase': self.phase,
            'current_player': self.current_player,
            'pieces_to_place': self.pieces_to_place.copy(),
            'pieces_on_board': self.pieces_on_board.copy(),
            'just_formed_mill': self.just_formed_mill,
            'captured': self.captured.copy()
        }

def play_game():
    """Run a command-line interface for the game."""
    game = NineMensMorrisGame()
    
    print("Welcome to Nine Men's Morris (with center position)!")
    print("Positions are specified with coordinates like 'a7', 'd4', etc.")
    print("White (●) goes first, then Black (○).")
    
    while game.phase != "game_over":
        game.print_board()
        
        if game.just_formed_mill:
            while True:
                pos = input("You formed a mill! Enter position to remove opponent's piece: ")
                success, message = game.remove_piece(pos)
                print(message)
                if success:
                    break
        
        elif game.phase == "placing":
            while True:
                pos = input(f"Player {game.current_player}, enter position to place a piece: ")
                success, message = game.place_piece(pos)
                print(message)
                if success:
                    break
        
        else:  # moving or flying phase
            while True:
                from_pos = input(f"Player {game.current_player}, enter position of piece to move: ")
                to_pos = input(f"Enter position to move to: ")
                success, message = game.move_piece(from_pos, to_pos)
                print(message)
                if success:
                    break
                    
    game.print_board()
    print("Game over!")

if __name__ == "__main__":
    play_game()
