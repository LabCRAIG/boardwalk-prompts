def create_board():
    """Create a 3x3 empty board."""
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    """Print the current state of the board."""
    print("  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
    print()

def check_win(board, player_piece):
    """Check if a player has won by filling a row, column, or diagonal."""
    # Check rows
    for row in board:
        if all(cell == player_piece for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col] == player_piece for row in range(3)):
            return True
    
    # Check main diagonal
    if all(board[i][i] == player_piece for i in range(3)):
        return True
    
    # Check other diagonal
    if all(board[i][2-i] == player_piece for i in range(3)):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def is_valid_move(board, row, col):
    """Check if a move is valid."""
    if not (0 <= row < 3 and 0 <= col < 3):
        return False
    return board[row][col] == ' '

def play_peridot():
    """Main function to play the game."""
    board = create_board()
    current_player = 1
    pieces = {1: 'A', 2: 'V'}
    game_over = False
    
    print("Welcome to Peridot!")
    print("Player 1 uses 'A', Player 2 uses 'V'")
    print("Enter your move as 'row col' (e.g., '1 2')")
    
    while not game_over:
        print_board(board)
        print(f"Player {current_player}'s turn ({pieces[current_player]})")
        
        valid_move = False
        while not valid_move:
            try:
                row, col = map(int, input("Enter row and column (0-2): ").split())
                valid_move = is_valid_move(board, row, col)
                if not valid_move:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter two numbers separated by a space.")
        
        board[row][col] = pieces[current_player]
        
        if check_win(board, pieces[current_player]):
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            game_over = True
        else:
            current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    play_peridot()