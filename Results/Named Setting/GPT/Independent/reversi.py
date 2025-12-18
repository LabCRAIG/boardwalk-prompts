def initialize_board():
    """Initialize the game board."""
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3], board[3][4] = 'O', 'X'
    board[4][3], board[4][4] = 'X', 'O'
    return board


def print_board(board):
    """Print the current board state."""
    print("  " + " ".join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(row))


def is_valid_move(board, row, col, player):
    """Check if a move is valid for the given player."""
    if board[row][col] != ' ':
        return False

    opponent = 'X' if player == 'O' else 'O'
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        has_opponent = False

        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            has_opponent = True
            r += dr
            c += dc

        if has_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True

    return False


def get_valid_moves(board, player):
    """Return a list of valid moves for the given player."""
    valid_moves = []
    for r in range(8):
        for c in range(8):
            if is_valid_move(board, r, c, player):
                valid_moves.append((r, c))
    return valid_moves


def make_move(board, row, col, player):
    """Make a move for the given player, flipping opponent pieces."""
    opponent = 'X' if player == 'O' else 'O'
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

    board[row][col] = player

    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []

        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc

        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for rr, cc in pieces_to_flip:
                board[rr][cc] = player


def has_valid_moves(board, player):
    """Check if the player has any valid moves."""
    return bool(get_valid_moves(board, player))


def count_pieces(board):
    """Count the number of pieces for each player."""
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    return x_count, o_count


def play_reversi():
    """Main function to play the game."""
    board = initialize_board()
    current_player = 'X'

    while True:
        print_board(board)
        print(f"Current player: {current_player}")

        if not has_valid_moves(board, current_player):
            print(f"No valid moves for {current_player}. Skipping turn.")
            current_player = 'X' if current_player == 'O' else 'O'
            if not has_valid_moves(board, current_player):
                print("No valid moves for both players. Game over!")
                break
            continue

        valid_moves = get_valid_moves(board, current_player)
        print("Valid moves:", valid_moves)

        while True:
            try:
                move = input("Enter your move (row col): ")
                row, col = map(int, move.split())
                if (row, col) in valid_moves:
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter row and column as numbers separated by space.")

        make_move(board, row, col, current_player)
        current_player = 'X' if current_player == 'O' else 'O'

    x_count, o_count = count_pieces(board)
    print_board(board)
    print(f"Final score - X: {x_count}, O: {o_count}")
    if x_count > o_count:
        print("Player X wins!")
    elif o_count > x_count:
        print("Player O wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    play_reversi()