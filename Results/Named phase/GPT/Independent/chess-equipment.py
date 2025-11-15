
import chess
import chess.engine
import chess.pgn

def create_custom_board():
    # Start with an empty board
    board = chess.Board()
    board.clear_board()

    # Place pawns
    for i in range(8):
        board.set_piece_at(chess.square(i, 1), chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(chess.square(i, 6), chess.Piece(chess.PAWN, chess.BLACK))

    # Place rooks
    board.set_piece_at(chess.A1, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.H1, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
    board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))

    # Place knights in the center (modified rule)
    board.set_piece_at(chess.D4, chess.Piece(chess.KNIGHT, chess.WHITE))
    board.set_piece_at(chess.E5, chess.Piece(chess.KNIGHT, chess.WHITE))
    board.set_piece_at(chess.E4, chess.Piece(chess.KNIGHT, chess.BLACK))
    board.set_piece_at(chess.D5, chess.Piece(chess.KNIGHT, chess.BLACK))

    # Place bishops
    board.set_piece_at(chess.C1, chess.Piece(chess.BISHOP, chess.WHITE))
    board.set_piece_at(chess.F1, chess.Piece(chess.BISHOP, chess.WHITE))
    board.set_piece_at(chess.C8, chess.Piece(chess.BISHOP, chess.BLACK))
    board.set_piece_at(chess.F8, chess.Piece(chess.BISHOP, chess.BLACK))

    # Place queens
    board.set_piece_at(chess.D1, chess.Piece(chess.QUEEN, chess.WHITE))
    board.set_piece_at(chess.D8, chess.Piece(chess.QUEEN, chess.BLACK))

    # Place kings
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

    return board

def play_game():
    # Create the custom board
    board = create_custom_board()
    print("Custom Starting Position:")
    print(board)

    # Play moves in a loop (or integrate with an engine)
    while not board.is_game_over():
        print("\nCurrent Board:")
        print(board)
        move = input("Enter your move in UCI format (e.g., e2e4): ").strip()
        try:
            board.push_uci(move)
        except ValueError:
            print("Invalid move. Try again.")
            continue

        if board.is_checkmate():
            print("\nCheckmate! Game over.")
            break
        elif board.is_stalemate():
            print("\nStalemate! Game over.")
            break
        elif board.is_insufficient_material():
            print("\nDraw due to insufficient material! Game over.")
            break

if __name__ == "__main__":
    play_game()
