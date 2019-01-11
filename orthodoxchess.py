from unorthodox import (BLACK, DoubleStepPawn, OrthodoxPosition, WHITE,
                        black_bishop, black_king, black_knight, black_queen,
                        black_rook, play, white_bishop, white_king,
                        white_knight, white_queen, white_rook)


# Standard-rules chess

white_pawn = DoubleStepPawn(WHITE, "P", (white_queen, white_bishop,
                                         white_knight, white_rook), 6)
black_pawn = DoubleStepPawn(BLACK, "p", (black_queen, black_bishop,
                                         black_knight, black_rook), 1)
position = OrthodoxPosition()
position[0, 0] = black_rook
position[0, 1] = black_knight
position[0, 2] = black_bishop
position[0, 3] = black_queen
position[0, 4] = black_king
position[0, 5] = black_bishop
position[0, 6] = black_knight
position[0, 7] = black_rook
position[1, 0] = black_pawn
position[1, 1] = black_pawn
position[1, 2] = black_pawn
position[1, 3] = black_pawn
position[1, 4] = black_pawn
position[1, 5] = black_pawn
position[1, 6] = black_pawn
position[1, 7] = black_pawn
position[6, 0] = white_pawn
position[6, 1] = white_pawn
position[6, 2] = white_pawn
position[6, 3] = white_pawn
position[6, 4] = white_pawn
position[6, 5] = white_pawn
position[6, 6] = white_pawn
position[6, 7] = white_pawn
position[7, 0] = white_rook
position[7, 1] = white_knight
position[7, 2] = white_bishop
position[7, 3] = white_queen
position[7, 4] = white_king
position[7, 5] = white_bishop
position[7, 6] = white_knight
position[7, 7] = white_rook
position.royal[WHITE] = 7, 4
position.royal[BLACK] = 0, 4
position.castling = [True, True, True, True]
if __name__ == "__main__":
    print("Standard-rules chess, inventor unknown")
    print("Rules: https://www.chessvariants.com/d.chess/chess.html")
    play(position, 10)
