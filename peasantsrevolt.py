from unorthodox import (BLACK, EnPassantPosition, DoubleStepPawn, WHITE,
                        black_bishop, black_king, black_knight, black_queen,
                        black_rook, play, white_bishop, white_king,
                        white_knight, white_queen, white_rook)


white_pawn = DoubleStepPawn(WHITE, "P", (white_queen, white_bishop,
                                         white_knight, white_rook), 6)
black_pawn = DoubleStepPawn(BLACK, "p", (black_queen, black_bishop,
                                         black_knight, black_rook), 1)
position = EnPassantPosition(size=(8, 8))
position[0, 1] = black_knight
position[0, 2] = black_knight
position[0, 4] = black_king
position[0, 6] = black_knight
position[1, 4] = black_pawn
position[6, 0] = white_pawn
position[6, 1] = white_pawn
position[6, 2] = white_pawn
position[6, 3] = white_pawn
position[6, 4] = white_pawn
position[6, 5] = white_pawn
position[6, 6] = white_pawn
position[6, 7] = white_pawn
position[7, 4] = white_king
position.royal[WHITE] = 7, 4
position.royal[BLACK] = 0, 4
if __name__ == "__main__":
    play(position, 10)
