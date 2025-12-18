
class NineMensMorris:
    def __init__(self):
        self.board = {
            "a1": None, "a4": None, "a7": None,
            "b2": None, "b4": None, "b6": None,
            "c3": None, "c4": None, "c5": None,
            "d1": None, "d2": None, "d3": None, "d5": None, "d6": None, "d7": None,
            "e3": None, "e4": None, "e5": None,
            "f2": None, "f4": None, "f6": None,
            "g1": None, "g4": None, "g7": None
        }
        self.mills = [
            # Horizontal mills
            ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
            ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
            ["f2", "f4", "f6"], ["g1", "g4", "g7"],
            # Vertical mills
            ["a1", "d1", "g1"], ["b2", "d2", "f2"], ["c3", "d3", "e3"],
            ["a4", "b4", "c4"], ["e4", "f4", "g4"], ["c5", "d5", "e5"],
            ["b6", "d6", "f6"], ["a7", "d7", "g7"]
        ]
        self.players = ["X", "O"]
        self.current_player = self.players[0]
        self.phase = 1  # 1 for placing pieces, 2 for moving pieces
        self.pieces = {player: 9 for player in self.players}
        self.placed_pieces = {player: 0 for player in self.players}

    def display_board(self):
        board = self.board
        print(f"""
        {board["a1"] or "."}---------{board["a4"] or "."}---------{board["a7"] or "."}
        |         |         |
        |   {board["b2"] or "."}-----{board["b4"] or "."}-----{board["b6"] or "."}   |
        |   |     |     |   |
        {board["c3"] or "."}---{board["c4"] or "."}-----{board["c5"] or "."}---{board["c5"] or "."}
        |   |     |     |   |
        |   {board["d2"] or "."}-----{board["d3"] or "."}-----{board["d6"] or "."}   |
        |         |         |
        {board["e3"] or "."}---------{board["e4"] or "."}---------{board["e5"] or "."}
""")


    def check_mill(self, position, player):
        for mill in self.mills:
            if position in mill and all(self.board[pos] == player for pos in mill):
                return True
        return False

    def place_piece(self, position):
        if self.phase != 1:
            print("You can only place pieces in phase 1.")
            return False
        if self.board[position] is not None:
            print("Position is already occupied!")
            return False
        self.board[position] = self.current_player
        self.placed_pieces[self.current_player] += 1
        if self.check_mill(position, self.current_player):
            print(f"{self.current_player} has formed a mill!")
            self.remove_opponent_piece(position)
        self.switch_player()
        if all(p == 9 for p in self.placed_pieces.values()):
            self.phase = 2
        return True

    def remove_opponent_piece(self, mill_position):
        opponent = self.players[1 - self.players.index(self.current_player)]
        valid_positions = [pos for pos in self.board if self.board[pos] == opponent and pos in self.get_square(mill_position)]
        if not valid_positions:
            print(f"No valid pieces to remove on the same square as {mill_position}.")
            return
        print(f"Remove one of opponent's pieces from {valid_positions}:")
        while True:
            pos = input("Enter position to remove: ")
            if pos in valid_positions:
                self.board[pos] = None
                self.pieces[opponent] -= 1
                break
            print("Invalid position. Try again.")

    def get_square(self, position):
        """
        Return the set of positions that belong to the same square as `position`.
        There are three squares: outer, middle, and inner.
        """
        outer_square = {"a1", "a4", "a7", "d1", "d7", "g1", "g4", "g7"}
        middle_square = {"b2", "b4", "b6", "d2", "d6", "f2", "f4", "f6"}
        inner_square = {"c3", "c4", "c5", "d3", "d5", "e3", "e4", "e5"}

        if position in outer_square:
            return outer_square
        elif position in middle_square:
            return middle_square
        elif position in inner_square:
            return inner_square
        return set()

    def switch_player(self):
        self.current_player = self.players[1 - self.players.index(self.current_player)]

# Example usage
game = NineMensMorris()
game.display_board()

while True:
    print(f"{game.current_player}'s turn. Phase: {game.phase}")
    if game.phase == 1:
        pos = input("Enter position to place piece: ")
        game.place_piece(pos)
    elif game.phase == 2:
        print("Phase 2 logic is not yet implemented.")
    game.display_board()
