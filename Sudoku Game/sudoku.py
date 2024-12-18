def is_valid_move(grid, row, col, number):
    """Checks if placing 'number' at (row, col) in 'grid' is valid.

    Args:
        grid: A 9x9 list of lists representing the Sudoku grid.
        row: The row index of the cell to check.
        col: The column index of the cell to check.
        number: The number to check if it can be placed.

    Returns:
        True if the move is valid, False otherwise.
    """

    # Check row
    for x in range(9):
        if grid[row][x] == number:
            return False

    # Check column
    for x in range(9):
        if grid[x][col] == number:
            return False

    # Check 3x3 subgrid
    corner_row = row // 3 * 3
    corner_col = col // 3 * 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False

    return True

def solve(grid, row, col):
    """
    Solves a Sudoku puzzle using backtracking.

    Args:
        grid: A 9x9 list of lists representing the Sudoku grid.
        row: The current row index.
        col: The current column index.

    Returns:
        True if the puzzle is solved, False otherwise.
    """

    # Base case: If we have reached the end of the grid, the puzzle is solved
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    # If the current cell already has a number, move to the next cell
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)

    # Try placing numbers from 1 to 9 in the current cell
    for num in range(1, 10):
        # Check if placing 'num' is valid
        if is_valid_move(grid, row, col, num):
            # Place 'num' in the grid
            grid[row][col] = num

            # Recursively solve the rest of the grid
            if solve(grid, row, col + 1):
                return True

            # If placing 'num' doesn't lead to a solution, backtrack
            grid[row][col] = 0

    # If no number can be placed in the current cell, return False
    return False

grid = [
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

if solve(grid, 0, 0):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=" ")
        print()
    print("Sudoku solved!")
else:
    print("No solution found.")
