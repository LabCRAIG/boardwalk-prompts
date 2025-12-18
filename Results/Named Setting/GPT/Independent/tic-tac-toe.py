def print_board(board):
    """Prints the current state of the board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board):
    """Checks if there's a winner or if the game is a draw."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    # Check for a draw
    for row in board:
        if " " in row:
            return None  # Game is still ongoing

    return "Draw"


def tic_tac_toe():
    """Main function to play the game."""
    # Initialize the board
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_turn = "X"

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        print(f"Player {player_turn}'s turn.")

        # Get player input
        try:
            row = int(input("Enter the row (0, 1, 2): "))
            col = int(input("Enter the column (0, 1, 2): "))
        except ValueError:
            print("Invalid input! Please enter numbers between 0 and 2.")
            continue

        # Validate input
        if row not in range(3) or col not in range(3):
            print("Invalid move! Position out of bounds. Try again.")
            continue

        if board[row][col] != " ":
            print("Invalid move! Cell already occupied. Try again.")
            continue

        # Make the move
        board[row][col] = player_turn
        print_board(board)

        # Check for a winner
        result = check_winner(board)
        if result:
            if result == "Draw":
                print("It's a draw!")
            else:
                print(f"Player {result} wins!")
            break

        # Switch player
        player_turn = "O" if player_turn == "X" else "X"


# Run the game
if __name__ == "__main__":
    tic_tac_toe()