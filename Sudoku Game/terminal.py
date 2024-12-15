def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))
    print()

def is_valid(board, row_sets, col_sets, box_sets, row, col, num):
    box_index = (row // 3) * 3 + (col // 3)
    return (num not in row_sets[row] and
            num not in col_sets[col] and
            num not in box_sets[box_index])

def ai_move(board, row_sets, col_sets, box_sets):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # Find an empty cell
                for num in range(1, 10):
                    if is_valid(board, row_sets, col_sets, box_sets, r, c, num):
                        # Place the number
                        board[r][c] = num
                        row_sets[r].add(num)
                        col_sets[c].add(num)
                        box_sets[(r // 3) * 3 + (c // 3)].add(num)
                        return True  # AI made a move
    return False  # No valid moves for AI

def player_move(board, row_sets, col_sets, box_sets):
    while True:
        try:
            row = int(input("Enter row (0-8): "))
            col = int(input("Enter column (0-8): "))
            num = int(input("Enter number (1-9): "))
            if is_valid(board, row_sets, col_sets, box_sets, row, col, num):
                board[row][col] = num
                row_sets[row].add(num)
                col_sets[col].add(num)
                box_sets[(row // 3) * 3 + (col // 3)].add(num)
                break
            else:
                print("Invalid move. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0-8 for row and column, and 1-9 for number.")

def solve_sudoku(board):
    row_sets = [set() for _ in range(9)]
    col_sets = [set() for _ in range(9)]
    box_sets = [set() for _ in range(9)]

    # Initialize sets with existing numbers
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                row_sets[r].add(num)
                col_sets[c].add(num)
                box_sets[(r // 3) * 3 + (c // 3)].add(num)

    turn = 'AI'  # Start with AI's turn
    while True:
        print_board(board)
        if all(all(cell != 0 for cell in row) for row in board):
            print("The Sudoku is solved!")
            break

        if turn == 'AI':
            print("AI's turn:")
            if not ai_move(board, row_sets, col_sets, box_sets):
                print("AI has no valid moves left.")
                break
            turn = 'Player'  # Switch to player's turn
        else:
            print("Player's turn:")
            player_move(board, row_sets, col_sets, box_sets)
            turn = 'AI'  # Switch to AI's turn

# Example Sudoku board (0 represents empty cells)
sudoku_board = [
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

print("Original Sudoku Board:")
print_board(sudoku_board)

solve_sudoku(sudoku_board)
