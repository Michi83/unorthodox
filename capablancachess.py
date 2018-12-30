from unorthodox import (BLACK, CapablancaPosition, Compound, DoubleStepPawn,
                        WHITE, black_bishop, black_king, black_knight,
                        black_queen, black_rook, play, white_bishop,
                        white_king, white_knight, white_queen, white_rook)


class Chancellor(Compound):
    value = 850


class Archbishop(Compound):
    value = 800


white_chancellor = Chancellor(WHITE, "C", (white_rook, white_knight))
black_chancellor = Chancellor(BLACK, "c", (black_rook, black_knight))
white_archbishop = Archbishop(WHITE, "A", (white_bishop, white_knight))
black_archbishop = Archbishop(BLACK, "a", (black_bishop, black_knight))
white_pawn = DoubleStepPawn(WHITE, "P", (white_queen, white_chancellor,
                                         white_archbishop, white_bishop,
                                         white_knight, white_rook), 6)
black_pawn = DoubleStepPawn(BLACK, "p", (black_queen, black_chancellor,
                                         black_archbishop, black_bishop,
                                         black_knight, black_rook), 1)
position = CapablancaPosition()
position[0, 0] = black_rook
position[0, 1] = black_knight
position[0, 2] = black_archbishop
position[0, 3] = black_bishop
position[0, 4] = black_queen
position[0, 5] = black_king
position[0, 6] = black_bishop
position[0, 7] = black_chancellor
position[0, 8] = black_knight
position[0, 9] = black_rook
position[1, 0] = black_pawn
position[1, 1] = black_pawn
position[1, 2] = black_pawn
position[1, 3] = black_pawn
position[1, 4] = black_pawn
position[1, 5] = black_pawn
position[1, 6] = black_pawn
position[1, 7] = black_pawn
position[1, 8] = black_pawn
position[1, 9] = black_pawn
position[6, 0] = white_pawn
position[6, 1] = white_pawn
position[6, 2] = white_pawn
position[6, 3] = white_pawn
position[6, 4] = white_pawn
position[6, 5] = white_pawn
position[6, 6] = white_pawn
position[6, 7] = white_pawn
position[6, 8] = white_pawn
position[6, 9] = white_pawn
position[7, 0] = white_rook
position[7, 1] = white_knight
position[7, 2] = white_archbishop
position[7, 3] = white_bishop
position[7, 4] = white_queen
position[7, 5] = white_king
position[7, 6] = white_bishop
position[7, 7] = white_chancellor
position[7, 8] = white_knight
position[7, 9] = white_rook
position.royal[WHITE] = 7, 5
position.royal[BLACK] = 0, 5
position.castling = [True, True, True, True]
if __name__ == "__main__":
    play(position, 1, 2, 2)
