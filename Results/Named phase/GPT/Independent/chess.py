# Researcher's note: in order to run this code and the other chess variations, this file must be renamed, or it will conflict with the chess package
import chess

def print_board(board):
    print(board)

def main():
    # Initialize the chess board
    board = chess.Board()

    print("Welcome to Chess!")
    print_board(board)

    while not board.is_game_over():
        try:
            # Input move from the current player
            move = input(f"{'White' if board.turn else 'Black'} to move: ")

            # Make the move on the board
            board.push_san(move)

            # Print the updated board
            print_board(board)
        except ValueError:
            print("Invalid move! Please try again.")

    # Check the result of the game
    if board.is_checkmate():
        print(f"Checkmate! {'White' if not board.turn else 'Black'} wins!")
    elif board.is_stalemate():
        print("Stalemate! The game is a draw.")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material.")
    elif board.is_seventyfive_moves():
        print("Draw due to 75-move rule.")
    elif board.is_fivefold_repetition():
        print("Draw due to fivefold repetition.")

if __name__ == "__main__":
    main()
