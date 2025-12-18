
class NineMensMorris:
    def __init__(self):
        # Initialize the board with 24 positions (0-23)
        # None represents an empty position
        # 'W' represents a white piece
        # 'B' represents a black piece
        self.board = [None] * 24
        self.phase = "placing"  # Game phases: "placing", "moving", "game_over"
        self.current_player = 'W'  # White player starts
        self.pieces_to_place = {'W': 9, 'B': 9}
        self.pieces_on_board = {'W': 0, 'B': 0}

        # Define mill configurations (positions that form a mill)
        self.mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal rows
            [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15],  # Vertical columns
            [1, 4, 7], [16, 19, 22],
            [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]

        # Define adjacent positions for each position
        self.adjacency = {
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

    def print_board(self):
        """Print the current board state."""
        board_template = """
        7 ({0})-----({1})-----({2})
        |       |       |
        6 ({3})--({4})--({5})
        |   |   |   |
        5 ({6})-({7})-({8})
          | | | | | |
        4 ({9})({10})({11}) ({12})({13})({14})
          | | | | | |
        3 ({15})-({16})-({17})
        |   |   |   |
        2 ({18})--({19})--({20})
        |       |       |
        1 ({21})-----({22})-----({23})
          a  b  c  d  e  f  g
        """
        # Convert None to empty space for display
        display_board = []
        for pos in self.board:
            if pos is None:
                display_board.append(".")
            else:
                display_board.append(pos)
        
        print(board_template.format(*display_board))
        print(f"Current player: {self.current_player}")
        print(f"Game phase: {self.phase}")
        print(f"Pieces to place - White: {self.pieces_to_place['W']}, Black: {self.pieces_to_place['B']}")
        print(f"Pieces on board - White: {self.pieces_on_board['W']}, Black: {self.pieces_on_board['B']}")

    def check_mill(self, position):
        """Check if a position is part of a mill."""
        piece = self.board[position]
        if piece is None:
            return False

        # Check all mill configurations containing this position
        for mill in self.mills:
            if position in mill:
                if all(self.board[pos] == piece for pos in mill):
                    return True
        return False

    def is_valid_move(self, from_pos, to_pos):
        """Check if a move is valid."""
        # Position must be empty
        if self.board[to_pos] is not None:
            return False
            
        # Flying phase for a player with only 3 pieces
        if self.pieces_on_board[self.current_player] == 3:
            return True
            
        # Normal movement - must be adjacent
        return to_pos in self.adjacency[from_pos]

    def place_piece(self, position):
        """Place a piece on the board during the placing phase."""
        if self.phase != "placing":
            print("Not in placing phase.")
            return False
        
        if position < 0 or position > 23:
            print("Invalid position.")
            return False
            
        if self.board[position] is not None:
            print("Position already occupied.")
            return False
            
        # Place the piece
        self.board[position] = self.current_player
        self.pieces_to_place[self.current_player] -= 1
        self.pieces_on_board[self.current_player] += 1
        
        mill_formed = self.check_mill(position)
        
        # Switch to moving phase if all pieces are placed
        if self.pieces_to_place['W'] == 0 and self.pieces_to_place['B'] == 0:
            self.phase = "moving"
            
        # If mill is formed, player can remove an opponent's piece
        if mill_formed:
            return "mill_formed"
        else:
            self.switch_player()
            return True

    def move_piece(self, from_pos, to_pos):
        """Move a piece on the board during the moving phase."""
        if self.phase != "moving":
            print("Not in moving phase.")
            return False
            
        if from_pos < 0 or from_pos > 23 or to_pos < 0 or to_pos > 23:
            print("Invalid position.")
            return False
            
        if self.board[from_pos] != self.current_player:
            print("You don't have a piece at the starting position.")
            return False
            
        if not self.is_valid_move(from_pos, to_pos):
            print("Invalid move.")
            return False
            
        # Move the piece
        self.board[from_pos] = None
        self.board[to_pos] = self.current_player
        
        mill_formed = self.check_mill(to_pos)
        
        # If mill is formed, player can remove an opponent's piece
        if mill_formed:
            return "mill_formed"
        else:
            self.switch_player()
            self.check_game_over()
            return True

    def remove_piece(self, position):
        """Remove an opponent's piece after forming a mill."""
        opponent = 'B' if self.current_player == 'W' else 'W'
        
        if position < 0 or position > 23:
            print("Invalid position.")
            return False
            
        if self.board[position] != opponent:
            print("You can only remove your opponent's pieces.")
            return False
            
        # Check if the piece is part of a mill
        if self.check_mill(position):
            # Check if all opponent's pieces are in mills
            all_in_mills = True
            for pos in range(24):
                if self.board[pos] == opponent and not self.check_mill(pos):
                    all_in_mills = False
                    break
                    
            if not all_in_mills:
                print("You can't remove a piece that's part of a mill if other pieces are available.")
                return False
        
        # Remove the piece
        self.board[position] = None
        self.pieces_on_board[opponent] -= 1
        
        self.switch_player()
        self.check_game_over()
        return True

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'B' if self.current_player == 'W' else 'W'

    def check_game_over(self):
        """Check if the game is over."""
        # A player loses if they have less than 3 pieces or can't move
        for player in ['W', 'B']:
            if self.pieces_on_board[player] < 3 and self.pieces_to_place[player] == 0:
                self.phase = "game_over"
                winner = 'W' if player == 'B' else 'B'
                print(f"Game over! {winner} wins because {player} has less than 3 pieces.")
                return True
                
            # Check if player can move (only in moving phase)
            if self.phase == "moving" and player == self.current_player:
                can_move = False
                for pos in range(24):
                    if self.board[pos] == player:
                        # If player has only 3 pieces, they can "fly" to any empty position
                        if self.pieces_on_board[player] == 3:
                            for dest in range(24):
                                if self.board[dest] is None:
                                    can_move = True
                                    break
                        else:
                            # Check for regular moves to adjacent positions
                            for adj in self.adjacency[pos]:
                                if self.board[adj] is None:
                                    can_move = True
                                    break
                        if can_move:
                            break
                
                if not can_move:
                    self.phase = "game_over"
                    winner = 'W' if player == 'B' else 'B'
                    print(f"Game over! {winner} wins because {player} can't move.")
                    return True
                    
        return False

    def play(self):
        """Main game loop."""
        print("Welcome to Nine Men's Morris!")
        print("Positions are numbered from 0 to 23.")
        
        while self.phase != "game_over":
            self.print_board()
            
            if self.phase == "placing":
                try:
                    position = int(input(f"Player {self.current_player}, place a piece (0-23): "))
                    result = self.place_piece(position)
                    
                    if result == "mill_formed":
                        self.print_board()
                        remove_pos = int(input(f"Mill formed! Player {self.current_player}, remove opponent's piece (0-23): "))
                        self.remove_piece(remove_pos)
                        
                except ValueError:
                    print("Please enter a valid position (0-23).")
                    
            elif self.phase == "moving":
                try:
                    from_pos = int(input(f"Player {self.current_player}, select piece to move (0-23): "))
                    to_pos = int(input(f"Move to position (0-23): "))
                    result = self.move_piece(from_pos, to_pos)
                    
                    if result == "mill_formed":
                        self.print_board()
                        remove_pos = int(input(f"Mill formed! Player {self.current_player}, remove opponent's piece (0-23): "))
                        self.remove_piece(remove_pos)
                        
                except ValueError:
                    print("Please enter valid positions (0-23).")
        
        self.print_board()
        print("Game over!")


# Run the game
if __name__ == "__main__":
    game = NineMensMorris()
    game.play()
