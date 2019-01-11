from unorthodox import (BLACK, DoubleStepPawn, EnPassantPosition, LeaperRider,
                        WHITE, black_bishop, black_king, black_knight,
                        black_queen, black_rook, empty, play, white_bishop,
                        white_king, white_knight, white_queen, white_rook)


class Chancellor(LeaperRider):
    value = 765
    rider_offsets = (-1, 0), (0, -1), (0, 1), (1, 0)
    leaper_offsets = (
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    )


class Archbishop(LeaperRider):
    value = 640
    rider_offsets = (-1, -1), (-1, 1), (1, -1), (1, 1)
    leaper_offsets = (
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    )


class CapablancaPosition(EnPassantPosition):
    """An 8x10 position with support for Capablanca castling."""

    def __init__(self, **kwargs):
        if "copy" in kwargs:
            copy = kwargs["copy"]
            EnPassantPosition.__init__(self, **kwargs)
            self.castling = list(copy.castling)  # copy castling rights
        else:
            EnPassantPosition.__init__(self, size=(8, 10))
            self.castling = [False, False, False, False]

    def black_kingside_castling(self):
        """Return True if black kingside castling is possible."""
        return (self.castling[2] and self.empty((0, 6)) and self.empty((0, 7))
                and self.empty((0, 8)) and not self.attacked((0, 5), WHITE)
                and not self.attacked((0, 6), WHITE) and not
                self.attacked((0, 7), WHITE))

    def black_queenside_castling(self):
        """Return True if black queenside castling is possible."""
        return (self.castling[3] and self.empty((0, 4)) and self.empty((0, 3))
                and self.empty((0, 2)) and self.empty((0, 1)) and not
                self.attacked((0, 5), WHITE) and not
                self.attacked((0, 4), WHITE) and not
                self.attacked((0, 3), WHITE))

    def generate_moves(self):
        moves = EnPassantPosition.generate_moves(self)
        # castling
        if self.player == WHITE:
            if self.white_kingside_castling():
                move = self.make_move((7, 5), (7, 8))
                move[7, 7] = white_rook
                move[7, 9] = empty
                moves.append(move)
            if self.white_queenside_castling():
                move = self.make_move((7, 5), (7, 2))
                move[7, 3] = white_rook
                move[7, 0] = empty
                moves.append(move)
        else:
            if self.black_kingside_castling():
                move = self.make_move((0, 5), (0, 8))
                move[0, 7] = black_rook
                move[0, 9] = empty
                moves.append(move)
            if self.black_queenside_castling():
                move = self.make_move((0, 5), (0, 2))
                move[0, 3] = black_rook
                move[0, 0] = empty
                moves.append(move)
        return moves

    def make_move(self, origin, target):
        move = EnPassantPosition.make_move(self, origin, target)
        # update castling rights
        if origin == (7, 5) or origin == (7, 9) or target == (7, 9):
            move.castling[0] = False
        if origin == (7, 5) or origin == (7, 0) or target == (7, 0):
            move.castling[1] = False
        if origin == (0, 5) or origin == (0, 9) or target == (0, 9):
            move.castling[2] = False
        if origin == (0, 5) or origin == (0, 0) or target == (0, 0):
            move.castling[3] = False
        return move

    def white_kingside_castling(self):
        """Return True if white kingside castling is possible."""
        return (self.castling[0] and self.empty((7, 6)) and self.empty((7, 7))
                and self.empty((7, 8)) and not self.attacked((7, 5), BLACK)
                and not self.attacked((7, 6), BLACK) and not
                self.attacked((7, 7), BLACK))

    def white_queenside_castling(self):
        """Return True if white queenside castling is possible."""
        return (self.castling[1] and self.empty((7, 4)) and self.empty((7, 3))
                and self.empty((7, 2)) and self.empty((7, 1)) and not
                self.attacked((7, 5), BLACK) and not
                self.attacked((7, 4), BLACK) and not
                self.attacked((7, 3), BLACK))


white_chancellor = Chancellor(WHITE, "C")
black_chancellor = Chancellor(BLACK, "c")
white_archbishop = Archbishop(WHITE, "A")
black_archbishop = Archbishop(BLACK, "a")
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
    print("Capablanca Chess by José Raúl Capablanca")
    print("Rules: https://www.chessvariants.com/large.dir/capablanca.html")
    play(position, 10)
