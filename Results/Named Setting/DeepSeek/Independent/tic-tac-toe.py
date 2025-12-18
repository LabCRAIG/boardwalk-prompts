import random

def print_board(board):
    """Prints the current state of the board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board):
    """Checks if there's a winner or if the game is a tie."""
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != " ":
            return board[i]
    
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != " ":
            return board[i]
    
    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]
    
    # Check for tie
    if " " not in board:
        return "Tie"
    
    return None

def player_move(board):
    """Handles the player's move."""
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def computer_move(board, computer_char):
    """Simple AI for the computer's move."""
    # Check for winning move
    for i in range(9):
        if board[i] == " ":
            board_copy = board.copy()
            board_copy[i] = computer_char
            if check_winner(board_copy) == computer_char:
                return i
    
    # Check for player's winning move and block
    player_char = "O" if computer_char == "X" else "X"
    for i in range(9):
        if board[i] == " ":
            board_copy = board.copy()
            board_copy[i] = player_char
            if check_winner(board_copy) == player_char:
                return i
    
    # Try to take the center
    if board[4] == " ":
        return 4
    
    # Try to take a corner
    corners = [0, 2, 6, 8]
    available_corners = [c for c in corners if board[c] == " "]
    if available_corners:
        return random.choice(available_corners)
    
    # Take any available edge
    edges = [1, 3, 5, 7]
    available_edges = [e for e in edges if board[e] == " "]
    if available_edges:
        return random.choice(available_edges)
    
    # Shouldn't reach here if game isn't over
    return -1

def play_game():
    """Main game loop."""
    board = [" "] * 9
    print("Welcome to Tic-Tac-Toe!")
    print("Positions are numbered 1-9 from top-left to bottom-right.")
    
    # Player chooses X or O
    player_char = input("Choose X or O: ").upper()
    while player_char not in ["X", "O"]:
        player_char = input("Please choose X or O: ").upper()
    
    computer_char = "O" if player_char == "X" else "X"
    
    # Determine who goes first
    current_player = "player" if player_char == "X" else "computer"
    print(f"You are {player_char}. {current_player.capitalize()} goes first.")
    
    while True:
        print_board(board)
        
        if current_player == "player":
            move = player_move(board)
            board[move] = player_char
        else:
            print("Computer's turn...")
            move = computer_move(board, computer_char)
            board[move] = computer_char
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "Tie":
                print("It's a tie!")
            elif winner == player_char:
                print("Congratulations! You win!")
            else:
                print("Computer wins!")
            break
        
        # Switch players
        current_player = "computer" if current_player == "player" else "player"

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break