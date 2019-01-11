from unorthodox import (BLACK, Bishop, CannonRider, King, Queen, Rider, WHITE,
                        black_knight, black_rook, play, white_knight,
                        white_rook)
from grandchess import GrandChessPawn, GrandChessPosition


class CaissaBritanniaQueen(Queen):
    def generate_moves(self, position, origin):
        moves = []
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                if position.attacked(target, -self.player):
                    break
                move = position.make_move(origin, target)
                moves.append(move)
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            if position.capturable(target):
                move = position.make_move(origin, target)
                moves.append(move)
        return moves


class CaissaBritanniaKing(King):
    value = 675

    def generate_moves(self, position, origin):
        moves = King.generate_moves(self, position, origin)
        for offset in self.offsets:
            target = (
                origin[0] + 2 * self.player * offset[0],
                origin[1] + 2 * offset[1]
            )
            while position.empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
        return moves


class Lion(CannonRider):
    value = 665
    offsets = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1),
        (0, 1), (1, -1), (1, 0), (1, 1),
    )


class Unicorn(Rider):
    value = 795
    offsets = (
        (-2, -1), (-2, 1), (-1, -2), (-1, -1), (-1, 1), (-1, 2),
        (1, -2), (1, -1), (1, 1), (1, 2), (2, -1), (2, 1)
    )


class Dragon(Rider):
    value = 455
    offsets = (
        (-2, -2), (-2, 0), (-2, 2), (0, -2),
        (0, 2), (2, -2), (2, 0), (2, 2)
    )


class CaissaBritanniaBishop(Bishop):
    value = 480
    non_capture_offsets = (-1, 0), (0, -1), (0, 1), (1, 0)

    def generate_moves(self, position, origin):
        moves = Bishop.generate_moves(self, position, origin)
        for offset in self.non_capture_offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if position.empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
        return moves


class CaissaBritanniaPawn(GrandChessPawn):
    def can_promote(self, position, target):
        return self.must_promote(position, target)


class CaissaBritanniaPosition(GrandChessPosition):
    def __init__(self, **kwargs):
        if "copy" in kwargs:
            GrandChessPosition.__init__(self, **kwargs)
        else:
            GrandChessPosition.__init__(self, size=(10, 10))
            self.promotions = {
                WHITE: {
                    white_king: 0,
                    white_lion: 0,
                    white_unicorn: 0,
                    white_dragon: 0,
                    white_rook: 0,
                    white_bishop: 0,
                    white_knight: 10,
                },
                BLACK: {
                    black_king: 0,
                    black_lion: 0,
                    black_unicorn: 0,
                    black_dragon: 0,
                    black_rook: 0,
                    black_bishop: 0,
                    black_knight: 10,
                }
            }


white_queen = CaissaBritanniaQueen(WHITE, "Q")
black_queen = CaissaBritanniaQueen(BLACK, "q")
white_king = CaissaBritanniaKing(WHITE, "K")
black_king = CaissaBritanniaKing(BLACK, "k")
white_lion = Lion(WHITE, "L")
black_lion = Lion(BLACK, "l")
white_unicorn = Unicorn(WHITE, "U")
black_unicorn = Unicorn(BLACK, "u")
white_dragon = Dragon(WHITE, "D")
black_dragon = Dragon(BLACK, "d")
white_bishop = CaissaBritanniaBishop(WHITE, "B")
black_bishop = CaissaBritanniaBishop(BLACK, "b")
white_pawn = CaissaBritanniaPawn(WHITE, "P", 7)
black_pawn = CaissaBritanniaPawn(BLACK, "p", 2)
position = CaissaBritanniaPosition()
position[0, 0] = black_dragon
position[0, 1] = black_rook
position[0, 2] = black_unicorn
position[0, 3] = black_bishop
position[0, 4] = black_queen
position[0, 5] = black_king
position[0, 6] = black_bishop
position[0, 7] = black_unicorn
position[0, 8] = black_rook
position[0, 9] = black_dragon
position[1, 1] = black_lion
position[1, 8] = black_lion
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
position[8, 1] = white_lion
position[8, 8] = white_lion
position[9, 0] = white_dragon
position[9, 1] = white_rook
position[9, 2] = white_unicorn
position[9, 3] = white_bishop
position[9, 4] = white_queen
position[9, 5] = white_king
position[9, 6] = white_bishop
position[9, 7] = white_unicorn
position[9, 8] = white_rook
position[9, 9] = white_dragon
position.royal[WHITE] = 9, 4
position.royal[BLACK] = 0, 4
if __name__ == "__main__":
    print("Caïssa Britannia by Fergus Duniho")
    print("Rules: https://www.chessvariants.com/large.dir/british.html")
    play(position, 10)
