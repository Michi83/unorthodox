from unorthodox import (BLACK, King, Leaper, OrthodoxPosition, Queen, WHITE,
                        black_bishop, black_king, black_knight, black_rook,
                        play, white_bishop, white_king, white_knight,
                        white_rook)


class SuperFarmerPosition(OrthodoxPosition):
    def __init__(self, **kwargs):
        OrthodoxPosition.__init__(self, **kwargs)
        if "copy" in kwargs:
            self.queens_moved = dict(kwargs["copy"].queens_moved)
        else:
            self.queens_moved = {WHITE: False, BLACK: False}

    def make_move(self, origin, target):
        move = OrthodoxPosition.make_move(self, origin, target)
        if origin == (7, 3) or origin == (0, 3):
            move.queens_moved[self.player] = True
        return move


class SuperFarmerJumpingQueen(Leaper):
    offsets = (
        (-2, -2), (-2, 0), (-2, 2), (0, -2),
        (0, 2), (2, -2), (2, 0), (2, 2),
    )


class SuperFarmerQueen(King):
    value = 375

    def attacks(self, position, square, origin):
        if King.attacks(self, position, square, origin):
            return True
        if not position.queens_moved[position.player]:
            if SuperFarmerJumpingQueen.attacks(self, position, square, origin):
                return True
        return False

    def generate_moves(self, position, origin):
        # king-like moves
        moves = King.generate_moves(self, position, origin)
        # jumps
        if not position.queens_moved[position.player]:
            moves += SuperFarmerJumpingQueen.generate_moves(self, position,
                                                            origin)
        return moves


white_queen = SuperFarmerQueen(WHITE, "Q")
black_queen = SuperFarmerQueen(BLACK, "q")
white_pawn = Queen(WHITE, "P")
black_pawn = Queen(BLACK, "p")
position = SuperFarmerPosition()
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
    print("Super Farmer Chess by @krasmanalderey on Twitter")
    print("Rules: https://pastebin.com/Ujg0XgPk")
    play(position, 10)
