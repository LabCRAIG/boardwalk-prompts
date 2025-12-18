
class NineMensMorris:
    def __init__(self):
        # Initialize the board with 24 valid positions plus the center (25th position)
        self.board = [" "] * 25  # " " represents an empty space
        self.players = ["X", "O"]  # Two players with pieces X and O
        self.current_player = 0  # Index for the current player
        self.phase = "placing"  # Game phases: 'placing' or 'moving'
        self.pieces = {"X": 9, "O": 9}  # Pieces left to place for each player
    
    def display_board(self):
        # Display the board in a human-readable format
        print(f"""
        {self.board[0]}---------{self.board[1]}---------{self.board[2]}
        |         |         |
        |   {self.board[8]}-----{self.board[9]}-----{self.board[10]}   |
        |   |     |     |   |
        |   | {self.board[16]}-{self.board[17]}-{self.board[18]} |   |
        {self.board[3]}-{self.board[11]}-{self.board[19]}     {self.board[20]}-{self.board[12]}-{self.board[4]}
        |   | {self.board[21]}-{self.board[22]}-{self.board[23]} |   |
        |   |     |     |   |
        |   {self.board[13]}-----{self.board[14]}-----{self.board[15]}   |
        |         |         |
        {self.board[5]}---------{self.board[6]}---------{self.board[7]}
                  {self.board[24]} (center)
        """)
    
    def is_valid_position(self, pos):
        # Check if a position is valid on the board
        return 0 <= pos <= 24 and self.board[pos] == " "
    
    def place_piece(self, pos):
        # Place a piece on the board during the placing phase
        if self.phase != "placing":
            print("You cannot place pieces during the moving phase!")
            return False
        if not self.is_valid_position(pos):
            print("Invalid position! Try again.")
            return False
        
        piece = self.players[self.current_player]
        self.board[pos] = piece
        self.pieces[piece] -= 1
        print(f"Player {piece} placed a piece at position {pos}.")
        
        # Check if all pieces have been placed
        if self.pieces["X"] == 0 and self.pieces["O"] == 0:
            self.phase = "moving"
            print("All pieces placed! Moving to the moving phase.")
        
        return True
    
    def move_piece(self, from_pos, to_pos):
        # Move a piece from one position to another during the moving phase
        if self.phase != "moving":
            print("You cannot move pieces during the placing phase!")
            return False
        piece = self.players[self.current_player]
        if self.board[from_pos] != piece or not self.is_valid_position(to_pos):
            print("Invalid move! Try again.")
            return False
        
        self.board[from_pos] = " "
        self.board[to_pos] = piece
        print(f"Player {piece} moved from position {from_pos} to position {to_pos}.")
        return True
    
    def switch_player(self):
        # Switch to the other player's turn
        self.current_player = 1 - self.current_player
    
    def check_mill(self, pos):
        # Check if a mill is formed (three pieces in a row)
        piece = self.players[self.current_player]
        # Define all possible mills (lines of three)
        mills = [
            [0, 1, 2], [3, 11, 19], [5, 6, 7], [8, 9, 10],
            [13, 14, 15], [16, 17, 18], [20, 21, 22], [23, 24, 25],
            # Add other mills as appropriate for the board layout
        ]
        for mill in mills:
            if pos in mill and all(self.board[p] == piece for p in mill):
                print(f"Player {piece} formed a mill!")
                return True
        return False
    
    def remove_piece(self, pos):
        # Remove an opponent's piece if a mill is formed
        piece = self.players[1 - self.current_player]
        if self.board[pos] != piece:
            print("You can only remove your opponent's piece! Try again.")
            return False
        self.board[pos] = " "
        print(f"Player {piece}'s piece at position {pos} has been removed.")
        return True
    
    def play_turn(self):
        # Play a single turn for the current player
        self.display_board()
        piece = self.players[self.current_player]
        print(f"Player {piece}'s turn.")
        
        if self.phase == "placing":
            pos = int(input("Enter the position to place your piece (0-24): "))
            if self.place_piece(pos):
                if self.check_mill(pos):
                    remove_pos = int(input("Mill formed! Choose a piece to remove (0-24): "))
                    self.remove_piece(remove_pos)
        elif self.phase == "moving":
            from_pos = int(input("Enter the position to move from (0-24): "))
            to_pos = int(input("Enter the position to move to (0-24): "))
            if self.move_piece(from_pos, to_pos):
                if self.check_mill(to_pos):
                    remove_pos = int(input("Mill formed! Choose a piece to remove (0-24): "))
                    self.remove_piece(remove_pos)
        
        self.switch_player()

# Main game loop
game = NineMensMorris()
while True:
    game.play_turn()
