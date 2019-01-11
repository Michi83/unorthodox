from random import choice
from threading import Thread


# A framework for implementing chess variants with a basic computer opponent
# good enough for test games.
#
# Tuples of two integers are used for board sizes, coordinates and offsets,
# i.e. changes in coordinates. The first integer is the rank, the second
# integer is the file. (0, 0) is white's upper left corner.
#
# For every piece type there should be one class and two instances thereof, one
# for white and one for black.


# Constants

WHITE = 1
NEUTRAL = 0
BLACK = -1
HUMAN = 1
COMPUTER = 2
RANDOM = 3
WIN = 1
DRAW = 0
LOSS = -1


# Piece types

class Piece:
    """Base class of all piece types.

    Subclasses should provide the following:
    value -- The piece's value in centipawns (a static field).
    generate_moves -- A method which generates all moves the piece can make.
    attacks -- Returns True if the piece attacks a particular square.
    """
    value = 0

    def __init__(self, player, symbol):
        """Initialize the piece.

        Parameters:
        player -- The piece's owner: WHITE, BLACK or NEUTRAL.
        symbol -- The piece's symbol (a string of at most two characters).
        """
        self.player = player
        self.symbol = symbol


class CannonRider(Piece):
    """Base class for piece that capture after jumping over a piece, e.g. the
    cannon in Xiangji.
    """

    def attacks(self, position, square, origin):
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            target = (
                target[0] + self.player * offset[0],
                target[1] + offset[1]
            )
            while position.empty(target):
                if target == square:
                    return True
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            if target == square:
                return True
        return False

    def generate_moves(self, position, origin):
        moves = []
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            target = (
                target[0] + self.player * offset[0],
                target[1] + offset[1]
            )
            while position.empty(target):
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            if position.capturable(target):
                move = position.make_move(origin, target)
                moves.append(move)
        return moves


class Leaper(Piece):
    """Leapers are pieces which move a certain number of ranks and files
    leaping over intervening pieces (e.g. the orthodox knight). This is their
    base class.
    """

    def attacks(self, position, square, origin):
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if target == square:
                return True
        return False

    def generate_moves(self, position, origin):
        moves = []
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if position.capturable_or_empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
        return moves


class LeaperRider(Piece):
    """Base class of compounds of leapers and riders."""

    def attacks(self, position, square, origin):
        # rider attacks
        for offset in self.rider_offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                if target == square:
                    return True
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1])
            if target == square:
                return True
        # leaper attacks
        for offset in self.leaper_offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if target == square:
                return True
        return False

    def generate_moves(self, position, origin):
        moves = []
        # rider moves
        for offset in self.rider_offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            if position.capturable(target):
                move = position.make_move(origin, target)
                moves.append(move)
        # leaper moves
        for offset in self.leaper_offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if position.capturable_or_empty(target):
                move = position.make_move(origin, target)
                moves.append(move)
        return moves


class Rider(Piece):
    """Riders are pieces which make multiple steps in one direction, e.g. the
    rook. This is their base class.
    """

    def attacks(self, position, square, origin):
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
                if target == square:
                    return True
                target = (
                    target[0] + self.player * offset[0],
                    target[1] + offset[1]
                )
            if target == square:
                return True
        return False

    def generate_moves(self, position, origin):
        moves = []
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            while position.empty(target):
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


class SingleStepPawn(Piece):
    """A pawn without an initial double step."""
    offsets = (-1, -1), (-1, 1)
    value = 100

    def __init__(self, player, symbol, promotions):
        Piece.__init__(self, player, symbol)
        self.promotions = promotions

    def attacks(self, position, square, origin):
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if target == square:
                return True
        return False

    def can_promote(self, position, square):
        return (self.player == WHITE and square[0] == 0 or self.player == BLACK
                and square[0] == position.size[0] - 1)

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
                else:
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
            else:
                moves.append(position.make_move(origin, target))
        return moves

    def generate_promotions(self, position, origin, target):
        moves = []
        for promotion in self.promotions:
            move = position.make_move(origin, target)
            move[target] = promotion
            move.notation += promotion.symbol
            moves.append(move)
        return moves


class King(Leaper):
    """The orthodox king."""
    value = 375
    offsets = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1),
        (0, 1), (1, -1), (1, 0), (1, 1),
    )


class Knight(Leaper):
    """The orthodox knight."""
    value = 300
    offsets = (
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1),
    )


class Bishop(Rider):
    """The orthodox bishop."""
    value = 340
    offsets = (-1, -1), (-1, 1), (1, -1), (1, 1)


class Queen(Rider):
    """The orthodox queen."""
    value = 800
    offsets = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1),
        (0, 1), (1, -1), (1, 0), (1, 1),
    )


class Rook(Rider):
    """The orthodox rook."""
    value = 465
    offsets = (-1, 0), (0, -1), (0, 1), (1, 0)


class DoubleStepPawn(SingleStepPawn):
    """A pawn with an initial double step."""

    def __init__(self, player, symbol, promotions, initial_rank):
        SingleStepPawn.__init__(self, player, symbol, promotions)
        self.initial_rank = initial_rank

    def generate_moves(self, position, origin):
        moves = SingleStepPawn.generate_moves(self, position, origin)
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


class TripleStepPawn(DoubleStepPawn):
    """A pawn with an initial triple step."""

    def generate_moves(self, position, origin):
        moves = DoubleStepPawn.generate_moves(self, position, origin)
        # en passant
        for offset in self.offsets:
            target = (
                origin[0] + self.player * offset[0],
                origin[1] + offset[1]
            )
            if target == position.en_passant2:
                move = position.make_move(origin, target)
                # coordinates of the captured pawn
                square = (
                    target[0] + 2 * self.player,
                    target[1]
                )
                move[square] = empty
        # triple step
        if origin[0] == self.initial_rank:
            # first intermediate square
            square1 = (
                origin[0] - self.player,
                origin[1]
            )
            if position.empty(square1):
                # second intermediate square
                square2 = (
                    square1[0] - self.player,
                    square1[1]
                )
                if position.empty(square2):
                    target = (
                        square2[0] - self.player,
                        square2[1]
                    )
                    if position.empty(target):
                        move = position.make_move(origin, target)
                        move.en_passant = square2
                        move.en_passant2 = square1
                        moves.append(move)
        return moves


# Predefined pieces

empty = Piece(NEUTRAL, ".")  # pseudo-piece for empty squares
lava = Piece(NEUTRAL, " ")  # pseudo-piece for forbidden squares
white_king = King(WHITE, "K")
black_king = King(BLACK, "k")
white_queen = Queen(WHITE, "Q")
black_queen = Queen(BLACK, "q")
white_bishop = Bishop(WHITE, "B")
black_bishop = Bishop(BLACK, "b")
white_knight = Knight(WHITE, "N")
black_knight = Knight(BLACK, "n")
white_rook = Rook(WHITE, "R")
black_rook = Rook(BLACK, "r")


# Positions

class Position:
    """The base class of all positions."""

    def __init__(self, **kwargs):
        """Create a new empty position or copy an existing one."""
        if "copy" in kwargs:
            copy = kwargs["copy"]
            self.board = [[j for j in i] for i in copy.board]
            self.player = copy.player
            self.royal = dict(copy.royal)
            self.size = copy.size
        else:
            size = kwargs["size"]
            self.board = [[empty for j in range(size[1])] for i in
                          range(size[0])]
            self.player = WHITE
            self.royal = {WHITE: None, BLACK: None}
            self.size = size

    def __getitem__(self, square):
        """Get a piece. Returns lava for coordinates out of bounds."""
        if (square[0] >= 0 and square[0] < self.size[0] and square[1] >= 0
                and square[1] < self.size[1]):
            return self.board[square[0]][square[1]]
        else:
            return lava

    def __setitem__(self, square, piece):
        """Set a piece."""
        self.board[square[0]][square[1]] = piece

    def __str__(self):
        """Draw an ASCII art diagram of the position."""
        buffer = []
        for i in range(self.size[0]):
            buffer.append("%2d " % (self.size[0] - i))
            for j in range(self.size[1]):
                buffer.append("%2s " % self[i, j].symbol)
            buffer.append("\n")
        buffer.append("   ")
        for i in range(self.size[1]):
            buffer.append("%2s " % chr(97 + i))
        buffer.append("\n")
        return "".join(buffer)

    def attacked(self, square, attacker):
        """Return True if a particular square is attacked by a player."""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                origin = i, j
                if (self[origin].player == attacker
                        and self[origin].attacks(self, square, origin)):
                    return True
        return False

    def capturable(self, square):
        """Return True if a piece belongs to the moving player's opponent."""
        return self[square].player == -self.player

    def capturable_or_empty(self, square):
        return self.capturable(square) or self.empty(square)

    def check(self, defender):
        """Return True if the defender's king is in check."""
        return self.attacked(self.royal[defender], -defender)

    def empty(self, square):
        """Return True if a square is empty."""
        return self[square] is empty

    def evaluate(self):
        """Evaluate the position in centipawns."""
        score = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                square = i, j
                score += self[square].player * self[square].value
        return self.player * score

    def game_over(self):
        """Return True if there are no legal moves."""
        return len(self.generate_legal_moves()) == 0

    def generate_legal_moves(self):
        """Generate a list of legal moves."""
        legal_moves = []
        for move in self.generate_moves():
            if move.legal():
                legal_moves.append(move)
        return legal_moves

    def generate_moves(self):
        """Generate a list of pseudo-legal moves."""
        moves = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                origin = i, j
                if self.movable(origin):
                    moves += self[origin].generate_moves(self, origin)
        return moves

    def legal(self):
        """Return True if the last move did not leave the king in check."""
        return (self.player == WHITE and not self.check(BLACK)
                or self.player == BLACK and not self.check(WHITE))

    def make_move(self, origin, target):
        """Copy the position and move a piece on the copy.

        Parameters:
        origin -- The square of origin.
        target -- The target square.
        """
        # copy position
        move = type(self)(copy=self)
        # move piece
        move[target] = move[origin]
        move[origin] = empty
        # update royal positions
        if origin == move.royal[move.player]:
            move.royal[move.player] = target
        # switch player
        move.player *= -1
        # set notation
        move.notation = "%s%d%s%d" % (chr(origin[1] + 97), move.size[0]
                                      - origin[0], chr(target[1] + 97),
                                      move.size[0] - target[0])
        return move

    def movable(self, square):
        """Return True if a piece belongs to the moving player."""
        return self[square].player == self.player


class EnPassantPosition(Position):
    def __init__(self, **kwargs):
        Position.__init__(self, **kwargs)
        self.en_passant = None


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


class OrthodoxPosition(EnPassantPosition):
    """An 8x8 position with support for castling."""

    def __init__(self, **kwargs):
        if "copy" in kwargs:
            EnPassantPosition.__init__(self, **kwargs)
            copy = kwargs["copy"]
            self.castling = list(copy.castling)  # copy castling rights
        else:
            EnPassantPosition.__init__(self, size=(8, 8))
            self.castling = [False, False, False, False]

    def black_kingside_castling(self):
        """Return True if black kingside castling is possible."""
        return (self.castling[2] and self.empty((0, 5)) and self.empty((0, 6))
                and not self.attacked((0, 4), WHITE) and not
                self.attacked((0, 5), WHITE))

    def black_queenside_castling(self):
        """Return True if black queenside castling is possible."""
        return (self.castling[3] and self.empty((0, 3)) and self.empty((0, 2))
                and self.empty((0, 1)) and not self.attacked((0, 4), WHITE)
                and not self.attacked((0, 3), WHITE))

    def generate_moves(self):
        moves = EnPassantPosition.generate_moves(self)
        # castling
        if self.player == WHITE:
            if self.white_kingside_castling():
                move = self.make_move((7, 4), (7, 6))
                move[7, 5] = white_rook
                move[7, 7] = empty
                moves.append(move)
            if self.white_queenside_castling():
                move = self.make_move((7, 4), (7, 2))
                move[7, 3] = white_rook
                move[7, 0] = empty
                moves.append(move)
        else:
            if self.black_kingside_castling():
                move = self.make_move((0, 4), (0, 6))
                move[0, 5] = black_rook
                move[0, 7] = empty
                moves.append(move)
            if self.black_queenside_castling():
                move = self.make_move((0, 4), (0, 2))
                move[0, 3] = black_rook
                move[0, 0] = empty
                moves.append(move)
        return moves

    def make_move(self, origin, target):
        move = EnPassantPosition.make_move(self, origin, target)
        # update castling rights
        if origin == (7, 4) or origin == (7, 7) or target == (7, 7):
            move.castling[0] = False
        if origin == (7, 4) or origin == (7, 0) or target == (7, 0):
            move.castling[1] = False
        if origin == (0, 4) or origin == (0, 7) or target == (0, 7):
            move.castling[2] = False
        if origin == (0, 4) or origin == (0, 0) or target == (0, 0):
            move.castling[3] = False
        return move

    def white_kingside_castling(self):
        """Return True if white kingside castling is possible."""
        return (self.castling[0] and self.empty((7, 5)) and self.empty((7, 6))
                and not self.attacked((7, 4), BLACK) and not
                self.attacked((7, 5), BLACK))

    def white_queenside_castling(self):
        """Return True if white queenside castling is possible."""
        return (self.castling[1] and self.empty((7, 3)) and self.empty((7, 2))
                and self.empty((7, 1)) and not self.attacked((7, 4), BLACK)
                and not self.attacked((7, 3), BLACK))


class TripleStepEnPassantPosition(EnPassantPosition):
    def __init__(self, **kwargs):
        EnPassantPosition.__init__(self, **kwargs)
        self.en_passant2 = None


# AI

best_move = None
killer_moves = None
nodes = None
score = None
stalemate_rule = None
stop = None


def alpha_beta(position, depth, alpha=-20000, beta=20000):
    """Perform an alpha-beta search on a position.

    Parameters:
    position -- A position.
    depth -- The search depth.
    alpha -- The lower limit of the alpha-beta window.
    beta -- The upper limit of the alpha-beta window.
    """
    global nodes
    if stop:
        raise TimeoutError()
    nodes += 1
    if depth == 0:
        return position.evaluate(), None
    moves = position.generate_legal_moves()
    # killer move presorting
    moves.sort(key=lambda move: move.notation != killer_moves[depth - 1])
    if len(moves) == 0:
        if position.check(position.player):
            return -20000, None
        else:
            return stalemate_rule * 20000, None
    score = -25000
    for move in moves:
        subscore = -alpha_beta(move, depth - 1, -beta, -alpha)[0]
        if subscore > score:
            score = subscore
            best_moves = [move]
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    killer_moves[depth - 1] = best_move.notation
                    break
        elif subscore == score:
            best_moves.append(move)
    return score, choice(best_moves)


def iterative_deepening(position):
    """Analyze a position with increasing depth.

    Returns None but overwrites global score and best_move.
    """
    try:
        global best_move, killer_moves, nodes, score
        print("depth   nodes   score   move")
        depth = 1
        killer_moves = []
        while True:
            killer_moves = [None] + killer_moves
            nodes = 0
            score, best_move = alpha_beta(position, depth)
            print("%7d %7d %7d %s" % (depth, nodes, score, best_move.notation))
            if abs(score) == 20000:
                return
            depth += 1
    except TimeoutError:
        return


def play(position, time_limit, white=HUMAN, black=COMPUTER, stalemate=DRAW):
    """Play a game of chess.

    Parameters:
    position -- A position.
    time_limit -- Time limit per move in seconds.
    white -- HUMAN or COMPUTER (default HUMAN).
    black -- HUMAN or COMPUTER (default COMPUTER).
    """
    global stalemate_rule, stop
    players = {WHITE: white, BLACK: black}
    stalemate_rule = stalemate
    count = 1
    print(position)
    while not position.game_over():
        # human move
        if players[position.player] == HUMAN:
            moves = position.generate_legal_moves()
            legal = False
            while True:
                if position.player == WHITE:
                    notation = input("%d. " % count)
                else:
                    notation = input("%d... " % count)
                for move in moves:
                    if move.notation == notation:
                        legal = True
                        position = move
                        break
                if legal:
                    break
        # computer move
        elif players[position.player] == COMPUTER:
            stop = False
            thread = Thread(target=iterative_deepening, args=(position,),
                            daemon=True)
            thread.start()
            thread.join(time_limit)
            stop = True
            print()
            if position.player == WHITE:
                print("%d. %s" % (count, best_move.notation))
            else:
                print("%d... %s" % (count, best_move.notation))
            position = best_move
        # random move
        elif players[position.player] == RANDOM:
            move = choice(position.generate_legal_moves())
            if position.player == WHITE:
                print("%d. %s" % (count, move.notation))
            else:
                print("%d... %s" % (count, move.notation))
            position = move
        print()
        print(position)
        if position.player == WHITE:
            count += 1
