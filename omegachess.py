from unorthodox import (BLACK, Leaper, TripleStepEnPassantPosition,
                        TripleStepPawn, WHITE, black_bishop, black_king,
                        black_knight, black_queen, black_rook, empty, lava,
                        play, white_bishop, white_king, white_knight,
                        white_queen, white_rook)


class Champion(Leaper):
    value = 400
    offsets = (
        (-1, 0), (0, -1), (0, 1), (1, 0),
        (-2, -2), (-2, 0), (-2, 2), (0, -2),
        (0, 2), (2, -2), (2, 0), (2, 2),
    )


class Wizard(Leaper):
    value = 400
    offsets = (
        (-1, -1), (-1, 1), (1, -1), (1, 1),
        (-3, -1), (-3, 1), (-1, -3), (-1, 3),
        (1, -3), (1, 3), (3, -1), (3, 1),
    )


class OmegaPawn(TripleStepPawn):
    def can_promote(self, position, square):
        return (self.player == WHITE and square[0] == 1 or self.player == BLACK
                and square[0] == 10)


class OmegaPosition(TripleStepEnPassantPosition):
    def __init__(self, **kwargs):
        if "copy" in kwargs:
            copy = kwargs["copy"]
            TripleStepEnPassantPosition.__init__(self, **kwargs)
            self.castling = list(copy.castling)  # copy castling rights
        else:
            TripleStepEnPassantPosition.__init__(self, size=(12, 12))
            for i in range(1, 11):
                self[0, i] = lava
                self[i, 0] = lava
                self[i, 11] = lava
                self[11, i] = lava
            self.castling = [False, False, False, False]

    def black_kingside_castling(self):
        """Return True if black kingside castling is possible."""
        return (self.castling[2] and self.empty((1, 7)) and self.empty((1, 8))
                and not self.attacked((1, 6), WHITE) and not
                self.attacked((1, 7), WHITE))

    def black_queenside_castling(self):
        """Return True if black queenside castling is possible."""
        return (self.castling[3] and self.empty((1, 5)) and self.empty((1, 4))
                and self.empty((1, 3)) and not self.attacked((1, 6), WHITE)
                and not self.attacked((1, 5), WHITE))

    def generate_moves(self):
        moves = TripleStepEnPassantPosition.generate_moves(self)
        # castling
        if self.player == WHITE:
            if self.white_kingside_castling():
                move = self.make_move((10, 6), (10, 8))
                move[10, 7] = white_rook
                move[10, 9] = empty
                moves.append(move)
            if self.white_queenside_castling():
                move = self.make_move((10, 6), (10, 4))
                move[10, 5] = white_rook
                move[10, 2] = empty
                moves.append(move)
        else:
            if self.black_kingside_castling():
                move = self.make_move((1, 6), (1, 8))
                move[1, 7] = black_rook
                move[1, 9] = empty
                moves.append(move)
            if self.black_queenside_castling():
                move = self.make_move((1, 6), (1, 4))
                move[1, 5] = black_rook
                move[1, 2] = empty
                moves.append(move)
        return moves

    def make_move(self, origin, target, promotion=None):
        move = TripleStepEnPassantPosition.make_move(self, origin, target)
        # update castling rights
        if origin == (10, 6) or origin == (10, 9) or target == (10, 9):
            move.castling[0] = False
        if origin == (10, 6) or origin == (10, 2) or target == (10, 2):
            move.castling[1] = False
        if origin == (1, 6) or origin == (1, 9) or target == (1, 9):
            move.castling[2] = False
        if origin == (1, 6) or origin == (1, 2) or target == (1, 2):
            move.castling[3] = False
        return move

    def white_kingside_castling(self):
        """Return True if white kingside castling is possible."""
        return (self.castling[0] and self.empty((10, 7))
                and self.empty((10, 8)) and not self.attacked((10, 6), BLACK)
                and not self.attacked((10, 7), BLACK))

    def white_queenside_castling(self):
        """Return True if white queenside castling is possible."""
        return (self.castling[1] and self.empty((10, 5))
                and self.empty((10, 4)) and self.empty((10, 3)) and not
                self.attacked((10, 6), BLACK) and not
                self.attacked((10, 5), BLACK))


white_champion = Champion(WHITE, "C")
black_champion = Champion(BLACK, "c")
white_wizard = Wizard(WHITE, "W")
black_wizard = Wizard(BLACK, "w")
white_pawn = OmegaPawn(WHITE, "P", (white_queen, white_bishop, white_knight,
                                    white_rook, white_champion, white_wizard),
                       9)
black_pawn = OmegaPawn(BLACK, "p", (black_queen, black_bishop, black_knight,
                                    black_rook, black_champion, black_wizard),
                       2)
position = OmegaPosition()
position[0, 0] = black_wizard
position[0, 11] = black_wizard
position[1, 1] = black_champion
position[1, 2] = black_rook
position[1, 3] = black_knight
position[1, 4] = black_bishop
position[1, 5] = black_queen
position[1, 6] = black_king
position[1, 7] = black_bishop
position[1, 8] = black_knight
position[1, 9] = black_rook
position[1, 10] = black_champion
position[2, 1] = black_pawn
position[2, 2] = black_pawn
position[2, 3] = black_pawn
position[2, 4] = black_pawn
position[2, 5] = black_pawn
position[2, 6] = black_pawn
position[2, 7] = black_pawn
position[2, 8] = black_pawn
position[2, 9] = black_pawn
position[2, 10] = black_pawn
position[9, 1] = white_pawn
position[9, 2] = white_pawn
position[9, 3] = white_pawn
position[9, 4] = white_pawn
position[9, 5] = white_pawn
position[9, 6] = white_pawn
position[9, 7] = white_pawn
position[9, 8] = white_pawn
position[9, 9] = white_pawn
position[9, 10] = white_pawn
position[10, 1] = white_champion
position[10, 2] = white_rook
position[10, 3] = white_knight
position[10, 4] = white_bishop
position[10, 5] = white_queen
position[10, 6] = white_king
position[10, 7] = white_bishop
position[10, 8] = white_knight
position[10, 9] = white_rook
position[10, 10] = white_champion
position[11, 0] = white_wizard
position[11, 11] = white_wizard
position.royal[WHITE] = 10, 6
position.royal[BLACK] = 1, 6
position.castling = [True, True, True, True]
if __name__ == "__main__":
    play(position, 10)
