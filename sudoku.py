import copy


def find_empty_cell(board: list):
    # self-explanatory?
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return x, y

    return -1


def print_board(board: list):
    # print-board in console
    print("    ", end="")
    for i in range(9):
        print(i, end="  ")

    print("")
    for i, row in enumerate(board):
        print(i, "", row)


# check if current board is solvable?
def can_solve(board: list):
    # ok so this algorithm looks messy because I wanted to reuse the is_possible() function instead of
    # reinventing the wheel, fuk
    for y in range(9):
        for x in range(9):
            if board[y][x] != 0:
                result = None
                val = board[y][x]  # store value at cell
                board[y][x] = 0  # clear the cell
                if is_possible(board, val, x, y):  # check if value at cell would be valid
                    result = True
                else:
                    result = False
                board[y][x] = val  # restore the cell's value

                if not result:  # if that value would've been illegal, return fase
                    return (x, y)

    return None


# check if putting val at (x, y) cell is possible
def is_possible(board: list, val: int, x: int, y: int):
    # check row for val
    for row in range(9):
        if board[row][x] == val:
            return False

    # check column
    for col in range(9):
        if board[y][col] == val:
            return False

    # calculate offsets for sub-grid
    # a neat little trick exploiting truncating division, I hate that Python uses // for this
    x_off = (x // 3) * 3
    y_off = (y // 3) * 3

    # finally check the sub-grid
    for y in range(3):
        for x in range(3):
            if board[y_off + y][x_off + x] == val:
                return False

    return True


def solve_sudoku(board: list):
    # find current empty position...
    pos = find_empty_cell(board)

    # if there is no empty cell, YAY! board is solved!
    if pos == -1:
        return True

    # ...else get empty cell position
    (x, y) = pos

    for val in range(1, 10):
        # check each value for possibility...
        if is_possible(board, val, x, y):
            # ...if possible, set the value
            board[y][x] = val
            # please ignore these, not part of algorithm...
            solve_sudoku.engine.render(x, y, (0, 255, 0, 255))
            solve_sudoku.engine.handle_input()

            # continue algorithm..
            # ...recursively call the function again
            if solve_sudoku(board):
                return True
            board[y][x] = 0

            # ignore...
            solve_sudoku.engine.render(x, y, (255, 0, 0, 255))
            solve_sudoku.engine.handle_input()
            # ---
    # if no value is valid at position, return False, go to previous stack frame..
    # hence triggering backtracking...
    return False
