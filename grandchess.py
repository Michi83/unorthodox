from unorthodox import (BLACK, DoubleStepPawn, EnPassantPosition, WHITE,
                        black_bishop, black_king, black_knight, black_queen,
                        black_rook, empty, play, white_bishop, white_king,
                        white_knight, white_queen, white_rook)
from capablancachess import Chancellor, Archbishop


class GrandChessPawn(DoubleStepPawn):
    """A pawn with support for the Grand Chess promotion rule."""

    def __init__(self, player, symbol, initial_rank):
        DoubleStepPawn.__init__(self, player, symbol, None, initial_rank)

    def can_promote(self, position, target):
        return (self.player == WHITE and target[0] <= 2 or self.player == BLACK
                and target[0] >= 7)

    def generate_moves(self, position, origin):
        moves = []
        # captures
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if position.capturable(target):
                # promotions
                if self.can_promote(position, target):
                    moves += self.generate_promotions(position, origin, target)
                # non-promotions
                if not self.must_promote(position, target):
                    move = position.make_move(origin, target)
                    moves.append(move)
        # non captures
        target = (
            origin[0] - self.player,
            origin[1]
        )
        if position.empty(target):
            # promotions
            if self.can_promote(position, target):
                moves += self.generate_promotions(position, origin, target)
            # non-promotions
            if not self.must_promote(position, target):
                moves.append(position.make_move(origin, target))
        # en passant
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if target == position.en_passant:
                move = position.make_move(origin, target)
                # coordinates of the captured pawn
                square = (
                    target[0] + self.player,
                    target[1]
                )
                move[square] = empty
        # double step
        if origin[0] == self.initial_rank:
            # the intermediate square
            square = (
                origin[0] - self.player,
                origin[1]
            )
            if position.empty(square):
                target = (
                    square[0] - self.player,
                    square[1]
                )
                if position.empty(target):
                    move = position.make_move(origin, target)
                    move.en_passant = square
                    moves.append(move)
        return moves

    def generate_promotions(self, position, origin, target):
        moves = []
        for promotion in position.promotions[self.player]:
            if position.promotions[self.player][promotion] > 0:
                move = position.make_move(origin, target)
                move[target] = promotion
                move.promotions[self.player][promotion] -= 1
                move.notation += promotion.symbol
                moves.append(move)
        return moves

    def must_promote(self, position, target):
        return (self.player == WHITE and target[0] == 0 or self.player == BLACK
                and target[0] == 9)


class GrandChessPosition(EnPassantPosition):
    """A position with support for the Grand Chess promotion rule."""

    def __init__(self, **kwargs):
        if "copy" in kwargs:
            EnPassantPosition.__init__(self, **kwargs)
            copy = kwargs["copy"]
            self.promotions = {
                WHITE: dict(copy.promotions[WHITE]),
                BLACK: dict(copy.promotions[BLACK])
            }
        else:
            EnPassantPosition.__init__(self, size=(10, 10))
            self.promotions = {
                WHITE: {
                    white_queen: 0,
                    white_marshal: 0,
                    white_cardinal: 0,
                    white_bishop: 0,
                    white_knight: 0,
                    white_rook: 0
                },
                BLACK: {
                    black_queen: 0,
                    black_marshal: 0,
                    black_cardinal: 0,
                    black_bishop: 0,
                    black_knight: 0,
                    black_rook: 0
                }
            }

    def make_move(self, origin, target):
        move = EnPassantPosition.make_move(self, origin, target)
        # update tally of captured pieces
        capture = self[target]
        if capture.player in move.promotions:
            if capture in move.promotions[capture.player]:
                move.promotions[capture.player][capture] += 1
        return move


white_marshal = Chancellor(WHITE, "M")
black_marshal = Chancellor(BLACK, "m")
white_cardinal = Archbishop(WHITE, "C")
black_cardinal = Archbishop(BLACK, "c")
white_pawn = GrandChessPawn(WHITE, "P", 7)
black_pawn = GrandChessPawn(BLACK, "p", 2)
position = GrandChessPosition()
position[0, 0] = black_rook
position[0, 9] = black_rook
position[1, 1] = black_knight
position[1, 2] = black_bishop
position[1, 3] = black_queen
position[1, 4] = black_king
position[1, 5] = black_marshal
position[1, 6] = black_cardinal
position[1, 7] = black_bishop
position[1, 8] = black_knight
position[2, 0] = black_pawn
position[2, 1] = black_pawn
position[2, 2] = black_pawn
position[2, 3] = black_pawn
position[2, 4] = black_pawn
position[2, 5] = black_pawn
position[2, 6] = black_pawn
position[2, 7] = black_pawn
position[2, 8] = black_pawn
position[2, 9] = black_pawn
position[7, 0] = white_pawn
position[7, 1] = white_pawn
position[7, 2] = white_pawn
position[7, 3] = white_pawn
position[7, 4] = white_pawn
position[7, 5] = white_pawn
position[7, 6] = white_pawn
position[7, 7] = white_pawn
position[7, 8] = white_pawn
position[7, 9] = white_pawn
position[8, 1] = white_knight
position[8, 2] = white_bishop
position[8, 3] = white_queen
position[8, 4] = white_king
position[8, 5] = white_marshal
position[8, 6] = white_cardinal
position[8, 7] = white_bishop
position[8, 8] = white_knight
position[9, 0] = white_rook
position[9, 9] = white_rook
position.royal[WHITE] = 8, 4
position.royal[BLACK] = 1, 4
if __name__ == "__main__":
    play(position, 10)
