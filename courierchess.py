from unorthodox import (BLACK, Bishop, King, Leaper, Position, SingleStepPawn,
                        WHITE, black_king, black_knight, black_rook, play,
                        white_king, white_knight, white_rook)
from shatranj import Elephant, Ferz


class Schleich(Leaper):
    value = 200
    offsets = (-1, 0), (0, -1), (0, 1), (1, 0)


white_queen = Ferz(WHITE, "Q")
black_queen = Ferz(BLACK, "q")
white_man = King(WHITE, "M")
black_man = King(BLACK, "m")
white_schleich = Schleich(WHITE, "S")
black_schleich = Schleich(BLACK, "s")
white_courier = Bishop(WHITE, "C")
black_courier = Bishop(BLACK, "c")
white_bishop = Elephant(WHITE, "B")
black_bishop = Elephant(BLACK, "b")
white_pawn = SingleStepPawn(WHITE, "P", (white_queen,))
black_pawn = SingleStepPawn(BLACK, "p", (black_queen,))
position = Position(size=(8, 12))
position[0, 0] = black_rook
position[0, 1] = black_knight
position[0, 2] = black_bishop
position[0, 3] = black_courier
position[0, 4] = black_man
position[0, 5] = black_king
position[0, 7] = black_schleich
position[0, 8] = black_courier
position[0, 9] = black_bishop
position[0, 10] = black_knight
position[0, 11] = black_rook
position[1, 1] = black_pawn
position[1, 2] = black_pawn
position[1, 3] = black_pawn
position[1, 4] = black_pawn
position[1, 5] = black_pawn
position[1, 7] = black_pawn
position[1, 8] = black_pawn
position[1, 9] = black_pawn
position[1, 10] = black_pawn
position[2, 6] = black_queen
position[3, 0] = black_pawn
position[3, 6] = black_pawn
position[3, 11] = black_pawn
position[4, 0] = white_pawn
position[4, 6] = white_pawn
position[4, 11] = white_pawn
position[5, 6] = white_queen
position[6, 1] = white_pawn
position[6, 2] = white_pawn
position[6, 3] = white_pawn
position[6, 4] = white_pawn
position[6, 5] = white_pawn
position[6, 7] = white_pawn
position[6, 8] = white_pawn
position[6, 9] = white_pawn
position[6, 10] = white_pawn
position[7, 0] = white_rook
position[7, 1] = white_knight
position[7, 2] = white_bishop
position[7, 3] = white_courier
position[7, 4] = white_man
position[7, 5] = white_king
position[7, 7] = white_schleich
position[7, 8] = white_courier
position[7, 9] = white_bishop
position[7, 10] = white_knight
position[7, 11] = white_rook
position.royal[WHITE] = 7, 5
position.royal[BLACK] = 0, 5
if __name__ == "__main__":
    play(position, 10)
