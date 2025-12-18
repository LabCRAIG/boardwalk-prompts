def print_board(board):
    for i in range(3):
        print("|".join(board[i]))
        if i < 2:
            print("-" * 5)

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    # Check for tie
    if all(" " not in row for row in board):
        return "Tie"
    
    return None

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    
    print("Welcome to Tic-Tac-Toe!")
    print("Enter your move as row,column (0-2)")
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        
        try:
            move = input("Enter your move (row,col): ")
            row, col = map(int, move.split(","))
            
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("Invalid move. Row and column must be between 0 and 2.")
                continue
                
            if board[row][col] != " ":
                print("That position is already taken. Try again.")
                continue
                
            board[row][col] = current_player
            
            winner = check_winner(board)
            if winner:
                print_board(board)
                if winner == "Tie":
                    print("It's a tie!")
                else:
                    print(f"Player {winner} wins!")
                break
                
            current_player = "O" if current_player == "X" else "X"
            
        except ValueError:
            print("Invalid input. Enter your move as 'row,col' (e.g., '1,2')")
        except IndexError:
            print("Invalid move. Row and column must be between 0 and 2.")

if __name__ == "__main__":
    tic_tac_toe()