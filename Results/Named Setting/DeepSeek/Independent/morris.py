import random
import os

class NineMensMorris:
    def __init__(self):
        self.board = {}
        self.positions = [
            'a1', 'd1', 'g1',
            'b2', 'd2', 'f2',
            'c3', 'd3', 'e3',
            'a4', 'b4', 'c4', 'e4', 'f4', 'g4',
            'c5', 'd5', 'e5',
            'b6', 'd6', 'f6',
            'a7', 'd7', 'g7'
        ]
        self.mills = [
            # Horizontal mills
            ['a1', 'd1', 'g1'],
            ['b2', 'd2', 'f2'],
            ['c3', 'd3', 'e3'],
            ['a4', 'b4', 'c4'],
            ['e4', 'f4', 'g4'],
            ['c5', 'd5', 'e5'],
            ['b6', 'd6', 'f6'],
            ['a7', 'd7', 'g7'],
            # Vertical mills
            ['a1', 'a4', 'a7'],
            ['b2', 'b4', 'b6'],
            ['c3', 'c4', 'c5'],
            ['d1', 'd2', 'd3'],
            ['d5', 'd6', 'd7'],
            ['e3', 'e4', 'e5'],
            ['f2', 'f4', 'f6'],
            ['g1', 'g4', 'g7']
        ]
        self.adjacent_positions = {
            'a1': ['d1', 'a4'],
            'd1': ['a1', 'g1', 'd2'],
            'g1': ['d1', 'g4'],
            'b2': ['d2', 'b4'],
            'd2': ['b2', 'd1', 'd3', 'f2'],
            'f2': ['d2', 'f4'],
            'c3': ['d3', 'c4'],
            'd3': ['c3', 'd2', 'e3'],
            'e3': ['d3', 'e4'],
            'a4': ['a1', 'b4', 'a7'],
            'b4': ['b2', 'a4', 'c4', 'b6'],
            'c4': ['c3', 'b4', 'c5'],
            'e4': ['e3', 'f4', 'e5'],
            'f4': ['f2', 'e4', 'g4', 'f6'],
            'g4': ['g1', 'f4', 'g7'],
            'c5': ['c4', 'd5'],
            'd5': ['c5', 'e5', 'd6'],
            'e5': ['e4', 'd5'],
            'b6': ['b4', 'd6'],
            'd6': ['b6', 'd5', 'd7', 'f6'],
            'f6': ['f4', 'd6'],
            'a7': ['a4', 'd7'],
            'd7': ['a7', 'd6', 'g7'],
            'g7': ['g4', 'd7']
        }
        self.reset_game()
        
    def reset_game(self):
        """Initialize the game state"""
        for pos in self.positions:
            self.board[pos] = ' '
        self.player_pieces = {'X': 9, 'O': 9}
        self.board_pieces = {'X': 0, 'O': 0}
        self.phase = {'X': 'placing', 'O': 'placing'}  # placing, moving, flying
        self.current_player = 'X'
        self.opponent = 'O'
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        """Display the current board state"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("    A   B   C   D   E   F   G")
        print("1   {}-----------{}-----------{}".format(
            self.board['a1'], self.board['d1'], self.board['g1']))
        print("    |           |           |")
        print("2   |   {}-------{}-------{}   |".format(
            self.board['b2'], self.board['d2'], self.board['f2']))
        print("    |   |       |       |   |")
        print("3   |   |   {}---{}---{}   |   |".format(
            self.board['c3'], self.board['d3'], self.board['e3']))
        print("    |   |   |       |   |   |")
        print("4   {}---{}---{}       {}---{}---{}".format(
            self.board['a4'], self.board['b4'], self.board['c4'],
            self.board['e4'], self.board['f4'], self.board['g4']))
        print("    |   |   |       |   |   |")
        print("5   |   |   {}---{}---{}   |   |".format(
            self.board['c5'], self.board['d5'], self.board['e5']))
        print("    |   |       |       |   |")
        print("6   |   {}-------{}-------{}   |".format(
            self.board['b6'], self.board['d6'], self.board['f6']))
        print("    |           |           |")
        print("7   {}-----------{}-----------{}".format(
            self.board['a7'], self.board['d7'], self.board['g7']))
        print()
        print(f"Player X pieces: {self.player_pieces['X']} (on board: {self.board_pieces['X']})")
        print(f"Player O pieces: {self.player_pieces['O']} (on board: {self.board_pieces['O']})")
        print(f"Current phase: {self.phase[self.current_player]}")
        print(f"Current player: {self.current_player}")
        
    def is_mill(self, position, player):
        """Check if a move creates a mill"""
        for mill in self.mills:
            if position in mill:
                if all(self.board[pos] == player for pos in mill):
                    return True
        return False
    
    def get_valid_places(self):
        """Get all valid placement positions"""
        return [pos for pos in self.positions if self.board[pos] == ' ']
    
    def get_valid_moves(self, player):
        """Get all valid moves for a player in moving phase"""
        valid_moves = []
        player_positions = [pos for pos in self.positions if self.board[pos] == player]
        
        for from_pos in player_positions:
            if self.phase[player] == 'moving':
                # Can only move to adjacent positions
                for to_pos in self.adjacent_positions[from_pos]:
                    if self.board[to_pos] == ' ':
                        valid_moves.append((from_pos, to_pos))
            elif self.phase[player] == 'flying':
                # Can move to any empty position
                for to_pos in self.positions:
                    if self.board[to_pos] == ' ':
                        valid_moves.append((from_pos, to_pos))
        return valid_moves
    
    def get_removable_pieces(self, player):
        """Get opponent pieces that can be removed (not in mills unless no other options)"""
        opponent = 'O' if player == 'X' else 'X'
        opponent_positions = [pos for pos in self.positions if self.board[pos] == opponent]
        
        # Check if all opponent pieces are in mills
        all_in_mills = all(self.is_mill(pos, opponent) for pos in opponent_positions)
        
        if all_in_mills:
            return opponent_positions  # Can remove any piece
        else:
            # Can only remove pieces not in mills
            return [pos for pos in opponent_positions if not self.is_mill(pos, opponent)]
    
    def place_piece(self, position, player):
        """Place a piece on the board"""
        if self.board[position] != ' ':
            return False
            
        self.board[position] = player
        self.player_pieces[player] -= 1
        self.board_pieces[player] += 1
        
        # Check if player can fly (only 3 pieces left)
        if self.board_pieces[player] == 3 and self.phase[player] != 'flying':
            self.phase[player] = 'flying'
            
        # Check if player moves to moving phase (all pieces placed)
        if self.player_pieces[player] == 0 and self.phase[player] == 'placing':
            self.phase[player] = 'moving'
            
        return True
    
    def move_piece(self, from_pos, to_pos, player):
        """Move a piece on the board"""
        if self.board[from_pos] != player or self.board[to_pos] != ' ':
            return False
            
        # Check if it's a valid move based on phase
        if self.phase[player] == 'moving':
            if to_pos not in self.adjacent_positions[from_pos]:
                return False
        # Flying phase can move anywhere, no restrictions needed
        
        self.board[from_pos] = ' '
        self.board[to_pos] = player
        return True
    
    def remove_piece(self, position, player):
        """Remove an opponent's piece from the board"""
        opponent = 'O' if player == 'X' else 'X'
        if self.board[position] != opponent:
            return False
            
        self.board[position] = ' '
        self.board_pieces[opponent] -= 1
        
        # Check if opponent can still move
        if self.board_pieces[opponent] < 3:
            self.game_over = True
            self.winner = player
            
        # If opponent was flying but now has more than 3 pieces, revert to moving
        if self.board_pieces[opponent] > 3 and self.phase[opponent] == 'flying':
            self.phase[opponent] = 'moving'
            
        return True
    
    def switch_player(self):
        """Switch to the other player"""
        self.current_player, self.opponent = self.opponent, self.current_player
    
    def check_game_over(self):
        """Check if the game is over"""
        # Check if a player has less than 3 pieces
        if self.board_pieces['X'] < 3:
            self.game_over = True
            self.winner = 'O'
            return True
        if self.board_pieces['O'] < 3:
            self.game_over = True
            self.winner = 'X'
            return True
            
        # Check if a player has no valid moves
        if self.phase['X'] != 'placing' and not self.get_valid_moves('X'):
            self.game_over = True
            self.winner = 'O'
            return True
        if self.phase['O'] != 'placing' and not self.get_valid_moves('O'):
            self.game_over = True
            self.winner = 'X'
            return True
            
        return False
    
    def make_ai_move(self):
        """Make a move for the AI player"""
        # Phase 1: Placing pieces
        if self.phase[self.current_player] == 'placing':
            valid_places = self.get_valid_places()
            
            # Try to form a mill if possible
            for pos in valid_places:
                # Test if placing here would form a mill
                self.board[pos] = self.current_player  # Temporarily place
                if self.is_mill(pos, self.current_player):
                    self.board[pos] = ' '  # Undo temporary placement
                    self.place_piece(pos, self.current_player)
                    return pos, None
                self.board[pos] = ' '  # Undo temporary placement
                
            # Try to block opponent mills
            opponent = self.opponent
            for pos in valid_places:
                # Test if placing here would block an opponent mill
                self.board[pos] = opponent  # Temporarily place as opponent
                if self.is_mill(pos, opponent):
                    self.board[pos] = ' '  # Undo temporary placement
                    self.place_piece(pos, self.current_player)
                    return pos, None
                self.board[pos] = ' '  # Undo temporary placement
                
            # Otherwise, choose a random valid position
            pos = random.choice(valid_places)
            self.place_piece(pos, self.current_player)
            return pos, None
            
        # Phase 2 & 3: Moving pieces
        else:
            valid_moves = self.get_valid_moves(self.current_player)
            
            # Try to form a mill if possible
            for from_pos, to_pos in valid_moves:
                # Test if moving would form a mill
                self.board[from_pos] = ' '  # Temporarily remove
                self.board[to_pos] = self.current_player  # Temporarily place
                if self.is_mill(to_pos, self.current_player):
                    self.board[from_pos] = self.current_player  # Undo
                    self.board[to_pos] = ' '  # Undo
                    self.move_piece(from_pos, to_pos, self.current_player)
                    return from_pos, to_pos
                self.board[from_pos] = self.current_player  # Undo
                self.board[to_pos] = ' '  # Undo
                
            # Otherwise, choose a random valid move
            if valid_moves:
                from_pos, to_pos = random.choice(valid_moves)
                self.move_piece(from_pos, to_pos, self.current_player)
                return from_pos, to_pos
                
            # No valid moves (game should end)
            return None, None
    
    def play(self):
        """Main game loop"""
        print("Welcome to Nine Men's Morris!")
        print("You are playing as X")
        print()
        
        while not self.game_over:
            self.print_board()
            mill_formed = False
            
            # Placing phase
            if self.phase[self.current_player] == 'placing':
                if self.current_player == 'X':  # Human player
                    valid_places = self.get_valid_places()
                    print(f"Valid positions: {', '.join(valid_places)}")
                    position = input("Enter position to place your piece: ").lower()
                    
                    while position not in valid_places:
                        print("Invalid position. Try again.")
                        position = input("Enter position to place your piece: ").lower()
                    
                    self.place_piece(position, self.current_player)
                    
                    # Check if mill was formed
                    if self.is_mill(position, self.current_player):
                        mill_formed = True
                        self.print_board()
                        print("You formed a mill! You can remove an opponent's piece.")
                        
                        removable = self.get_removable_pieces(self.current_player)
                        print(f"Removable pieces: {', '.join(removable)}")
                        remove_pos = input("Enter position to remove: ").lower()
                        
                        while remove_pos not in removable:
                            print("Invalid position. Try again.")
                            remove_pos = input("Enter position to remove: ").lower()
                            
                        self.remove_piece(remove_pos, self.current_player)
                        
                else:  # AI player
                    position, _ = self.make_ai_move()
                    
                    # Check if mill was formed
                    if self.is_mill(position, self.current_player):
                        mill_formed = True
                        removable = self.get_removable_pieces(self.current_player)
                        remove_pos = random.choice(removable)
                        self.remove_piece(remove_pos, self.current_player)
                        print(f"AI formed a mill and removed your piece at {remove_pos}")
                        input("Press Enter to continue...")
            
            # Moving phase
            else:
                if self.current_player == 'X':  # Human player
                    valid_moves = self.get_valid_moves(self.current_player)
                    print("Valid moves (from->to):")
                    for i, (from_pos, to_pos) in enumerate(valid_moves):
                        print(f"{i+1}: {from_pos} -> {to_pos}")
                    
                    try:
                        choice = int(input("Select move by number: ")) - 1
                        while choice < 0 or choice >= len(valid_moves):
                            print("Invalid choice. Try again.")
                            choice = int(input("Select move by number: ")) - 1
                            
                        from_pos, to_pos = valid_moves[choice]
                        self.move_piece(from_pos, to_pos, self.current_player)
                        
                        # Check if mill was formed
                        if self.is_mill(to_pos, self.current_player):
                            mill_formed = True
                            self.print_board()
                            print("You formed a mill! You can remove an opponent's piece.")
                            
                            removable = self.get_removable_pieces(self.current_player)
                            print(f"Removable pieces: {', '.join(removable)}")
                            remove_pos = input("Enter position to remove: ").lower()
                            
                            while remove_pos not in removable:
                                print("Invalid position. Try again.")
                                remove_pos = input("Enter position to remove: ").lower()
                                
                            self.remove_piece(remove_pos, self.current_player)
                            
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                        
                else:  # AI player
                    from_pos, to_pos = self.make_ai_move()
                    
                    # Check if mill was formed
                    if self.is_mill(to_pos, self.current_player):
                        mill_formed = True
                        removable = self.get_removable_pieces(self.current_player)
                        remove_pos = random.choice(removable)
                        self.remove_piece(remove_pos, self.current_player)
                        print(f"AI formed a mill and removed your piece at {remove_pos}")
                        input("Press Enter to continue...")
            
            # If no mill was formed, switch players
            if not mill_formed:
                self.switch_player()
                
            # Check if game is over
            self.check_game_over()
        
        # Game over
        self.print_board()
        if self.winner == 'X':
            print("Congratulations! You won!")
        else:
            print("The AI won. Better luck next time!")

# Start the game
if __name__ == "__main__":
    game = NineMensMorris()
    game.play()