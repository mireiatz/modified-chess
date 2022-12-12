import pytest
from chess_puzzle import *


# location to index
def test_location2index1():
    assert location2index("Ke2") == (5, 2)


def test_location2index2():
    assert location2index("Nz26") == (26, 26)


def test_location2index3():
    assert location2index("Nk18") == (11, 18)


def test_location2index4():
    assert location2index("Ko2") == (15, 2)


def test_location2index5():
    assert location2index("Ka1") == (1, 1)


# index to location
def test_index2location1():
    assert index2location(5, 2) == "e2"


def test_index2location2():
    assert index2location(26, 26) == "z26"


def test_index2location3():
    assert index2location(3, 24) == "c24"


def test_index2location4():
    assert index2location(22, 2) == "v2"


def test_index2location5():
    assert index2location(1, 1) == "a1"


wn1 = Knight(1, 2, True)
wn2 = Knight(5, 2, True)
wn3 = Knight(5, 4, True)
wk1 = King(3, 5, True)

bn1 = Knight(1, 1, False)
bk1 = King(2, 3, False)
bn2 = Knight(2, 4, False)

B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
"""
\u2001\u2001♔\u2001\u2001
\u2001♞\u2001\u2001♘
\u2001♚\u2001\u2001\u2001
♘\u2001\u2001\u2001♘
♞\u2001\u2001\u2001\u2001
"""


# check if piece at location
def test_is_piece_at1():
    assert is_piece_at(2, 2, B1) == False


def test_is_piece_at2():
    assert is_piece_at(5, 2, B1) 


def test_is_piece_at3():
    assert is_piece_at(2, 1, B1) is False


def test_is_piece_at4():
    assert is_piece_at(2, 3, B1) 


def test_is_piece_at5():
    assert is_piece_at(5, 5, B1) is False


# piece at location
def test_piece_at1():
    assert piece_at(1, 1, B1) == bn1


def test_piece_at2():
    assert piece_at(5, 4, B1) == wn3


def test_piece_at3():
    assert piece_at(2, 3, B1) == bk1


def test_piece_at4():
    assert piece_at(3, 5, B1) == wk1


def test_piece_at5():
    assert piece_at(2, 4, B1) == bn2


# meets [Rule1] or [Rule2] and [Rule3]
def test_can_reach1():
    """checks Rule 1 - move not allowed for knight"""
    assert bn1.can_reach(2, 2, B1) is False


def test_can_reach2():
    """checks Rule 1 - move allowed for knight"""
    assert wn2.can_reach(3, 1, B1) 


def test_can_reach3():
    """checks Rule 2 - move not allowed for king"""
    assert wk1.can_reach(4, 2, B1) is False


def test_can_reach4():
    """checks Rule 2 - move allowed for king"""
    assert wk1.can_reach(2, 5, B1) 


def test_can_reach5():
    """checks Rule 3 for white - cannot capture own side"""
    assert wn3.can_reach(3, 5, B1) is False


def test_can_reach6():
    """checks Rule 3 for white - can capture opposite side"""
    assert wn1.can_reach(2, 4, B1) 


def test_can_reach7():
    """checks Rule 3 for black - cannot capture own side"""
    assert bk1.can_reach(2, 4, B1) is False


def test_can_reach8():
    """checks Rule 3 for black - can capture opposite side"""
    assert bn2.can_reach(1, 2, B1) 


# meets all other rules - Rule 4
def test_can_move_to1():
    """white king moves - results in check"""
    assert wk1.can_move_to(4, 5, B1) is False


def test_can_move_to2():
    """black king moves - results in check"""
    assert bk1.can_move_to(3, 3, B1) is False


def test_can_move_to3():
    """white king moves - does not result in check"""
    assert wk1.can_move_to(2, 5, B1) 


def test_can_move_to4():
    """black king moves - does not result in check"""
    assert bk1.can_move_to(1, 3, B1) 


def test_can_move_to5():
    """white knight moves - does not result in check for white"""
    assert wn2.can_move_to(3, 3, B1) 
    assert wn2.can_move_to(3, 1, B1) 


def test_can_move_to6():
    """black knight moves - does not result in check for black"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    assert bn2.can_move_to(4, 3, B1) 
    assert bn2.can_move_to(4, 3, B1) 


# new board configuration
def test_move_to1():
    """checks a move that captures another piece - white knight moves"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Actual_B = wn1.move_to(2, 4, B1)
    wn1a = Knight(2, 4, True)
    Expected_B = (5, [wn1a, bn1, wn2, wn3, wk1, bk1])
    """
    \u2001\u2001♔\u2001\u2001\u2001
    \u2001♘\u2001\u2001♘
    \u2001♚\u2001\u2001\u2001
    \u2001\u2001\u2001\u2001♘
    ♞\u2001\u2001\u2001\u2001
    """
    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_move_to2():
    """checks a move that captures another piece - white king moves"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Actual_B = wk1.move_to(2, 4, B1)
    wk1a = King(2, 4, True)
    Expected_B = (5, [wn1, bn1, wn2, wn3, wk1a, bk1])
    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_move_to3():
    """checks a move that captures another piece - black knight moves"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Actual_B = bn2.move_to(1, 2, B1)
    bn2a = Knight(1, 2, False)
    Expected_B = (5, [bn1, wn2, bn2a, wn3, wk1, bk1])
    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_move_to4():
    """checks a move that captures another piece - black king moves"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Actual_B = bk1.move_to(1, 2, B1)
    bk1a = King(1, 2, False)
    Expected_B = (5, [bn1, wn2, bn2, wn3, wk1, bk1a])
    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

 
def test_move_to5():
    """checks a move that does not result in capture"""
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Actual_B = bk1.move_to(1, 3, B1)
    bk1a = King(1, 3, False)
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1a])
    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


# is in check
def test_is_check1():  
    """is check for white by black knight"""
    wk1a = King(4, 5, True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    """
    \u2001\u2001\u2001♔\u2001\u2001
    \u2001♞\u2001\u2001♘
    \u2001♚\u2001\u2001\u2001
    ♘\u2001\u2001\u2001♘
    ♞\u2001\u2001\u2001\u2001
    """
    assert is_check(True, B2) 

 
def test_is_check2():  
    """is check for white by black king"""
    bk1a = King(3, 4, False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1a])
    assert is_check(True, B2) 


def test_is_check3():  
    """is not check for white"""
    bk1a = King(3, 3, False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, bk1a, wk1])
    assert is_check(True, B2) is False


def test_is_check4():  
    """is check for black by white knight"""
    wn1a = Knight(4, 2, True)
    B2 = (5, [wn1a, bn1, wn2, bn2, wn3, wk1, bk1])
    assert is_check(False, B2) 


def test_is_check5():  
    """is check for black by white king"""
    bk1a = King(4, 4, False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1a])
    assert is_check(False, B2) 
    

def test_is_check6(): 
    """is not check for black"""
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, bk1, wk1])
    assert is_check(False, B2) is False


# is checkmate
def test_is_checkmate1():
    """checkmate for white"""
    wk1a = King(1, 5, True)
    bn2a = Knight(3, 4, False)
    bn3 = Knight(4, 4, False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])
    '''
    ♔    
      ♞♞♘
     ♚   
    ♘   ♘
    ♞    
    '''
    assert is_checkmate(True, B2) == True

def test_is_checkmate2():
    """checkmate for white"""
    wk1a = King(3, 4, True)
    bn4 = Knight(3, 2, False)
    bn5 = Knight(5, 3, False)
    bn6 = Knight(1, 4, False)
    bn7 = Knight(4, 4, False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, bk1, wk1a, bn4, bn5, bn6, bn7])
    assert is_checkmate(True, B2)


def test_is_checkmate3():
    """checkmate for black"""
    wn4 = Knight(4, 4, True)
    wn5 = Knight(4, 1, True)
    wn6 = Knight(5, 3, True)
    wn7 = Knight(2, 2, True)
    wn8 = Knight(2, 1, True)
    B2 = (5, [wn1, wn2, wn3, wn4, wn5, wn6, wn7, wn8, wk1, bn1, bk1, bn2])
    assert is_checkmate(False, B2)


def test_is_checkmate4():
    """checkmate for black"""
    bk1a = King(1, 5, False)
    wn4 = Knight(2, 2, True)
    wn5 = Knight(3, 4, True)
    wn6 = Knight(3, 2, True)
    wn7 = Knight(3, 1, True)
    B2 = (5, [wn1, wn2, wn3, wk1, bn1, bk1a, bn2, wn4, wn5, wn6, wn7])
    assert is_checkmate(False, B2)


def test_is_checkmate5():  
    """no checkmate for white"""
    wk1a = King(1, 5, True)
    bn1a = Knight(3, 1, False)
    bn1b = Knight(3, 4, False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1a, bk1])
    assert is_checkmate(True, B2) is False


def test_is_checkmate6():
    """no checkmate for black"""
    B2 = (5, [wn1, wn2, wn3, wk1, bn1, bk1, bn2])
    assert is_checkmate(False, B2) is False

# is stalemate
def test_is_stalemate1():
    """stalemate for white"""
    B2 = (4, [Knight(1, 2, False), King(3, 3, False), King(4, 1, True)])
    assert is_stalemate(True, B2)


def test_is_stalemate2():
    """stalemate for white"""
    B2 = (3, [King(1, 3, False), Knight(1, 1, False), King(3, 3, True)])
    assert is_stalemate(True, B2)


def test_is_stalemate3():
    """stalemate for black"""
    B2 = (5, [King(1, 1, False), Knight(2, 4, True), King(3, 2, True)])
    assert is_stalemate(False, B2)


def test_is_stalemate4():
    """stalemate for black"""
    B2 = (4, [King(2, 3, True), Knight(3, 1, True), King(4, 4, False)])
    assert is_stalemate(False, B2)


def test_is_stalemate5():
    """not stalemate for white"""
    assert is_stalemate(True, B1) is False


def test_is_stalemate6():
    """not stalemate for black"""
    assert is_stalemate(False, B1) is False


# read board configuration
def test_read_board1():
    B = read_board("board_examp.txt")
    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    assert B[0] == 5

    for piece in B[1]:  # we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_read_board2():
    """checks that the right board configuration is returned, bigger board"""

    B = read_board("board_example_success1.txt")
    B2 = (10, [Knight(7, 3, True), Knight(1, 5, True), King(9, 9, True), King(4, 1, False), Knight(5, 5, False),
               Knight(6, 6, False)])
    assert B[0] == 10

    for piece in B[1]:  # we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B2[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B2[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_read_board3():
    """checks that a wrong filename raises an exception"""
    with pytest.raises(OSError):
        read_board("board_example_non_existent.txt")


def test_read_board4():
    """checks that the wrong file format raises an exception"""
    with pytest.raises(OSError):
        B = read_board("board_example_fail1.txt")


def test_read_board5():
    """checks that an empty file raises an exception"""
    with pytest.raises(OSError):
        B = read_board("board_example_fail6.txt")


# check if locations are valid
def test_validate_locations1():
    """checks for syntax format - right format"""
    assert validate_locations('Na1, Kb3, Nb4') 


def test_validate_locations2():
    """checks for syntax format - Knight or King, wrong letter"""
    assert validate_locations('Aa1, Kb3, Nb4') is False


def test_validate_locations3():
    """checks for syntax format - Knight or King, lowercase letter"""
    assert validate_locations('ka1, Kb3, Nb4') is False


def test_validate_locations4():
    """checks for syntax format - Knight or King, integer"""
    assert validate_locations('1a1, Kb3, Nb4') is False


def test_validate_locations5():
    """checks for syntax format - columns, capital letters"""
    assert validate_locations('NA1, Kb3, Nb4') is False


def test_validate_locations6():
    """checks for syntax format - columns, integer"""
    assert validate_locations('N41, Kb3, Nb4') is False


def test_validate_locations7():
    """checks for syntax format - columns, especial character"""
    assert validate_locations('N*1, Kb3, Nb4') is False


def test_validate_locations8():
    """checks for syntax format - rows, letter"""
    assert validate_locations('Nar, Kb3, Nb4') is False


def test_validate_locations9():
    """checks for syntax format - rows, especial character"""
    assert validate_locations('Na*, Kb3, Nb4') is False


def test_validate_locations10():
    """checks for rule 'Each location is within s*s'"""
    assert validate_locations('Na1, Kb28, Nb4') is False


def test_validate_locations11():
    """checks for rule 'Only one piece per location'"""
    assert validate_locations('Na1, Kb3, Nb4, Nb4') is False


def test_validate_locations12():
    """checks for rule 'One king per colour', > 1 kings"""
    assert validate_locations('Ka1, Kb3, Nb4, Nb4') is False


def test_validate_locations13():
    """checks for rule 'One king per colour', 0 kings"""
    assert validate_locations('Na1, Nb3, Nb4, Nb4') is False


# check board configuration file
def test_validate_board1():
    """checks first line - size greater than 3"""
    assert validate_board('board_example_fail1.txt') is False


def test_validate_board2():
    """checks first line - size lower than 26"""
    assert validate_board('board_example_fail2.txt') is False


def test_validate_board3():
    """checks first line - size is numeric, especial character"""
    assert validate_board('board_example_fail3.txt') is False


def test_validate_board4():
    """checks first line - size is numeric, letter"""
    assert validate_board('board_example_fail4.txt') is False


def test_validate_board5():
    """checks first line - empty (only second line, only second and third lines)"""
    assert validate_board('board_example_fail5.txt') is False


# file
def test_validate_board6():
    """empty file"""
    assert validate_board('board_example_fail6.txt') is False


def test_validate_board7():
    """only first line"""
    assert validate_board('board_example_fail7.txt') is False


def test_validate_board8():
    """only first and second line"""
    assert validate_board('board_example_fail8.txt') is False


def test_validate_board9():
    """only first and third line"""
    assert validate_board('board_example_fail9.txt') is False


def test_validate_board10():
    """right format"""
    assert validate_board('board_example_success1.txt')
    assert validate_board('board_examp.txt')


# convert locations into pieces
def test_locations2pieces1():
    """checks conversion for white knight"""
    p = locations2pieces('Na2', True)
    assert p[0].pos_x == 1 and p[0].pos_y == 2 and p[0].side == True and p[0].type == 'N'


def test_locations2pieces2():
    """checks conversion for white king"""
    p = locations2pieces('Kc5', True)
    assert p[0].pos_x == 3 and p[0].pos_y == 5 and p[0].side == True and p[0].type == 'K'


def test_locations2pieces3():
    """checks conversion for black knight"""
    p = locations2pieces('Nz13', False)
    assert p[0].pos_x == 26 and p[0].pos_y == 13 and p[0].side == False and p[0].type == 'N'


def test_locations2pieces4():
    """checks conversion for black king"""
    p = locations2pieces('Km22', True)
    assert p[0].pos_x == 13 and p[0].pos_y == 22 and p[0].side == True and p[0].type == 'K'


def test_locations2pieces5():
    """checks conversion for multiple values, white"""
    p = locations2pieces('Na2, Ne2, Ne4, Kc5', True)
    assert p[0].pos_x == 1 and p[0].pos_y == 2 and p[0].side == True and p[0].type == 'N'
    assert p[1].pos_x == 5 and p[1].pos_y == 2 and p[1].side == True and p[1].type == 'N'
    assert p[2].pos_x == 5 and p[2].pos_y == 4 and p[2].side == True and p[2].type == 'N'
    assert p[3].pos_x == 3 and p[3].pos_y == 5 and p[3].side == True and p[3].type == 'K'


def test_locations2pieces6():
    """checks conversion for multiple values, black"""
    p = locations2pieces('Na1, Kb3, Nb4', False)
    assert p[0].pos_x == 1 and p[0].pos_y == 1 and p[0].side == False and p[0].type == 'N'
    assert p[1].pos_x == 2 and p[1].pos_y == 3 and p[1].side == False and p[1].type == 'K'
    assert p[2].pos_x == 2 and p[2].pos_y == 4 and p[2].side == False and p[2].type == 'N'


# configuration to unicode conversion
wn4 = Knight(2, 4, True)
wk2 = King(2, 3, True)
wk3 = King(1, 5, True)
bn3 = Knight(4, 4, False)
bn4 = Knight(3, 4, False)
bk2 = King(3, 3, False)

def test_conf2unicode1():
    B = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    assert conf2unicode(
        B) == '\u2001\u2001♔\u2001\u2001\n\u2001♞\u2001\u2001♘\n\u2001♚\u2001\u2001\u2001\n♘\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'


def test_conf2unicode2():
    B = (3, [wn1, wk2, bn1, bk2])
    assert conf2unicode(B) == '\u2001♔♚\n♘\u2001\u2001\n♞\u2001\u2001\n'


def test_conf2unicode3():
    B = (10, [Knight(7, 3, True), Knight(1, 5, True), King(9, 9, True), King(4, 1, False), Knight(5, 5, False),
              Knight(6, 6, False)])
    assert conf2unicode(
        B) == '\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001♔\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001♞\u2001\u2001\u2001\u2001\n♘\u2001\u2001\u2001♞\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001♘\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001♚\u2001\u2001\u2001\u2001\u2001\u2001\n'


def test_conf2unicode4():
    B = (4, [wn4, bn1, wk2, bk2])
    assert conf2unicode(B) == '\u2001♘\u2001\u2001\n\u2001♔♚\u2001\n\u2001\u2001\u2001\u2001\n♞\u2001\u2001\u2001\n'


def test_conf2unicode5():
    B = (5, [wn1, wn2, wn3, wk3, bn1, bk1, bn2, bn3])
    assert conf2unicode(
        B) == '♔\u2001\u2001\u2001\u2001\n\u2001♞\u2001♞♘\n\u2001♚\u2001\u2001\u2001\n♘\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'


# convert piece to class type
p1 = Piece(1, 2, True, 'K')
p2 = Piece(5, 6, True, 'N')
p3 = Piece(2, 8, False, 'K')
p4 = Piece(9, 1, False, 'N')
p5 = Piece(1, 1, True, 'K')

def test_piece2type1():
    p = piece2type(p1)
    assert p.pos_x == 1 and p.pos_y == 2 and p.side == True and p.type == 'K'


def test_piece2type2():
    p = piece2type(p2)
    assert p.pos_x == 5 and p.pos_y == 6 and p.side == True and p.type == 'N'


def test_piece2type3():
    p = piece2type(p3)
    assert p.pos_x == 2 and p.pos_y == 8 and p.side == False and p.type == 'K'


def test_piece2type4():
    p = piece2type(p4)
    assert p.pos_x == 9 and p.pos_y == 1 and p.side == False and p.type == 'N'


def test_piece2type5():
    p = piece2type(p5)
    assert p.pos_x == 1 and p.pos_y == 1 and p.side == True and p.type == 'K'


# read move
def test_read_move1():
    """check move format, from_column"""
    with pytest.raises(OSError):
        read_move('*2b1', True, B1)


def test_read_move2():
    """check move format, from_row"""
    with pytest.raises(OSError):
        read_move('aab1', True, B1)


def test_read_move3():
    """check move format, to_column"""
    with pytest.raises(OSError):
        read_move('a221', True, B1)


def test_read_move4():
    """check move format, to_row"""
    with pytest.raises(OSError):
        read_move('a2b*', True, B1)


def test_read_move5():
    """check move format, within board size"""
    with pytest.raises(OSError):
        read_move('a22c3', True, B1)


def test_read_move6():
    """check move format, right format"""
    assert read_move('a2c3', True, B1) == ((1, 2), (3, 3))


# board configuration to file format 
def test_conf2file1():
    B = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    assert conf2file(B) == 'Na2, Ne2, Ne4, Kc5\nNa1, Nb4, Kb3'


def test_conf2file2():
    B = (15, [Knight(3, 1, True), Knight(5, 10, True), King(2, 15, True), King(8, 8, False), Knight(12, 10, False)])
    assert conf2file(B) == 'Nc1, Ne10, Kb15\nKh8, Nl10'


def test_conf2file3():
    B = (8, [Knight(2, 3, True), King(3, 3, True), King(8, 8, False), Knight(2, 4, False)])
    assert conf2file(B) == 'Nb3, Kc3\nKh8, Nb4'


def test_conf2file4():
    B = (10, [Knight(7, 3, True), Knight(1, 5, True), King(9, 9, True), King(4, 1, False), Knight(5, 5, False),
              Knight(6, 6, False)])
    assert conf2file(B) == 'Ng3, Na5, Ki9\nKd1, Ne5, Nf6'


def test_conf2file5():
    B = (3, [Knight(1, 2, True), King(1, 1, True), King(2, 2, False), Knight(3, 3, False)])
    assert conf2file(B) == 'Na2, Ka1\nKb2, Nc3'