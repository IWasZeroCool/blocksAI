
import numpy as np

"""
Pieces are a 5x5 array with 1's meaning there's a piece item there and 0 for empty spot.

Pieces are placed on the board using the top-left corner space as the origin location, so if 
a piece is placed in row 3, column 2 of the board, the top-left space is in row 3, col 2, and 
the piece is spread out to the right and below from there.
"""

"""
For testing:
test = np.array([
[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]
])
"""

piece_size_map = {
    0: 1,
    1: 2,
    2: 2,
    3: 3,
    4: 3,
    5: 4,
    6: 4,
    7: 5,
    8: 5,
    9: 3,
    10: 3,
    11: 3,
    12: 3,
    13: 5,
    14: 5,
    15: 5,
    16: 5,
    17: 4,
    18: 6
}


def count_piece(piece):
    pcount = 0
    for r in range(0, 5):
        for c in range(0, 5):
            if piece[r, c] == 1:
                pcount += 1
    return pcount


def piece_to_id(piece, piece_count=0):
    pcount = piece_count
    if piece_count < 1:
        pcount = count_piece(piece)
    if pcount < 1:
        return -1
    pieces_to_check = []
    for pid, psize in piece_size_map.items():
        if psize == pcount:
            pieces_to_check.append(pid)
    assert len(pieces_to_check) > 0
    pieceBuffer = dot()
    for pid in pieces_to_check:
        piece_from_id(pid, pieceBuffer)
        if np.array_equal(piece, pieceBuffer):
            return pid
    return -1


def piece_from_id(piece_id, pieceArray=None):
    if piece_id == -1:
        return __normalize_piece_input(pieceArray)
    return piece_map[piece_id](pieceArray)


def random_piece(np_random, exclude_pieces=[]):
    piece = np_random.randint(0, 19)
    if piece in exclude_pieces:
        return random_piece(np_random, exclude_pieces)
    return piece


def clear_piece(pieceArray):
    pieceArray[:] = 0


def __normalize_piece_input(pieceArray):
    a = pieceArray
    if a is None:
        a = np.zeros((5, 5), dtype=np.uint8)
    clear_piece(a)
    return a


def piece_id_to_one_hot(pid):
    if pid == -1:
        return np.zeros((1, 19), dtype=np.uint8)[0]
    return np.eye(19, dtype=np.uint8)[pid]


def one_hot_to_piece_id(one_hot_array):
    pid = np.argmax(one_hot_array, axis=0)
    if pid == 0 and one_hot_array[0] == 0:
        return -1
    return pid


def dot(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    return a


def two_horizontal(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:1, 0:2] = 1
    return a


def two_vertical(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:2, 0:1] = 1
    return a


def three_horizontal(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:1, 0:3] = 1
    return a


def three_vertical(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:3, 0:1] = 1
    return a


def four_horizontal(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:1, 0:4] = 1
    return a


def four_vertical(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:4, 0:1] = 1
    return a


def five_horizontal(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:1, 0:5] = 1
    return a


def five_vertical(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0:5, 0:1] = 1
    return a


def small_upper_left(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[1, 0] = 1
    return a


def small_upper_right(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[1, 1] = 1
    return a


def small_lower_left(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[1, 0] = 1
    a[1, 1] = 1
    return a


def small_lower_right(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[1, 1] = 1
    a[0, 1] = 1
    a[1, 0] = 1
    return a


def large_upper_left(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[0, 2] = 1
    a[1, 0] = 1
    a[2, 0] = 1
    return a


def large_upper_right(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[0, 2] = 1
    a[1, 2] = 1
    a[2, 2] = 1
    return a


def large_lower_left(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[1, 0] = 1
    a[2, 0] = 1
    a[2, 1] = 1
    a[2, 2] = 1
    return a


def large_lower_right(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 2] = 1
    a[1, 2] = 1
    a[2, 2] = 1
    a[2, 1] = 1
    a[2, 0] = 1
    return a


def small_cube(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[1, 0] = 1
    a[1, 1] = 1
    return a


def large_cube(pieceArray=None):
    a = __normalize_piece_input(pieceArray)
    a[0, 0] = 1
    a[0, 1] = 1
    a[0, 2] = 1
    a[1, 0] = 1
    a[1, 1] = 1
    a[1, 2] = 1
    a[2, 0] = 1
    a[2, 1] = 1
    a[2, 2] = 1
    return a


def dump_pieces():
    # print("dot\n", dot())
    # print("two_horizontal\n", two_horizontal())
    # print("two_vertical\n", two_vertical())
    # print("three_horizontal\n", three_horizontal())
    # print("three_vertical\n", three_vertical())
    # print("four_horizontal\n", four_horizontal())
    # print("four_vertical\n", four_vertical())
    # print("five_horizontal\n", five_horizontal())
    # print("five_vertical\n", five_vertical())
    # print("small_upper_left\n", small_upper_left())
    # print("small_upper_right\n", small_upper_right())
    # print("small_lower_left\n", small_lower_left())
    # print("small_lower_right\n", small_lower_right())
    # print("large_upper_left\n", large_upper_left())
    # print("large_upper_right\n", large_upper_right()) #borked
    # print("large_lower_left\n", large_lower_left()) #borked
    # print("large_lower_right\n", large_lower_right()) #borked
    # print("small_cube\n", small_cube())
    # print("large_cube\n", large_cube())
    return


piece_map = {
    0: dot,
    1: two_horizontal,
    2: two_vertical,
    3: three_horizontal,
    4: three_vertical,
    5: four_horizontal,
    6: four_vertical,
    7: five_horizontal,
    8: five_vertical,
    9: small_upper_left,
    10: small_upper_right,
    11: small_lower_left,
    12: small_lower_right,
    13: large_upper_left,
    14: large_upper_right,
    15: large_lower_left,
    16: large_lower_right,
    17: small_cube,
    18: large_cube
}
