
import numpy as np
import Piece

"""
For console testing:
aboard = np.array([
[1, 1, 1, 1, 1, 0, 1, 1],
[1, 1, 0, 1, 1, 1, 1, 1],
[1, 1, 0, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 0, 1],
[1, 0, 1, 0, 1, 1, 1, 1],
[1, 0, 1, 1, 1, 1, 1, 1],
[0, 1, 0, 1, 0, 1, 1, 0],
[0, 0, 1, 1, 1, 1, 1, 1],
])
piece_can_fit(aboard, 11)
apply_piece(aboard, 11, 0, 6)
"""


def find_piece(action_board, pieces_in_play):
    """
    returns tuple (piece_id, piece_origin_x, piece_origin_y)
    """
    assert len(pieces_in_play) > 0
    piece_count = 0
    item_indexes = []
    for r in range(0, 8):
        for c in range(0, 8):
            if action_board[r, c] == 1:
                piece_count += 1
                item_indexes.append((r, c))
    if piece_count == 0:
        return -1, -1, -1
    leftMost = -1
    topMost = -1
    for row, col in item_indexes:
        if col < leftMost or leftMost < 0:
            leftMost = col
        if row < topMost or topMost < 0:
            topMost = row
    piece = np.zeros((5, 5), dtype=np.uint8)
    for row, col in item_indexes:
        piece[row - topMost, col - leftMost] = 1
    pid = Piece.piece_to_id(piece)
    if pid not in pieces_in_play:
        return -2, -1, -1
    return pid, leftMost, topMost


def apply_piece(board, piece_id, piece_origin_x, piece_origin_y):
    """
    returns the modified board and score based on the move and new state of the board
    """
    piece = Piece.piece_from_id(piece_id)
    new_board = apply_piece_only(board, piece, piece_origin_x, piece_origin_y)
    if new_board is None:
        return board, 0, 0, 0
    full_row = np.array([1, 1, 1, 1, 1, 1, 1, 1])
    rows_cleared = []
    cols_cleared = []
    for r in range(0, 8):
        if np.array_equal(full_row, new_board[r]):
            rows_cleared.append(r)
    for c in range(0, 8):
        if np.array_equal(full_row, new_board[:, c]):
            cols_cleared.append(c)
    score = Piece.piece_size_map[piece_id]
    line_score = 0
    lines_cleared = len(rows_cleared) + len(cols_cleared)
    if lines_cleared > 0:
        modifier = max(1., (1.5 * (lines_cleared - 1)))
        line_score = (8 * lines_cleared) * modifier
    score += line_score
    for r in rows_cleared:
        new_board[r] = 0
    for c in cols_cleared:
        new_board[:, c] = 0
    return new_board, score, lines_cleared, (10 + lines_cleared * 100)


def piece_can_fit(board, piece_id):
    piece = Piece.piece_from_id(piece_id)
    for br in range(0, 8):
        for bc in range(0, 8):
            if board[br, bc] == 0:
                if apply_piece_only(board, piece, bc, br) is not None:
                    return True
    return False


def apply_piece_only(board, piece, piece_origin_x, piece_origin_y):
    new_board = board.copy()
    for r in range(0, 5):
        for c in range(0, 5):
            if piece[r, c] == 1:
                if r + piece_origin_y > 7 or c + piece_origin_x > 7:
                    return None
                if new_board[r + piece_origin_y, c + piece_origin_x] == 1:
                    return None
                new_board[r + piece_origin_y, c + piece_origin_x] = 1
    return new_board
