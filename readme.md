
# Modified Chess

This chess console game was developed as part of coursework. It consists of a modified version in which the following configuration applies:
- only the **knight and king** pieces are involved,
- the board size is `S x S`, where `S`  is a number between `3` and `26`,
- the columns are designated by small letter characters from `a` to `z` and the rows by numbers from `1` to `26`. The leftmost column is `a` and the bottom row is `1`.
- each side plays with any number of knights in any positions (as long as they fit the board),
- each side has exactly one king,
- white starts the game.

In terms of moves the following rules apply:
- the pieces move like in usual chess:
  - A knight may move two squares vertically and one square horizontally or two squares horizontally and one square vertically. It can jump over other pieces.
  - The king moves one square in any direction, including diagonal. 
- to indicate the moves, strings of the form `crCR` are used where `cr` indicates the column and row of the origin of the move, and `CR` indicates the row and column of the destination of the move. 
- as a result of any move, the piece that is moved either occupies a previously empty board location, or captures the other side's piece.
- A piece of side X cannot move to a location occupied by a piece of side X.
- A piece of side X cannot make a move, if the configuration resulting from this move is a check for X. **Check** for side X is a configuration of the board when X's king can be captured by a piece of the other side Y (in one move).

Every game results in:
- a win of side X, meaning the game reaches a configuration which is a checkmate for the opposite side. **Checkmate** for side X is a configuration of the board when the king of a side X is in *check* and there is no move available for X to eliminate the *check* situation.
- stalemate for side X. **Stalemate** for side X is a configuration of the board when the side X is *not in check* and there is no move available for X.
- runs infinitely. 
