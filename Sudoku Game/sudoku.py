
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def is_valid_move(board, row, col, number):
    for x in range(9):
        if board[row][x] == number:
            return False

    for x in range(9):
        if board[x][col] == number:
            return False

    corner_row = row // 3 * 3
    corner_col = col // 3 * 3
    for x in range(3):
        for y in range(3):
            if board[corner_row + x][corner_col + y] == number:
                return False
    return True

def solve(board, row, col):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if board[row][col] > 0:
        return solve(board, row, col + 1)

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num

            if solve(board, row, col + 1):
                return True
            board[row][col] = 0

    return False

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

print("Initial Sudoku grid:")
print_board(board)

if solve(board, 0, 0):
    print("\nSudoku solved:")
    print_board(board)
else:
    print("No solution found.")
    