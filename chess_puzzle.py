from typing import Union
import copy
import random
import os
import sys


def location2index(loc: str) -> tuple[int, int]:
    """Converts chess location to corresponding x and y coordinates."""
    x = ord(loc[1]) - 96
    y = int(loc[2:])
    return x, y


def index2location(x: int, y: int) -> str:
    """converts a pair of coordinates to corresponding location"""
    a = chr(x + 96)
    b = str(y)
    return a + b


class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black
    type: str  # 'K' for King and 'N' for Knight

    def __init__(self, pos_X: int, pos_Y: int, side_: bool, type_: str):
        """sets initial values"""
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_
        self.type = type_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    """checks if there is piece at coordinates pox_X, pos_Y of board B"""
    for piece in B[1]:
        if pos_X == piece.pos_x and pos_Y == piece.pos_y:
            return True
    return False


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    """
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    """
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece


class Knight(Piece):
    type: str = 'N'

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_X, pos_Y, side_, self.type)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        """
        # rule 1
        if (pos_X == self.pos_x - 1 and pos_Y == self.pos_y - 2) or (
                pos_X == self.pos_x - 1 and pos_Y == self.pos_y + 2) or (
                pos_X == self.pos_x + 1 and pos_Y == self.pos_y - 2) or (
                pos_X == self.pos_x + 1 and pos_Y == self.pos_y + 2) or (
                pos_X == self.pos_x - 2 and pos_Y == self.pos_y - 1) or (
                pos_X == self.pos_x - 2 and pos_Y == self.pos_y + 1) or (
                pos_X == self.pos_x + 2 and pos_Y == self.pos_y - 1) or (
                pos_X == self.pos_x + 2 and pos_Y == self.pos_y + 1):

            # rule 3
            if is_piece_at(pos_X, pos_Y, B):
                piece_at_destination = piece_at(pos_X, pos_Y, B)
                if piece_at_destination.side == self.side:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        """
        # rule 1 and rule 3
        if self.can_reach(pos_X, pos_Y, B):
            B2 = copy.deepcopy(B)

            # capture destination piece
            if is_piece_at(pos_X, pos_Y, B2):
                piece_at_destination = piece_at(pos_X, pos_Y, B2)
                B2[1].remove(piece_at_destination)

            # change location of origin piece
            for piece in B2[1]:
                if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.type == self.type and piece.side == self.side:
                    piece.pos_x = pos_X
                    piece.pos_y = pos_Y
                    break

            # is in check
            if is_check(self.side, B2):
                return False
            else:
                return True
        else:
            return False

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        """
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B, assumes this move is valid according to chess rules
        """
        for piece in B[1]:
            # capture
            if piece.pos_x == pos_X and piece.pos_y == pos_Y:
                B[1].remove(piece)

            # move from location
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y:
                B[1].remove(piece)

        # move to location
        B[1].append(piece2type(Piece(pos_X, pos_Y, self.side, self.type)))
        return B


class King(Piece):
    type: str = 'K'

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_X, pos_Y, side_, self.type)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3] """
        # rule 1
        if (pos_X == self.pos_x - 1 and pos_Y == self.pos_y) or (
                pos_X == self.pos_x - 1 and pos_Y == self.pos_y - 1) or (
                pos_X == self.pos_x - 1 and pos_Y == self.pos_y + 1) or (
                pos_X == self.pos_x + 1 and pos_Y == self.pos_y) or (
                pos_X == self.pos_x + 1 and pos_Y == self.pos_y - 1) or (
                pos_X == self.pos_x + 1 and pos_Y == self.pos_y + 1) or (
                pos_X == self.pos_x and pos_Y == self.pos_y - 1) or (
                pos_X == self.pos_x and pos_Y == self.pos_y + 1):
            # rule 3
            if is_piece_at(pos_X, pos_Y, B):
                piece_at_destination = piece_at(pos_X, pos_Y, B)
                if piece_at_destination.side == self.side:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules"""
        # rule 1 and rule 3
        if self.can_reach(pos_X, pos_Y, B):
            B2 = copy.deepcopy(B)

            # capture destination piece
            if is_piece_at(pos_X, pos_Y, B2):
                piece_at_destination = piece_at(pos_X, pos_Y, B2)
                B2[1].remove(piece_at_destination)

            # change location of origin piece
            for piece in B2[1]:
                if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.type == self.type and piece.side == self.side:
                    piece.pos_x = pos_X
                    piece.pos_y = pos_Y
                    break

            # is in check
            if is_check(self.side, B2):
                return False
            else:
                return True
        else:
            return False

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        """
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B, assumes this move is valid according to chess rules
        """
        for piece in B[1]:
            # capture
            if piece.pos_x == pos_X and piece.pos_y == pos_Y:
                B[1].remove(piece)

            # move from location
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y:
                B[1].remove(piece)

        # move to location
        B[1].append(piece2type(Piece(pos_X, pos_Y, self.side, self.type)))
        return B


def is_check(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is in check for side - if an enemy can reach the side's king then side is in check

    Hint: use can_reach
    """
    enemy_pieces = []
    for piece in B[1]:
        if piece.side != side:
            enemy_pieces.append(piece)
        if piece.side == side and piece.type == 'K':
            side_king = piece
    for enemy_piece in enemy_pieces:
        if piece2type(enemy_piece).can_reach(side_king.pos_x, side_king.pos_y, B):
            return True
    return False


def is_checkmate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is checkmate for side - if side is in check and cannot move the king to a location the enemy cannot reach then side is in checkmate

    Hints:
    - use is_check
    - use can_reach
    """
    if is_check(side, B):
        enemy_pieces = []
        all_locations = []
        checkmate = True
        for piece in B[1]:
            if piece.side != side:
                enemy_pieces.append(piece)
            if piece.side == side and piece.type == 'K':
                side_king = piece

        for row in range(B[0], 0, -1):
            for column in range(1, B[0] + 1):
                all_locations.append((column, row))

        for location in all_locations:
            if piece2type(side_king).can_reach(location[0], location[1], B):
                checkmate = False
                for enemy_piece in enemy_pieces:
                    if piece2type(enemy_piece).can_reach(location[0], location[1], B):
                        checkmate = True
                        break
        return checkmate
    else:
        return False


def is_stalemate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is stalemate for side - if side is not in check but there is no available move then side is in stalemate

    Hints:
    - use is_check
    - use can_move_to
    """
    if is_check(side, B) is False:
        pieces = []
        locations = []
        for piece in B[1]:
            if piece.side == side:
                pieces.append(piece)

        for row in range(B[0], 0, -1):
            for column in range(1, B[0] + 1):
                locations.append((column, row))

        for location in locations:
            for piece in pieces:
                if piece.can_move_to(location[0], location[1], B):
                    return False
        return True
    else:
        return False


def validate_locations(locations: str) -> bool:
    """checks if a locations line in a file is of a valid format according to:
        - String like Xcr where X is either K or N (King or kNight) and cr is the columns and row numbers
        - Only one king of each colour
        - Only one piece for location
        - Each location is within s*s"""

    locations_list = locations.split(',')
    king = 0
    for location in locations_list:
        location = location.strip()
        # syntax
        if (location[0] == 'N' or location[0] == 'K') and location[1].isalpha() and location[1].islower() and location[
                                                                                                              2:].isnumeric() and 0 < int(
                location[2:]) < 26:
            # only one king
            if location[0] == 'K':
                king += 1
                if king != 1:
                    return False
        else:
            return False

    # only one piece for location - no duplicates
    if len(locations_list) != len(set(locations_list)):
        return False

    return True


def validate_board(filename: str) -> bool:
    """
    validates board configuration:
        - First line: number representing the size of the board
        - Second line: piece locations of white pieces separated by ,
        - Third line: piece locations of black pieces separated by ,
        - There needs to be 3 lines
    """

    # handle empty file
    if os.stat(filename).st_size == 0:
        return False

    file = open(filename, 'r')

    # 1st line - size
    board_size = file.readline().replace("\n", "")

    if board_size.isnumeric() and 3 <= int(board_size) < 26:
        # 2nd line - white
        locations_white = file.readline().replace("\n", "")
        if locations_white == '':
            return False
        locations_white = locations_white.strip()
        if locations_white[-1] == ',':
            locations_white = locations_white[:-1]

        validated_white = validate_locations(locations_white)

        if validated_white:
            # 3rd line - black
            locations_black = file.readline().replace("\n", "")
            if locations_black == '':
                return False
            locations_black = locations_black.strip()
            if locations_black[-1] == ',':
                locations_black = locations_black[:-1]

            validated_black = validate_locations(locations_black)

            if validated_black:
                file.close()
                return True
            else:
                file.close()
                return False
        else:
            file.close()
            return False
    else:
        file.close()
        return False


def locations2pieces(locations: str, side: bool) -> list[Piece]:
    """turns locations into pieces and returns a list of pieces"""
    locations_list = locations.split(',')
    pieces = []
    for location in locations_list:
        location = location.strip()
        index = location2index(location)
        if location[0] == 'N' and side:
            piece = Knight(index[0], index[1], True)
        elif location[0] == 'N' and side is False:
            piece = Knight(index[0], index[1], False)
        elif location[0] == 'K' and side:
            piece = King(index[0], index[1], True)
        else:
            piece = King(index[0], index[1], False)
        pieces.append(piece)
    return pieces


def read_board(filename: str) -> Board:
    """
    reads board configuration from file in current directory in plain format
    raises OSError exception if file is not valid (see section Plain board configurations)
    """
    if validate_board(filename):
        file = open(filename, 'r')

        board_size = int(file.readline())

        # white pieces
        locations_white = file.readline().replace("\n", "")
        locations_white = locations_white.strip()
        if locations_white[-1] == ',':
            locations_white = locations_white[:-1]
        pieces_white = locations2pieces(locations_white, True)

        # black pieces
        locations_black = file.readline().replace("\n", "")
        locations_black = locations_black.strip()
        if locations_black[-1] == ',':
            locations_black = locations_black[:-1]
        pieces_black = locations2pieces(locations_black, False)

        all_pieces = pieces_white + pieces_black

        board = (board_size, all_pieces)
        file.close()
        return board
    else:
        raise OSError


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    """
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere

    Hints:
    - use methods of random library
    - use can_move_to
    """
    locations = []
    possible_moves = []
    for row in range(B[0], 0, -1):
        for column in range(1, B[0] + 1):
            locations.append((column, row))

    for piece in B[1]:
        if piece.side is False:
            for location in locations:
                if piece2type(piece).can_move_to(location[0], location[1], B):
                    possible_moves.append((piece, location[0], location[1]))

    r = random.randrange(len(possible_moves))

    return possible_moves[r]


def conf2unicode(B: Board) -> str:
    """converts board configuration B to unicode format string (see section Unicode board configurations)"""
    unicode = ''
    for row in range(B[0], 0, -1):
        for column in range(1, B[0] + 1):

            for piece in B[1]:
                code = ''
                if piece.pos_x == column and piece.pos_y == row:
                    if piece.side and piece.type == 'K':
                        code = '\u2654'
                    elif piece.side and piece.type == 'N':
                        code = '\u2658'
                    elif piece.side is False and piece.type == 'K':
                        code = '\u265A'
                    elif piece.side is False and piece.type == 'N':
                        code = '\u265E'
                    unicode += code
                    break

            if code == '':
                unicode += '\u2001'

        unicode += '\n'
    return unicode


def conf2file(B: Board) -> str:
    """converts board configuration to lines to be saved on file"""
    file_line_white = ''
    file_line_black = ''
    for piece in B[1]:
        if piece.side and piece.type == 'K':
            file_line_white += f'K{index2location(piece.pos_x, piece.pos_y)}, '
        elif piece.side and piece.type == 'N':
            file_line_white += f'N{index2location(piece.pos_x, piece.pos_y)}, '
        elif piece.side is False and piece.type == 'K':
            file_line_black += f'K{index2location(piece.pos_x, piece.pos_y)}, '
        elif piece.side is False and piece.type == 'N':
            file_line_black += f'N{index2location(piece.pos_x, piece.pos_y)}, '

    return f'{file_line_white[:-2]}\n{file_line_black[:-2]}'


def save_board(filename: str, B: Board) -> None:
    """saves board configuration into file in current directory in plain format"""
    file = open(filename, 'w')
    file.write(f'{B[0]}\n{conf2file(B)}')
    file.close()
    print("The game configuration was saved.")
    sys.exit()


def read_move(move: str, side: bool, B: Board) -> tuple[tuple[int, int], tuple[int, int]]:
    """checks if move is of valid format and returns the locations"""

    # check syntax
    if move.isalnum():
        from_column = move[0]
        if move[1:3].isnumeric():
            from_row = move[1:3]
            to_column = move[3]
            to_row = move[4:]
        else:
            from_row = move[1:2]
            to_column = move[2]
            to_row = move[3:]

        # check syntax
        if from_column.isalpha() and from_row.isnumeric() and 0 < int(from_row) <= B[
            0] and to_column.isalpha() and to_row.isnumeric() and 0 < int(to_row) <= B[0]:
            # there is a piece at the "from" location
            from_indexes = location2index(f' {from_column}{from_row}')
            to_indexes = location2index(f' {to_column}{to_row}')
            if is_piece_at(from_indexes[0], from_indexes[1], B):
                piece_at_origin = piece_at(from_indexes[0], from_indexes[1], B)
                if piece_at_origin.side == side:
                    return from_indexes, to_indexes
                else:
                    raise OSError
            else:
                raise OSError
        else:
            raise OSError
    else:
        raise OSError


def piece2type(piece: Piece) -> Union[King, Knight]:
    """converts pieces into their class type"""
    if piece.side and piece.type == 'K':
        return King(piece.pos_x, piece.pos_y, True)
    elif piece.side and piece.type == 'N':
        return Knight(piece.pos_x, piece.pos_y, True)
    elif piece.side is False and piece.type == 'K':
        return King(piece.pos_x, piece.pos_y, False)
    elif piece.side is False and piece.type == 'N':
        return Knight(piece.pos_x, piece.pos_y, False)


def next_round(B: Board) -> None:
    """runs next round"""
    move_white = input("Next move of White: ")
    while move_white != 'QUIT':
        try:
            # validate move - white
            move = read_move(move_white, True, B)
            piece = piece2type(piece_at(move[0][0], move[0][1], B))
            if piece.can_move_to(move[1][0], move[1][1], B):
                # make move - white
                new_board_white = piece.move_to(move[1][0], move[1][1], B)
                unicode = conf2unicode(new_board_white)
                print(f"The configuration after White's move is:\n{unicode}")
                if is_checkmate(True, new_board_white):
                    print("Game over. White wins.")
                    break
                elif is_stalemate(True, new_board_white):
                    print("Game over. Stalemate.")
                    break
                else:
                    # get move - black
                    move_black = find_black_move(new_board_white)
                    move_from = index2location(move_black[0].pos_x, move_black[0].pos_y)
                    move_to = index2location(move_black[1], move_black[2])
                    # make move - black
                    new_board_black = piece2type(move_black[0]).move_to(move_black[1], move_black[2], B)
                    if is_checkmate(False, new_board_black):
                        print("Game over. Black wins.")
                        break
                    elif is_stalemate(False, new_board_black):
                        print("Game over. Stalemate.")
                        break
                    else:
                        unicode = conf2unicode(new_board_black)
                        print(f"Next move of Black is {move_from}{move_to}. The configuration after Black's move is:\n{unicode}")
                        B = copy.deepcopy(new_board_black)
                        move_white = input("Next move of White: ")
            else:
                raise OSError
        except OSError:
            move_white = input("This is not a valid move. Next move of White: ")
    filename = input("File name to store the configuration: ")
    save_board(filename, B)


def main() -> None:
    """runs the play"""
    initial_filename = input("File name for initial configuration: ")
    get_filename = True
    while get_filename:
        try:
            if initial_filename == 'QUIT':
                break
            else:
                board = read_board(initial_filename)
                get_filename = False
                unicode = conf2unicode(board)
                print(f"The initial configuration is:\n{unicode}")
                next_round(board)
        except OSError:
            initial_filename = input("This is not a valid file. File name for initial configuration: ")


if __name__ == '__main__': #keep this in
   main()
