def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    x = ord(loc[1]) - 96
    y = int(loc[2])
    return x, y

def index2location(x: int, y: int) -> str:
    '''converts pair of coordinates to corresponding location'''
    a = chr(x + 96)
    b = str(y)
    return a + b

class Piece():
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black
    type: str

    def __init__(self, pos_X: int, pos_Y: int, side_: bool, type_: str):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_
        self.type = type_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''

class Knight(Piece):
    type: str = 'N'

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_, self.type)

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

class King(Piece):
    type: str = 'K'

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_, self.type)
   
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''

def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''

def validate_locations(locations: str) -> bool:
    '''checks if a locations line in a file is of a valid format according to:
        - String like Xcr where X is either K or N (King or kNight) and cr is the columns and row numbers
        - Only one king of each colour
        - Only one piece for location
        - Each location is within s*s'''

    locations_list = locations.split(',')
    king = 0
    for location in locations_list:
        location = location.strip()
        # syntax
        if (location[0] == 'N' or location[0] == 'K') and location[1].isalpha() and location[1].islower() and location[2:].isnumeric() and 0 < int(location[2:]) < 26:
            # only one king
            if location[0] == 'K':
                king += 1
                if king > 1:
                    return False
        else:
            return False

    # only one piece for location - no duplicates
    if len(locations_list) != len(set(locations_list)):
        return False

    return True

def validate_board(filename: str) -> bool:
    '''
    validates board configuration:
        - First line: number representing the size of the board
        - Second line: piece locations of white pieces separated by ,
        - Third line: piece locations of black pieces separated by ,
    '''
    file = open(filename, 'r')
    # 1st line - size
    board_size = file.readline().replace("\n", "")

    if board_size.isnumeric() and 3 < int(board_size) < 26:
        # 2nd line - white
        locations_white = file.readline().replace("\n", "")
        validated_white = validate_locations(locations_white)

        if validated_white:
            # 3rd line - black
            locations_black = file.readline().replace("\n", "")
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

def locations2pieces(locations: str, colour: str) -> list[Piece]:
    '''turns locations into pieces and returns a list of pieces'''
    locations_list = locations.split(',')
    pieces = []
    for location in locations_list:
        location = location.strip()
        index = location2index(location)
        if location[0] == 'N' and colour == 'w':
            piece = Knight(index[0], index[1], True)
        elif location[0] == 'N' and colour == 'b':
            piece = Knight(index[0], index[1], False)
        elif location[0] == 'K' and colour == 'w':
            piece = King(index[0], index[1], True)
        else:
            piece = King(index[0], index[1], False)
        pieces.append(piece)
    return pieces

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    if validate_board(filename):
        file = open(filename, 'r')

        board_size = int(file.readline())

        #white pieces
        locations_white = file.readline().replace("\n", "")
        pieces_white = locations2pieces(locations_white, 'w')

        #black pieces
        locations_black = file.readline().replace("\n", "")
        pieces_black = locations2pieces(locations_black, 'b')

        all_pieces = pieces_white + pieces_black

        board = (board_size, all_pieces)

        return board
    else:
        raise IOError


def save_board(filename: str, B: Board) -> None:
    """saves board configuration into file in current directory in plain format"""
    file = open(filename, 'w')
    file.write(f'{B[0]}\n{conf2file(B)}')
    file.close()
    print("The game configuration was saved.")


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''

def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''


def next_round(B: Board) -> None:
    """runs next round"""
    move_white = input("Next move of White: ")
    get_move_white = True
    while get_move_white:
        try:
            if move_white == 'QUIT':
                filename = input("File name to store the configuration: ")
                save_board(filename, B)
                break
            else:
                # validate move
                move = read_move(move_white, True, B)
                piece = piece2type(piece_at(move[0][0], move[0][1], B))
                print(f'moving piece {piece.type} {piece.pos_x}, {piece.pos_y}')
                print(f'move to {move[1][0]}, {move[1][1]}')
                if piece.can_move_to(move[1][0], move[1][1], B):
                    # make move
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
                        # get validated move
                        move_black = find_black_move(new_board_white)
                        move_from = index2location(move_black[0].pos_x, move_black[0].pos_y)
                        move_to = index2location(move_black[1], move_black[2])
                        # make move
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
                            next_round(new_board_black)
                else:
                    raise IOError
        except IOError:
            move_white = input("This is not a valid move. Next move of White: ")


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
        except IOError:
            print("This is not a valid file.")
            initial_filename = input("File name for initial configuration: ")


if __name__ == '__main__': #keep this in
   main()
