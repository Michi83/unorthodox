# Unorthodox

Unorthodox is a framework for implementing chess variants and test-playing them against a basic computer opponent.

## How to play

Start a game from the command line, e.g.

```
python3 orthodoxchess.py
```

Input moves by specifying their origin and target squares, e.g. "e2e4".

* For pawn promotions add the desired piece type, e.g. "e2e4Q".
* For castling input the king's move, e.g. "e1g1".

## How to implement variants

Implementing a variant is generally a five-step process.

1. Import or create a board.
2. Import or create some pieces.
3. Put pieces on the board.
4. Designate royal pieces that must be checkmated.
5. Call the `play` function.

See the variants already implemented for examples.

Tuples of two integers are used for board sizes, coordinates and offsets, i.e. changes in coordinates. The first integer is the rank, the second integer is the file. (0, 0) is white's upper left corner.
