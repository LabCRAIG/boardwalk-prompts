
class NineMensMorris:
    def __init__(self):
        # Initialize an empty board
        # 0 represents empty positions, 1 for player 1, 2 for player 2
        self.board = [0] * 24
        self.phase = 'placing'  # Game phases: 'placing', 'moving', 'flying'
        self.current_player = 1
        self.pieces_to_place = {1: 9, 2: 9}  # Each player starts with 9 pieces
        self.pieces_on_board = {1: 0, 2: 0}
        
        # Define connections between positions (adjacency)
        self.connections = {
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
        
        # Define squares for the modified mill rule
        # Each list contains positions of one square (inner, middle, outer)
        self.squares = [
            [3, 4, 5, 10, 13, 18, 19, 20],     # Inner square
            [1, 7, 9, 11, 12, 14, 16, 22],     # Middle square
            [0, 2, 6, 8, 15, 17, 21, 23]       # Outer square
        ]
        
        # Define all possible mills
        self.mills = [
            # Horizontal mills
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [9, 10, 11], [12, 13, 14], [15, 16, 17],
            [18, 19, 20], [21, 22, 23],
            # Vertical mills
            [0, 9, 21], [3, 10, 18], [6, 11, 15],
            [1, 4, 7], [16, 19, 22], [8, 12, 17],
            [5, 13, 20], [2, 14, 23]
        ]
    
    def get_square_index(self, position):
        """Return the square index (0, 1, or 2) that a position belongs to."""
        for i, square in enumerate(self.squares):
            if position in square:
                return i
        return -1  # Should never reach here
    
    def print_board(self):
        """Print the current state of the board."""
        symbols = {0: '·', 1: 'X', 2: 'O'}
        
        # Convert board to symbols
        board_symbols = [symbols[p] for p in self.board]
        
        # Print the board
        print(f"{board_symbols[0]}-----{board_symbols[1]}-----{board_symbols[2]}")
        print("|     |     |")
        print(f"| {board_symbols[3]}---{board_symbols[4]}---{board_symbols[5]} |")
        print("| |   |   | |")
        print(f"| | {board_symbols[6]}-{board_symbols[7]}-{board_symbols[8]} | |")
        print("| | |   | | |")
        print(f"{board_symbols[9]}-{board_symbols[10]}-{board_symbols[11]}   {board_symbols[12]}-{board_symbols[13]}-{board_symbols[14]}")
        print("| | |   | | |")
        print(f"| | {board_symbols[15]}-{board_symbols[16]}-{board_symbols[17]} | |")
        print("| |   |   | |")
        print(f"| {board_symbols[18]}---{board_symbols[19]}---{board_symbols[20]} |")
        print("|     |     |")
        print(f"{board_symbols[21]}-----{board_symbols[22]}-----{board_symbols[23]}")
        
        # Display game info
        print(f"\nPlayer 1 (X): {self.pieces_on_board[1]} pieces on board, {self.pieces_to_place[1]} to place")
        print(f"Player 2 (O): {self.pieces_on_board[2]} pieces on board, {self.pieces_to_place[2]} to place")
        print(f"Current phase: {self.phase}")
        print(f"Current player: {'X' if self.current_player == 1 else 'O'}")
    
    def is_mill(self, position):
        """Check if placing a piece at position forms a mill."""
        player = self.board[position]
        if player == 0:
            return False
            
        # Check all possible mills that include this position
        for mill in self.mills:
            if position in mill:
                if all(self.board[pos] == player for pos in mill):
                    return mill
        return False
    
    def get_valid_moves(self, position):
        """Get valid moves from a position based on the current game phase."""
        if self.phase == 'flying' and self.pieces_on_board[self.current_player] <= 3:
            # In flying phase, can move to any empty position
            return [pos for pos in range(24) if self.board[pos] == 0]
        else:
            # In moving phase, can only move to adjacent empty positions
            return [pos for pos in self.connections[position] if self.board[pos] == 0]
    
    def place_piece(self, position):
        """Place a piece in the placing phase."""
        if position < 0 or position >= 24:
            print("Invalid position.")
            return False
            
        if self.board[position] != 0:
            print("Position already occupied.")
            return False
            
        # Place the piece
        self.board[position] = self.current_player
        self.pieces_to_place[self.current_player] -= 1
        self.pieces_on_board[self.current_player] += 1
        
        # Check if a mill was formed
        mill = self.is_mill(position)
        if mill:
            square_index = self.get_square_index(position)
            return {'mill': mill, 'square': square_index}
        
        # Switch players
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        
        # Check if we need to move to the next phase
        if self.pieces_to_place[1] == 0 and self.pieces_to_place[2] == 0:
            self.phase = 'moving'
            
        return True
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece in the moving or flying phase."""
        if from_pos < 0 or from_pos >= 24 or to_pos < 0 or to_pos >= 24:
            print("Invalid position.")
            return False
            
        if self.board[from_pos] != self.current_player:
            print("You don't have a piece at the starting position.")
            return False
            
        if self.board[to_pos] != 0:
            print("Destination position is already occupied.")
            return False
            
        # Check if the move is valid based on the phase
        if self.phase == 'moving' and to_pos not in self.connections[from_pos]:
            print("Invalid move. You can only move to adjacent positions.")
            return False
            
        # Move the piece
        self.board[from_pos] = 0
        self.board[to_pos] = self.current_player
        
        # Check if a mill was formed
        mill = self.is_mill(to_pos)
        if mill:
            square_index = self.get_square_index(to_pos)
            return {'mill': mill, 'square': square_index}
        
        # Switch players
        self.current_player = 3 - self.current_player
        
        # Update phase if needed
        if self.pieces_on_board[1] <= 3 or self.pieces_on_board[2] <= 3:
            self.phase = 'flying'
            
        return True
    
    def remove_piece(self, position, mill_square):
        """Remove an opponent's piece after forming a mill."""
        opponent = 3 - self.current_player
        
        if position < 0 or position >= 24:
            print("Invalid position.")
            return False
            
        if self.board[position] != opponent:
            print("You can only remove your opponent's pieces.")
            return False
        
        # Check if position is in the same square as the mill
        if self.get_square_index(position) != mill_square:
            print("You can only remove pieces from the same square as your mill.")
            return False
            
        # Check if the piece is part of a mill
        if self.is_mill(position):
            # Check if all opponent's pieces are in mills
            all_in_mills = True
            for pos in range(24):
                if self.board[pos] == opponent and not self.is_mill(pos):
                    all_in_mills = False
                    break
                    
            if not all_in_mills:
                print("You cannot remove a piece that is part of a mill if other pieces are available.")
                return False
        
        # Remove the piece
        self.board[position] = 0
        self.pieces_on_board[opponent] -= 1
        
        # Check win condition
        if self.phase != 'placing' and self.pieces_on_board[opponent] < 3:
            print(f"Player {self.current_player} wins! Player {opponent} has fewer than 3 pieces.")
            return {'winner': self.current_player}
            
        # Switch players
        self.current_player = 3 - self.current_player
        
        return True
    
    def check_win_condition(self):
        """Check if the game has been won."""
        if self.phase == 'placing':
            return None  # Can't win in placing phase
            
        for player in [1, 2]:
            opponent = 3 - player
            
            # Win by reducing opponent to fewer than 3 pieces
            if self.pieces_on_board[opponent] < 3:
                return player
                
            # Win if opponent can't move
            if self.current_player == opponent:
                can_move = False
                for pos in range(24):
                    if self.board[pos] == opponent:
                        valid_moves = self.get_valid_moves(pos)
                        if valid_moves:
                            can_move = True
                            break
                            
                if not can_move:
                    return player
                    
        return None  # No winner yet
    
    def play_game(self):
        """Main game loop."""
        game_over = False
        winner = None
        
        while not game_over:
            self.print_board()
            
            # Check for win condition
            winner = self.check_win_condition()
            if winner:
                print(f"Player {winner} wins!")
                game_over = True
                break
                
            player_symbol = 'X' if self.current_player == 1 else 'O'
            
            if self.phase == 'placing':
                print(f"Player {player_symbol}, place a piece (0-23):")
                try:
                    position = int(input())
                    result = self.place_piece(position)
                    
                    if isinstance(result, dict) and 'mill' in result:
                        print(f"Mill formed! You can remove an opponent's piece from square {result['square']}.")
                        self.print_board()
                        print("Enter position to remove:")
                        remove_pos = int(input())
                        self.remove_piece(remove_pos, result['square'])
                        
                except ValueError:
                    print("Please enter a valid number.")
                    
            else:  # moving or flying phase
                print(f"Player {player_symbol}, select a piece to move:")
                try:
                    from_pos = int(input())
                    print("Enter destination position:")
                    to_pos = int(input())
                    
                    result = self.move_piece(from_pos, to_pos)
                    
                    if isinstance(result, dict) and 'mill' in result:
                        print(f"Mill formed! You can remove an opponent's piece from square {result['square']}.")
                        self.print_board()
                        print("Enter position to remove:")
                        remove_pos = int(input())
                        self.remove_piece(remove_pos, result['square'])
                        
                except ValueError:
                    print("Please enter valid numbers.")
                    
        print("Game over!")


# Run the game
if __name__ == "__main__":
    game = NineMensMorris()
    game.play_game()
