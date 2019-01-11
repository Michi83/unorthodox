from unorthodox import (BLACK, LOSS, Leaper, NEUTRAL, Position, SingleStepPawn,
                        WHITE, black_king, black_knight, black_rook, play,
                        white_king, white_knight, white_rook)


class Ferz(Leaper):
    value = 175
    offsets = (-1, -1), (-1, 1), (1, -1), (1, 1)


class Elephant(Leaper):
    value = 130
    offsets = (-2, -2), (-2, 2), (2, -2), (2, 2)


class BareKingPosition(Position):
    """A board with support for the bare king rule."""

    def __init__(self, **kwargs):
        Position.__init__(self, **kwargs)
        if "copy" in kwargs:
            self.pieces = dict(kwargs["copy"].pieces)
        else:
            self.pieces = {WHITE: 0, BLACK: 0}

    def __setitem__(self, square, piece):
        """Put a piece on a square and update the piece count."""
        if self[square].player != NEUTRAL:
            self.pieces[self[square].player] -= 1
        if piece.player != NEUTRAL:
            self.pieces[piece.player] += 1
        Position.__setitem__(self, square, piece)

    def check(self, defender):
        """Return True if the defender's king is in check or bare."""
        return (Position.check(self, defender) or self.pieces[defender] == 1
                and self.pieces[-defender] > 1)


white_ferz = Ferz(WHITE, "F")
black_ferz = Ferz(BLACK, "f")
white_elephant = Elephant(WHITE, "E")
black_elephant = Elephant(BLACK, "e")
white_pawn = SingleStepPawn(WHITE, "P", (white_ferz,))
black_pawn = SingleStepPawn(BLACK, "p", (black_ferz,))
position = BareKingPosition(size=(8, 8))
position[0, 0] = black_rook
position[0, 1] = black_knight
position[0, 2] = black_elephant
position[0, 3] = black_king
position[0, 4] = black_ferz
position[0, 5] = black_elephant
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
position[7, 2] = white_elephant
position[7, 3] = white_king
position[7, 4] = white_ferz
position[7, 5] = white_elephant
position[7, 6] = white_knight
position[7, 7] = white_rook
position.royal[WHITE] = 7, 3
position.royal[BLACK] = 0, 3
if __name__ == "__main__":
    print("Shatranj, inventor unknown")
    print("Rules: https://www.chessvariants.com/historic.dir/shatranj.html")
    play(position, 10, stalemate=LOSS)
