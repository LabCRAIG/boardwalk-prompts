def print_board(board):
    """Print the current state of the board."""
    for i in range(5):
        row = " | ".join(board[i])
        print(row)
        if i < 4:
            print("-" * 17)

def check_win(board, player):
    """Check if the player has won."""
    # Check rows
    for row in board:
        for i in range(1):
            if row[i:i+5] == [player] * 5:
                return True
    
    # Check columns
    for col in range(5):
        for i in range(1):
            if all(board[i+j][col] == player for j in range(5)):
                return True
    
    # Check diagonals
    if all(board[i][i] == player for i in range(5)):
        return True
    if all(board[i][4-i] == player for i in range(5)):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    for row in board:
        if " " in row:
            return False
    return True

def get_move():
    """Get a valid move from the player."""
    while True:
        try:
            move = input("Enter your move (row,col): ")
            row, col = map(int, move.split(","))
            if 0 <= row < 5 and 0 <= col < 5:
                return row, col
            else:
                print("Invalid coordinates. Please enter values between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter row,col (e.g., 2,3)")

def play_game():
    """Main game function."""
    # Initialize empty board
    board = [[" " for _ in range(5)] for _ in range(5)]
    current_player = "X"
    
    print("Welcome to 5x5 Tic-Tac-Toe!")
    print("Enter moves as 'row,col' with 0-indexed coordinates")
    print_board(board)
    
    while True:
        print(f"\nPlayer {current_player}'s turn")
        row, col = get_move()
        
        # Check if cell is already occupied
        if board[row][col] != " ":
            print("That cell is already taken. Try again.")
            continue
        
        # Make the move
        board[row][col] = current_player
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"\nPlayer {current_player} wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("\nIt's a draw!")
            break
        
        # Switch player
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()