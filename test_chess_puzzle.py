import pytest
from chess_puzzle import *


#location to index
def test_location2index1():
    assert location2index("e2") == (5, 2)

def test_location2index2():
    assert location2index("z26") == (26, 26)

def test_location2index3():
    assert location2index("k18") == (11, 18)

def test_location2index4():
    assert location2index("o2") == (15, 2)

def test_location2index5():
    assert location2index("a1") == (1, 1)


#index to location
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

wn1 = Knight(1,2,True)
wn2 = Knight(5,2,True)
wn3 = Knight(5,4, True)
wk1 = King(3,5, True)

bn1 = Knight(1,1,False)
bk1 = King(2,3, False)
bn2 = Knight(2,4, False)

B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
'''
  ♔  
 ♞  ♘
 ♚   
♘   ♘
♞    
'''


#check if piece at location
def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False

def test_is_piece_at2():
    assert is_piece_at(5,2, B1) == True


#piece at location
def test_piece_at1():
    assert piece_at(1,1, B1) == bn1

def test_piece_at2():
    assert piece_at(5,4, B1) == wn3


#meets [Rule1] or [Rule2] and [Rule3]
def test_can_reach1():
    assert bn1.can_reach(2,2, B1) == False

def test_can_reach2():
    assert wk1.can_reach(3,6, B1) == True


#meets all other rules
def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False

def test_can_move_to2():
    assert bk1.can_move_to(3,3, B1) == False #cannot move to where it becomes in check


#new board configuration
def test_move_to1():
    Actual_B = wn1.move_to(2,4, B1)
    wn1a = Knight(2,4,True)
    Expected_B = (5, [wn1a, bn1, wn2, wn3, wk1, bk1]) 
    '''
      ♔   
     ♘  ♘
     ♚   
        ♘
    ♞    
    '''
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to2():
    Actual_B = bk1.move_to(1,3, B1)
    bk1a = King(2,4,False)
    Expected_B = (5, [bk1a, bn1, wn2, wn3, wk1, bk1]) 
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


#is check
def test_is_check1():
    wk1a = King(4,5,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    '''
       ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    assert is_check(True, B2) == True

def test_is_check2():
    bk1a = King(3,3,False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, bk1a, bk1])
    assert is_check(True, B2) == True


#is checkmate
def test_is_checkmate1():
    wk1a = King(1,5,True)
    bn2a = Knight(3,4, False)
    bn3 = Knight(4,4,False)
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
    bn1a = King(3,1,False)
    B2 = (5, [wn1, wn2, wn3, bn1a, bk1])
    assert is_checkmate(True, B2) == True


#read board configuration
def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_read_board2():
    '''checks that the right board configuration is returned, different board
    '''

    B = read_board("board_example_success1.txt")
    B2 = (10, [Knight(7, 3, True), Knight(1, 5, True), King(9, 9, True), King(4, 1, False), Knight(5, 5, False), Knight(6, 6, False)])
    assert B[0] == 10

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B2[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B2[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board3():
    '''checks that a wrong filename raises an exception'''
    B = read_board("board_example_non_existent.txt")
    with pytest.raises(IOError):
        print("IOError")

def test_read_board4():
    '''checks that the wrong file format raises an exception'''
    B = read_board("board_example_fail1.txt")
    with pytest.raises(IOError):
        print("IOError")

def test_read_board5():
    '''checks that an empty file raises an exception'''
    B = read_board("board_example_fail6.txt")
    with pytest.raises(IOError):
        print("IOError")


#check if locations are valid
def test_validate_locations1():
    '''checks for syntax format - right format'''
    assert validate_locations('Na1, Kb3, Nb4') is True

def test_validate_locations2():
    '''checks for syntax format - Knight or King, wrong letter'''
    assert validate_locations('Aa1, Kb3, Nb4') is False

def test_validate_locations3():
    '''checks for syntax format - Knight or King, lowercase letter'''
    assert validate_locations('ka1, Kb3, Nb4') is False

def test_validate_locations4():
    '''checks for syntax format - Knight or King, integer'''
    assert validate_locations('1a1, Kb3, Nb4') is False

def test_validate_locations5():
    '''checks for syntax format - columns, capital letters'''
    assert validate_locations('NA1, Kb3, Nb4') is False

def test_validate_locations6():
    '''checks for syntax format - columns, integer'''
    assert validate_locations('N41, Kb3, Nb4') is False

def test_validate_locations7():
    '''checks for syntax format - columns, especial character'''
    assert validate_locations('N*1, Kb3, Nb4') is False

def test_validate_locations8():
    '''checks for syntax format - rows, letter'''
    assert validate_locations('Nar, Kb3, Nb4') is False

def test_validate_locations9():
    '''checks for syntax format - rows, especial character'''
    assert validate_locations('Na*, Kb3, Nb4') is False

def test_validate_locations10():
    '''checks for rule "Only one king per colour"'''
    assert validate_locations('Ka1, Kb3, Nb4, Nb4') is False

def test_validate_locations11():
    '''checks for rule "Only one piece per location"'''
    assert validate_locations('Na1, Kb3, Nb4, Nb4') is False

def test_validate_locations12():
    '''checks for rule "Each location is within s*s"'''
    assert validate_locations('Na1, Kb28, Nb4') is False


#check board configuration file
#1st line
def test_validate_board1():
    '''checks first line - size greater than 3'''
    assert validate_board('board_example_fail1.txt') is False

def test_validate_board2():
    '''checks first line - size lower than 26'''
    assert validate_board('board_example_fail2.txt') is False

def test_validate_board3():
    '''checks first line - size is numeric, especial character'''
    assert validate_board('board_example_fail3.txt') is False

def test_validate_board4():
    '''checks first line - size is numeric, letter'''
    assert validate_board('board_example_fail4.txt') is False

def test_validate_board5():
    '''checks first line - size is numeric, empty'''
    assert validate_board('board_example_fail5.txt') is False

#file
def test_validate_board6():
    '''empty file'''
    assert validate_board('board_example_fail6.txt') is False

def test_validate_board7():
    '''only one line'''
    assert validate_board('board_example_fail7.txt') is False

def test_validate_board8():
    '''right format'''
    assert validate_board('board_examp.txt') is True


#convert locations into pieces
def test_locations2pieces1():
    '''checks conversion for white knight'''
    assert locations2pieces('Na2', 'w') == [Knight(1, 2, True)]

def test_locations2pieces2():
    '''checks conversion for white king'''
    assert locations2pieces('Kc5', 'w') == [King(3, 5, True)]

def test_locations2pieces3():
    '''checks conversion for black knight'''
    assert locations2pieces('Nz13', 'b') == [Knight(26, 13, False)]

def test_locations2pieces4():
    '''checks conversion for black king'''
    assert locations2pieces('Km22', 'w') == [King(13, 22, False)]

def test_locations2pieces5():
    '''checks conversion for multiple values, white'''
    assert locations2pieces('Na2, Ne2, Ne4, Kc5', 'w') == [Knight(1, 1, True), Knight(5, 2, True), Knight(5, 4, True), King(3, 5, True)]

def test_locations2pieces6():
    '''checks conversion for multiple values, white'''
    assert locations2pieces('Na1, Kb3, Nb4', 'b') == [Knight(1, 1, False), King(2, 3, False), Knight(2, 4, False)]


#configuration to unicode conversion
def test_conf2unicode1():
    assert conf2unicode(B1) == '\u2001\u2001♔\u2001\u2001\n\u2001♞\u2001\u2001♘\n\u2001♚\u2001\u2001\u2001\n♘\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'

def test_conf2unicode2():
    wk1a = King(4, 5, True)
    B = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    assert conf2unicode(B) == '\u2001\u2001\u2001♔\u2001\u2001\n\u2001♞\u2001\u2001♘\n\u2001♚\u2001\u2001\u2001\n    ♘\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'

def test_conf2unicode3():
    B = (10, [Knight(7, 3, True), Knight(1, 5, True), King(9, 9, True), King(4, 1, False), Knight(5, 5, False),
              Knight(6, 6, False)])
    assert conf2unicode(B1) == '\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001♔\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001♞\u2001\u2001\u2001\u2001\n♘\u2001\u2001\u2001♞\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001♘\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001♚\u2001\u2001\u2001\u2001\u2001\u2001\n'

def test_conf2unicode4():
    wn1a = Knight(2, 4, True)
    B = (5, [wn1a, bn1, wn2, wn3, wk1, bk1])
    assert conf2unicode(B) == '\u2001\u2001♔\u2001\u2001\u2001\n\u2001♘\u2001\u2001♘\n\u2001♚\u2001\u2001\u2001\n    \u2001\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'

def test_conf2unicode5():
    wk1a = King(1, 5, True)
    bn2a = Knight(3, 4, False)
    bn3 = Knight(4, 4, False)
    B = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])
    assert conf2unicode(B) == '♔\u2001\u2001\u2001\u2001\n\u2001\u2001♞♞♘\n\u2001♚\u2001\u2001\u2001\n    ♘\u2001\u2001\u2001♘\n♞\u2001\u2001\u2001\u2001\n'

