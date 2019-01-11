from unorthodox import (BLACK, Position, SingleStepPawn, WHITE, black_king,
                        black_knight, black_queen, black_rook, play,
                        white_king, white_knight, white_queen, white_rook)


white_pawn = SingleStepPawn(WHITE, "P", (white_queen, white_knight,
                                         white_rook))
black_pawn = SingleStepPawn(BLACK, "p", (black_queen, black_knight,
                                         black_rook))
position = Position(size=(6, 6))
position[0, 0] = black_rook
position[0, 1] = black_knight
position[0, 2] = black_queen
position[0, 3] = black_king
position[0, 4] = black_knight
position[0, 5] = black_rook
position[1, 0] = black_pawn
position[1, 1] = black_pawn
position[1, 2] = black_pawn
position[1, 3] = black_pawn
position[1, 4] = black_pawn
position[1, 5] = black_pawn
position[4, 0] = white_pawn
position[4, 1] = white_pawn
position[4, 2] = white_pawn
position[4, 3] = white_pawn
position[4, 4] = white_pawn
position[4, 5] = white_pawn
position[5, 0] = white_rook
position[5, 1] = white_knight
position[5, 2] = white_queen
position[5, 3] = white_king
position[5, 4] = white_knight
position[5, 5] = white_rook
position.royal[WHITE] = 5, 3
position.royal[BLACK] = 0, 3
if __name__ == "__main__":
    print("Los Alamos Chess by Paul Stein and Mark Wells")
    print("Rules: https://www.chessvariants.com/small.dir/losalamos.html")
    play(position, 10)
