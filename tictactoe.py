"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cells_in_board = [cell for row in board for cell in row] #get each cell from the board
    x_count = cells_in_board.count(X) #get x count
    o_count = cells_in_board.count(O) #get o count
    return X if x_count <= o_count else O #this is to make sure each player gets a turn sequentially

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set() #initialize set
    for i in range(3): #get i value of tuple for row of the move
        for j in range(3): #get j value of tuple for cell in row
            if board[i][j] == EMPTY: #if possible to make move, then add to actions set
                action_set.add((i,j))
    return action_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board): #raise exception if action not in actions
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board) #create a new board so that original is unmodified
    new_board[action[0]][action[1]] = player(board) #player is able to make move given result
    return new_board #return new board which is a copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3): #finding 3 X's in a row
        if all(board[i][j] == X for j in range(3)): #vertical
            return X
        if all(board[j][i] == X for j in range(3)): #horizontal
            return X
    if all(board[i][i] == X for i in range(3)) or all(board[i][2 - i] == X for i in range(3)): #diagonal
        return X # X has won 

    for i in range(3): #finding 3 O's in a row
        if all(board[i][j] == O for j in range(3)): #vertical
            return O
        if all(board[j][i] == O for j in range(3)): #horizontal
            return O
    if all(board[i][i] == O for i in range(3)) or all(board[i][2 - i] == O for i in range(3)): #diagonal
        return O # O has won 

    return None #no winner case

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None: #if there is a winner
        return True 
    for row in board:
        if EMPTY in row: #if empty spaces left
            return False #game is still playing
    return True #return True if there is tie

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board) #get winner
    if result == X: #if x is winner, utility is 1
        return 1
    elif result == O: #if O is winner, utility is -1
        return -1
    else:   #if tie
        return 0 

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None #if board is terminal, return None

    current_player = player(board) #get current player
    if current_player == X:
        _, move = get_max_value(board) #use helper function to get optimal move for X
    else:
        _, move = get_min_value(board) #use helper function to get optimal move for O

    return move #return optimal action

def get_max_value(board):
    """
    Helper function for minimax. Recursively searches for best move for max player (X).
    """
    if terminal(board): #if board is terminal, return None
        return utility(board), None

    v = float("-inf") #initialize v 
    best_move = None #initialize best move

    for action in actions(board): # check possible actions
        min_val, _ = get_min_value(result(board, action)) #recursively get min val
        if min_val > v: #if min value is greater than v
            v = min_val #update v
            best_move = action #assign best move
    return v, best_move 

def get_min_value(board):
    """
    Helper function for minimax. Recursively searches for best move for min player (O).
    """
    if terminal(board): #if board is terminal, return None
        return utility(board), None

    v = float("inf") #initialize v 
    best_move = None #initialize best move

    for action in actions(board): # check possible actions
        max_val, _ = get_max_value(result(board, action)) #recursively get max val
        if max_val < v: #if min value is less than v
            v = max_val #update v 
            best_move = action #assign best move
    return v, best_move