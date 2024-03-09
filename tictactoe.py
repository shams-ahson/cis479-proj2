import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    flat_board = [cell for row in board for cell in row]
    x_count = flat_board.count(X)
    o_count = flat_board.count(O)

    return X if x_count <= o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if all(board[i][j] == X for j in range(3)):
            return X
        if all(board[j][i] == X for j in range(3)):
            return X
    if all(board[i][i] == X for i in range(3)) or all(board[i][2 - i] == X for i in range(3)):
        return X

    for i in range(3):
        if all(board[i][j] == O for j in range(3)):
            return O
        if all(board[j][i] == O for j in range(3)):
            return O
    if all(board[i][i] == O for i in range(3)) or all(board[i][2 - i] == O for i in range(3)):
        return O

    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float("-inf")
    best_move = None

    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_move = action

    return v, best_move

def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float("inf")
    best_move = None

    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_move = action

    return v, best_move
