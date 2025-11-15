def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * (len(board) * 4 - 1))


def check_winner(board, player):
    """Checks if the given player has 5 in a row."""
    size = len(board)
    
    # Check rows
    for row in board:
        if "".join(row).find(player * 5) != -1:
            return True
    
    # Check columns
    for col in range(size):
        column = "".join([board[row][col] for row in range(size)])
        if column.find(player * 5) != -1:
            return True
    
    # Check diagonals
    for row in range(size - 4):
        for col in range(size - 4):
            # Check main diagonal
            if all(board[row + i][col + i] == player for i in range(5)):
                return True
            # Check anti-diagonal
            if all(board[row + i][col + 4 - i] == player for i in range(5)):
                return True
    
    return False


def is_full(board):
    """Checks if the board is full."""
    return all(cell != " " for row in board for cell in row)


def get_player_input(board, player):
    """Gets valid input from the player."""
    while True:
        try:
            move = input(f"Player {player}, enter your move (row and column separated by space, e.g., '1 2'): ")
            row, col = map(int, move.split())
            if board[row][col] == " ":
                return row, col
            else:
                print("That cell is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers within the range of the board.")


def play_game():
    """Main function to play 5x5 Tic-Tac-Toe."""
    size = 5
    board = [[" " for _ in range(size)] for _ in range(size)]
    players = ["X", "O"]
    turn = 0
    
    print("Welcome to 5x5 Tic-Tac-Toe! Get 5 in a row to win!")
    print_board(board)
    
    while True:
        current_player = players[turn % 2]
        print(f"Player {current_player}'s turn.")
        
        # Get player input
        row, col = get_player_input(board, current_player)
        board[row][col] = current_player
        
        # Print the updated board
        print_board(board)
        
        # Check for a winner
        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break
        
        # Check for a draw
        if is_full(board):
            print("It's a draw!")
            break
        
        # Switch turn
        turn += 1


if __name__ == "__main__":
    play_game()