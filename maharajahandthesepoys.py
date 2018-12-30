from unorthodox import (BLACK, DoubleStepPawn, LeaperRider, OrthodoxPosition,
                        WHITE, black_bishop, black_king, black_knight,
                        black_queen, black_rook, play)


class Maharajah(LeaperRider):
    value = 1200

    leaper_offsets = (
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1),
    )

    rider_offsets = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1),
        (0, 1), (1, -1), (1, 0), (1, 1),
    )


class SepoyPawn(DoubleStepPawn):
    def __init__(self, player, symbol, initial_rank):
        DoubleStepPawn.__init__(self, player, symbol, (), initial_rank)

    def can_promote(self, square, position):
        return False

    def must_promote(self, square, position):
        return False


white_maharajah = Maharajah(WHITE, "M")
black_pawn = SepoyPawn(BLACK, "p", 1)
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
position[7, 4] = white_maharajah
position.royal[WHITE] = 7, 4
position.royal[BLACK] = 0, 4
position.castling = [False, False, True, True]
if __name__ == "__main__":
    play(position, 10, 2, 1)
